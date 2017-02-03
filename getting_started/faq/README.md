# Queue system


## Why my jobs on CSCS machines don't start?

### Q: My jobs at CSCS do not start at the moment. Why is it so? When can I expect the jobs to start?

Please check the priority of your submitted job: your jobs will have less priority if your are overusing the budget. You can check the usage of your budget against what is expected typing the command `monthly_usage`.

Please have a look at the CSCS User Portal for more details on how to check your budget.

---

## How can I run my jobs under a specific project?

### Q: I would like to run some simulations drawing budget from a secondary account: is it possible?

If you are a member of the group `gid`, you can use the following directive:
```
#SBATCH --account=gid
```

This will tell SLURM to charge the compute budget of the selected group for the current job.


---

## How can I set automatically a group account when submitting jobs?

### Q: I would like to set automatically one account when I use an interactive session invoked with `salloc -N 1`: how can you do that?

In case your username belongs to different projects, you can override the default account using the SLURM flag `-A/--account=myaccount` when calling `sbatch` or `salloc`.

You can do this automatically adding this line in your SLURM script:
```
#SBATCH --account=myaccount
```

You can add as well a line in your profile file for interactive sessions:

```
alias interactive='salloc -A myaccount'
```

or

```
export SALLOC_ACCOUNT=myaccount
```


---

## I would like to increase the priority of my runs, I am always standing in the queue!

### Q: I would like to do some benchmark tests for code development with my code. However, other users submit jobs all the time. Due to their higher priority, their jobs overtake mine in the queue, so I have to wait a very long time until my jobs start to run.

You have already used over 100% of your budget, whereas the other  projects you mention used less: manually adjusting the priorities is not  possible, since it will prevent a fair share of the computing resources  among our users.

---

## Can I extend the wall time of a pending job?

### Q: I would like to extend the time of a job that is already pending in the queue. Is is possible?

Some SLURM settings of a pending job can be modified using the command `scontrol update`: you should use the same format of the show command. E.g.:
```
scontrol update JobId=2543 Name=newtest TimeLimit=00:10:00
```
The command above will set a new job name and time limit to the pending job with `JobId 2543`: the command will fail to change the time limit if the job is in state `R (RUNNING)`, but it will still manage to update the job name.

---

## Why do I get the error __invalid account__ when submitting a job?

### Q: I'm having trouble when submitting jobs to one of the projects I'm currently involved in. In order to draw CPU time from that project, I use the following SLURM option: `#SBATCH –account=pid`, where `pid` stands for my project id. I'm getting the following response:
```
salloc: error: Failed to allocate resources: Invalid account or account/partition combination specified.
```
I don't specify explicitly the partition: even if I do, I get the same error with the SLURM option: `#SBATCH --partition=normal`

The error __Invalid account__ might depend on the lack of a group membership for your username: you can verify if that is the case typing the command `groups` on your shell.

If your project number doesn't appear in the list of your groups (`gid`), then you won't be allowed to use that project in order to run your jobs: if this is the case, please check your group membership with the principal investigator (PI) of the project.

Another reason is often the lack of computing resources associated to your project: to check it, please type `sbucheck` on your shell.

---

## Where can I get tips to use efficiently Cray machines?

### Q: Do you have a cookbook on how to use Cray machines efficiently, including general rules, best way to submit jobs...? I think I need to use srun to submit jobs. Can you show me a test job script?

Please have a look at the page explaining how to run a batch job; if you wish to improve the performance of your code, you might use the Cray Performance and Analysis Tools (CrayPat), available loading the perftools module.

---

## My job has been successfully submitted but it's not listed in the queue

### Q: I tried to submit a job located in my `$HOME` folder with the command `sbatch cp2k`. I get the output: `Submitted batch job 222266`. However if I type `squeue -u $USER` my job is never listed.

In order to submit batch jobs, you need to create a SLURM script that contains the correct header information so that the scheduler can allocate resources and place your job in the queue. Please have a look at the SLURM section on the CSCS User Portal.

---

## How to optimize the number of tasks per node?

### Q: I had to reduce the number of tasks per node, since my application was running out of memory. Is there an optimal choice for the number of tasks per node?

Remember that you are charged resources per node: of course when memory becomes an issue, then you need to reduce the number of tasks per node.

However you will gain not only the extra memory but also more memory bandwidth, so the code should run a bit faster.

If your application makes use of OpenMP threads, you might try to use less tasks per node and set `--cpus-per-task` within your batch script, that distribute them evenly across the node.

In some cases you might gain a speed up, but this is strongly application dependent.

---

## How to place and release a job from hold state?


### Q: How can I place my SLURM job into an hold state? And how can I release the hold?

In order to place a job on hold type `scontrol hold JOB_ID`.

To release the job from the hold state, issue `scontrol release JOB_ID`.

---

## Error Invalid account when submitting a batch job

### Q: I'm trying to submit a SLURM batch script, but I am getting the following error:
```
sbatch: error: Batch job submission failed: Invalid account or account/partition combination specified.
```
Could you please help me?

The error might be related to the lack of computing resources locally on the system that you are using.

A reason for this error could be as well that your username belongs to multiple projects you can verify immediately by adding the following line in your script:
```
#SBATCH --account=gid
```

In this way the batch scheduler will charge the computing time on the specified project (`gid`).

---

## What is the meaning of job state codes?

### Q: I have submitted a job with SLURM, but I don't understand the meaning of the different job state codes displayed in output by the command squeue.

Jobs typically pass through several states in the course of their execution. The typical states are PENDING, RUNNING, SUSPENDED, COMPLETING and COMPLETED.An explanation of each state follows:
* CA (CANCELLED): the job was explicitly cancelled by the user or system administrator. The job may or may not have been initiated.
* CD (COMPLETED): the job has terminated all processes on all nodes.
* CF (CONFIGURING): the job has been allocated resources, but are waiting for them to become ready for use (e.g.booting).
* CG (COMPLETING): the job is in the process of completing. Some processes on some nodes may still be active.
* F (FAILED): the job terminated with non-zero exit code or other failure condition.
* NF (NODE_FAIL): the job terminated due to failure of one or more allocated nodes.
* PD (PENDING): the job is awaiting resource allocation.
* PR (PREEMPTED): the job terminated due to preemption.
* R (RUNNING): the job currently has an allocation.
* S (SUSPENDED): the job has an allocation, but execution has been suspended.
* TO (TIMEOUT): the job terminated upon reaching its time limit.

---

## How to display job accounting information?

### Q: How can I display accounting informations of my SLURM jobs?

You can have this information with the command `sacct -l -u $USER`

---

## How to have the list of available nodes and partitions?

### Q: How can I view the list of available partitions and nodes and obtain detailed information on them?

The command `sinfo -a -l` gives you a list of the available partitions.

`scontrol show partition <partition_name>` will give you the details on the chosen partition: if you don't specify a partition, you will see the details of all the partitions.

---

## How to manage my jobs in the queue?

### Q: How can I list all my jobs in the system, get details on each of them and delete one of my jobs in the queue?

You can see your jobs in the queue issuing the command `squeue -a -l -u $USER`. In order to see details on a specific job, type `scontrol show JOB_ID`. If you want to delete one of your submitted jobs, the command you need is `scancel JOB_ID`.

---

























# Accounting



## How can I check the usage of my budget?

### Q: Is there a way to check how much computing time my group has already consumed?

You can check the usage of your budget on the systems at CSCS with two scripts:
* `sbucheck` \(per-project usage of the budget allocated quarterly\)
* `monthly_usage` \(use option `--individual` to see a per-user breakdown\)

You can find more details on these two commands under [Compute Budget](http://user.cscs.ch/getting_started/compute_budget/index.html#c4214).

On the CSCS User Portal you can also check your account after logging in, following the link [My Projects](http://user.cscs.ch/nc/my_projects/index.html#c3248).

---

## How to write on `/project` when I belong to more than one group

### Q: I would like to store data under a second `/project` folder, since I am a collaborator of that group as well.

If you belong to more than one project, you should see the corresponding group IDs issuing the command `groups` on your shell. You are always logged in as your primary project: therefore, if wish to write on the `/project` folder of a secondary group (e.g. with group ID `sXYZ`), you will need to change project ID using the following command: `newgrp sXYZ`.

Then you will be able to write on `/project/sXYZ` and to check the computing budget of the secondary project with the usual commands `sbucheck` and `monthly_usage`. For further details on the command `newgrp`, please have a look at `man newgrp`.

---
























# Login



## How can I get an account at CSCS? Where can I find the forms?

### Q: I wished to apply for an account at CSCS for me and my collaborators, but I wasn't able to find the forms to be filled in.

The forms to be filled in to get and account as Principal Investigator (PI) or new member of a group within an existing project can be found on [CSCS web site](http://www.cscs.ch/), under the __User Lab__ section __Applying for Accounts__.

---

## Can you allow an existing user to charge computing time on my project?

### Q: I would like to have a collaborator, who is already a CSCS user, included in my project. Could you please add him to my project, in order to allow him to charge my allocation?

We will allow the user to charge your allocation as a secondary project, when the request will be approved by the principal investigator of the project.

---

## I'm not able to login on the systems: `Host key verification failed`

### Q: I got a warning message while trying to access your system. Is it safe to pursue as suggested by adding the new host key?

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED! @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that the RSA host key has just been changed.
Please contact your system administrator.
Add correct host key in .ssh/known_hosts to get rid of this message.
Host key verification failed.
```

Please proceed as suggested, deleting all the entries wth the name of the system from your `.ssh/known_hosts` file. E.g. for Pilatus:

```
sed -i '/^pilatus/d' ~/.ssh/known_hosts
```

This command will delete all lines beginning with "pilatus" from the file `.ssh/known_hosts`, then you should be prompted only once a message like the following:

```
The authenticity of host 'pilatus.cscs.ch' can't be established.
[...] Are you sure you want to continue connecting (yes/no)?
```

Type `yes`. In case you are prompted similar messages again, delete manually all lines in the `.ssh/known_hosts` file or even the file itself and try again.

---

## I'm not able to login at CSCS after the last configuration change!

### Q: Since the latest changes that you applied to the configuration of the machine that I am using at CSCS, I can't login anymore from my local computer and I get the following message:

```
@ WARNING: POSSIBLE DNS SPOOFING DETECTED! @
```

Please, edit the file `.ssh/known_hosts` in your `$HOME` and remove any line containing the name of the machine that you were using at CSCS. Then try to connect again on that machine.

---


## How can I set up a passwordless access to CSCS systems from Ela?

### Q: When I log from Ela onto CSCS systems, I have to type the password each time. Is there a way to avoid typing the password?

You can generate a public/private rsa key pair on the system of your choice:

* `ssh-keygen` You will be asked to Enter file in which to save the key: just confirm the default pressing enter. Then you will be asked to Enter passphrase;
* `ssh-copy-id -i .ssh/id_rsa.pub ela1` to copy your key on ela1;
* Follow the instructions printed on screen and try to login: `ssh ela1`. You should be able to log on Ela from the chosen system without typing passwords, and viceversa.

---

## Direct access to CSCS machines from local clients

### How can I connect directly to the systems at CSCS from my local client?

In order to login on CSCS systems you need to access the front-end Ela first.

If you want to copy your output files from a CSCS production system to your local client, outgoing connections will work if your client has a static IP address.

Otherwise, you can configure your local client to forward the connection from Ela to the CSCS system that you wish to access, editing the file `.ssh/config` on your local client.

For instance, you would write the following in `.ssh/config` for Piz Daint:
```
host esdaint
Hostname daint.cscs.ch
User <username>
ForwardAgent yes
Port 22
ProxyCommand ssh -q -Y <username>@ela.cscs.ch netcat %h %p -w 10
```

Then you will be able to run the command `ssh` or `scp` on your local client outside CSCS:
```
$ scp esdaint <path> <localpath>
```
Please note that you need to edit `username`, `<path>` and `<localpath>`, since they are user specific.

---






















# Storage and Data Transfer


## What is the cleaning policy on `/scratch?`

### Q: I've found today that my files on `/scratch` have been deleted. Is it still possible to get back those files?

Files older than a month are deleted by a cleaning script: please check the cleaning policy on the `/scratch` filesystem on the Filesystems page of the CSCS User Portal.

Unfortunately, once the files on `/scratch` have been deleted, there is no way to recover them. In fact, `/scratch` is meant to keep only the temporary files needed for a run.

---

## Could you tell me why I ran out of quota on my `$HOME?`

### Q: I moved several big files to the `/project` filesystem, since I have no more space under my `$HOME`.
Are the data under `/project` counted in my `$HOME` quota?

The disk space available on each user's `$HOME` is 10 Gb, while the group data under the `/project` filesystem have a separate and bigger quota in general. However the quota on `/project` is shared by all members of the group.

---

## How to transfer efficiently data

### Q: How can I move a considerable amount of data efficiently to and from CSCS?

If you want to copy your output files from a CSCS production system to your local client, outgoing connections will work if your client has a static IP address.

In case you need to transfer a large amount of data from your local platform to your folder under `/project` or `/store` at CSCS or viceversa, you have an alternative that might run faster then `sftp` or `scp`. For further information, please have a look the Data transfer page.

---

## How to check the quota on `/project`

### Q: I can I check my quota on <code>/project?</code>

You can check your quota on `$HOME=/users/<username>` and `$PROJECT=/project/<project_id>` with the command `quota` on the front-end system Ela (ela.cscs.ch).

Please note that on `/project` the number of files as well is listed on the first line in output (`N. FILE USED ON PROJECT`).

Please consider archiving folders with the tar command in order to keep low the number of files owned by your group.

---

## File transfer to CSCS machines

### Q: I'm a new user at CSCS. I cannot use ftp to connect to the system and upload files. Could you give some advice?

You should be able to use `rsync`, `scp` or `sftp` instead: please check the availability of these commands using `which` within the terminal. For more information on their usage, please have a look at the corresponding manual pages with the commnad `man`.

---

















# Compilation and Optimization


## Running executables on different machines

### Q: Does an executable from a machine also run on another one at CSCS?

Not in general. This is mainly because it may happen that the MPI  devices of different machines are different: if this is the case, the  MPI libraries associated with them will be incompatible.

---

## I have problems running my executable dynamically linked to shared libraries

### Q: I have to link my application with `libGL` and `libOSMesa`. I want to build a static executable, so I compiled the static version of these libs by myself, since they are not available in `/usr/lib64`. Could you please provide the static versions in `/usr/lib64`? In fact, using the `.so` versions available in `/usr/lib64` doesn't work at runtime, although `ldd` shows the path correctly.

In order to use the available libraries dynamically, you have to add the directory `/usr/lib64` to the path list of the environment variable `$LD_LIBRARY_PATH` before the execution of your job starts, as follows:
```
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/lib64
```
for bash or
```
set LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/lib64
```
for csh

---

## I get an error message when loading shared libraries!

### Q: I try to use an executable which I compiled before, it worked then but today I get the following error message: error while loading shared libraries and cannot open shared object file: No such file or directory. What do I need to do?

> If you cannot use static libraries since only the corresponding dynamic libraries are available, then you should always load the system module containing the missing library.

> The appropriate paths to the library will be added to the compiler wrappers \(`ftn` for Frotran codes, `cc` for C, `CC` for C++\). For example, if you are missing the netcdf library, then you should add the corresponding module by typing `module load netcdf` in your shell.

---

## Linking FFTW libraries fails

### Q: I was able to compile successfully my code some time ago. Now, even if I load the module fftw I'm not able to do so, because the linker says that the libraries are not found. Could you check if there is any problem with the fftw module?

Your configure script is likely not picking up the fftw: please, examine the file config.log after configure to see where it fails.
```
module show fftw
```
will print on screen the version and paths of the loaded module, in case you need to add them manually during configuration.

Then the Cray wrapper (`cc`, `CC` or `ftn`) should link the library automatically, if the corresponding module is loaded.

---

## Where to find Third Party Scientific Libraries

### Q: Which modules provide optimized scientific libraries?

On Cray systems, please have a look at `module help cray-tpsl` TPSL (Third Party Scientific Libraries) is the name of a module containing a collection of mathematical libraries that can be used with PETSc and Trilinos for solving problems in dense and sparse linear algebra.

The tpsl module is automatically loaded when PETSc or Trilinos is loaded. The libraries included are Hypre, SuperLU, SuperLU_dist, MUMPs, ParMetis, Sundials, and Scotch.

---

## How can I check the commands and flags invoked by the compiler wrapper?

### Q: I would like to check which command and flags are invoked by the compiler wrapper of the Programming Environment that I have loaded. Is it possible?

After you load all modules that you need, you can issue one of the following commands to have a list of the flags invoked by the appropriate compiler wrapper: `cc -###` (or `ftn` or `CC` in place of `cc`) or `cc -v` (or `ftn` or `CC` in place of `cc`). Depending on the Programming Environment that you have loaded, you might need to give a filename on the command line, however an empty `foo.c` or `foo.f90` or `foo.C` will be enough (e.g.: the Cray compiler requires a filename with `-v`).

---

## Why do I get `Illegal instruction` when running my code?

### Q: I have managed to compile my code, but when I try to run it I get `Illegal Instruction` or even `Fatal error in MPI_Init` and similar error messages. Why?

The system on which you have compiled your code have a different architecture with respect to the compute nodes of the system where you are trying to run your executable.

The Cray compiler wrappers provided by the programming environment on Cray systems will cross-compile your code in order to run on the compute nodes.

---

## Where can I find BLAS and SCALAPACK on Cray machines?

### Q: I need to link linear algebra routines to my code, but I can't find the BLAS and SCALAPACK libraries and their headers. Are these available on Cray systems?

BLAS and SCALAPACK functions are provided by the `cray-libsci` module on Cray systems.

The following commands will give you some information on the module:
```
module show cray-libsci
module help cray-libsci
```
If you use the flag `-v` when compiling with the wrapper, you will see a verbose list of all the include and library paths called by the compiler driver.

---

## Error linking MPI library

### Q: I am compiling a code on a Cray system and when I link I get the following error message:
```
fatal error: mpi.h: No such file or directory. Compilation terminated.
```
Do I need to explicitly link the MPI library?

On the Cray systems you should compile your code using the compiler wrappers:
* `cc` for C
* `CC` for C++
* `ftn` for Fortran
Please set the proper compiler driver in your Makefile and the MPI libraries will be linked automatically.

---

## How can I find the path to a library?

### I would like to link my code to a specific library. How can I find its path on the system?

In order to compile your code on a machine at CSCS you should load the module of a Programming Environment and of the libraries that you need:

* `module avail` lists of the modules available on the machine
* `module show "modulename"` lists the variables and paths related to a single module (change modulename with the module of your choice)
On Cray systems you should use the wrapper to compile (`ftn` for Fortran, `cc` for C or `CC` for C++): the wrapper will add the correct path of the libraries that have been loaded.

For more information on compiling, please have a look at the section _Compiling and Optimizing_ on the top menu.

---

## How to measure the performance of an application

### What is the meaning of flop/s?

The flop/s is a rate of execution of 64 bits floating point operations (either addition or multiplication) per second. Its multiples are Mflop/s (millions), Gflop/s (billions), Tflop/s (trillions) and so on...

The theoretical peak performance is the upper bound peak rate of execution of floating point operations for a given processor. It can determined by counting the number of floating-point additions and multiplications (in full precision) that can be completed during the clock time of the processor.

Flop/s can give a measure of&nbsp;application performance: given a processor's theoretical peak performance, one can work out how efficiently the cpu's floating point units are used. An application which runs at 10% of the peak performance has room for optimization, while one that runs over 50% is probably not going to improve much unless the underlying algorithm is rewritten

Most performance tools can measure the floating-point rate of execution  of any given application (for instance, Craypat on Cray systems).

---


























# Computing systems

## Where can I find the documentation of the systems available at CSCS?

### Q: Is there a web page where I can find information and guidelines regarding the machines at CSCS?

You can find the documentation for the systems available at CSCS on the [CSCS User Portal](/).

The different sections listed in the top menu of the page will guide you through the facilities offered to the users community.

Please check as well the [list of FAQs](FAQS), where you can find answers to the most general issues.

---

## How to check the free memory on selected nodes

### Q: A job crashed after running for several hours with the following error message:
```
[NID 01490] 2011-12-05 00:20:27 Apid 168352: OOM killer terminated this process.
```
Jobs of the same size used to run before without errors: could you please check this issue?

The out of memory issue (OOM) might arise from a temporarily low free memory on a node: you can check the free memory on the nodes that you allocate by inserting the following command in your batch script:
```
aprun -n $SLURM_JOB_NUM_NODES -N 1 free -m
```
The free memory per node is usually slightly less than the nominal value, since it is partly used by the filesystem. If the free memory on the nodes where you run is already close to the maximum value, then please try running with more nodes, using fewer tasks per node.

---

## Getting information on the configuration and nodes available

### Q: How can I see the detailed configuration of the current SLURM system and see the list of the available nodes?

The corresponding SLURM commands are the following:
```
scontrol show config
scontrol show nodes
```

---

## How to check the memory usage of a code

### I would like to check the memory footprint of my code, how can I do that?

You can insert in your code the C or Fortran examples that you find in `/project/csstaff/examples/memory`: they read the file `/proc/self/statm` and print current information about memory usage, measured in page units (please type `man 5 proc` for more details):
* size (total program size, same as VmSize in `/proc/[pid]/status`);
* resident set size (same as VmRSS in `/proc/[pid]/status`);
* share (shared pages, from shared mappings);
* text (text code);
* lib (library, unused in Linux 2.6);
* data (data + stack);
* dt (dirty pages, unused in Linux 2.6)

The CUDA runtime API provides memory management functions such as `cudaMemGetInfo` which can be called to get the free and total amount of memory available on GPU devices in bytes.

For more details. please have a look at the following HTML file on Piz Daint: `/opt/nvidia/cudatoolkit/default/doc/html/cuda-runtime--pi/group__CUDART__MEMORY.html`

---

## Which HPC system is available for pre- and post-processing?

### Q: I recently obtained an account at CSCS for a production project onMonte Rosa and I would like to get the access rights for a machine to do the post-processing of my data.

Currently The system for pre- and post-processing for production projects at CSCS is Pilatus. You can choose Pilatus for your job adding the following line in your SLURM batch script:
```
#SBATCH --cluster=pilatus
```
Alternatively, you can submit using the command
```
sbatch --cluster=pilatus
```
or
```
sbatch -M pilatus
```
or setting the following variable:
```
SLURM_CLUSTER=pilatus
```

Please note that the following preference list holds:
* command line argument (`-M / --cluster=`)
* environment variable (`$SLURM_CLUSTER`)
* script directive (`#SBATCH --cluster=pilatus`)

If the post-processing job depends on a job running on Piz Daint, add this line at the end of your job script, to submit the next job on Pilatus using the SLURM batch script `post-processing.sbatch`:
```
sbatch --cluster=pilatus post-processing.sbatch
```












# Software and Modules

## Useful commands of the module framework

### Q: Where can I find a list of module commands?

You can have a list of the most useful module commands printed on the screen typing `module`.

---

## Where can I run Matlab, do you have a template script?

### Q: I made an executable out of my matlab source file using the command
```
mcc -o myexe -m=myfile.m
```
Then I tried to execute it, but I wasn't able so far to run it. Is there an easy way to run a matlab code within a batch script?

Matlab is available as a module on daint for post-processing jobs. Therefore you may submit a matlab script (e.g.: `matlab.m`) within a SLURM batch job using the following template script:
```
#!/bin/bash -l
#SBATCH --nodes=1
#SBATCH --tasks-per-node=12
#SBATCH --time=01:00:00
#SBATCH --job-name=matlab
module load matlab
matlab -nodisplay < matlab.m
```

Please have a look at Running jobs to learn how to submit a SLURM batch job.






























































