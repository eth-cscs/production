def daint = [name: 'daint',
             archs: ['gpu', 'mc'],
             buildPath: '/dev/shm/$USER/easybuild/stage/build',
             unusePath: '/apps/daint/UES/jenkins/6.0.UP04/ARCH/easybuild/modules/all',
             modulesProduction: '/apps/common/UES/jenkins/production/login-UP04',
             modulesUnuseProduction: '/apps/daint/UES/easybuild/modulefiles',
             prefixProduction: '$APPS/UES/jenkins/6.0.UP04/ARCH/easybuild']

def dom = [name: 'dom',
           archs: ['gpu', 'mc'],
           buildPath: '/tmp/$USER/easybuild',
           unusePath: '/apps/daint/UES/jenkins/6.0.UP04/ARCH/easybuild/modules/all',
           modulesProduction: '',
           modulesUnuseProduction: '',
           prefixProduction: '$APPS/UES/jenkins/6.0.UP06/ARCH/easybuild']

def fulen = [name: 'fulen',
             archs: [],
             buildPath: '/dev/shm/$USER/easybuild/stage/build',
             unusePath: '',
             modulesProduction: '',
             modulesUnuseProduction: '',
             prefixProduction: '/apps/fulen/UES/jenkins/RH7.4/easybuild']

def kesch = [name: 'kesch',
             archs: [],
             buildPath: '/dev/shm/$USER/easybuild/stage/build',
             unusePath: '/apps/escha/UES/generic/modulefiles:/apps/escha/UES/PrgEnv-gnu-17.02/modulefiles:/apps/escha/UES/PrgEnv-cray-17.06/modulefiles:/apps/escha/UES/experimental/modulefiles',
             modulesProduction: '',
             modulesUnuseProduction: '',
             prefixProduction: '/apps/escha/UES/jenkins/RH7.3-gnu_PE17.02/easybuild']

def leone = [name: 'leone',
             archs: [],
             buildPath: '/dev/shm/$USER/easybuild/stage/build',
             unusePath: '/apps/leone/UES/PrgEnv-gnu-2016b',
             modulesProduction: '',
             modulesUnuseProduction: '',
             prefixProduction: '$APPS/UES/jenkins/RH6.7EUS/easybuild']


def monch = [name: 'monch',
             archs: [],
             buildPath: '/dev/shm/$USER/easybuild/stage/build',
             unusePath: '/apps/monch/UES/jenkins/RH6.9-17.06/easybuild/modules/all/',
             modulesProduction: '',
             modulesUnuseProduction: '',
             prefixProduction: '$APPS/UES/jenkins/RH6.9-17.06/easybuild']

return [daint, dom, fulen, kesch, leone, monch]
