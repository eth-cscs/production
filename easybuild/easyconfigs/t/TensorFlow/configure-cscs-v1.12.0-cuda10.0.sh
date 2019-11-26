#!/bin/bash

CONF_IN="configure.in"

echo "/opt/python/$PYMAJVER.$PYMINVER.$PYREVVER/bin/python"$PYMAJVER > $CONF_IN
echo "/opt/python/$PYMAJVER.$PYMINVER.$PYREVVER/lib/python"$PYMAJVER"."$PYMINVER"/site-packages" >> $CONF_IN
echo "n" >> $CONF_IN # Do you wish to build TensorFlow with Apache Ignite support? [Y/n]:
echo "n" >> $CONF_IN # Do you wish to build TensorFlow with XLA JIT support? [Y/n]:
echo "n" >> $CONF_IN # Do you wish to build TensorFlow with OpenCL SYCL support? [y/N]:
echo "n" >> $CONF_IN # Do you wish to build TensorFlow with ROCm support? [y/N]:
echo "y" >> $CONF_IN # Do you wish to build TensorFlow with CUDA support? [y/N]:
echo "10.0" >> $CONF_IN # Please specify the CUDA SDK version you want to use
echo $CRAY_CUDATOOLKIT_DIR >> $CONF_IN # Please specify the CUDA SDK version you want to use
echo "7.5.0" >> $CONF_IN # Please specify the cuDNN version you want to use.
echo $EBROOTCUDNN >> $CONF_IN # Please specify the location where cuDNN 5 library is installed.
echo "n" >> $CONF_IN # Do you wish to build TensorFlow with TensorRT support? [y/N] n
echo "2.4.2" >> $CONF_IN # Please specify the NCCL version you want to use.
echo "$EBROOTNCCL" >> $CONF_IN # Please specify the location where NCCL 6 library is installed.
echo "6.0" >> $CONF_IN # Please specify a list of comma-separated Cuda compute capabilities you want to build with.
echo "n" >> $CONF_IN # Do you want to use clang as CUDA compiler? [y/N] n
echo $GCC_PATH"/bin/gcc" >> $CONF_IN # Please specify which gcc should be used by nvcc as the host compiler 
echo "n" >> $CONF_IN # MPI support?
echo "-march=native" >> $CONF_IN # Please specify optimization flags "--config=opt" :
echo "n" >> $CONF_IN # Android builds?

cat $CONF_IN
echo "---"
./configure < $CONF_IN

exit
