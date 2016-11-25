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
echo -e "\n List of production builds: \n $list"

# cscs ARCH setup
module load daint-$ARCH
echo -e "\n Loading modules: \n - module load daint-$ARCH"

# EasyBuild setup
echo -e "\n EasyBuild setup: \n source $PWD/easybuild/setup.sh $APPS/UES/jenkins/$OS/$ARCH $PWD"
source $PWD/easybuild/setup.sh $APPS/UES/jenkins/$OS/$ARCH $PWD

# start time
echo -e "\n Builds started on $(date)"

# loop over list 
for build in $list; do
# build
 echo -e "\n eb $build -r --modules-header=$APPS/UES/login/daint-${ARCH}.h \n"
 eb $build -r --modules-header=$APPS/UES/login/daint-${ARCH}.h 
# define name and version of the current build
 version=$(basename ${build#[aA-z-Z]*-} .eb)
 name=${build%-${version}.eb}
# create default
 echo -e "\n Creating file ${EASYBUILD_PREFIX}/modules/all/${name}/.version to set ${version} as default for ${name}"
 cat > ${EASYBUILD_PREFIX}/modules/all/${name}/.version<<EOF 
#%Module
set ModulesVersion "${version}"
EOF
# change permissions for selected builds (note that $USER needs to be member of the group to use the command chgrp)
 if [[ ${name} =~ "CPMD" || ${name} =~ "VASP" ]]; then
  echo -e "\n Changing permissions (umask 750) for ${name} folders:\n - ${EASYBUILD_PREFIX}/modules/all/${name} \n - ${EASYBUILD_PREFIX}/software/${name}"
  chmod 750 ${EASYBUILD_PREFIX}/modules/all/${name} ${EASYBUILD_PREFIX}/software/${name}/*
  chgrp ${name,,} ${EASYBUILD_PREFIX}/modules/all/${name} ${EASYBUILD_PREFIX}/software/${name}
 fi
done 

# end time
echo -e "\n Builds ended on $(date)"
