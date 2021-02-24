def daint = [name: 'daint',
             archs: ['gpu', 'mc'],
             cpus: ['gpu': 12, 'mc': 36],
             buildPath: '$XDG_RUNTIME_DIR/easybuild/build',
             unusePath: '/apps/daint/UES/jenkins/7.0.UP02/ARCH/easybuild/tools/modules/all:/apps/daint/UES/jenkins/7.0.UP02/ARCH/easybuild/modules/all',
             modulesProduction: '/apps/common/UES/jenkins/production/login',
             prefixProduction: '$APPS/UES/jenkins/7.0.UP02/ARCH/easybuild']

def dom = [name: 'dom',
           archs: ['gpu', 'mc'],
           cpus: ['gpu': 12, 'mc': 36],
           buildPath: '$XDG_RUNTIME_DIR/easybuild/build',
           unusePath: '/apps/dom/UES/jenkins/7.0.UP02/ARCH/easybuild/tools/modules/all:/apps/dom/UES/jenkins/7.0.UP02/ARCH/easybuild/modules/all',
           modulesProduction: '',
           prefixProduction: '$APPS/UES/jenkins/7.0.UP02/ARCH/easybuild']

def eiger = [name: 'eiger',
             archs: [],
             cpus: 128,
             buildPath: '$XDG_RUNTIME_DIR/build',
             unusePath: '/apps/eiger/UES/jenkins/1.3.2/20.10',
             modulesProduction: '',
             prefixProduction: '/apps/eiger/UES/jenkins/1.3.2/20.10']

def pilatus = [name: 'pilatus',
               archs: [],
               cpus: 128,
               buildPath: '$XDG_RUNTIME_DIR/build',
               unusePath: '/apps/pilatus/UES/jenkins/1.3.2',
               modulesProduction: '',
               prefixProduction: '/apps/pilatus/UES/jenkins/1.3.2']

def tsa = [name: 'tsa',
           archs: [],
           buildPath: '/tmp/$USER/easybuild/build',
           unusePath: '/apps/arolla/UES/jenkins/RH7.7/MCH-PE20.06/generic/easybuild/modules/all',
           modulesProduction: '',
           modulesUnuseProduction: '',
           prefixProduction: '/apps/arolla/UES/jenkins/RH7.7/MCH-PE20.08/generic/easybuild']

return [daint, dom, eiger, pilatus, tsa]
