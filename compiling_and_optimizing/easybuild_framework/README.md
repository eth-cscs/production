# EasyBuild framework

The [EasyBuild](http://easybuild.readthedocs.org/en/latest/Writing_easyconfig_files.html) framework is available through the module `EasyBuild-custom`. This module defines the location of the EasyBuild configuration files, recipes and installation directories.

```
module load EasyBuild-custom
```

On Piz Daint, which is a heterogeneous system, you need to select which architecture should be targeted when building software. For example you can target the Intel Haswell architecture accessing the **gpu** software stack using the command below:

```
module load daint-gpu EasyBuild-custom
```

Alternatively, you can target the Intel Broadwell architecture and the **mc** (multicore) software stack:

```
module load daint-mc EasyBuild-custom
```

---

On Piz Daint, EasyBuild software and modules will be installed by default under the following folder:

```
$HOME/easybuild/<system-name>/<architecture>
```

Here `<architecture>` is either `<haswell>` or `<broadwell>`. On the other systems the default installation folder is instead the following:

```
$HOME/easybuild/<system-name>
```

The variable `<system-name>` is the login name of the system, e.g. daint, leone, monch... You can override the default installation folder and the default repository path by exporting the environment variables listed below, before loading the EasyBuild modulefile:

```
export EASYBUILD_PREFIX=/your/preferred/installation/folder
export EB_CUSTOM_REPOSITORY=/your/cscs/repository/folder
module load EasyBuild-custom
```

---

## Building a program

Please load the EasyBuild-custom module to build your code using the EasyBuild command `eb`:

```
module load EasyBuild-custom
eb <filename>.eb -r
```

The build command just needs the configuration file name and not the full path, provided that the configuration file is in your search path. You can check if any EasyBuild configuration file already exists for a given program name, using the following search command:

```
eb -S <program_name>.eb
```

Please note that on Cray systems you can use the configuration files that make use of a Cray toolchain, which you will find in the configuration filename (`eb -S <name> | grep Cray`)

---

You will then be able to load modules that have been created by EasyBuild in the folder that you have selected with the `EASYBUILD_PREFIX` variable:

```
module use $EASYBUILD_PREFIX/modules/all
module load <modulename>/version
```

The command module use will prepend the selected folder to your `MODULEPATH` environment variable, therefore you will see the new modules with module avail.
Please note that by default `EASYBUILD_PREFIX` is set to a folder inside your `$HOME`, however the `$HOME` folder is by default not readable by other users.
Therefore if you want to make your builds available to your group, then you need to allow read-only access to other members of your group using the command `chmod g+rx $HOME`.