#!/bin/bash -l

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

# EasyBuild setup
export EASYBUILD_PREFIX=$APPS/UES/jenkins/$OS/$ARCH/easybuild
export EB_CUSTOM_REPOSITORY=$PWD/easybuild
module use $PWD/easybuild/module
module load Easybuild
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

# loop over list
for build in $list; do

# define name and version of the current build
 version=$(basename ${build#[aA-z-Z]*-} .eb)
 name=${build%-${version}.eb}

 echo -e "\n===============================================================\n"
# build
eb -f EasyBuild-custom-cscs.eb

### START workaround for Dom
 fullpath=$(eb --search $build | grep -v = | awk '{print $2}');
 sed "s/44_GA_2.2.7_g4a6c213-2.1/34_2.2.5_g8ce7a9a-2.1/" $fullpath > ./$build
### END workaround for Dom

# use module footer and adjust ownership and permissions for selected builds
 if [[ ${name} =~ "CPMD" || ${name} =~ "VASP" ]]; then
  echo -e "Creating a footer for ${name} modulefile to warn users not belonging to group ${name,,}\n"
  cat > ${EASYBUILD_TMPDIR}/${name}.footer<<EOF
if { [lsearch [exec groups] "${name,,}"]==-1 && [module-info mode load] } {
 puts stderr "WARNING: Only users belonging to group ${name,,} with a valid ${name} license are allowed to access ${name} executables and library files"
}
EOF
  echo -e "eb ./$build -r --modules-header=$APPS/UES/login/daint-${ARCH}.h --modules-footer=${EASYBUILD_TMPDIR}/${name}.footer\n"
  eb ./$build -r --modules-header=$APPS/UES/login/daint-${ARCH}.h --modules-footer=${EASYBUILD_TMPDIR}/${name}.footer
# change permissions for selected builds (note that $USER needs to be member of the group to use the command chgrp)
  echo -e "\n Changing group ownership and permissions for ${name} folders:\n - ${EASYBUILD_PREFIX}/software/${name}"
  chgrp ${name,,} -R ${EASYBUILD_INSTALLPATH}/software/${name}
  chmod -R o-rwx ${EASYBUILD_INSTALLPATH}/software/${name}/*
# standard build without need to add a module footer or adjusting ownership and permissions
 else
  echo -e "eb ./$build -r --modules-header=$APPS/UES/login/daint-${ARCH}.h"
  eb ./$build -r --modules-header=$APPS/UES/login/daint-${ARCH}.h
 fi

# create default
 echo -e "\n Creating file ${EASYBUILD_INSTALLPATH}/modules/all/${name}/.version to set ${version} as default for ${name}"
 cat > ${EASYBUILD_INSTALLPATH}/modules/all/${name}/.version<<EOF
#%Module
set ModulesVersion "${version}"
EOF
### START workaround for Dom
 rm -f ./$build
### END workaround for Dom
done

# end time
endtime=$(date +%s)
# time difference
difftime=$(($endtime-$starttime))
# convert seconds to hours minutes seconds format
 ((h=${difftime}/3600))
 ((m=(${difftime}%3600)/60))
 ((s=${difftime}%60))
echo -e "\n Builds ended on $(date) (elapsed time is $difftime s : ${h}h ${m}m ${s}s) \n"
