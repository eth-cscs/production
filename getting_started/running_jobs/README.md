# Running jobs

All CSCS systems use the SLURM batch system for the submission, control and management of user jobs.

[SLURM](https://computing.llnl.gov/linux/slurm/) provides a rich set of features for organizing your workload and provides an extensive array of tools for managing your resource usage, however in normal interaction with the batch system you only need to know three basic commands:

* __sbatch__ - submit a batch script
* __squeue__ - check the status of jobs on the system
* __scancel__ - delete one of your jobs from the queue