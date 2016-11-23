# Jenkins production builds (EasyBuild)

## Disclaimer

* Use the files below to keep the list of eb files used on production up to date. 

* All changes need to be reviewed:
   * **please issue a Pull Request** for adding new packages 
   * [Procedure for accepting pull requests](https:///production/wikis/home) 

## Link to EB file lists 
* [6.0.UP01-2016.06] (https:///production/blob/master/6.0.UP01-2016.06-brisi)
  * Will be installed by Jenkins on Brisi

* [6.0.UP02-2016.11] (https:///production/blob/master/6.0.UP01-2016.11) (TODO)
  * Will be installed by Jenkins on Daint+ (haswell and broadwell versions)

* [monch-RH6.7-15.12](https:///production/blob/master/monch-RH6.7-15.12)
  * Will be installed on  Monch

* [MCH-RH6.7-15.11](https:///scs/production/blob/master/MCH-RH6.7-15.11)
  * Will be installed on Escha/Kesch 

* [common-SLES12-2016.10](https:///scs/production/blob/master/common-RH6.7-2016.10)
  * Generic builds based on RH6.7 system gcc ( Kesch / module purge)
  * Will be installed by jenkins in /apps/common/UES/jenkins/RH6.7
    * Usable on kesch  
      * ```module use /apps/common/UES/jenkins/RH6.7/easybuild/modules/all```

* [common-SLES12-2016.10](https:///scs/production/blob/master/common-SLES12-2016.10)
  * Generic builds based on SLES12 system gcc ( = gcc/4.8.5 brisi101, unset EASYBUILD_OPTARCH)
  * Will be installed by jenkins in /apps/common/UES/jenkins/SLES12/
    *  Usable on santis, brisi, dom, daint
      * ```module use /apps/common/UES/jenkins/SLES12/easybuild/modules/all```
