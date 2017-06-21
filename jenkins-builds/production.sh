#!/bin/bash -l

# New modulefiles/software will automatically be added to xalt list of modulefiles (reversemap) at the end of this script.
# Hence one should not use it as CI.
# The xalt list of modulefiles will be updated only by user jenkins. So this script should only be used by jenkins.

scriptname=`basename $0`

usage() {
    echo "Usage: $0 [OPTIONS] <list-of-ebfiles>
    -p installation prefix folder (mandatory)
    -a architecture (Piz Daint only)
    -l production list (contains list of eb files)
    -f force the build for a given package (optional)
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

if [ -z "$PREFIX" ]; then
    echo -e "\n Prefix folder not defined. Please use the option -p to define the prefix folder \n"
    usage
    exit 1
fi

if [ -z "$ARCH" ] && [[ $system =~ "daint" ]]; then
    echo -e "\n No architecture defined. Please use the option -a to define the architecture \n"
    usage
    exit 1
fi

#
# These are additional args to be used based on the system
#
eb_args=""

# defines OS VERSION and ARCH parsing the selected production filename
echo -e "\n - PREFIX FOLDER: '$PREFIX'"
if [ -n "$ARCH" ]; then
    echo -e " - ARCH: '$ARCH' \n"
fi
if [ ${#production_files[@]} -eq 1 ]; then
    echo -e " Production file is: ${production_files[@]}"
elif [ ${#production_files[@]} -gt 1 ]; then
    echo -e " Production files are: ${production_files[@]}"
fi

# list of builds
echo -e "\n List of production builds with additional options: \n"
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

# loop over list
for ((i = 0; i < ${#eb_files[@]}; i++)); do
    build=${eb_files[$i]}

    echo -e "\n===============================================================\n"

# define name and version of the current build
    name=`echo ${build} | cut -d'-' -f 1`

    #
    # VASP and CPMD builds
    #
    if [[ $build == *"VASP"* || $build == *"CPMD"* ]]; then

        #echo -e "Creating a footer for ${name} modulefile to warn users not belonging to group ${name,,}\n"
        tmp_footer=""
        if [ "Xdaint" == "X$hostName" ]; then
           tmp_footer="--modules-footer=${EASYBUILD_TMPDIR}/${name}.footer"
           cat > ${EASYBUILD_TMPDIR}/${name}.footer<<EOF
if { [lsearch [exec groups] "${name,,}"]==-1 && [module-info mode load] } {
 puts stderr "WARNING: Only users belonging to group ${name,,} with a valid ${name} license are allowed to access ${name} executables and library files"
}
EOF
        fi
        echo -e "eb $build -r ${eb_args} ${tmp_footer}\n"
        eb $build -r ${eb_args} ${tmp_footer}

        # change permissions for selected builds (note that $USER needs to be member of the group to use the command chgrp)
        echo -e "\n Changing group ownership and permissions for ${name} folders:\n - ${EASYBUILD_PREFIX}/software/${name}"
        chgrp ${name,,} -R ${EASYBUILD_INSTALLPATH}/software/${name}
        chmod -R o-rwx ${EASYBUILD_INSTALLPATH}/software/${name}/*

        #
        # The other builds
        #
    else
        echo -e "eb $build -r ${eb_args}"
        eb $build -r ${eb_args}
    fi

done

if [ "Xdaint" == "X$hostName" ]; then
    # update xalt table of modulefiles
    echo "loading PrgEnv-cray"
    module load PrgEnv-cray/6.0.3
    echo "module use craypat apps"
    module use /apps/daint/UES/6.0.UP02/craypat/easybuild/modules/all
    # Removing Easybuild module before the reverseMapD operation
    # because spider the mapping the programs to Easybuild
    module unload Easybuild
    echo "running reverseMapD"
    userid=`id -u`
    # run only for jenscscs user
    if [ "X$userid" == "X23395" ]; then
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
