#!/bin/bash

CONF_IN="configure.in"

echo "/opt/python/$PYVER/bin/python" > $CONF_IN
echo "/opt/python/$PYVER/lib/python"$PYSHORTVER"/site-packages" >> $CONF_IN
echo "n" >> $CONF_IN # Do you wish to build TensorFlow with OpenCL SYCL support? [y/N]
echo "n" >> $CONF_IN # Do you wish to build TensorFlow with ROCm support? [y/N]
echo "y" >> $CONF_IN # Do you wish to build TensorFlow with CUDA support? [y/N]
echo "n" >> $CONF_IN # Do you wish to build TensorFlow with TensorRT support? [y/N]
# Asking for detailed CUDA configuration...
echo "10.1" >> $CONF_IN   # Please specify the CUDA SDK version you want to use. [Leave empty to default to CUDA 10]:
echo "7.6.4" >> $CONF_IN  # Please specify the cuDNN version you want to use. [Leave empty to default to cuDNN 7]:
echo "2.6.4" >> $CONF_IN  # Please specify the locally installed NCCL version you want to use. [Leave empty to use http://github.com/nvidia/nccl]:
echo "$EBROOTCUDA,$EBROOTCUDNN,$EBROOTNCCL" >> $CONF_IN # Please specify the comma-separated list of base paths to look for CUDA libraries and headers.
echo "5.0" >> $CONF_IN # Please specify a list of comma-separated Cuda compute capabilities you want to build with.
# echo "n" >> $CONF_IN   # Do you wish to download a fresh release of clang? (Experimental) [y/N]
# echo "n" >> $CONF_IN # Do you wish to build TensorFlow with XLA JIT support? [Y/n]:
# echo "n" >> $CONF_IN # Do you wish to build TensorFlow with OpenCL SYCL support? [y/N]:
# echo "n" >> $CONF_IN # Do you wish to build TensorFlow with ROCm support? [y/N]:
# echo "y" >> $CONF_IN # Do you wish to build TensorFlow with CUDA support? [y/N]:
# echo "n" >> $CONF_IN # Do you wish to build TensorFlow with TensorRT support?
# echo "10.1" >> $CONF_IN # Please specify the CUDA SDK version you want to use
# echo "7.6.4" >> $CONF_IN # Please specify the cuDNN version you want to use.
# echo "2.4.8" >> $CONF_IN # Please specify the NCCL version you want to use.
echo "n" >> $CONF_IN # Do you want to use clang as CUDA compiler? [y/N] n
echo $GCC_PATH"/snos/bin/gcc" >> $CONF_IN # Please specify which gcc should be used by nvcc as the host compiler 
echo "-march=native" >> $CONF_IN # Please specify optimization flags "--config=opt" :
echo "n" >> $CONF_IN # Would you like to interactively configure ./WORKSPACE for Android builds?
echo "n" >> $CONF_IN # Android builds?


cat $CONF_IN
echo "---"
./configure < $CONF_IN

exit
