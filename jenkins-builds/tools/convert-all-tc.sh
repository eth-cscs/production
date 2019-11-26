#!/bin/sh
# author: @gppezzi

# Useful for bulk creating new toolchain versions based on old versions
# New ebs are created in place in order to avoid manual copying (--try-toolchain)

for TC in CrayGNU CrayIntel CrayCCE
do
    find -name *-$TC-17.08* -exec python ./switch-tc.py --filename {} --toolchain $TC --version 17.12 \;
done
