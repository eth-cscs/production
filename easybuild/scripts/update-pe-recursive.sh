#!/bin/sh

#for TC in CrayGNU CrayIntel CrayCCE
for TC in CrayGNU 
do
    find -name *-$TC-2015.11* -exec python /apps/common/UES/tools/easybuild/new-tc.py --filename {} --toolchain $TC --version 2016.03 \;
done
