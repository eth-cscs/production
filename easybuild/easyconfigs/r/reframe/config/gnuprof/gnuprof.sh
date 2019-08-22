#!/bin/bash

source /usr/share/lmod/lmod/init/profile
module use /root/.local/easybuild/modules/all
module load reframe

/reframe.git/reframe.py -C ./docker.py \
-r -c ./miniapp_strongscaling_gnuprof.py \
--system docker:mc --skip-system-check \
-p PrgEnv-gnu \
--performance-report 

echo done
