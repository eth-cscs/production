def daint = [name: 'daint',
             archs: ['gpu', 'mc'],
             cpus: ['gpu': 12, 'mc': 36],
             buildPath: '$XDG_RUNTIME_DIR/easybuild/build',
             unusePath: '/apps/daint/UES/jenkins/6.0.UP07/ARCH/easybuild/tools/modules/all:/apps/daint/UES/jenkins/6.0.UP07/ARCH/easybuild/modules/all',
             modulesProduction: '/apps/common/UES/jenkins/production/login',
             modulesUnuseProduction: '/apps/daint/UES/easybuild/modulefiles',
             prefixProduction: '$APPS/UES/jenkins/6.0.UP07/ARCH/easybuild']

def dom = [name: 'dom',
           archs: ['gpu', 'mc'],
           cpus: ['gpu': 12, 'mc': 36],
           buildPath: '$XDG_RUNTIME_DIR/easybuild/build',
           unusePath: '/apps/dom/UES/jenkins/7.0.UP01/ARCH/easybuild/tools/modules/all:/apps/dom/UES/jenkins/7.0.UP01/ARCH/easybuild/modules/all',
           modulesProduction: '',
           modulesUnuseProduction: '',
           prefixProduction: '$APPS/UES/jenkins/7.0.UP01/ARCH/easybuild']

def kesch = [name: 'kesch',
             archs: [],
             cpus: 24,
             buildPath: '$XDG_RUNTIME_DIR/easybuild/build',
             unusePath: '/apps/escha/UES/easybuild/modulefiles',
             modulesProduction: '',
             modulesUnuseProduction: '',
             prefixProduction: '/apps/escha/UES/jenkins/RH7.5/generic/easybuild']

return [daint, dom, kesch]
