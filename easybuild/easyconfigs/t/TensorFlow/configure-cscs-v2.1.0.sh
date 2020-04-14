#!/bin/bash

CONF_IN="configure.in"

echo "/opt/python/$PYMAJVER.$PYMINVER.$PYREVVER/bin/python"$PYMAJVER > $CONF_IN
echo "/opt/python/$PYMAJVER.$PYMINVER.$PYREVVER/lib/python"$PYMAJVER"."$PYMINVER"/site-packages" >> $CONF_IN
echo "n" >> $CONF_IN # Do you wish to build TensorFlow with XLA JIT support? [Y/n]:
echo "n" >> $CONF_IN # Do you wish to build TensorFlow with OpenCL SYCL support? [y/N]:
echo "n" >> $CONF_IN # Do you wish to build TensorFlow with ROCm support? [y/N]:
echo "n" >> $CONF_IN # Do you wish to build TensorFlow with CUDA support? [y/N]:
echo "n" >> $CONF_IN # Do you wish to build TensorFlow with TensorRT support?
echo "n" >> $CONF_IN # MPI support?
echo "-march=native" >> $CONF_IN # Please specify optimization flags "--config=opt" :
echo "n" >> $CONF_IN # Android builds?

cat $CONF_IN
echo "---"
./configure < $CONF_IN

exit
