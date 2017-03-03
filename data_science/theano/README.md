# Theano

This document gives a quick introduction how to get a first test program running.

## Supported Systems
Theano has been tested on Piz Daint only.

## Load Theano Module

As an example we use Theano 0.8.2, for but other versions might be available on
the system. Use `module avail` to get an overview.

```
module load daint-gpu
module use /apps/daint/UES/6.0.UP02/sandbox-ds/easybuild/haswell/modules/all/
module load Theano/0.8.2-CrayGNU-2016.11-Python-3.5.2
```

## Run Theano Test

### Simple Import Test

On the login node load the Theano module as described above. Trying to import
Theano on a login node results usually in an MPI error. Thus, even simple tests
have to be run on a compute node:

```
export CRAY_CUDA_MPS=1
salloc -N1 -C gpu
srun python -c 'import theano; theano.test()'
```

The output should be something like this:

```
Using gpu device 0: Tesla P100-PCIE-16GB (CNMeM is disabled, cuDNN 5105)
/apps/daint/UES/6.0.UP02/sandbox-ds/easybuild/haswell/software/Theano/0.8.2-CrayGNU-2016.11-Python-3.5.2/lib/python3.5/site-packages/Theano-0.8.2-py3.5.egg/theano/sandbox/cuda/__init__.py:600: UserWarning: Your cuDNN version is more recent than the one Theano officially supports. If you see any problems, try updating Theano or downgrading cuDNN to version 5.
  warnings.warn(warn)
/apps/daint/UES/6.0.UP02/sandbox-ds/easybuild/haswell/software/Theano/0.8.2-CrayGNU-2016.11-Python-3.5.2/lib/python3.5/site-packages/Theano-0.8.2-py3.5.egg/theano/tensor/signal/downsample.py:6: UserWarning: downsample module has been moved to the theano.tensor.signal.pool module.
  "downsample module has been moved to the theano.tensor.signal.pool module.")
................
```

The test runs for quite a while, but important is that the GPU is correctly recognized.

### Test using the LeNet demo model

A more elaborate test is to actually train a model using the GPU. We can, e.g.,
use the LeNet demo model from deeplearining.net:

```
wget http://deeplearning.net/tutorial/code/convolutional_mlp.py
salloc -N1 -C gpu
export CRAY_CUDA_MPS=1
export THEANO_FLAGS='cuda.root=$CRAY_CUDATOOLKIT_DIR,device=gpu,floatX=float32'
time srun python convolutional_mlp.py
```

The output should be something like this:

```
... loading data
... building the model
... training
training @ iter =  0
epoch 1, minibatch 100/100, validation error 9.230000 %
     epoch 1, minibatch 100/100, test error of best model 9.540000 %
training @ iter =  100
epoch 2, minibatch 100/100, validation error 6.170000 %
     epoch 2, minibatch 100/100, test error of best model 6.480000 %
training @ iter =  200
epoch 3, minibatch 100/100, validation error 4.640000 %
     epoch 3, minibatch 100/100, test error of best model 4.840000 %
...
training @ iter =  19900
epoch 200, minibatch 100/100, validation error 0.940000 %
Optimization complete.
Best validation score of 0.920000 % obtained at iteration 10900, with test performance 0.960000 %
```

The run time on Daint should be less than 5 minutes.

## Submit a Job

To manage jobs on Daint, CSCS uses the workload manager Slurm. Jobs are defined
by so-called sbatch files. A simple sbatch file to test Theano look as
follows:

```
#!/bin/bash
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=12
#SBATCH --ntasks=1
#SBATCH --constraint=gpu
#SBATCH --output=test-th-%j.log
#SBATCH --error=test-th-%j.log

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export CRAY_CUDA_MPS=1

module use /apps/daint/UES/6.0.UP02/sandbox-ds/easybuild/haswell/modules/all/
module load daint-gpu
module load Theano/0.8.2-CrayGNU-2016.11-Python-3.5.2

export THEANO_FLAGS='cuda.root=$CRAY_CUDATOOLKIT_DIR,device=gpu,floatX=float32'
srun python convolutional_mlp.py
```

Say, this sbatch file is named `test-th.sbatch`, then it is submitted to Slurm by

```
sbatch test-th.sbatch
```

The status of Slurm's queue can be viewed with
```
squeue -u $USER
```

and a job can be cancelled running
```
scancel <JOBID>
```

A more detailed documentation on how to submit a job can be found [here](http://user.cscs.ch/getting_started/running_jobs/piz_daint/index.html).

