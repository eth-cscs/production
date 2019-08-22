import reframe as rfm
import reframe.utility.sanity as sn


class SphExaMiniAppSquarepatchBaseTest(rfm.RegressionTest):
    """This test checks GNU's gprof: https://sourceware.org/binutils/docs/gprof,
    report is postprocessed with gprof2dot/graphviz to create the callgraph.
    """
    def __init__(self):
        super().__init__()
        self.descr = 'Strong scaling study'
        self.valid_prog_environs = ['PrgEnv-gnu', 'PrgEnv-intel', 'PrgEnv-cray',
                                    'PrgEnv-cray_classic', 'PrgEnv-pgi']
        self.prgenv_flags = {
            'PrgEnv-gnu': ['-I./include', '-std=c++14', '-g', '-O3', '-pg',
                                       '-DUSE_MPI', '-DNDEBUG'],
            'PrgEnv-intel': ['-I./include', '-std=c++14', '-g', '-O3',
                                         '-DUSE_MPI', '-DNDEBUG'],
            'PrgEnv-cray': ['-I./include', '-hstd=c++14', '-g', '-O3',
                            '-hnoomp', '-DUSE_MPI', '-DNDEBUG'],
            'PrgEnv-cray_classic': ['-I./include', '-hstd=c++14', '-g', '-O3',
                                     '-DUSE_MPI', '-DNDEBUG'],
            'PrgEnv-pgi': ['-I./include', '-std=c++14', '-g', '-O3',
                           '-mp', '-DUSE_MPI', '-DNDEBUG'],
        }
        if self.current_system.name != 'docker':
            self.modules = ['gprof2dot']

        self.build_system = 'SingleSource'
        self.testname = 'sqpatch'
        self.sourcepath = '%s.cpp' % self.testname
        self.executable = './%s.exe' % self.testname
        self.maintainers = ['JG']
        self.tags = {'pasc'}

        self.rpt_file = '%s_rpt.txt' % self.testname
        self.rpt_file_flat = '%s_flat_rpt.txt' % self.testname
        self.rpt_file_line = '%s_line_rpt.txt' % self.testname
        self.rpt_file_src = '%s_src_rpt.txt' % self.testname
        self.rpt_file_pdf = '%s_rpt.pdf' % self.testname
        self.rpt_file_doc = '%s_rpt.doc' % self.testname
        self.sanity_patterns = sn.assert_found('Total time for iteration\(1\)',
                                               self.stdout)
        self.post_run = [
            'gprof %s &> %s' % (self.executable, self.rpt_file),
            'gprof --flat-profile %s &> %s' % (self.executable, self.rpt_file_flat),
            'gprof --line %s &> %s' % (self.executable, self.rpt_file_line),
            'gprof --annotated-source %s &> %s' % (self.executable, self.rpt_file_src),
            'gprof2dot --strip %s | dot -Tpdf -o %s' % (self.rpt_file, self.rpt_file_pdf),
            'file %s &> %s' % (self.rpt_file_pdf, self.rpt_file_doc)
        ]

    def setup(self, partition, environ, **job_opts):
        super().setup(partition, environ, **job_opts)
        environ_name = self.current_environ.name
        prgenv_flags = self.prgenv_flags[environ_name]
        self.build_system.cxxflags = prgenv_flags

@rfm.parameterized_test(*[[mpitask, cubesize]
                         for mpitask in [1]
                         ## for cubesize in [20]
                         ## for cubesize in [100, 80, 60, 40, 20]
                         for cubesize in [60, 40, 20]
# cubesize=100  np=1,000,000
# cubesize=90   np=729,000
# cubesize=80   np=512,000
# cubesize=70   np=343,000
# cubesize=60   np=216,000
# cubesize=50   np=125,000
# cubesize=40   np=64,000
# cubesize=30   np=27,000
# cubesize=20   np=8,000
])
class SphExaMiniAppSquarepatchBroadwellTest(SphExaMiniAppSquarepatchBaseTest):
    def __init__(self, mpitask, cubesize):
        super().__init__()
        ompthread = 1
        self.valid_systems = ['daint:mc', 'dom:mc']
        self.name = 'sphexa_gnuprof_{}_{:03d}mpi_{:03d}omp_{}n'.format(self.testname, mpitask, ompthread, cubesize)
        self.time_limit = (0, 10, 0)
        self.exclusive = True
        self.num_tasks = mpitask
        self.num_tasks_per_node = 1
        self.num_cpus_per_task = ompthread
        self.num_tasks_per_core = 1
        self.use_multithreading = False
        self.variables = {
            'CRAYPE_LINK_TYPE': 'dynamic',
            'OMP_NUM_THREADS': str(self.num_cpus_per_task),
        }
        self.executable_opts = ['-n', '%s' % cubesize, '-s', '4']

        # --- Elapsed time from report (sum of self seconds):
        #Each sample counts as 0.01 seconds.
        #  %   cumulative   self              self     total
        # time   seconds   seconds    calls  Ts/call  Ts/call  name
        # 52.79      0.19     0.19                             void sphexa::sph::computeMomentumAndEnergy<...
        # 33.34      0.31     0.12                             void sphexa::sph::computeDensity<...
        # 11.11      0.35     0.04                             sphexa::Octree...
        # etc...
        regex_seconds = r'^\s+\d+.\d+\s+\d+.\d+\s+(?P<sec>\d+.\d+) '
        seconds = sn.round(sn.sum(sn.extractall(regex_seconds, self.rpt_file_flat, 'sec', float)), 6)

        # --- inclusive time (in %) from report: 
        regex_inclusive_pct_cme = r'^\s+(?P<inclusive>\d+.\d+).*\ssphexa::sph::computeMomentumAndEnergy'
        inclusive_pct_cme = sn.extractsingle(regex_inclusive_pct_cme,
                                             self.rpt_file_flat,
                                             'inclusive', float)

        # --performance-report:
        self.perf_patterns = {
            'elapsed': seconds,
            'Energy_inclusive%': inclusive_pct_cme,
        }

        self.reference = {
            '*': {
                'elapsed': (0, None, None, 'sec'),
                'Energy_inclusive%': (0, None, None, '%'),
                }
        }
