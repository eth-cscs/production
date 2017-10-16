def daint = [name: 'daint',
             archs: ['gpu', 'mc'],
             unusePath: '/apps/daint/UES/jenkins/6.0.UP04/ARCH/easybuild/modules/all'] 

def dom = [name: 'dom',
           archs: ['gpu', 'mc'],
           unusePath: '/apps/dom/UES/jenkins/6.0.UP04/ARCH/easybuild/modules/all'] 

def kesch = [name: 'kesch',
             archs: [],
             unusePath: '/apps/escha/UES/generic/modulefiles:/apps/escha/UES/PrgEnv-gnu-17.02/modulefiles:/apps/escha/UES/PrgEnv-cray-17.06/modulefiles:/apps/escha/UES/experimental/modulefiles']

def leone = [name: 'leone',
             archs: [],
             unusePath: '/apps/leone/UES/PrgEnv-gnu-2016b'] 

def monch = [name: 'monch',
             archs: [],
             unusePath: '/apps/monch/UES/jenkins/RH6.9-17.06/easybuild/modules/all/'] 

return [daint, dom, kesch, leone, monch]
