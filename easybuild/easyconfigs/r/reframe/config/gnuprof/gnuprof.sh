#!/bin/bash

source /usr/share/lmod/lmod/init/profile
module use /root/.local/easybuild/modules/all
module load reframe

cd SPH-EXA_mini-app.git

/reframe.git/reframe.py -C /root/docker.py \
-r -c /root/miniapp_strongscaling_gnuprof.py \
--system docker:mc --skip-system-check \
-p PrgEnv-gnu \
--performance-report 

echo done
