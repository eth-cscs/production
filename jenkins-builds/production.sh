#!/bin/bash

# New modules will be added to xalt list (reversemap) at the end of this script, so one shouldn't use it as CI.
# The xalt list will be updated only by user jenkins, therefore this script can only be used by user jenkins.

# name of the script withouth the path
scriptname=$(basename $0)
# path to the folder containing the script
scriptdir=$(dirname $0)

usage() {
    echo -e "\n Usage: $0 [OPTIONS] -l <list> -p <prefix>
    
    -a,--arch     Architecture (gpu or mc)           (mandatory: Dom and Piz Daint only)
    -f,--force    Force build of item(s) in list     (optional: double quotes for multiple items)
    -h,--help     Help message
    -l,--list     Absolute path to production file   (mandatory: EasyBuild production list)
    -p,--prefix   Absolute path to EasyBuild prefix  (mandatory: installation folder)
    -u,--unuse    Module unuse colon separated PATH  (optional: default is null)
    -x,--xalt     [yes|no] update XALT database      (optional: default is yes)
    "
    exit 1;
}

longopts="arch:,force:,help,list:,prefix:,unuse:,xalt:"
shortopts="a:,f:,h,l:,p:,u:,x:"
eval set -- $(getopt -o ${shortopts} -l ${longopts} -n ${scriptname} -- "$@" 2> /dev/null)

eb_files=()
eb_lists=()
while [ $# -ne 0 ]; do
    case $1 in
        -a | --arch)
            shift
            ARCH="$1"
            ;;
        -f | --force)
            shift
            force_list="$1"
            ;;
        -h | --help)
            usage
            ;;
        -l | --list)
            shift
            mapfile -O ${#eb_files[@]} -t eb_files < $1
            eb_lists+=($1)
            ;;
        -p | --prefix)
            shift
            PREFIX="$1"
            ;;
        -u | --unuse)
            shift
            unuse_path="$1"
            ;;
        -x | --xalt)
            shift
            update_xalt_table={$1,,}
            ;;
        --)
            ;;
        *)
            usage
            ;;
    esac
    shift
done

# checks force_list
if [ -n "${force_list}" ]; then
# match force_list items with production lists: 
# 'grep -n' returns the 1-based line number of the matching pattern within its file
 idx=();
 nidx=0; 
 for item in ${force_list}; do 
     idx[$nidx]=$(cat ${eb_lists[@]} | grep -n $item | awk -F ':' '{print $(NF-1)-1}') 
     ((nidx++)) 
 done
# append force flag '-f' to matching items in production lists
 for ((i=0; i<$nidx; i++)); do
     eb_files[${idx[$i]}]+=" -f"
 done
fi

# optional EasyBuild arguments
eb_args=""

# system name (excluding node number)
if [[ "$HOSTNAME" =~ esch ]]; then
 system=${HOSTNAME%%[cl]n-[0-9]*}
else
 system=${HOSTNAME%%[0-9]*}
fi

# --- SYSTEM SPECIFIC SETUP ---
if [[ "$system" =~ "daint" || "$system" =~ "dom" ]]; then
# architecture (Dom and Piz Daint only)
    if [ -z "$ARCH" ]; then
        echo -e "\n No architecture defined. Please use the option -a,--arch to define the architecture \n"
        usage
    else
        module purge
        module load craype craype-network-aries modules perftools-base ugni
        module load daint-${ARCH}
        eb_args="${eb_args} --modules-header=${scriptdir%/*}/login/daint-${ARCH}.h --modules-footer=${scriptdir%/*}/login/daint.footer"
    fi
fi

# --- COMMON SETUP ---
# xalt table update for Piz Daint
if [ -z "$update_xalt_table" ]; then
    update_xalt_table=yes
fi
# check prefix folder
if [ -z "$PREFIX" ]; then
    echo -e "\n Prefix folder not defined. Please use the option -p,--prefix to define the prefix folder \n"
    usage
else
 export EASYBUILD_PREFIX=$PREFIX
fi
# set production repository folder
if [ -z "$EB_CUSTOM_REPOSITORY" ]; then
    export EB_CUSTOM_REPOSITORY=/apps/common/UES/jenkins/production/easybuild
fi
# load module EasyBuild-custom
module load EasyBuild-custom/cscs
# print EasyBuild configuration, module list, production file(s), list of builds
echo -e "\n EasyBuild version and configuration ('eb --version' and 'eb --show-config'): "
echo -e " $(eb --version) \n $(eb --show-config) \n"
echo -e " Modules loaded ('module list -t'): "
echo -e " $(module list -t)"
echo -e " Production file(s): ${eb_lists[@]} \n"
echo -e " List of builds (including options):"
for ((i=0; i<${#eb_files[@]}; i++)); do
    echo ${eb_files[$i]}
done
# module unuse PATH before building
if [ -n "$unuse_path" ]; then
 module unuse $unuse_path
fi

# start time
echo -e "\n Starting ${system} builds on $(date)"
starttime=$(date +%s)

# cumulative exit status of EasyBuild commands in the loop
status=0
# loop over the list of EasyBuild files to build
for((i=0; i<${#eb_files[@]}; i++)); do
    echo -e "\n===============================================================\n"
# define name and version of the current build
    name=$(echo ${eb_files[$i]} | cut -d'-' -f 1)
# build licensed software (CPMD and VASP)
    if [[ "$name" =~ "CPMD" || "$name" =~ "VASP" ]]; then
# custom footer for ${name} modulefile with a warning for users not belonging to group ${name,,}
        footer="if { [lsearch [exec groups] \"${name,,}\"]==-1 && [module-info mode load] } {
 puts stderr \"WARNING: Only users belonging to group ${name,,} with a valid ${name} license are allowed to access ${name} executables and library files\"
}"
        if [[ "$system" =~ "daint" || "$system" =~ "dom" ]]; then
            (cat ${scriptdir%/*}/login/daint.footer; echo "$footer") > ${EASYBUILD_TMPDIR}/${name}.footer
        else
            echo "$footer" > ${EASYBUILD_TMPDIR}/${name}.footer
        fi
        echo -e "eb ${eb_files[$i]} -r ${eb_args} --modules-footer=${EASYBUILD_TMPDIR}/${name}.footer\n"
        eb ${eb_files[$i]} -r ${eb_args} --modules-footer=${EASYBUILD_TMPDIR}/${name}.footer
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

# --- SYSTEM SPECIFIC POST-PROCESSING ---
if [[ $system =~ "daint" && $update_xalt_table =~ "y" ]]; then
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

# cumulative exit status of all the builds and the last command
exit $[status+$?]
