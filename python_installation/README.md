# List of supported Python modules 

* Available on all Python installations (module called "Python", with capital P)
   * the lowercase "python" modules are old versions and are not supported anymore by CSCS

## Notes on the Python modules built with EasyBuild 

* The current set up contains basic modules on the main Python easyconfig file 
* Special modules come as separated easyconfig files 
  * and once installed, they appear as a loadable module.

---

## Built-in modules

* Can be imported after loading the Python module    
  * Setuptools 
  * Pip
  * Nose 
  * Numpy 
  * Scipy 
  * mpi4py 
  * Cython  
  * Six  
  * Virtualenv 
  * pandas  

## Loadable modules

* Need an extra module load before the 'import'
  * h5py (serial/parallel) 
  * matplotlib 
  * pyCuda  (Daint only)
  * netcdf4 