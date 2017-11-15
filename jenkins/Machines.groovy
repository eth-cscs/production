def daint = [name: 'daint',
             archs: ['gpu', 'mc'],
             toolkits: ['CrayCCE', 'CrayGNU', 'CrayIntel', 'CrayPGI'],
             toolkitVersions: ['17.08'],
             unusePath: '/apps/daint/UES/jenkins/6.0.UP04/ARCH/easybuild/modules/all',
             scratchCommand: 'echo $SCRATCH',
             sourceProfile: '']


def dom = [name: 'dom',
           archs: ['gpu', 'mc'],
           toolkits: ['CrayCCE', 'CrayGNU', 'CrayIntel', 'CrayPGI'],
           toolkitVersions: ['17.08'],
           unusePath: '/apps/daint/UES/jenkins/6.0.UP04/ARCH/easybuild/modules/all',
           scratchCommand: 'echo $SCRATCH',
           sourceProfile: '']

def kesch = [name: 'kesch',
             archs: [],
             toolkits: ['gmvolf', 'CrayCCE', 'GCC', 'GCCcore', 'gmvapich2', 'foss'],
             toolkitVersions: ['17.02'],
             unusePath: '/apps/escha/UES/generic/modulefiles:/apps/escha/UES/PrgEnv-gnu-17.02/modulefiles:/apps/escha/UES/PrgEnv-cray-17.06/modulefiles:/apps/escha/UES/experimental/modulefiles',
             scratchCommand: 'echo /scratch/jenscscs',
             sourceProfile: 'source $HOME/.profile']

def leone = [name: 'leone',
             archs: [],
             toolkits: ['GCC', 'GCCcore', 'gmvapich2', 'gmvolf', 'foss'],
             toolkitVersions: ['17.06'],
             unusePath: '/apps/leone/UES/PrgEnv-gnu-2016b', 
             scratchCommand: 'echo /scratch/leone/jenscscs',
             sourceProfile: 'source $HOME/.profile']

def monch = [name: 'monch',
             archs: [],
             toolkits: ['GCC', 'GCCcore', 'gmvapich2', 'gmvolf', 'foss'],
             toolkitVersions: ['17.06'],
             unusePath: '/apps/monch/UES/jenkins/RH6.9-17.06/easybuild/modules/all/',
             scratchCommand: 'source $HOME/.profile && echo $SCRATCH',
             sourceProfile: 'source $HOME/.profile']
 

return [daint, dom, kesch, leone, monch]
