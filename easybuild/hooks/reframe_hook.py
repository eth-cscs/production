import copy
import os
import random
import shlex
import subprocess

from vsc.utils import fancylogger

from easybuild.tools.build_log import EasyBuildError, dry_run_msg
from easybuild.tools.modules import get_software_root

from easybuild.tools.config import build_option, log_path

_log = fancylogger.getLogger('hooks', fname=False)


def run_reframe(cmd, dir=None, shell=False):
    cwd = os.getcwd()

    if dir:
        os.chdir(dir)

    _log.info("ReFrame hook executed as: " + cmd)

    proc = subprocess.Popen(shlex.split(cmd),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            shell=shell)
    proc_stdout, proc_stderr = proc.communicate()
    if proc.returncode != 0:
        raise EasyBuildError("ReFrame execution error: %s" % proc_stdout)
    else:
        _log.info("ReFrame execution was successful: %s" % proc_stdout)

    if dir:
        os.chdir(cwd)

def post_sanitycheck_hook(self, *args, **kwargs):
    """Example post sanity check hook to invoke reframe."""

    """Defining inside the hook function, because it is an easyblock function"""
    def prepend_fake_module_path():
        """modified from easybuild.framework.easyblock.Easyblock.load_fake_module function"""
        env = copy.deepcopy(os.environ)
        fake_mod_path = self.make_module_step(fake=True)
        self.modules_tool.prepend_module_path(os.path.join(fake_mod_path, self.mod_subdir), priority=10000)
        return (fake_mod_path, env)

    if self.name == 'reframe':
        # Run ReFrame unittests?
        return
    else:
        # Load reframe module
        self.modules_tool.load(["reframe"], allow_reload=False)

    # Probe relevant informations to select reframe tests
    CUDA = get_software_root("CUDA")

    # Prepend newly created module to MODULEPATH
    dry_run = build_option('extended_dry_run')
    silent = build_option('silent')
    if not dry_run:
        fake_mod_data = prepend_fake_module_path()

    random_int = random.randint(0, 9999999)
    random_folder = "tmp-%07d" % random_int

    # Set ReFrame output and perflogs folders
    output_dir = os.path.join(self.installdir, log_path(), 'reframe_output')
    _log.info("ReFrame output dir: %s", output_dir)

    perflogs_dir = os.path.join(self.installdir, log_path(), 'reframe_perflogs')
    _log.info("ReFrame perflogs dir: %s", perflogs_dir)

    # Set ReFrame run and stage dir
    # stage dir cannot be self.builddir because on daint it is /run/user
    # which is a non shared filesystem with the compute nodes
    stage_dir = os.path.join(self.builddir, log_path(), 'reframe_stage')
    rfm_run_dir = self.builddir
    scratch = os.getenv('SCRATCH', None)
    if scratch:
        stage_dir = os.path.join(scratch, log_path(), random_folder, 'reframe_stage')
        rfm_run_dir = os.path.join(scratch, log_path(), random_folder, 'rfm_run_dir')
    elif self.build_in_installdir and not dry_run:
        # generating self.builddir
        self.gen_builddir()
        rfm_run_dir = self.builddir
        stage_dir = os.path.join(self.builddir, log_path(), random_folder, 'reframe_stage')
        # restoring the self.builddir status
        self.builddir = self.installdir

    _log.info("ReFrame stage dir: %s", stage_dir)
    _log.info("ReFrame run dir: %s", rfm_run_dir)

    # creating run dir if it does not exist
    if not os.path.exists(rfm_run_dir):
        os.makedirs(rfm_run_dir)

    if dry_run:
        dry_run_msg("ReFrame dirs:", silent=silent)
        dry_run_msg("  * run: %s" % rfm_run_dir, silent=silent)
        dry_run_msg("  * output: %s" % output_dir, silent=silent)
        dry_run_msg("  * perflogs: %s" % perflogs_dir, silent=silent)
        dry_run_msg("  * stage: %s" % stage_dir, silent=silent)

    # add to rfm_cmd your common system flags
    rfm_cmd = "reframe --nocolor -r "
    rfm_cmd += "-o %s " % output_dir
    rfm_cmd += "-s %s " % stage_dir
    rfm_cmd += "--perflogdir %s " % perflogs_dir
    rfm_cmd += "--save-log-files "

    if self.name == 'GROMACS' and CUDA:
        rfm_cmd += " -n gromacs_gpu_prod_check -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'GROMACS':
        rfm_cmd += " -n gromacs_cpu_prod_check -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'CUDA':
        rfm_cmd += " -n FlexibleCudaMemtest"
        rfm_cmd += " -n GpuBandwidthCheck"
        rfm_cmd += " -n NvmlCheck"
        rfm_cmd += " -n CudaMatrixmulCublasCheck"
        rfm_cmd += " -n CudaDeviceQueryCheck"
        rfm_cmd += " -n CudaConcurrentKernelsCheck"
        rfm_cmd += " -n CudaSimpleMPICheck"
        rfm_cmd += " -n GpuDirectCudaCheck"
        rfm_cmd += " -n CudaGdbCheck"
        rfm_cmd += " -n NvprofCheck"
        rfm_cmd += " -n opencl_check"
    elif self.name in ['gmpolf', 'foss', 'gmvolf', 'CrayCCE', 'CrayGNU', 'CrayIntel' 'CrayPGI']:
        rfm_cmd += " -n HelloWorldTestSerial_cpp_dynamic"
        rfm_cmd += " -n HelloWorldTestSerial_cpp_static"
        rfm_cmd += " -n HelloWorldTestSerial_c_dynamic"
        rfm_cmd += " -n HelloWorldTestSerial_c_static"
        rfm_cmd += " -n HelloWorldTestSerial_f90_dynamic"
        rfm_cmd += " -n HelloWorldTestSerial_f90_static"
        rfm_cmd += " -n HelloWorldTestOpenMP_cpp_dynamic"
        rfm_cmd += " -n HelloWorldTestOpenMP_cpp_static"
        rfm_cmd += " -n HelloWorldTestOpenMP_c_dynamic"
        rfm_cmd += " -n HelloWorldTestOpenMP_c_static"
        rfm_cmd += " -n HelloWorldTestOpenMP_f90_dynamic"
        rfm_cmd += " -n HelloWorldTestOpenMP_f90_static"
        rfm_cmd += " -n HelloWorldTestMPI_cpp_dynamic"
        rfm_cmd += " -n HelloWorldTestMPI_cpp_static"
        rfm_cmd += " -n HelloWorldTestMPI_c_dynamic"
        rfm_cmd += " -n HelloWorldTestMPI_c_static"
        rfm_cmd += " -n HelloWorldTestMPI_f90_dynamic"
        rfm_cmd += " -n HelloWorldTestMPI_f90_static"
        rfm_cmd += " -n HelloWorldTestMPIOpenMP_cpp_dynamic"
        rfm_cmd += " -n HelloWorldTestMPIOpenMP_cpp_static"
        rfm_cmd += " -n HelloWorldTestMPIOpenMP_c_dynamic"
        rfm_cmd += " -n HelloWorldTestMPIOpenMP_c_static"
        rfm_cmd += " -n HelloWorldTestMPIOpenMP_f90_dynamic"
        rfm_cmd += " -n HelloWorldTestMPIOpenMP_f90_static"
        rfm_cmd += " -n jacobi_C"
        rfm_cmd += " -n jacobi_Cpp"
        rfm_cmd += " -n jacobi_F9"
        rfm_cmd += " -n DGEMMTest"
        rfm_cmd += " -n ScaLAPACKSanity_static"
        rfm_cmd += " -n ScaLAPACKSanity_dynamic"
        rfm_cmd += " -n mpi_helloworld_check"
    elif self.name == 'VASP' and CUDA:
        rfm_cmd += " -n VASPGPUCheck -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'VASP':
        rfm_cmd += " -n VASPCPUCheck  -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'CP2K' and CUDA:
        rfm_cmd += " -n cp2k_gpu_prod_check -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'CP2K':
        rfm_cmd += " -n cp2k_cpu_prod_check -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'QuantumESPRESSO':
        rfm_cmd += " -n quantum_espresso_cpu_check -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'LAMMPS' and CUDA:
        rfm_cmd += " -n LAMMPSGPUProdCheck -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'LAMMPS':
        rfm_cmd += " -n LAMMPSCPUProdCheck -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'NAMD' and CUDA:
        rfm_cmd += " -n namd_gpu_prod_check -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'NAMD':
        rfm_cmd += " -n namd_cpu_prod_check -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'ParaView':
        rfm_cmd += " -n paraview_gpu_check -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'Amber' and CUDA:
        rfm_cmd += " -n amber_gpu_prod_check -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'Amber':
        rfm_cmd += " -n amber_cpu_check -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'CPMD':
        rfm_cmd += " -n cpmd_cpu_check -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'TensorFlow':
        rfm_cmd += " -n tensorflow_mnist_check"
        rfm_cmd += " -n tensorflow_wide_deep_check -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'ICON':
        rfm_cmd += " -n RRTMGPTest -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'Trilinos':
        rfm_cmd += " -n TrilinosTest_static"
    elif self.name == 'PETSc':
        rfm_cmd += " -n PetscPoisson2DCheck_dynamic"
        rfm_cmd += " -n PetscPoisson2DCheck_static -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'Boost':
        rfm_cmd += " -n BoostCrayGnuPythonTest_1_67_0_18_08_2_7"
        rfm_cmd += " -n BoostCrayGnuPythonTest_1_67_0_18_08_3_6 -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'HDF5':
        rfm_cmd += " -n HDF5Test_c_static"
        rfm_cmd += " -n HDF5Test_c_dynamic"
        rfm_cmd += " -n HDF5Test_f90_static"
        rfm_cmd += " -n HDF5Test_f90_dynamic -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name in ['netCDF', 'netCDF-Fortran', 'netCDF-C++']:
        rfm_cmd += " -n NetCDFTest_cpp_dynamic"
        rfm_cmd += " -n NetCDFTest_cpp_static"
        rfm_cmd += " -n NetCDFTest_c_dynamic"
        rfm_cmd += " -n NetCDFTest_c_static"
        rfm_cmd += " -n NetCDFTest_f90_dynamic"
        rfm_cmd += " -n NetCDFTest_f90_static -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'Spark':
        rfm_cmd += " -n SparkAnalyticsCheck -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'magma':
        rfm_cmd += " -n MagmaCheck_cblas_z_2_2_prod"
        rfm_cmd += " -n MagmaCheck_cblas_z_2_4_prod"
        rfm_cmd += " -n MagmaCheck_zgemm_2_2_prod"
        rfm_cmd += " -n MagmaCheck_zgemm_2_4_prod"
        rfm_cmd += " -n MagmaCheck_zsymmetrize_2_2_prod"
        rfm_cmd += " -n MagmaCheck_zsymmetrize_2_4_prod"
        rfm_cmd += " -n MagmaCheck_ztranspose_2_2_prod"
        rfm_cmd += " -n MagmaCheck_ztranspose_2_4_prod"
        rfm_cmd += " -n MagmaCheck_zunmbr_2_2_prod -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'NCO':
        rfm_cmd += " -n NCO_DependencyTest"
        rfm_cmd += " -n NCO_NC4SupportTest"
        rfm_cmd += " -n NCO_CDOModuleCompatibilityTest"
        rfm_cmd += " -n NCO_InfoNCTest"
        rfm_cmd += " -n NCO_InfoNC4Test"
        rfm_cmd += " -n NCO_InfoNC4CTest"
        rfm_cmd += " -n NCO_MergeNCTest"
        rfm_cmd += " -n NCO_MergeNC4Test"
        rfm_cmd += " -n NCO_MergeNC4CTest -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'CDO':
        rfm_cmd += " -n CDO_DependencyTest"
        rfm_cmd += " -n CDO_NC4SupportTest"
        rfm_cmd += " -n CDO_NCOModuleCompatibilityTest"
        rfm_cmd += " -n CDO_InfoNCTest"
        rfm_cmd += " -n CDO_InfoNC4Test"
        rfm_cmd += " -n CDO_InfoNC4CTest"
        rfm_cmd += " -n CDO_MergeNCTest"
        rfm_cmd += " -n CDO_MergeNC4Test"
        rfm_cmd += " -n CDO_MergeNC4CTest -M %s:%s" % (self.name, self.short_mod_name)
    elif self.name == 'ddt':
        rfm_cmd += " -n DdtCheck_F90"
        rfm_cmd += " -n DdtCheck_C"
        rfm_cmd += " -n DdtCheck_Cpp"
        rfm_cmd += " -n DdtCheck_Cuda -M %s:%s" % (self.name, self.short_mod_name)
    elif 'Score-P' == self.name:
        rfm_cmd += " -n scorep_mpi_omp_C"
        rfm_cmd += " -n scorep_mpi_omp_Cpp"
        rfm_cmd += " -n scorep_mpi_omp_F90 -M %s:%s" % (self.name, self.short_mod_name)
    else:
        _log.info("No dedicated ReFrame test found. Skipping ReFrame run...")
        if dry_run:
            dry_run_msg("No dedicated ReFrame test found. Skipping ReFrame run...\n", silent=silent)
        return

    if not dry_run:
        run_reframe(rfm_cmd, dir=rfm_run_dir, shell=False)
        self.clean_up_fake_module(fake_mod_data)
    else:
        dry_run_msg("ReFrame command: %s" % rfm_cmd, silent=silent)
