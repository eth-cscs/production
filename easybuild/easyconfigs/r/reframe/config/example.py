import reframe as rfm
import reframe.utility.sanity as sn


@rfm.simple_test
class Example7Test(rfm.RegressionTest):
    def __init__(self):
        self.descr = 'bla'
        self.valid_systems = ['dom:mc']
        self.valid_prog_environs = ['PrgEnv-gnu']
        self.build_system = 'SingleSource'
        self.sourcepath = 'hello_world_serial.cpp'
        self.sanity_patterns = sn.assert_found(
            r'time for single matrix vector multiplication', self.stdout)
        self.perf_patterns = {
            'perf': sn.extractsingle(r'Performance:\s+(?P<Gflops>\S+) Gflop/s',
                                     self.stdout, 'Gflops', float)
        }
        self.reference = {
            'dom:mc': {
                'perf': (50.0, -0.1, 0.1, 'Gflop/s'),
            }
        }
        self.maintainers = ['you-can-type-your-email-here']
        self.tags = {'tutorial'}
