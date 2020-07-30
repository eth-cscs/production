#!/bin/sh

#for TC in CrayGNU CrayIntel CrayCCE
for TC in CrayIntel CrayCCE 
do
    find -name *-$TC-19.10* -exec python /apps/common/UES/tools/easybuild/new-tc.py --filename {} --toolchain $TC --version 20.06 \;
done
