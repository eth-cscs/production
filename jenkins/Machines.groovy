def daint = [name: 'daint',
             archs: ['gpu', 'mc'],
             cpus: ['gpu': 12, 'mc': 36],
             buildPath: '$XDG_RUNTIME_DIR//build',
             unusePath: '/apps/daint/UES/jenkins/7.0.UP03/21.09/daint-ARCH/tools/modules/all:/apps/daint/UES/jenkins/7.0.UP03/daint-ARCH/modules/all',
             modulesProduction: '/apps/common/UES/jenkins/production/login',
             prefixProduction: '/apps/daint/UES/jenkins/7.0.UP03/21.09/daint-ARCH']

def dom = [name: 'dom',
           archs: ['gpu', 'mc'],
           cpus: ['gpu': 12, 'mc': 36],
           buildPath: '$XDG_RUNTIME_DIR/build',
           unusePath: '/apps/dom/UES/jenkins/7.0.UP03/21.09/dom-ARCH/tools/modules/all:/apps/dom/UES/jenkins/7.0.UP03/dom-ARCH/modules/all',
           modulesProduction: '',
           prefixProduction: '/apps/dom/UES/jenkins/7.0.UP03/21.09/dom-ARCH']

def eiger = [name: 'eiger',
             archs: [],
             cpus: 128,
             buildPath: '$XDG_RUNTIME_DIR/build',
             unusePath: '$APPS/UES/modulefiles',
             modulesProduction: '',
             prefixProduction: '$APPS/easybuild']

def pilatus = [name: 'pilatus',
               archs: [],
               cpus: 128,
               buildPath: '$XDG_RUNTIME_DIR/build',
               unusePath: '$APPS/modulefiles',
               modulesProduction: '',
               prefixProduction: '$APPS/easybuild']

def tsa = [name: 'tsa',
           archs: [],
           buildPath: '/tmp/$USER/easybuild/build',
           unusePath: '',
           modulesProduction: '',
           modulesUnuseProduction: '',
           prefixProduction: '/apps/arolla/UES/jenkins/RH7.9/MCH-PE20.08-UP01/generic/easybuild']

return [daint, dom, eiger, pilatus, tsa]
