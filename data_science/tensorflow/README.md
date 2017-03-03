# Tensorflow

This document gives a quick introduction how to get a first test program in
TensorFlow running. All instructions have been tested on Piz Daint only. As an
example we use TensorFlow 0.11.0 but other versions might be available on the
system. Use `module avail` to get an overview.


## Loading the Module

To use TensorFlow on Piz Daint you have to load the corresponding module:

```
module load daint-gpu
module use /apps/daint/UES/6.0.UP02/sandbox-ds/easybuild/haswell/modules/all/
module load TensorFlow/0.11.0-CrayGNU-2016.11-Python-3.5.2
```

Note that there is a mor elaborate documentation on the
[module system](https://eth-cscs.github.io/production/getting_started/faq/#software-and-modules).

## Testing TensorFlow

### Simple Import Test
On the Daint login node, directly try to import the TensorFlow module:

```
python -c 'import tensorflow as tf'
```

The output should look like:

```
I tensorflow/stream_executor/dso_loader.cc:111] successfully opened CUDA library libcublas.so.8.0 locally
I tensorflow/stream_executor/dso_loader.cc:111] successfully opened CUDA library libcudnn.so.5 locally
I tensorflow/stream_executor/dso_loader.cc:111] successfully opened CUDA library libcufft.so.8.0 locally
I tensorflow/stream_executor/dso_loader.cc:111] successfully opened CUDA library libcuda.so.1 locally
I tensorflow/stream_executor/dso_loader.cc:111] successfully opened CUDA library libc
```

### Testing MNIST demo model

A more elaborate test is to actually train a model using the GPU:

```
salloc -N1 -C gpu
srun python -m 'tensorflow.models.image.mnist.convolutional'
```

The output should look like:

```
I tensorflow/stream_executor/dso_loader.cc:111] successfully opened CUDA library libcublas.so.8.0 locally
I tensorflow/stream_executor/dso_loader.cc:111] successfully opened CUDA library libcudnn.so.5 locally
I tensorflow/stream_executor/dso_loader.cc:111] successfully opened CUDA library libcufft.so.8.0 locally
I tensorflow/stream_executor/dso_loader.cc:111] successfully opened CUDA library libcuda.so.1 locally
I tensorflow/stream_executor/dso_loader.cc:111] successfully opened CUDA library libcurand.so.8.0 locally
I tensorflow/core/common_runtime/gpu/gpu_device.cc:951] Found device 0 with properties:
name: Tesla P100-PCIE-16GB
major: 6 minor: 0 memoryClockRate (GHz) 1.3285
pciBusID 0000:02:00.0
Total memory: 15.90GiB
Free memory: 15.62GiB
I tensorflow/core/common_runtime/gpu/gpu_device.cc:972] DMA: 0
I tensorflow/core/common_runtime/gpu/gpu_device.cc:982] 0:   Y
I tensorflow/core/common_runtime/gpu/gpu_device.cc:1041] Creating TensorFlow device (/gpu:0) -> (device: 0, name: Tesla P100-PCIE-16GB, pci bus id: 0000:02:00.0)
Extracting data/train-images-idx3-ubyte.gz
```

## Submiting a Job

The following script exemplifies how to submit a TensorFlow job to the
queing system. The script asks for 1 nodes, making 12 CPUs available to the 1
Python task. Further, the job is constraint to the GPU nodes of Piz Daint and its
running time is 10 minutes. For TensorFlow, it is usually a good idea to set
CRAY_CUDA_MPS=1 to enable multiple tasks to access the GPU device at the same
time.

```
#!/bin/bash
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=12
#SBATCH --ntasks=1
#SBATCH --constraint=gpu
#SBATCH --output=test-tf-%j.log
#SBATCH --error=test-tf-%j.log

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export CRAY_CUDA_MPS=1

module use /apps/daint/UES/6.0.UP02/sandbox-ds/easybuild/haswell/modules/all/
module load daint-gpu
module load TensorFlow/0.11.0-CrayGNU-2016.11-Python-3.5.2

srun python -m 'tensorflow.models.image.mnist.convolutional'
```

Say, this sbatch file is named `test-tf.sbatch`, then it is submitted to Slurm by

```
sbatch test-tf.sbatch
```

The status of Slurm's queue can be viewed with

```
squeue -u $USER
```

and a job can be cancelled running
```
scancel <JOBID>
```

A more detailed documentation on how to submit a job can be found
[here](http://user.cscs.ch/getting_started/running_jobs/piz_daint/index.html).
