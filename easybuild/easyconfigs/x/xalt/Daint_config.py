# This is the config file for specifying tables necessary to configure XALT:

# The patterns listed here are the hosts that can track executable with XALT.
# Typical usage is that compute nodes track executable with XALT while login
# nodes do not.

import sys

# Note that linking an executable is everywhere and is independent of
# hostname_patterns

hostname_patterns = [
  ['KEEP', '^nid.*'],
  ['KEEP', '^daint.*'],
  ['KEEP', '^dom.*'],
  ['KEEP', '.*']
  ]

#------------------------------------------------------------
# This "table" is use to filter executables by their path
# The value on the left is either KEEP or SKIP.  If the value
# is KEEP then if the path matches the regular expression then
# the executable is acceptable as far as the path test goes.
# If the value on the left is SKIP then if the path matches
# the regular expression then executable is not acceptable so
# no XALT tracking is done for that path.

# This "table" is used to generate a flex routine that processes
# the paths. So the regular express must follow flex rules.
# In particular, in order to match the pattern must match the whole path
# No partial matches allowed.  Also do not use $ to match the
# end of the string.  Finally slash is a special character and must
# be quoted with a backslash.

# The path are conceptionally matched from the first regular
# expression to the last.  Once a match is found no other later
# matches are checked. The upshot of this is that if you want to
# track say /usr/bin/ddt, but ignore everything in /usr, then keep
# /usr/bin/ddt first and skip /usr/.* after.

# If a path does not match any patterns it is marked as KEEP.

# There are special scalar programs that must generate a start record.
# These are marked as SPSR

path_patterns = [
    #['KEEP',  r'^\/usr\/bin\/srun'],
    ['SKIP',  r'^\/usr\/bin\/.*'],
    ['SKIP',  r'^\/usr\/.*'],
    ['SKIP',  r'^\/sbin\/.*'],
    ['SKIP',  r'^\/opt\/.*'],
    ['SKIP',  r'^\/bin\/.*'],
    ['SKIP',  r'^\/etc\/.*'],
    ['SKIP',  r'^\/root\/.*'],
    #['PKGS',  r'.*\/R'],
    #['PKGS',  r'.*\/MATLAB'],
    #['PKGS',  r'.*\/python[0-9.]*'],
    #['KEEP',  r'^\/usr\/bin\/.*'],
    # ['KEEP',  r'^\/usr\/.*'],
    # ['KEEP',  r'^\/bin\/.*'],
    # ['KEEP',  r'^\/sbin\/.*'],
    # ['KEEP',  r'^\/etc\/.*'],
    ['SKIP',  r'^\/usr\/bin\/squeue'],
    ['SKIP',  r'^\/usr\/bin\/srun'],
    ['SKIP',  r'^\/usr\/bin\/sbatch'],
    ['SKIP',  r'^\/usr\/bin\/sacct'],
    ['SKIP',  r'^\/usr\/bin\/salloc'],
    ['SKIP',  r'^\/usr\/bin\/cp'],
    ['SKIP',  r'^\/usr\/bin\/mv'],
    ['SKIP',  r'^\/usr\/bin\/gawk'],
    ['SKIP',  r'^\/usr\/bin\/sed'],
    ['SKIP',  r'^\/usr\/bin\/perl'],
    ['SKIP',  r'^\/usr\/bin\/python'],
    ['SKIP',  r'^\/usr\/bin\/grep'],
    ['SKIP',  r'^\/usr\/bin\/bzip2'],
    ['SKIP',  r'^\/usr\/bin\/gzip'],
    ['SKIP',  r'^\/usr\/bin\/tar'],
    ['SKIP',  r'^\/bin\/cp'],
    ['SKIP',  r'^\/bin\/mv'],
    ['SKIP',  r'^\/bin\/gawk'],
    ['SKIP',  r'^\/bin\/sed'],
    ['SKIP',  r'^\/bin\/perl'],
    ['SKIP',  r'^\/bin\/python'],
    ['SKIP',  r'^\/bin\/grep'],
    ['SKIP',  r'^\/bin\/bzip2'],
    ['SKIP',  r'^\/bin\/gzip'],
    ['SKIP',  r'^\/bin\/tar'],
    ['SKIP',  r'^\/usr\/.*'],
    ['SKIP',  r'^\/sbin\/.*'],
    ['SKIP',  r'^\/bin\/.*'],
    ['SKIP',  r'^\/etc\/.*'],
    ['SKIP',  r'^\/root\/.*'],
    ['SKIP',  r'^\/opt\/intel\/.*'],
    ['SKIP',  r'^\/opt\/cray\/.*'],
    ['SKIP',  r'^\/opt\/pgi\/.*'],
    ['SKIP',  r'^\/opt\/gcc\/.*'],
    ['SKIP',  r'^\/opt\/modules\/.*'],
    #['SKIP',  r'^\/opt\/apps\/mpi_wrapper\/.*'],
#    ['SKIP',  r'^\/opt\/apps\/slurm_wrapper\/.*'],
#    ['SKIP',  r'^\/opt\/apps\/intel\/.*'],
#    ['SKIP',  r'^\/opt\/apps\/cuda\/.*'],
#    ['SKIP',  r'^\/opt\/apps\/lua\/.*'],
#    ['SKIP',  r'^\/opt\/apps\/lmod\/.*'],
#    ['SKIP',  r'^\/opt\/apps\/shell_startup_debug\/.*'],
#    ['SKIP',  r'^\/opt\/apps\/tacc_tips\/.*'],
#    ['SKIP',  r'.*\/l\/pkg\/xalt\/'],
#    ['SKIP',  r'.*\/l\/pkg\/lua\/'],
#    ['SKIP',  r'.*\/l\/pkg\/lmod\/'],
#    ['SKIP',  r'^\/opt\/apps\/xalt\/.*'],
#    ['SKIP',  r'^\/opt\/apps\/git\/.*'],
#    ['SKIP',  r'^\/opt\/apps\/cmake\/.*'],
#    ['SKIP',  r'^\/opt\/apps\/autotools\/.*'],
#    ['SKIP',  r'^\/opt\/apps\/intel[0-9][0-9_]*\/mvapich2\/.*'],
#    ['SKIP',  r'^\/opt\/apps\/intel[0-9][0-9_]*\/cray_mpich\/.*'],
#    ['SKIP',  r'^\/opt\/apps\/intel[0-9][0-9_]*\/impi\/.*'],
#    ['SKIP',  r'^\/opt\/apps\/gcc[0-9][0-9_]*\/mvapich2\/.*'],
#    ['SKIP',  r'^\/opt\/apps\/gcc\/.*'],
#    ['SKIP',  r'.*\/git'],
#    ['SKIP',  r'.*\/lua'],
#    ['SKIP',  r'.*\/mpiCC'],
#    ['SKIP',  r'.*\/mpicc'],
#    ['SKIP',  r'.*\/mpicxx'],
#    ['SKIP',  r'.*\/mpif77'],
#    ['SKIP',  r'.*\/mpif90'],
#    ['SKIP',  r'.*\/mpifort'],
#    ['SKIP',  r'.*\/mpifc'],
#    ['SKIP',  r'.*\/mpigcc'],
#    ['SKIP',  r'.*\/mpigxx'],
#    ['SKIP',  r'.*\/mpiicc'],
#    ['SKIP',  r'.*\/mpiicpc'],
#    ['SKIP',  r'.*\/mpiifort'],
#    ['SKIP',  r'.*\/mpiexec.hydra'],
#    ['SKIP',  r'.*\/hydra_pmi_proxy'],
#    ['SKIP',  r'.*\/ompi_info'],
#    ['SKIP',  r'.*\/opal_wrapper'],
#    ['SKIP',  r'.*\/orterun'],
#    ['SKIP',  r'.*\/vtwrapper'],
#    ['SKIP',  r'.*\/conftest'],
#    ['SKIP',  r'.*\/CMakeTmp\/cmTryCompileExec[0-9][0-9]*'],
#    ['SKIP',  r'.*\/CMakeTmp\/cmTC_[a-f0-9][a-f0-9]*'],
    ['KEEP',  r'^\/.*'],
  ]

#------------------------------------------------------------
# XALT samples non-mpi executions, based on this table.
# All mpi executions are sampled at 100% when there are
# two more tasks.
#
# The array of array used by interval_array has the following
# structure:
#
#   interval_array = [
#                     [ t_0,     probability_0],
#                     [ t_1,     probability_1],
#                     ...
#                     [ t_n,     probability_n],
#                     [ 1.0e308, 1.0],
#
#
# The first number is the left edge of the time range.  The
# second number is the probability of being sampled. Where a
# probability of 1.0 means a 100% chance of being recorded and a
# value of 0.01 means a 1% chance of being recorded.
#
# So a table that looks like this:
#     interval_array = [
#                       [ 0.0,                0.0001 ],
#                       [ 300.0,              0.01   ],
#                       [ 600.0,              1.0    ],
#                       [ sys.float_info.max, 1.0    ]
#     ]
#
# would say that program with execution time that is between
# 0.0 and 300.0 seconds has a 0.01% chance of being recorded.
# Execution times between 300.0 and 600.0 seconds have a 1%
# chance of being recorded and and programs that take longer
# than 600 seconds will always be recorded.
#
# The absolute minimum table would look like:
#
#     interval_array = [
#                       [ 0.0,                1.0 ],
#                       [ sys.float_info.max, 1.0 ]
#     ]
#
# which says to record every scalar (non-mpi) program no matter
# the execution time.
#
# Note that scalar execution only uses this table IFF
# $XALT_SCALAR_AND_SPSR_SAMPLING equals yes

interval_array = [
    [ 0.0,                1.0 ],
    [ sys.float_info.max, 1.0 ]
]

#------------------------------------------------------------
# XALT filter environment variables.  Those variables
# which pass through the filter are save in an SQL table that is
# searchable via sql commands.  The environment variables are passed
# to this filter routine as:
#
#      env_key=env_value
#
# So the regular expression patterns must match the whole string.


# The value on the left is either KEEP or SKIP.  If the value
# is KEEP then if the environment string matches the regular
# expression then the variable is stored. If the value on the left
# is SKIP then if the variable matches it is not stored.

# Order of the list matters.  The first match is used even if a
# later pattern would also match.  The upshot is that special pattern
# matches should appear first and general ones later.

# If the environment string does not match any pattern then it is
# marked as SKIP.


env_patterns = [
    [ 'SKIP', r'^__.*'],
    [ 'KEEP', r'^ALLINEA.*' ],
    [ 'KEEP', r'^ALT_LINKER.*' ],
    [ 'KEEP', r'^CRAYPE_NETWORK_TARGET.*' ],
    [ 'KEEP', r'^CRAYPE_VERSION.*' ],
    [ 'KEEP', r'^CRAY_CPU_TARGET.*' ],
    [ 'KEEP', r'^CRAY_CUDA_MPS.*' ],
    [ 'KEEP', r'^CRAY_LD_LIBRARY_PATH.*' ],
    [ 'KEEP', r'^CRAY_LIBSCI_PREFIX_DIR.*' ],
    [ 'KEEP', r'^CRAY_MPICH_DIR.*' ],
    [ 'KEEP', r'^CUDA_CACHE_PATH.*' ],
    [ 'KEEP', r'^CUDA_LIB_PATH.*' ],
    [ 'KEEP', r'^CUDA_PATH.*' ],
    [ 'KEEP', r'^CUDA_TOOLKIT_PATH.*' ],
    [ 'KEEP', r'^CUDNN_INSTALL_PATH.*' ],
    [ 'KEEP', r'^CUDNN_PATH.*' ],
    [ 'KEEP', r'^GCC_PATH.*' ],
    [ 'KEEP', r'^HDF5PATH.*' ],
    [ 'KEEP', r'^HOSTNAME.*' ],
    [ 'KEEP', r'^KMP_AFFINITY.*' ],
    [ 'KEEP', r'^KMP_STACKSIZE.*' ],
    [ 'KEEP', r'^LD.*' ],
    [ 'KEEP', r'^MIC_LD_LIBRARY_PATH.*' ],
    [ 'KEEP', r'^MIC_LIBRARY_PATH.*' ],
    [ 'KEEP', r'^MKL.*'],
    [ 'KEEP', r'^MKL_DYNAMIC.*' ],
    [ 'KEEP', r'^MKL_LIBS.*' ],
    [ 'KEEP', r'^MKL_NUM_THREADS.*' ],
    [ 'KEEP', r'^MKL_VERBOSE.*' ],
    [ 'KEEP', r'^MPICH_DIR.*' ],
    [ 'KEEP', r'^MV2_.*'],
    [ 'KEEP', r'^OFFLOAD.*'],
    [ 'KEEP', r'^OMP.*'],
    [ 'KEEP', r'^PATH.*' ],
    [ 'KEEP', r'^PE_ENV.*' ],
    [ 'KEEP', r'^PGI_PATH.*' ],
    [ 'KEEP', r'^PYTHON.*'],
    [ 'KEEP', r'^SHELL.*' ],
    [ 'KEEP', r'^SLURM.*' ],
    [ 'KEEP', r'SYS_NAME' ],
    [ 'KEEP', r'^USER' ],
    [ 'KEEP', r'^XTPE_NETWORK_TARGET.*' ],
    [ 'KEEP', r'^LOADEDMODULES.*' ],
    [ 'KEEP', r'^MODULEPATH.*' ],
    [ 'SKIP', r'.*'],
  ]

