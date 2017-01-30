# EasyBuild Workshop
![EB workshop group photo](https://raw.githubusercontent.com/eth-cscs/tools/master/easybuild/easy_cscs.jpeg)

---

## Slides

  * [Welcome/Intro](https://github.com/eth-cscs/tools/raw/master/easybuild/EasyBuild-intro-workshop-cscs.pdf)  -- G. Peretti

  * EasyBuild: building software with ease -- K. Hoste
    * [Introduction](http://users.ugent.be/~kehoste/EasyBuild-intro-CSCS_20150908.pdf)
    * [Writing easyconfigs and easyblocks: the basics](http://users.ugent.be/~kehoste/EasyBuild-basics-CSCS_20150908.pdf) 

  * [EasyBuild 2.3 on Cray Linux Environment](https://github.com/eth-cscs/tools/raw/master/easybuild/Using-EB-on-CLE-for-CSCS.pdf) -- P. Forai

  * [EasyBuild @ CSCS: Current status and roadmap](https://github.com/eth-cscs/tools/raw/master/easybuild/EasyBuild-workshop-cscs.pdf) -- G. Peretti

  * [Approaching EasyBuild with an Intel toolchain](https://github.com/eth-cscs/tools/raw/master/easybuild/ApproachingEasyBuild.pdf) -- L. Marsella

---

## VM Image for VirtualBox

  * This VM is useful to who
    * doesn't have access to Daint/Dora or 
    * wishes to test Lmod

  * /apps/common/tools/easybuild/EB230.ova (or [here](http://users.ugent.be/~kehoste/EB230.ova))
    * contains Easybuild 2.3.0 + Lmod
    * user/pass
      * eb_lmod/eb_lmod

---

# Hands On Instructions for CSCS

## Setup EB

### To create your own software stack
  * Can be tested on Daint, Dora, Santis, Brisi, Pilatus, Castor, Monch

```
source  /apps/common/easybuild/setup.sh  $SCRATCH 
```

  * This will install your software under $SCRATCH/easybuild (you can choose another prefix and use as argument instead of $SCRATCH

---

## Build your first app
   * HPL on Daint using CrayGNU toolchain

```
eb HPL-2.1-CrayGNU-5.2.40.eb -r
```

This will (1) install the toolchain CrayGNU/5.2.40 (that wraps the PrgEnv) and (2) compile HPL/2.1.
  * Check the logs and try to understand the compilation steps 
    * Which modules were loaded, variables set and compilation parameters
    * [Understanding EasyBuild logs](http://easybuild.readthedocs.org/en/latest/Logfiles.html)
    * You can enable debug logging by adding -d to the command line

---

## Find an existing easyconfig file and build
  * List all easyconfig files available for the toolchain CrayGNU version 5.2.40

```
eb -S CrayGNU-5.2.40
```

  * Choose one file and build (with automatic dependency installation '-r')
    * Full path can be omitted

```
eb YourApp-Cray-5.2.40.eb -r
```

or see the easyconfigs repository @ https://github.com/hpcugent/easybuild-easyconfigs

---

# Using non-cray toolchains on Daint/Dora 

  * Disable Cray experimental support on Daint/Dora

```
unset EASYBUILD_EXPERIMENTAL
unset EASYBUILD_OPTARCH
```

---

## Setup foss/2015b toolchain

### Build complete toolchain (will take a while)
```
eb foss-2015b.eb -r
```

### Use pre-built foss/2015b (DORA only)
```
module use $APPS/sandbox/eb_workshop
```

---

## Build app available from foss/2015b toolchain
  * Find one and build

```
eb -S foss-2015b
eb app.eb -r
```
  
  * Or, for example, you can just try HPL

```
eb HPL-2.1-foss-2015b.eb -r
```