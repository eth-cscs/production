#!/bin/bash

function usage() {
    echo "Usage: $0 <gpu|mc>"
    exit 1;
}

function check_argument() {
    if [ "$1" = "gpu" ] || [ "$1" = "mc" ] ;then
        echo > /dev/null
    else
        usage
    fi
}

# ---------------------------------------------------------------------------
# --- focus on production modulepaths only
function init_paths() {
#{{{!
    # topdir=/apps/dom/UES/jenkins/$clev/$partitionsuffix/easybuild
	MODULEPATH=$topdir/modules/all
    #TODO: tools/
	#MODULEPATH=$topdir/tools/modules/all:$MODULEPATH
	#MODULEPATH=/apps/daint/UES/easybuild/modulefiles:$MODULEPATH
	MODULEPATH=/opt/cray/ari/modulefiles:$MODULEPATH
	MODULEPATH=/opt/cray/modulefiles:$MODULEPATH
	MODULEPATH=/opt/cray/pe/ari/modulefiles:$MODULEPATH
	MODULEPATH=/opt/cray/pe/craype/2.5.15/modulefiles:$MODULEPATH
	MODULEPATH=/opt/cray/pe/modulefiles:$MODULEPATH
	MODULEPATH=/opt/cray/pe/perftools/7.0.2/modulefiles:$MODULEPATH
	MODULEPATH=/opt/modulefiles:$MODULEPATH
	export MODULEPATH
}
#!}}}

# ---------------------------------------------------------------------------
# --- retrieve the list of .eb files installed by jenkins:
function find_installed_ebs() {
#{{{!

    echo "searching for .ebs in $topdir/software/"
    installed_ebs0=`find $topdir/software -name \*.eb 2> /dev/null`
    
    #echo "searching for .ebs in $topdir/tools/software/"
    #installed_ebs1=`find $topdir/tools/software -name \*.eb 2> /dev/null`

    installed_ebs=`echo $installed_ebs0 $installed_ebs1`
    
    outlog=$0.log
    echo $installed_ebs |tr " " "\n" > $outlog
    echo $installed_ebs |tr " " "\n"
    echo "# --- step0 done"
}
#!}}}

# ---------------------------------------------------------------------------
# --- go through the list of jenkins-builds .eb files ($jenkins_eblist) and get their modulefile name
function eb2dot() {
# {{{!
# Example: ../../jenkins-builds/6.0.UP07-18.08-gpu
#  abcpy-0.5.1-CrayGNU-18.08-python3.eb   --set-default-module
#  advisor_2018.eb                        --set-default-module --installpath=/apps/dom/UES/jenscscs/6.0.UP07/gpu/easybuild/tools
#  advisor_2019.eb                        --installpath=/apps/dom/UES/jenscscs/6.0.UP07/gpu/easybuild/tools
#  Boost-1.67.0-CrayGNU-18.08-python2.eb
#  ...
mflist=""
productiondir=../..
jenkinslist=$productiondir/jenkins-builds/$clev-$pev-$partitionsuffix 
# jenkinslist=./jg # = debug
jenkins_eblist=`grep -v \# $jenkinslist |awk '{print $1}' |tr -d " "` 
echo "jenkinslist=$jenkinslist"
for jenkins_eb_file in $jenkins_eblist ;do

    jenkins_eb_file_fullpath=`echo $installed_ebs |tr " " "\n" |grep "$jenkins_eb_file"`
    mf=`echo $jenkins_eb_file_fullpath |sed "s-$topdir/software--" |awk -F/ '{print $2"/"$3}'`    

    if [ $mf != "/" ] ;then    
        mflist="$mf $mflist"
    else
        echo "jenkins_eb_file=$jenkins_eb_file"
        echo "jenkins_eb_file_fullpath=$jenkins_eb_file_fullpath"
        echo "mf=$mf"
        echo
    fi
done
echo -e "\n $mflist" >> $outlog
echo "# --- step1 done"
# Example: $mflist
	# VMD/1.9.3-ogl VMD/1.9.3-egl VASP/5.4.4-CrayIntel-18.08-cuda-9.1
	# Theano/1.0.2-CrayGNU-18.08-cuda-9.1-python3
	# Theano/1.0.2-CrayGNU-18.08-cuda-9.1-python2
	# TensorFlow/1.7.0-CrayGNU-18.08-cuda-9.1-python3
	# Spark/2.3.1-CrayGNU-18.08-Hadoop-2.7 PyExtensions/3.6.5.1-CrayGNU-18.08 ...

# exit 0

# ---------------------------------------------------------------------------
# Go through the list of modulefiles ($mflist) and follow the dependencies (module load xxx)

echo "digraph `echo $HOSTNAME |cut -c1-3` {" > $0.dot

echo > $tmp0
for mf in $mflist ;do
    echo "# Processing $mf ..." |tee -a $outlog

    # Example: Processing Boost/1.67.0-CrayGNU-18.08 ...
    # mss Boost/1.67.0-CrayGNU-18.08
    # /apps/dom/UES/jenkins/6.0.UP07/gpu/easybuild/modules/all/Boost/1.67.0-CrayGNU-18.08:
    # -- level0 deps:
    #    module		 load CrayGNU/.18.08                                    = level0
    #    module		 load bzip2/.1.0.6-CrayGNU-18.08                        = level0
    #    module		 load zlib/.1.2.11-CrayGNU-18.08                        = level0
	# 	"Boost/1.67.0-CrayGNU-18.08" -> "CrayGNU/.18.08";                   = level0
	# 	"Boost/1.67.0-CrayGNU-18.08" -> "bzip2/.1.0.6-CrayGNU-18.08";       = level0
	# 	"Boost/1.67.0-CrayGNU-18.08" -> "zlib/.1.2.11-CrayGNU-18.08";       = level0
    # -- level1 deps:
    # mss CrayGNU/.18.08 2>&1 |grep load                                    = level1
    #   module		 load PrgEnv-gnu                                        = level1
    #   module		 load gcc/6.2.0                                         = level1
	# 	"CrayGNU/.18.08" -> "PrgEnv-gnu";                                   = level1
	# 	"CrayGNU/.18.08" -> "atp/2.1.2";                                    = level1 
	# 	"CrayGNU/.18.08" -> "cray-libsci/18.07.1";                          = level1
	# 	"CrayGNU/.18.08" -> "cray-mpich/7.7.2";                             = level1
	# 	"CrayGNU/.18.08" -> "craype/2.5.15";                                = level1
	# 	"CrayGNU/.18.08" -> "gcc/6.2.0";                                    = level1
	# 	"CrayGNU/.18.08" -> "pmi/5.0.14";                                   = level1
    # mss bzip2/.1.0.6-CrayGNU-18.08                                        = level1
    #   module		 load CrayGNU/.18.08                                    = level1
    #   "bzip2/.1.0.6-CrayGNU-18.08" -> "CrayGNU/.18.08";                   = level1
    # mss zlib/.1.2.11-CrayGNU-18.08                                        = level1
    #   module		 load CrayGNU/.18.08                                    = level1
    # etc...

    module show $mf > $outf0 2>&1 
    # if mfile is hidden, module will raise error 105:
    # UDUNITS(3):ERROR:105: Unable to locate a modulefile for 'UDUNITS/2.2.26'
    grep -q "ERROR:105" $outf0 ;rc=$?
    mfn=`echo $mf |cut -d/ -f1`
    if [ $rc = 0 ] ;then
        # --- if rc=0 then mfile is probably hidden or non available:
        mfv=`echo $mf |cut -d/ -f2`
        module show $mfn/.$mfv > $outf0 2>&1
    fi
    echo $mf >> $tmp0
    listofdeps0=`grep " load " $outf0 |awk -Fload '{print $2}' |tr -d " "`
    # if $listofdeps0 is not empty, go deeper:
    if [ -n "$listofdeps0" ] ;then

        for deps0 in $listofdeps0 ;do 
            echo "\"$mf\" -> \"$deps0\";"

            # --- sublevel1
            module show $deps0 > $outf1 2>&1
            grep -q "ERROR:105" $outf1 ;rc=$?
            if [ $rc = 0 ] ;then
            # --- if rc=0 then mfile is probably hidden or non available:
                deps0n=`echo $deps0 |cut -d/ -f1`
                mfv=`echo $deps0 |cut -d/ -f2`
                module show $deps0n/.$mfv > $outf1 2>&1
            fi

            listofdeps1=`grep " load " $outf1 |awk -Fload '{print $2}' |tr -d " "`
            if [ -n "$listofdeps1" ] ;then
                for deps1 in $listofdeps1 ;do
                    echo "\"$deps0\" -> \"$deps1\";"

                    # --- sublevel2
                    module show $deps1 > $outf2 2>&1
                    grep -q "ERROR:105" $outf2 ;rc=$?
		            if [ $rc = 0 ] ;then
		            # --- if rc=0 then mfile is probably hidden or non available:
		                deps1n=`echo $deps1 |cut -d/ -f1`
		                mfv=`echo $deps1 |cut -d/ -f2`
		                module show $deps1n/.$mfv > $outf2 2>&1
		            fi

                    listofdeps2=`grep " load " $outf2 |awk -Fload '{print $2}' |tr -d " "`
                    if [ -n "$listofdeps2" ] ;then
                        for deps2 in $listofdeps2 ;do
                            echo "\"$deps1\" -> \"$deps2\";"
                        done
                    fi # --- sublevel2

                done
            fi # --- sublevel1

        done
    fi # --- sublevel0

done |sort -u >> $0.dot 
# removes the duplicates with `sort -u`

echo '}' >> $0.dot
echo "# --- step2 done"

# To use dot/graphviz, uncomment the following lines:
# echo "module load stat"
# echo 'export LD_LIBRARY_PATH=/opt/cray/pe/stat/default/lib:$LD_LIBRARY_PATH'
# echo "dot -Tpng $0.dot > $0.png"
# echo "dot -Tjpg $0.dot > $0.jpg"
# echo "circo -Teps ./$0.dot > $0.eps"
# echo "try http://tulip.labri.fr/TulipDrupal/ too"
}
#!}}}

# ---------------------------------------------------------------------------
# --- convert the .dot file to neo4j format:
function dot2neo4j() {
#{{{!
    in="$1"
    mf0name=`echo "$in" |tr -d \" |awk -F'->' '{print $1}' |cut -d/ -f1 |tr -d " "`
    mf0version=`echo "$in" |tr -d \" |awk -F'->' '{print $1}' |cut -d/ -f2 |tr -d " " |tr -d \;`
    mf0id=`echo "$in" |tr -d \" |tr -d \. |awk -F'->' '{print $1}' |tr -d \- |tr -d / |tr -d " " |tr -d \;`

    mf1name=`echo "$in" |tr -d \" |awk -F'->' '{print $2}' |cut -d/ -f1 |tr -d " "`
    mf1version=`echo "$in" |tr -d \" |awk -F'->' '{print $2}' |cut -d/ -f2 |tr -d " " |tr -d \;`
    mf1id=`echo "$in" |tr -d \" |tr -d \. |awk -F'->' '{print $2}' |tr -d \- |tr -d / |tr -d " " |tr -d \;`

    echo "CREATE ($mf0id:mfile {name:'$mf0name', version:'$mf0version'})"
    echo "CREATE ($mf1id:mfile {name:'$mf1name', version:'$mf1version'})"
    echo "CREATE ($mf0id)-[:DEPSON]->($mf1id)"
}
#!}}}

# --------------------------------------------------------------------------
function main() {

# --- set gpu|mc modulepaths and specific versions:
clev=6.0.UP07
pev=18.08
topdir=/apps/dom/UES/jenkins/$clev/$partitionsuffix/easybuild
init_paths # set MODULEPATH 
# echo MODULEPATH=$MODULEPATH |tr : "\n"
outf0=eff0
outf1=eff1
outf2=eff2
tmp0=eff.level0
echo "Processing the .eb in /apps/dom/UES/jenkins/$clev/$partitionsuffix/easybuild/"

# needed to create list of dependencies:
find_installed_ebs
    # Example:
    #  /apps/dom/UES/jenkins/6.0.UP07/gpu/easybuild/software/nodejs/8.9.4-CrayGNU-18.07/easybuild/nodejs-8.9.4-CrayGNU-18.07.eb
    #  /apps/dom/UES/jenkins/6.0.UP07/gpu/easybuild/software/nodejs/8.9.4-CrayGNU-18.08/easybuild/nodejs-8.9.4-CrayGNU-18.08.eb
    #  /apps/dom/UES/jenkins/6.0.UP07/gpu/easybuild/software/zlib/1.2.11-CrayGNU-18.08/easybuild/zlib-1.2.11-CrayGNU-18.08.eb
    #  ...

# create list of dependencies:
#debug: set -x 
eb2dot 
#debug: set +x 

# -- convert to neo4j format:
grep ^\" $0.dot |tr -d \; > $0.dot2
while read line ;do
    dot2neo4j "$line"
done < $0.dot2 | sort -u > $outf0
# remove duplicates with `sort -u`
# -- nodes first:
grep -v DEPSON $outf0 > $0.neo4j
# -- then relationships:
grep    DEPSON $outf0 >> $0.neo4j
# -- import to neo4j
# echo "neo4j start"
cat $0.neo4j
# echo "neo4j stop"

}

# ---------------------------------------------------------------------------
# big bang:
# --- check if we use gpu|mc:
partitionsuffix=$1
check_argument $partitionsuffix
main















# ---------------------------------------------------------------------------
# working on improving the dependencies tree...
#dev = wip
#dev #set -x
#dev # iterate through the list of software (=level0)
#dev for l0 in `sort -u $tmp0` ;do
#dev 
#dev #echo continue;read
#dev     #echo "Listing l0=$l0 ..."
#dev     unset listl1a
#dev     unset listl1b
#dev     unset listl2a
#dev     unset listl2b
#dev     # iterate through the list of deps (=level1)
#dev     listofl1deps=`grep "^\"$l0\" ->" $0.dot |awk -F"->" '{print $2}' |tr -d \;`
#dev     for l1 in $listofl1deps ;do 
#dev         # is this the end ?
#dev         rc=`grep -m1 -q "^$l1 ->" $0.dot;echo $?`
#dev         if [ $rc -ne 0 ] ;then
#dev             # no more dep = end of the chain
#dev             listl1a="${listl1a} $l1 "
#dev         else
#dev             # more dep down the chain = continue parsing
#dev             l1tmp=`grep -m1 "^$l1 ->" $0.dot |awk -F"->" '{printf "%s ",$1}' |tr -d \;`
#dev             listl1b=${listl1b}$l1tmp
#dev         fi        
#dev     done       
#dev     listl1s=`echo $listl1a $listl1b |tr " " "\n" |sort -u |awk '{printf "%s ",$0}'`
#dev     #echo "## l0=$l0: $listl1s"
#dev     echo '------------------------------------------------------------------'
#dev 
#dev     # iterate through the list of deps'deps (=level2)
#dev     unset listl2s listl2 l2tmp 
#dev     for l1 in $listl1b ;do        
#dev         l2tmp=`grep "^$l1 ->" $0.dot |awk -F"->" '{print $2}' |tr -d \;`
#dev         listl2=${listl2}$l2tmp
#dev         listl2s=`echo $listl2 |tr " " "\n" |sort -u |awk '{printf "%s ",$0}'`
#dev     done
#dev 
#dev     listls=`echo $listl1s $listl2s |tr " " "\n" |sort -u |awk '{printf "%s ",$0}' |tr -d \"`
#dev     echo "## l0=$l0: $listls"
#dev 
#dev done
#dev echo "# --- final step done"
#dev set +x
