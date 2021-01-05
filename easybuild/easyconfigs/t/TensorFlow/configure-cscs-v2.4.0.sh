#!/bin/bash

CONF_IN="configure.in"

# Please specify the location of python.
echo "/opt/python/$PYVER/bin/python" > $CONF_IN
# Please input the desired Python library path to use.
echo "/opt/python/$PYVER/lib/python"$PYSHORTVER"/site-packages" >> $CONF_IN
# Do you wish to build TensorFlow with ROCm support? [y/N]
echo "n" >> $CONF_IN
# Do you wish to build TensorFlow with CUDA support? [y/N]
echo "y" >> $CONF_IN
# Do you wish to build TensorFlow with TensorRT support? [y/N]
echo "n" >> $CONF_IN
# Asking for detailed CUDA configuration...
echo "$CUDATOOLKITVER" >> $CONF_IN   # Please specify the CUDA SDK version you want to use. [Leave empty to default to CUDA 10]:
echo "$EBVERSIONCUDNN" >> $CONF_IN  # Please specify the cuDNN version you want to use. [Leave empty to default to cuDNN 7]:
echo "$EBVERSIONNCCL" >> $CONF_IN  # Please specify the locally installed NCCL version you want to use. [Leave empty to use http://github.com/nvidia/nccl]:
echo "$CRAY_CUDATOOLKIT_DIR,$EBROOTCUDNN,$EBROOTNCCL" >> $CONF_IN # Please specify the comma-separated list of base paths to look for CUDA libraries and headers.
echo "6.0" >> $CONF_IN # Please specify a list of comma-separated Cuda compute capabilities you want to build with.
echo "n" >> $CONF_IN # Do you want to use clang as CUDA compiler? [y/N] n
echo $GCC_PATH"/snos/bin/gcc" >> $CONF_IN # Please specify which gcc should be used by nvcc as the host compiler 
echo "-march=native" >> $CONF_IN # Please specify optimization flags "--config=opt" :
echo "n" >> $CONF_IN # Would you like to interactively configure ./WORKSPACE for Android builds?
echo "n" >> $CONF_IN # Android builds?


cat $CONF_IN
echo "---"
./configure < $CONF_IN

exit
