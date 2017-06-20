# Jenkins production builds (EasyBuild)

## Disclaimer

* Use the files below to keep the list of eb files used on production up to date. 

* All changes need to be reviewed:
   * **please issue a Pull Request** for adding new packages 

## Link to EB file lists 
* **Piz Daint**
  * [6.0.UP02-2016.11-gpu](https://github.com/eth-cscs/production/blob/master/jenkins-builds/6.0.UP02-2016.11-gpu): CUDA/haswell software stack
  * [6.0.UP02-2016.11-mc](https://github.com/eth-cscs/production/blob/master/jenkins-builds/6.0.UP02-2016.11-mc): Multicore/broadwell software stack
* **Mönch**: [monch-RH6.9-17.06](https://github.com/eth-cscs/production/blob/master/jenkins-builds/monch-RH6.9-17.06)
* **Piz Escha/Kesch**: [MCH-RH6.7-15.11](https://github.com/eth-cscs/production/blob/master/jenkins-builds/MCH-RH6.7-15.11)
* Generic RH6.7 builds (Kesch): [common-RH6.7-2016.10](https://github.com/eth-cscs/production/blob/master/jenkins-builds/common-RH6.7-2016.10)
  * builds based on RH6.7 system gcc (Kesch / module purge)
    * Usable on kesch  
      * ```module use /apps/common/UES/jenkins/RH6.7/easybuild/modules/all```
* Generic SLES12 builds (Daint, santis, brisi, dom): [common-SLES12-2016.10](https://github.com/eth-cscs/production/blob/master/jenkins-builds/common-SLES12-2016.10)
    * Generic builds based on SLES12 system gcc ( = gcc/4.8.5 brisi101, unset EASYBUILD_OPTARCH)
    *  Usable on dom, daint
      * ```module use /apps/common/UES/jenkins/SLES12/easybuild/modules/all```
