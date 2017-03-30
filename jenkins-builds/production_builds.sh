#!/bin/bash -l

# NEW: new modulefiles/software will automatically be added to xalt list of modulefiles (reversemap) at the end of this script.
# Hence one should not use it as CI.
# The xalt list of modulefiles will be updated only by user jenkins. So this script should only be used by jenkins.

# Retrieve host name (excluding node number)
if [[ -z $hostName ]] ; then
    hostName=`uname -n | cut -c1-5`
fi

# expects production file as command line argument
if [ -z "$1" ]; then
 echo -e "\n Error! Please insert production file on command line! \n"
 exit 1
else
 filename=$(basename $1)
fi

# defines OS VERSION and ARCH parsing the selected production filename
OS=${filename%-[0-9]*.[0-9]*-[a-z]*}
ARCH=${filename#$OS-[0-9]*.[0-9]*-}
echo -e "\n Production file is $1: \n - OS VERSION is $OS \n - ARCH is $ARCH"

# list of builds
list=$(cat $1 | grep -v ^#)
echo -e "\n List of production builds: \n$list"

# cscs ARCH setup
module load daint-$ARCH
echo -e "\n Loading modules: \n - module load daint-$ARCH"
module rm xalt

# EasyBuild setup
export EASYBUILD_PREFIX=$APPS/UES/jenkins/$OS/$ARCH/easybuild
export EB_CUSTOM_REPOSITORY=$PWD/easybuild
module use $PWD/easybuild/module
module load Easybuild
export EASYBUILD_BUILDPATH=/dev/shm/jenscscs/easybuild/stage-$ARCH
echo -e "\n Easybuild setup:"
echo -e " - EASYBUILD_PREFIX=$EASYBUILD_PREFIX"
echo -e " - EB_CUSTOM_REPOSITORY=$EB_CUSTOM_REPOSITORY"
echo -e " - module load EasyBuild-custom/cscs"

echo -e "\n Easybuild configuration:"
echo -e " - eb --show-config"
eb --show-config

# start time
echo -e "\n Builds started on $(date)"
starttime=$(date +%s)

# Installing the EasyBuild-custom/cscs module
eb -f EasyBuild-custom-cscs.eb

# loop over list
for build in $list; do

# define name and version of the current build
 version=$(basename ${build#[aA-z-Z]*-} .eb)
 name=${build%-${version}.eb}

 echo -e "\n===============================================================\n"
# build

# use module footer and adjust ownership and permissions for selected builds
 if [[ ${name} =~ "CPMD" || ${name} =~ "VASP" ]]; then
  echo -e "Creating a footer for ${name} modulefile to warn users not belonging to group ${name,,}\n"
  cat > ${EASYBUILD_TMPDIR}/${name}.footer<<EOF
if { [lsearch [exec groups] "${name,,}"]==-1 && [module-info mode load] } {
 puts stderr "WARNING: Only users belonging to group ${name,,} with a valid ${name} license are allowed to access ${name} executables and library files"
}
EOF
  echo -e "eb $build -r --modules-header=$APPS/UES/login/daint-${ARCH}.h --modules-footer=${EASYBUILD_TMPDIR}/${name}.footer\n"
  eb $build -r --modules-header=$APPS/UES/login/daint-${ARCH}.h --modules-footer=${EASYBUILD_TMPDIR}/${name}.footer
# change permissions for selected builds (note that $USER needs to be member of the group to use the command chgrp)
  echo -e "\n Changing group ownership and permissions for ${name} folders:\n - ${EASYBUILD_PREFIX}/software/${name}"
  chgrp ${name,,} -R ${EASYBUILD_INSTALLPATH}/software/${name}
  chmod -R o-rwx ${EASYBUILD_INSTALLPATH}/software/${name}/*
# standard build without need to add a module footer or adjusting ownership and permissions
 else
  echo -e "eb $build -r --modules-header=$APPS/UES/login/daint-${ARCH}.h"
  eb $build -r --modules-header=$APPS/UES/login/daint-${ARCH}.h
 fi

# create default
 echo -e "\n Creating file ${EASYBUILD_INSTALLPATH}/modules/all/${name}/.version to set ${version} as default for ${name}"
 cat > ${EASYBUILD_INSTALLPATH}/modules/all/${name}/.version<<EOF
#%Module
set ModulesVersion "${version}"
EOF
done

# update xalt table of modulefiles
userid=`id -u`
if [ "X$userid" == "X23395" ] && [ "X$hostName" == "Xdaint" ]; then
	module purge
	module load Lmod
	export PATH=$EBROOTLMOD/lmod/7.1/libexec:$PATH  # !!! for spider !!!
	export XALTJENKINS=/apps/daint/UES/xalt/JENSCSCS
	export XALTPROD=/apps/daint/UES/xalt/git
	cd $XALTJENKINS/
	rm -rf $XALTJENKINS/reverseMapD
	./cray_build_rmapT.sh .
	cp ./reverseMapD/*    $XALTPROD/etc/reverseMapD/
	cd -
fi

# end time
endtime=$(date +%s)
# time difference
difftime=$(($endtime-$starttime))
# convert seconds to hours minutes seconds format
 ((h=${difftime}/3600))
 ((m=(${difftime}%3600)/60))
 ((s=${difftime}%60))
echo -e "\n Builds ended on $(date) (elapsed time is $difftime s : ${h}h ${m}m ${s}s) \n"
