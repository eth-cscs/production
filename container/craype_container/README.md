# Contenairizing Cray PE

## Proof of Concept Objectives

1. Enable the capability to build container with any PE version
   * Full module list is present including cudatoolkit

2. A CRAYPE-BUILD container can build any application
   * Input: source codes are mounted inside the container
   * Output: binaries are installed outside the container
   * One can add the required tools to build an app inside the container (easybuild,…)

3. A CRAYPE-RUN container can run an application built with a PE-build container
   * The container holds the binaries and the runtime libraries
   * Special environment can be setup


# DISCLAIMER:

1. _Manipulating Cray PE should be done on a Cray system_
2. _For secuirty reason, it is forbidden to install Docker on a Cray machine or on a machine having access to a parallel file system_
3. _You can't build sources using a Contenarized PE with Shifter-NG installed on Daint (the CN /opt is mounted by Shifter-NG and replace the one in the container where the PE is located)_


# Building the CRAYPE-BUILD container

## Step 0

Docker should have an image installed based on the elogin node.
To install such image, copy the file `elogin_prod_up07_20181205160931.squashfs`, convert it and install it inside docker.
You will need to have the 'squashfs tools' installed.

```
$ scp /project/.../elogin_prod_up07_20181205160931.squashfs .
$ mkdir unsqashfs
$ sudo unsquashfs -f -d unsquashfs elogin_prod_up07_20181205160931.squashfs
$ sudo tar -C unsquashfs -c . | docker import - elogin_prod:up07_20181205160931
```

## Step 1

Obtain the Cray PE you want to install in the format of an iso files.
Iso files are located in CrayPort, you can download them.
Example: `CDT-16.11-07.iso` or `CDT-18.10-03.iso`

## Step 2

Copy from `/project/.../cuda/*.rpm` inside a directory named `cuda` in the same location as the Dockerfile

## Step 3

Mount the iso file into a directory named `volume/<my cdt version>` in the same location as the Dockerfile to create the containerized Cray PE.

```
$ ls .
Dockerfile
cuda
volume

$ ls cuda/
cray-cudatoolkit7.5-7.5.18_2.1.7-6.0.7.0_18.1__gd80efc5.x86_64.rpm
cray-cudatoolkit8.0-8.0.61_2.4.9-6.0.7.0_17.1__g899857c.x86_64.rpm
cray-cudatoolkit9.0-9.0.103_3.15-6.0.7.0_14.1__ge802626.x86_64.rpm
cray-cudatoolkit9.1-9.1.85_3.18-6.0.7.0_5.1__g2eb7c52.x86_64.rpm
cray-cudatoolkit9.2-9.2.148_3.19-6.0.7.1_2.1__g3d9acc8.x86_64.rpm
cray-nvidia-libcuda-390.46_3.1.30-6.0.7.0_24.8__g83596c3.ari.x86_64.rpm
cray-nvidia-libcuda-390.46_3.1.32-6.0.7.1_6.1__g15a0cc2.ari.x86_64.rpm
cray-nvidia-libcuda-396.44_3.1.31-6.0.7.1_2.1__g97ab0cf.ari.x86_64.rpm
cray-nvidia-libcuda-396.44_3.1.33-6.0.7.1_3.2__gac01daf.ari.x86_64.rpm

$ ls volume/
16.11-07

$ ls volume/16.11-07/
TRANS.TBL    conf         docs         installer    packages     release_info
```

## Step 4

Execute the build process of docker. You need to select 4 arguments for the build process:
   - CDT_VERSION which is the Cray PE version (the iso) [default 18.10-03PRE]
   - CPU_TARGET which is a cpu name like haswell, broadwell,... [default haswell]
   - ACCELERATORS which is the GPU family name like PASCAL, KEPLER,... [default PASCAL]
   - CUDATOOLKIT which is the cuda toolkit version: 7.5, 8.0,... [default 7.5]
 
Select a name and a tag for the image that reflect this selection like:
craype:cdt16.11-07.haswell.pascal.cudatoolkit7.5

```
$ docker build --build-arg CDT_VERSION=16.11-07 \
                -t craype:cdt16.11-07.haswell.pascal.cudatoolkit7.5 .
```

and wait... it takes a couple of hours.


## Step 5

Run the container and compile your code

```
$ docker run -v /Users/maximem/dev/docker/my_source:/home/pe_user/sources \
             -v /Users/maximem/dev/pe_container/my_binaries:/home/pe_user/install \
             --rm -it craype:cdt16.11-07.haswell.pascal.cudatoolkit7.5 /bin/bash
```

# Building the CRAYPE_RUN container

The purpose of this container is to contain the binaries and runtime libraries that
have been built with a CRAYPE_BUILD container.

## Step 6

Once your code has been compiled, you need to extract all dependencies by using ldd.
A tool has been added to help you inside the CRAYPE_BUILD container.
We suppose that the code you have built is installed in `/home/pe_user/install`.
From that container do:

```
$ cd /home/pe_user/install
$ ldd_parser --binaries /opt/cray/pe/cce/8.7.3/cce/x86_64/lib/libfi.so
ldd: warning: you do not have execution permission for `/opt/gcc/6.2.0/snos/lib/../lib64/libgcc_s.so.1'
ldd: warning: you do not have execution permission for `/opt/cray/pe/gcc-libs/libgcc_s.so.1'
/opt/cray/pe/gcc-libs/libstdc++.so.6
/opt/cray/pe/gcc-libs/libgfortran.so.3
/opt/cray/pe/cce/8.7.3/cce/x86_64/lib/libf.so.1
/opt/cray/pe/cce/8.7.3/cce/x86_64/lib/libcsup.so.1
/opt/cray/pe/cce/8.7.3/cce/x86_64/lib/libu.so.1
/opt/cray/pe/cce/8.7.3/cce/x86_64/lib/libcraymath.so.1
Duplicated reference to libraries:
/opt/cray/pe/cce/8.7.3/cce/x86_64/lib/libquadmath.so.0
/opt/cray/pe/gcc-libs/libgcc_s.so.1
/opt/gcc/6.2.0/snos/lib/../lib64/libgcc_s.so.1
/opt/gcc/6.2.0/snos/lib/../lib64/libquadmath.so.0
Dlopen identified libraries:
libmemkind.so.0
libnuma.so
$ # copy the required libraries to /home/pe_user/install
```

Note that the `ldd_parser` will identify libraries recursively of all dependencies, it might find duplicated references and it will try to find out `dlopen` libraries.
You need to select which libraries to copy.
It is not a perfect tool to find all dependencies, so at running time libraries could be missed (you need an error and trial approach).
Now in `/home/pe_user/install` you should see all the libraries of the PE required by your binaries.
You can now leave the CRAYPE_BUILD container

## Step 7

Let's build the container that will hold the just-built binaries.
This container is called a CRAYPE_RUN, it expect to have the binaries to install
inside a directory called `install` at the same level as the Docerkfile.CRAYPE_RUN.

```
$ docker build craype_run:myapplication_1.0 .
```

## Step 8

You can now run the CRAYPE_RUN container and your binaries.

```
$ docker run -it --rm craype_run:myapplication_1.0
$ ./mybin1
```

End of instruction.




