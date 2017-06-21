#!/bin/bash -l

# New modules will be added to xalt list (reversemap) at the end of this script, so one shouldn't use it as CI.
# The xalt list will be updated only by user jenkins, therefore this script can only be used by user jenkins.

scriptname=$(basename $0)

usage() {
    echo "Usage: $0 [OPTIONS] <list-of-ebfiles>
    -p installation prefix folder               (mandatory)
    -a architecture                             (mandatory on Piz Daint only)
    -l production list                          (mandatory: contains the list of EasyBuild files with extension '.eb')
    -f force the build for a given package      (optional)
    -h help
    "
    exit 1;
}

shortopts="h,p:,a:,l:,f:"
eval set -- $(getopt -o ${shortopts} -n ${scriptname} -- "$@" 2> /dev/null)

eb_files=()
production_files=()
while [ $# -ne 0 ]; do
    case $1 in
        -h | --help)
            usage
            exit 0 ;;
        -p)
            shift
            PREFIX="$1" ;;
        -a)
            shift
            ARCH="$1" ;;
        -f)
            shift
            eb_files+=("$1 -f")
            ;;
        -l)
            shift
            mapfile -t list < $1
            for ((i = 0; i < ${#list[@]}; i++)); do
                eb_files+=("${list[$i]}")
            done
            production_files+=($1)
            ;;
        --)
            ;;
        *)
            eb_files+=($1)
            ;;
    esac
    shift
done

# system name (excluding node number)
if [[ "$HOSTNAME" =~ esch ]]; then
 system=$(hostname | sed 's/ln-[0-9]*//g');
else
 system=$(hostname | sed 's/[0-9]*//g');
fi

# define prefix folder
if [ -z "$PREFIX" ]; then
    echo -e "\n Prefix folder not defined. Please use the option -p to define the prefix folder \n"
    usage
    exit 1
fi

# define architecture (Piz Daint only)
if [ -z "$ARCH" ] && [[ $system =~ "daint" ]]; then
    echo -e "\n No architecture defined. Please use the option -a to define the architecture \n"
    usage
    exit 1
fi

# optional EasyBuild arguments
eb_args=""

# prints production file(s), PREFIX, ARCH
echo -e "\n - Production file(s): ${production_files[@]}"
echo -e " - PREFIX FOLDER: '$PREFIX'"
if [ -n "$ARCH" ]; then
    echo -e " - ARCH: '$ARCH' \n"
fi

# list of builds
echo -e "\n List of builds (including options): \n"
for ((i = 0; i < ${#eb_files[@]}; i++)); do
    echo ${eb_files[$i]}
done

# cscs ARCH setup
if [[ $system =~ "daint" ]]; then
    module load daint-$ARCH
    echo -e "\n Loading modules: \n - module load daint-$ARCH"
    module rm xalt
    eb_args="${eb_args} --modules-header=$APPS/UES/login/daint-${ARCH}.h"
fi

# EasyBuild setup
export EASYBUILD_PREFIX=$PREFIX/easybuild
export EB_CUSTOM_REPOSITORY=$PWD/easybuild
module use $PWD/easybuild/module
module load Easybuild
export EASYBUILD_BUILDPATH=/dev/shm/$USER/easybuild/stage
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

# cumulative exit status of EasyBuild commands in the loop
status=0
# loop over the list of EasyBuild files to build
for((i=0; i<${#eb_files[@]}; i++)); do

    echo -e "\n===============================================================\n"

# define name and version of the current build
    name=$(echo ${eb_files[$i]} | cut -d'-' -f 1)

# build VASP and CPMD
    if [[ $name =~ "VASP" || $name =~ "CPMD" ]]; then
# creating a footer for ${name} modulefile to warn users not belonging to group ${name,,}
        tmp_footer=""
        if [[ system =~ "daint" ]]; then
            tmp_footer="--modules-footer=${EASYBUILD_TMPDIR}/${name}.footer"
            cat > ${EASYBUILD_TMPDIR}/${name}.footer<<EOF
if { [lsearch [exec groups] "${name,,}"]==-1 && [module-info mode load] } {
 puts stderr "WARNING: Only users belonging to group ${name,,} with a valid ${name} license are allowed to access ${name} executables and library files"
}
EOF
        fi
        echo -e "eb ${eb_files[$i]} -r ${eb_args} ${tmp_footer}\n"
        eb ${eb_files[$i]} -r ${eb_args} ${tmp_footer}
        status=$[status+$?]

# change permissions for selected builds (note that $USER needs to be member of the group to use the command chgrp)
        echo -e "\n Changing group ownership and permissions for ${name} folders:\n - ${EASYBUILD_PREFIX}/software/${name}"
        chgrp ${name,,} -R ${EASYBUILD_INSTALLPATH}/software/${name}
        chmod -R o-rwx ${EASYBUILD_INSTALLPATH}/software/${name}/*

# build other software
    else
        echo -e "eb ${eb_files[$i]} -r ${eb_args}"
        eb ${eb_files[$i]} -r ${eb_args}
        status=$[status+$?]
    fi
done

if [[ $system =~ "daint" ]]; then
# update xalt table of modulefiles
    echo "loading PrgEnv-cray"
    module load PrgEnv-cray/6.0.3
    echo "module use craypat apps"
    module use /apps/daint/UES/6.0.UP02/craypat/easybuild/modules/all
# removing Easybuild module before the reverseMapD operation
    module unload Easybuild
    echo "running reverseMapD"
    userid=$(id -u)
# commands run by jenscscs user only
    if [ $userid -eq 23395 ]; then
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

exit $[status+$?]
