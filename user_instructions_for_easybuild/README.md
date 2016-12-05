## Set up EasyBuild environment:

On CSCS systems, EasyBuild is available through the module `EasyBuild-custom`. This module defines the location of EasyBuild configuration files, recipes and installation directories. 

<pre>
$ module load EasyBuild-custom
</pre>

On Piz Daint, which is a heterogeneous system, you need to select which architecture should be targeted when building software. 

For example: targeting **haswell** and accessing the **gpu** software stack 

<pre>
$ module load daint-gpu EasyBuild-custom
</pre>

or: for targeting **broadwell** and accessing the **mc** (multicore) software stack 

<pre>
$ module load daint-mc EasyBuild-custom
</pre>

---

On Piz Daint, the EasyBuild software and modules will be installed by default at 

<pre>
$HOME/easybuild/&ltsystem-name&gt/&ltarchitecture&gt
</pre>

and for other systems

<pre>
$HOME/easybuild/&ltsystem-name&gt
</pre>

where:
`system-name` is the name of the cluster, e. g., `daint`, `leone`, `monch`. And `architecture` is either `haswell` or `broadwell`.

## Changing the default installation folder and custom CSCS custom EasyBuild repository

You can override the default installation folder (`EASYBUILD_PREFIX`) and the default CSCS repository folder (`EB_CUSTOM_REPOSITORY`) by exporting:
<pre>
$ export EASYBUILD_PREFIX=/your/preferred/installation/folder
$ export EB_CUSTOM_REPOSITORY=/your/cscs/repository/folder
$ module load EasyBuild-custom
</pre>

---

## Building a program
<pre>
$ eb Program-xxxxxxx.eb -r
</pre>

## Using the new modules on a clean shell

You need to load the `EasyBuild-custom` module before using your own modules
<pre>
$ module load EasyBuild-custom
$ module load ProgramModuleName/version
</pre>

Note that *ALL* previous section apply to this stage. Therefore any change to the `EASYBUILD_PREFIX` variable should be performed before loading the `EasyBuild-custom` module.

<pre>
$ export EASYBUILD_PREFIX=/your/preferred/installation/folder (if set when the desired software was installed)
$ module load EasyBuild-custom
$ module load ProgramModuleName/version
</pre>
Alternatively, one can use just the easy-built program module directly
<pre>
$ module use /your/easybuild_installpath/installation/folder/modules/all
$ module load ProgramModuleName/version
</pre>

---

## Sharing modules with your group

By default the `EASYBUILD_PREFIX` is set to a folder inside your `$HOME`. But the `$HOME` folder is not readable by other users. Therefore you need to allow read-only access 
to others `$ chmod g+rx $HOME` or you need to change the `EASYBUILD_PREFIX` variable to point to a folder inside `$SCRATCH` and re-compile the software.