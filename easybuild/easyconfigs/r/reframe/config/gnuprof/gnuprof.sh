#!/bin/bash

source /usr/share/lmod/lmod/init/profile
module use /root/.local/easybuild/modules/all
module load reframe

# cd SPH-EXA_mini-app.git
ln -fs SPH-EXA_mini-app.git/src .

/reframe.git/reframe.py \
-r \
-C /docker.py \
-c /miniapp_strongscaling_gnuprof.py \
-p PrgEnv-gnu \
--system docker:mc --skip-system-check \
--performance-report 

echo done
