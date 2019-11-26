#!/bin/sh

productiondir=/apps/common/UES/sandbox/jgp/production.git
jenkinslist=$productiondir/jenkins-builds/6.0.UP04-17.08-gpu
easyconfigdir=$productiondir/easybuild/easyconfigs
topdir=/apps/dom/UES/jenkins/6.0.UP04/gpu/easybuild/modules/all
export MODULEPATH=$topdir:/users/piccinal/easybuild/sles12/modules/all
# find $productiondir/easybuild/easyconfigs -name \*.eb

function recurse() {
    ebmf="$1"
    module show $ebmf 2>&1 |grep -q " load " ;rcin=$?
    #  rc=0 means load is present = follow the link
    # rc/=0 means load is not present = stop
    if [ $rcin -ne 0 ] ;then
        # stop
        ## stop recursion:
        bugger=stopit
        echo " / end"
    else 
        # continue
        module show $ebmf 2>&1 |grep " load " ;rcin=$?
        children2=`module show $ebmf 2>&1 |grep " load " |awk '{print $3}'`
        for mf in $children2 ;do
                echo "xchild=$mf"
                recurse $mf
        done
        bugger=continueit
    fi
    #grep "module swap " $ebmf
}

# --- module show:

# for ebmf in `find $topdir -type f |grep -v .version |grep -v PrgEnv- |egrep -v "h5py|IPM|Charm++" |head -15` ;do

# for ebmf in /apps/dom/UES/jenkins/6.0.UP04/gpu/easybuild/modules/all/Scalasca/2.3.1-CrayIntel-17.08 ;do

# for ebmf in /apps/dom/UES/jenkins/6.0.UP04/gpu/easybuild/modules/all/Scalasca/2.3.1-CrayGNU-17.08 ;do

# for ebmf in /users/piccinal/easybuild/sles12/modules/all/mympingpong/0.7.1-CrayGNU-17.08-cray-python-17.06.1 ;do

for ebmf in `find $topdir -type f |grep -v .version |grep -v PrgEnv- ` ;do

# for ebmf in $1 ;do
    # /apps/dom/UES/jenkins/6.0.UP04/gpu/easybuild/modules/all/VMD/1.9.3-egl
    # /apps/dom/UES/jenkins/6.0.UP04/gpu/easybuild/modules/all/vampir/9.3.0

    echo
    # echo "$ebmf" 
    ebdir=`echo "$ebmf" | sed "s@modules/all@software@"`
    ebcfg=`basename $ebdir/easybuild/*.eb`
    ebmf_name=`dirname $ebmf |xargs basename`
    ebmf_version=`basename $ebmf`

# /apps/dom/UES/jenkins/6.0.UP04/gpu/easybuild/modules/all/h5py/2.7.0-CrayGNU-17.08-cray-python-17.06.1-cray-hdf5-parallel-1.10
# /apps/dom/UES/jenkins/6.0.UP04/gpu/easybuild/software   /h5py/2.7.0-CrayGNU-17.08-cray-python-17.06.1-cray-hdf5-parallel-1.10

    # --- is the easyconfig in production ? if not, skip it
    grep -q "$ebcfg" $jenkinslist ;rc=$?
    if [ $rc -ne 0 ] ;then
        # not in production => skipping
        echo "Skipping $ebmf" > /dev/null
    else
        #debug: echo "# +++ $ebmf" 
        #debug: grep " load " $ebmf |awk '{print "child="$3}'
        #sed "s- load - show -"
        #TODO: grep "module swap " $ebmf
        children1=`grep " load " $ebmf |grep "module " |awk '{print $3}'`
        if [ -z "$children1" ] ;then   
            #echo " / end"
            echo "parent=$ebmf_name/$ebmf_version child=none / end"
        else
            bugger="continueit"
            while [ "$bugger" = "continueit" ] ;do
                for mf in $children1 ;do
                    echo -n "parent=$ebmf_name/$ebmf_version child=$mf"
                    recurse $mf
                done
            done
        fi
    fi

done

#-D  export EASYBUILD_ROBOT_PATHS=$easyconfigdir
#-D  # CFGS1=/apps/common/UES/sandbox/jgp/production.git/easybuild/easyconfigs/z/zlib
#-D  
#-D  #no! $EASYBUILD_ROBOT_PATHS
#-D  
#-D  # topdir=/apps/common/UES/sandbox/jgp/production.git
#-D  # find $topdir -name Scalasca-2.3.1-CrayIntel-17.08.eb 
#-D  
#-D  mll daint-gpu
#-D  mll EasyBuild-custom/cscs
#-D  module rm xalt/daint-2016.11
#-D  module rm Vim/8.0
#-D  module rm git/2.14.1
#-D  module rm Ruby/2.4.1
#-D  module rm htop/2.0.1
#-D  module rm hwloc/1.11.7
#-D  module rm likwid/4.3.0
#-D  module rm lynx/2.8.9dev.16
#-D  module rm tmux/2.5
#-D  module rm vampir/9.2.0
#-D  module rm ncurses/.6.0
#-D  module rm libevent/.2.1.8
#-D  # module rm daint-gpu
#-D  
#-D  # --- 6.0.UP04-17.08-gpu ---
#-D  #  Amber-16-CrayGNU-17.08-cuda-8.0.eb
#-D  #  Amber-16-CrayGNU-17.08-parallel.eb
#-D  #  Amber-16-CrayGNU-17.08-serial.eb
#-D  #  Boost-1.65.0-CrayGNU-17.08-python2.eb
#-D  
#-D  # --- eb -D is SLOW !!!
#-D  # * [x] $CFGS/l/libunwind/libunwind-1.2.1.eb (module: libunwind/.1.2.1)
#-D  # * [x] $CFGS/c/Cube/Cube-4.3.5.eb (module: Cube/.4.3.5)
#-D  # * [x] $CFGS/o/OPARI2/OPARI2-2.0.2.eb (module: OPARI2/.2.0.2)
#-D  # * [x] $CFGS/o/OTF2/OTF2-2.0.eb (module: OTF2/.2.0)
#-D  # * [x] $CFGS/p/PDT/PDT-3.24.eb (module: PDT/.3.24)
#-D  # * [x] $CFGS/c/CrayPGI/CrayPGI-17.08.eb (module: CrayPGI/17.08)
#-D  # * [x] $CFGS/s/SIONlib/SIONlib-1.7.1-CrayPGI-17.08.eb (module: SIONlib/.1.7.1-CrayPGI-17.08)
#-D  # * [x] $CFGS/v/vampir/vampir-9.3.0.eb (module: vampir/9.3.0)
#-D  # * [x] $CFGS/s/Scalasca/Scalasca-2.3.1-CrayPGI-17.08.eb (module: Scalasca/2.3.1-CrayPGI-17.08)
