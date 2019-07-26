def daint = [name: 'daint',
             archs: ['gpu', 'mc'],
             buildPath: '$XDG_RUNTIME_DIR/easybuild/build',
             unusePath: '/apps/daint/UES/jenkins/6.0.UP07/ARCH/easybuild/tools/modules/all:/apps/daint/UES/jenkins/6.0.UP07/ARCH/easybuild/modules/all',
             modulesProduction: '/apps/common/UES/jenkins/production/login',
             modulesUnuseProduction: '/apps/daint/UES/easybuild/modulefiles',
             prefixProduction: '$APPS/UES/jenkins/6.0.UP07/ARCH/easybuild']

def dom = [name: 'dom',
           archs: ['gpu', 'mc'],
           buildPath: '$XDG_RUNTIME_DIR/easybuild/build',
           unusePath: '/apps/dom/UES/jenkins/7.0.UP00/PE19.06/ARCH/easybuild/tools/modules/all:/apps/dom/UES/jenkins/7.0.UP00/PE19.06/ARCH/easybuild/modules/all',
           modulesProduction: '',
           modulesUnuseProduction: '',
           prefixProduction: '$APPS/UES/jenkins/7.0.UP00/PE19.06/ARCH/easybuild']

def fulen = [name: 'fulen',
             archs: [],
             buildPath: '/dev/shm/$USER/easybuild/build',
             unusePath: '/apps/fulen/UES/modulefiles',
             modulesProduction: '',
             modulesUnuseProduction: '',
             prefixProduction: '/apps/fulen/UES/jenkins/RH7.4/easybuild']

def kesch = [name: 'kesch',
             archs: [],
             buildPath: '$XDG_RUNTIME_DIR/easybuild/build',
             unusePath: '/apps/escha/UES/easybuild/modulefiles',
             modulesProduction: '',
             modulesUnuseProduction: '',
             prefixProduction: '/apps/escha/UES/jenkins/RH7.5/generic/easybuild']

def leone = [name: 'leone',
             archs: [],
             buildPath: '/dev/shm/$USER/easybuild/build',
             unusePath: '/apps/leone/UES/modulefiles',
             modulesProduction: '',
             modulesUnuseProduction: '',
             prefixProduction: '/apps/leone/UES/jenkins/RHEL6.10/easybuild']

return [daint, dom, kesch, leone]