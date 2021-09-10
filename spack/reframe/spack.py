# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import copy
import glob
import re
import semver
import os
import yaml

import reframe as rfm
import reframe.core.exceptions as error
import reframe.utility as util
import reframe.utility.osext as osext
import reframe.utility.sanity as sn
import reframe.utility.udeps as udeps

from reframe.core.exceptions import SanityError

spacklib = util.import_module_from_file(os.path.join(os.path.dirname(__file__), 'src', 'spack_util', 'spacklib.py'))
spackconfig = util.import_module_from_file(os.path.join(os.path.dirname(__file__), 'src', 'spack_util', 'spack_config.py'))

SPACK_VERSIONS = ['develop', '0.15.4', '0.16.1']

# TODO find a mechanism to include intel in the list
base_cuda_compilers = ['gcc', 'cce']
base_generic_compilers = ['gcc', 'cce', 'pgi']

cuda_compatible_compilers = spacklib.generate_compiler_list_for_testing([r'cdt-cuda/'], base_cuda_compilers)
generic_compilers = spacklib.generate_compiler_list_for_testing([r'cdt/'], base_generic_compilers)

# Do not add anything very dramatic here
# This list is meant for smoke tests!!!
# So, things with fast compilation times, please
SPACK_CUDA_TEST_PKGS = [
    # # petsc cannot detect the NVCC compiler if it doesn't have the ^cuda
    # # I think this is due to the module mapping generated in the packages.yaml file
    # # r'petsc %gcc +cuda ^cuda', # this takes ~20 min to run
    # r'gromacs %gcc +cuda ^fftw',

    # # using COSMA master because version < 2.3.0 doesn't support the CCE compiler
    # r'cosma@master %gcc',
    # r'cosma@master %cce ^cmake%gcc',
    # r'cosma@master %intel ^cmake%gcc',
]

SPACK_TEST_PKGS = [
    # r'petsc %gcc ~cuda',
    # r'gromacs %gcc ~cuda ^fftw',
    r'zlib %gcc',
    r'zlib %cce',
    # r'pkg-config',
    # r'cosma@master ~cuda cuda_arch=none %gcc',
    # r'cosma@master ~cuda cuda_arch=none %cce',
    # r'cosma@master ~cuda cuda_arch=none %intel'
]


SPACK_TEST_SPECS = spacklib.generate_spec_with_proper_compilers(SPACK_CUDA_TEST_PKGS, cuda_compatible_compilers)
SPACK_TEST_SPECS |= spacklib.generate_spec_with_proper_compilers(SPACK_TEST_PKGS, generic_compilers)


@rfm.simple_test
class spack_config_check(rfm.RunOnlyRegressionTest):
    spack_version = parameter(SPACK_VERSIONS)
    valid_prog_environs = ['builtin']
    valid_systems = ['daint:login', 'dom:login']
    executable = 'spack'
    executable_opts = ['compiler', 'find', '--scope', 'site/cray']
    num_tasks = 1
    num_tasks_per_node = 1
    exclusive = True
    tags = {'maintenance', 'production'}
    maintainers = ['VH']

    def __init__(self):
        self.sanity_patterns = self.assert_config()
        self.sourcesdir = 'https://github.com/spack/spack.git'

        self.legacy_spack = False
        if self.spack_version != 'develop':
            self.prerun_cmds = [
                f'git checkout -b v{self.spack_version} v{self.spack_version}',
            ]
            if spacklib.parse_version(self.spack_version) >= spacklib.parse_version('0.16.0'):
                self.postrun_cmds += ['spack external find --scope site/cray']
            elif spacklib.parse_version(self.spack_version) < spacklib.parse_version('0.15.0'):
                raise ValueError(f'Sparck version {self.spack_version} is not supported')
            else:
                self.legacy_spack = True
                self.postrun_cmds += [
                    'spack external find',
                ]
        else:
            self.postrun_cmds += ['spack external find --scope site/cray']

        self.postrun_cmds += ['spack --version']

        self.all_cdt_compilers = {}
        self.all_compilers = {}
        self.os_compilers = {}
        self.compiler_types = ['gcc', 'intel', 'pgi', 'cce']
        self.pe_path = os.path.join(os.sep, 'opt', 'cray', 'pe')
        self.cray_system_modules_path = os.path.join(os.sep, 'opt', 'cray', 'modulefiles')

        # the OS cmake is in general too old. it is worthless to use it
        self.exclude_packages = ['cmake']

        self.pe_independent_pkgs = spackconfig.PE_INDEPENDENT_PKGS
        self.pe_dependent_pkgs = spackconfig.PE_DEPENDENT_PKGS

        self.keep_files = [os.path.join('etc', 'spack', 'cray')]

    @run_after('setup')
    def set_spack_config(self):
        self.spack_path = self.stagedir
        self.variables = {
            'SPACK_ROOT': f'{self.spack_path}',
            'PATH': '$SPACK_ROOT/bin:$PATH',
        }
        spack_etc_dir = os.path.join(self.spack_path, 'etc', 'spack', 'cray')
        self.compilers_file_path = os.path.join(spack_etc_dir, 'compilers.yaml')
        self.packages_file_path = os.path.join(spack_etc_dir, 'packages.yaml')
        self.config_file_path = os.path.join(spack_etc_dir, 'config.yaml')
        self.modules_file_path = os.path.join(spack_etc_dir, 'modules.yaml')
        # self.keep_files = [spack_etc_dir]

        # This is a workaround for the lack of --scope in spack external find in 0.15.x versions
        if self.legacy_spack:
            self.variables['HOME'] = spack_etc_dir

    @deferrable
    def assert_config(self):
        patterns = [
            sn.assert_found(r'Added \d+ new compilers', self.stdout),
            sn.assert_not_found(r'ERROR', self.stdout),
        ]

        # Compiler assertions
        with open(self.compilers_file_path) as f:
            spack_compilers = yaml.safe_load(f)

        all_compilers = sorted(self.all_compilers)
        for compiler in all_compilers:
            patterns += [sn.assert_found(f'spec: {compiler}', self.compilers_file_path)]

        if 'compilers' in spack_compilers:
            compilers = []
            for compiler in spack_compilers['compilers']:
                if 'compiler' in compiler:
                    spec = compiler['compiler']
                    if 'spec' in spec:
                        compilers.append(spec['spec'])
                    else:
                        raise SanityError(f'spec entry missing in {spec} inside the compiler.yaml file')
                else:
                    raise SanityError(f'compiler entry missing in {compiler} inside the compiler.yaml file')
            for i, a in enumerate(sorted(compilers)):
                # we should have a one to one mapping between the identified
                # compilers and the entries inside the newly generated compilers.yaml file
                patterns += [sn.assert_eq(a, all_compilers[i])]
        else:
            raise SanityError('compilers entry not found in compilers.yaml file')

        # package assertions
        with open(self.packages_file_path) as f:
            spack_packages = yaml.safe_load(f)

        if 'packages' in spack_packages:
            pkgs = set()
            for name, pkg in self.pe_independent_pkgs.items():
                if 'name' in pkg:
                    pkgs.add(pkg['name'])
                else:
                    pkgs.add(name)
            for name, pkg in self.pe_dependent_pkgs.items():
                if 'name' in pkg:
                    pkgs.add(pkg['name'])
                else:
                    pkgs.add(name)

            for pkg in pkgs:
                patterns += [sn.assert_found(f'{pkg}:', self.packages_file_path)]
        else:
            raise SanityError('packages entry not found in packages.yaml file')


        config = spackconfig.SPACK_CONFIG

        # config assertions
        with open(self.config_file_path) as f:
            spack_config = yaml.safe_load(f)

        if 'config' in spack_config:
            for option in ['build_stage', 'source_cache', 'misc_cache', 'db_lock_timeout', 'build_jobs']:
                patterns += [sn.assert_found(f'{option}:', self.config_file_path)]
        else:
            raise SanityError('config entry not found in config.yaml file')

        return sn.all(patterns)

    @run_after('run')
    def capture_compilers(self):
        with open(self.compilers_file_path) as f:
            spack_compilers = yaml.safe_load(f)

        # since cdt-cuda is a sub set of cdt, then one can skip the cdt-cuda from the list of cdts
        # but we are leaving the work to find a cuda compatible compiler to the end user
        self.modulerc_files = spacklib.get_cdts_modulerc_files(include_cdts=['cdt/'])

        for modulerc_file in self.modulerc_files:
            cdt_name, cdt_version = spacklib.get_cdt_info_from_modulerc_file(modulerc_file)

            for compiler in self.compiler_types:
                self.all_compilers.update(self.generate_compiler_entries(compiler, spack_compilers, modulerc_file, cdt_name, cdt_version))

    @run_after('run')
    def update_compilers_file(self):
        spack_compilers = {'compilers' : []}
        for _, spec in self.all_compilers.items():
            spack_compilers['compilers'].append({'compiler': spec})

        with open(self.compilers_file_path, 'w') as fp:
             yaml.dump(spack_compilers, fp, default_flow_style=False, canonical=False)

    def generate_compiler_entries(self, compiler_type, spack_compilers, modulerc_file, cdt_name, cdt_version):
        ret = {}

        self.os_compilers.update(spacklib.get_spack_os_compilers(compiler_type, spack_compilers))
        cdt_compilers = spacklib.get_spack_cdt_compilers(compiler_type, spack_compilers)

        try:
            default_cdt_compiler_version = spacklib.parse_version(spacklib.get_default_package_versions_from_modulerc(compiler_type, modulerc_file))
        except ValueError:
            # intel compilers are not listed in the default cdts
            # so we assume that they are compatible will all cdts
            # we are assuming that the compiler was detected by spack
            default_cdt_compiler_version = spacklib.get_highest_version(cdt_compilers)

        # pruning compilers to remove non compatible compilers with the current cdt
        # assuming that all compilers lower than the default one from the cdt are compatible with that cdt
        compiler_versions = list(cdt_compilers.keys())
        if compiler_type != 'cce':
            for version in compiler_versions:
                if spacklib.parse_version(version) > default_cdt_compiler_version:
                    cdt_compilers.pop(version)
        else:
            # for cce the compiler should only be associated with a given cdt, in principle
            for version in compiler_versions:
                if spacklib.parse_version(version) != default_cdt_compiler_version:
                    cdt_compilers.pop(version)

        # adding the cdt call to each compiler
        for version, spec in cdt_compilers.items():
            modules = spec['modules']

            # cdt compilers have modules, if not they are considered os compilers
            modules.append(cdt_name + '/' + cdt_version)
            modules.append(compiler_type + '/' + version)
            spec['spec'] += '.' + cdt_version

            ret.update({
                spec['spec'] : spec
            })
            spacklib.compile_cdt_compilers_list(self.all_cdt_compilers, cdt_name, cdt_version, spec['spec'])

        # adding the os compilers
        for version, spec in self.os_compilers.items():
            ret.update({
                spec['spec'] : spec
            })

        return ret

    def generate_pe_independent_package_entries(self, pe_pkgs):
        pkgs = {}
        for pkg_name, pkg_data in pe_pkgs.items():
            spack_pkg_name, variant, pkg = spacklib.get_pkg_properties(pkg_name, pkg_data, pkgs)

            if variant and not 'modules' in pkg_data:
                pkg['variants'] = variant

            if 'modules' in pkg_data:
                pkg_versions = spacklib.get_module_available_versions(pkg_data['modules'])
            else:
                #TODO verify how to ge the version of prefix only packages like intel-mkl
                pkg_versions = []

            external_specs = set()
            for pkg_version in pkg_versions:
                external = spacklib.add_to_external(pkg_name, pkg_data, pkg_version, None, external_specs)
                if external:
                    if not 'externals' in pkg:
                        pkg['externals'] = []
                    if 'prefix' in pkg_data:
                        if pkg_data['prefix']:
                            if isinstance(pkg_data['prefix'], str):
                                external['prefix'] = pkg_data['prefix']
                            # elif isinstance(pkg_data['prefix'], bool):
                            #     #TODO fixme
                            #     print('TODO autogenerate prefix')

                    pkg['externals'].append(external)

            pkgs.update({spack_pkg_name: pkg})

        return pkgs

    def generate_pe_dependent_package_entries(self, pe_pkgs):
        pkgs = {}
        for pkg_name, pkg_data in pe_pkgs.items():
            spack_pkg_name, variant, pkg = spacklib.get_pkg_properties(pkg_name, pkg_data, pkgs)

            external_specs = set()
            for modulerc_file in self.modulerc_files:
                cdt_name, cdt_version = spacklib.get_cdt_info_from_modulerc_file(modulerc_file)
                full_cdt_name = spacklib.get_full_cdt_name(cdt_name, cdt_version)

                if 'modules' in pkg_data:
                    pkg_version = spacklib.get_default_package_versions_from_modulerc(pkg_data['modules'], modulerc_file)
                else:
                    #TODO verify how to ge the version of prefix only packages like intel-mkl
                    pkg_version = None

                for compiler in self.all_cdt_compilers[full_cdt_name]:
                    external = spacklib.add_to_external(pkg_name, pkg_data, pkg_version, compiler, external_specs)
                    if external:
                        if not 'externals' in pkg:
                            pkg['externals'] = []
                        if 'prefix' in pkg_data:
                            if isinstance(pkg_data['prefix'], str):
                                external['prefix'] = pkg_data['prefix']
                            # elif isinstance(pkg_data['prefix'], bool):
                            #     #TODO fixme
                            #     print('TODO autogenerate prefix')

                        pkg['externals'].append(external)

            pkgs.update({spack_pkg_name: pkg})

        return pkgs


    @run_after('run')
    def update_packages_file(self):
        if os.path.isfile(self.packages_file_path):
            with open(self.packages_file_path) as f:
                spack_packages = yaml.safe_load(f)
        else:
            spack_packages = {}

        pkgs_all = {}
        pkgs_all['compiler'] = self.compiler_types
        pkgs_all['providers'] = {
            'mpi': ['cray-mpich', 'mpich', 'openmpi'],
            'mkl': ['intel-mkl'],
            'fftw-api': ['cray-fftw', 'fftw', 'intel-mkl'],
            'blas': ['cray-libsci', 'intel-mkl', 'blis', 'openblas'],
            'scalapack': ['cray-libsci', 'intel-mkl', 'netlib-scalapack'],
            'lapack': ['cray-libsci', 'intel-mkl', 'openblas', 'netlib-lapack'],
            'pkgconfig': ['pkg-config'],
            'golang': ['go'],
            'tbb': ['intel-tbb']
        }

        pkgs = spacklib.extract_all_spack_generated_packages(spack_packages)
        if self.legacy_spack:
            pkgs.update(spacklib.convert_packages_to_legacy(
                self.generate_pe_dependent_package_entries(self.pe_dependent_pkgs)
            ))
            pkgs.update(spacklib.convert_packages_to_legacy(
                self.generate_pe_independent_package_entries(self.pe_independent_pkgs)
            ))
        else:
            pkgs.update(self.generate_pe_dependent_package_entries(self.pe_dependent_pkgs))
            pkgs.update(self.generate_pe_independent_package_entries(self.pe_independent_pkgs))

        # the mentality is to add to the file, not remove from it
        # we are replacing some entries like the 'all' one and adding the
        # cray specific ones
        if not 'packages' in spack_packages:
            spack_packages = {'packages' : {}}

        spack_packages['packages'].update({'all' : pkgs_all})
        spack_packages['packages'].update(pkgs)

        for pkg in self.exclude_packages:
            if pkg in spack_packages['packages']:
                spack_packages['packages'].pop(pkg)

        with open(self.packages_file_path, 'w') as fp:
            yaml.dump(spack_packages, fp, default_flow_style=False, canonical=False)

    @run_after('run')
    def generate_config_file(self):
        config = spackconfig.SPACK_CONFIG

        with open(self.config_file_path, 'w') as fp:
            yaml.dump(config, fp, default_flow_style=False, canonical=False)

    @run_after('run')
    def generate_module_file(self):
        blacklisted_pkg_modules = spackconfig.BLACKLISTED_PKG_MODULES
        module_suffixes = spackconfig.MODULE_SUFFIXES
        module_configs = spackconfig.MODULE_CONFIGS

        #TODO move this away from here
        module_configs['modules']['lmod']['blacklist'] = blacklisted_pkg_modules
        module_configs['modules']['tcl']['blacklist'] = blacklisted_pkg_modules
        module_configs['modules']['lmod']['all']['suffixes'] = module_suffixes
        module_configs['modules']['tcl']['all']['suffixes'] = module_suffixes

        with open(self.modules_file_path, 'w') as fp:
            yaml.dump(module_configs, fp, default_flow_style=False, canonical=False)


@rfm.simple_test
class spack_pkg_check(rfm.RunOnlyRegressionTest):
    spack_version = parameter(SPACK_VERSIONS)
    spack_pkg = parameter(list(SPACK_TEST_SPECS))
    valid_prog_environs = ['builtin']
    valid_systems = ['daint:login', 'dom:login']
    executable = 'spack'
    executable_opts = ['spec', '-IlN']
    num_tasks = 1
    num_tasks_per_node = 1
    exclusive = True
    tags = {'maintenance', 'production'}
    maintainers = ['VH']
    time_limit = '12h'

    def __init__(self):
        self.dep_name = f'spack_config_check_{util.toalphanum(self.spack_version)}'
        self.depends_on(self.dep_name, how=udeps.by_env)

        self.sanity_patterns = sn.all([
            sn.assert_not_found(r'ERROR', self.stderr),
            sn.assert_not_found(r'Error', self.stderr),
            sn.assert_not_found(r'missing', self.stderr),
            sn.assert_not_found(r'command not found', self.stderr),
        ])
        self.executable_opts += [self.spack_pkg]
        self.postrun_cmds = [f'spack install {self.spack_pkg}']

    @run_after('setup')
    def config_spack(self):
        target = self.getdep(self.dep_name, 'builtin')
        self.variables = target.variables


@rfm.simple_test
class spack_push_config_check(rfm.RunOnlyRegressionTest):
    spack_version = parameter(SPACK_VERSIONS)
    valid_prog_environs = ['builtin']
    valid_systems = ['daint:login', 'dom:login']
    modules = ['daint-gpu', 'hub']
    executable = 'git'
    executable_opts = ['add', 'spack']
    num_tasks = 1
    num_tasks_per_node = 1
    exclusive = True
    tags = {'maintenance', 'production'}
    maintainers = ['VH']

    def __init__(self):
        self.branch = f'{self.current_system.name}_spack_config_{util.toalphanum(self.spack_version)}'
        self.repo = 'git@github.com:eth-cscs/production.git'
        self.prerun_cmds = [
            f'''
git clone {self.repo} {self.branch}
cd {self.branch}
if [ -n "$(git ls-remote --heads {self.repo} {self.branch})" ]; then
    git checkout {self.branch}
else
    git checkout -b {self.branch}
fi'''
        ]

        self.postrun_cmds = [
            f'''
if [ -n "$(git status --porcelain)" ]; then
    git commit -m "Update Spack config for version {self.spack_version} on {self.current_system.name}"
    if [ -n "$(hub pr list --head {self.branch})" ]; then
        git push origin HEAD
    else
        hub pull-request -p -m "[{self.current_system.name}] Update Spack config for version {self.spack_version} on {self.current_system.name}"
    fi
fi'''
        ]

        self.dep_name = f'spack_config_check_{util.toalphanum(self.spack_version)}'
        self.depends_on(self.dep_name, how=udeps.by_env)
        for pkg in list(SPACK_TEST_SPECS):
            dep_name = f'spack_pkg_check_{util.toalphanum(self.spack_version)}_{util.toalphanum(pkg)}'
            self.depends_on(dep_name, how=udeps.by_env)

        self.sanity_patterns = sn.all([
            sn.assert_not_found(r'ERROR', self.stderr),
            sn.assert_not_found(r'Error', self.stderr),
            sn.assert_not_found(r'error', self.stderr),
            sn.assert_not_found(r'fatal', self.stderr),
        ])

    @run_before('run')
    def config_spack(self):
        target = self.getdep(self.dep_name, 'builtin')
        self.etc_dir = os.path.join(target.stagedir, 'etc', 'spack', 'cray')

        if self.spack_version != 'develop':
            self.destination = os.path.join(self.stagedir, self.branch, 'spack', self.spack_version, self.current_system.name)
        else:
            self.destination = os.path.join(self.stagedir, self.branch, 'spack', self.current_system.name)

        self.prerun_cmds += [
            f'mkdir -p {self.destination}',
            f'cp {self.etc_dir}/* {self.destination}'
        ]
