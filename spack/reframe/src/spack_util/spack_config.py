PE_INDEPENDENT_PKGS = {
    'cuda': {
        'buildable' : False,
        'modules' : 'cudatoolkit',
    },
    'cosma': {
        'variants': "+ipo+scalapack+cuda cuda_arch=60 build_type=Release"
    },
    'fftw': {
        'variants': "+mpi +openmp precision=long_double,double,float"
    },
    'gromacs': {
        'variants': "+mpi+cuda+cycle_subcounters+ipo+blas+lapack build_type=Release"
    },
    'mpich': {
        'version': ['3.1.2']
    },
    'netlib-scalapack': {
        'variants': "build_type=Release"
    },
    'netlib-lapack': {
        'variants': "build_type=Release"
    },
    'openblas': {
        'variants': "+pic +shared threads=openmp ~virtual_machine"
    },
}

PE_DEPENDENT_PKGS = {
    'cray-libsci': {
        'buildable' : False,
        'variants' : "+mpi+openmp",
        'modules' : 'cray-libsci'
    },
    'cray-fftw': {
        'buildable' : False,
        'modules' : 'cray-fftw'
    },
    'cray-mpich': {
        'buildable' : False,
        'modules' : 'cray-mpich'
    },
    'papi': {
        'buildable' : False,
        'modules' : 'papi'
    },
    'mpich': {
        'buildable' : False,
        'modules' : 'cray-mpich',
        'version_map' : {'7.7.15': '3.1.4', 'default': '3.2.1'},
    },
    'cray-python': {
        'buildable' : True,
        'name': 'python',
        'modules' : 'cray-python'
    },
    'cray-hdf5': {
        'buildable' : True,
        'name': 'hdf5',
        'variants': "~mpi+hl+fortran",
        'modules' : 'cray-hdf5'
    },
    'cray-hdf5-parallel': {
        'buildable' : True,
        'name': 'hdf5',
        'variants': "+mpi+hl+fortran",
        'modules' : 'cray-hdf5-parallel'
    },
    'cray-netcdf-hdf5parallel': {
        'buildable' : True,
        'name': 'netcdf',
        'variants': "+parallel-netcdf+mpi",
        'modules' : 'cray-hdf5-parallel'
    },
    'cray-netcdf-hdf5parallel-fortran': {
        'buildable' : True,
        'name': 'netcdf-fortran',
        'variants': "+parallel-netcdf+mpi",
        'modules' : 'cray-netcdf-hdf5parallel'
    },
    'cray-netcdf-hdf5parallel-c': {
        'buildable' : True,
        'name': 'netcdf-c',
        'variants': "+parallel-netcdf+mpi",
        'modules' : 'cray-netcdf-hdf5parallel'
    },
    'cray-netcdf-parallel': {
        'buildable' : True,
        'name': 'parallel-netcdf',
        'variants': "+cxx+fortran",
        'modules' : 'cray-netcdf-hdf5parallel'
    },
    'cray-netcdf-fortran': {
        'buildable' : True,
        'name': 'netcdf-fortran',
        'variants': "~parallel-netcdf+mpi",
        'modules' : 'cray-netcdf'
    },
    'cray-netcdf-c': {
        'buildable' : True,
        'name': 'netcdf-c',
        'variants': "~parallel-netcdf+mpi",
        'modules' : 'cray-netcdf'
    },
    'cray-petsc': {
        'buildable' : True,
        'name': 'petsc',
        'variants': "~int64~complex~cuda",
        'modules' : 'cray-petsc'
    },
    'cray-petsc-complex': {
        'buildable' : True,
        'name': 'petsc',
        'variants': "~int64+complex~cuda",
        'modules': 'cray-petsc-complex'
    },
    'cray-petsc-64': {
        'buildable' : True,
        'name': 'petsc',
        'variants': "+int64~complex~cuda",
        'modules': 'cray-petsc-64'
    },
    'cray-petsc-complex-64': {
        'buildable' : True,
        'name': 'petsc',
        'variants': "+int64+complex~cuda",
        'modules': 'cray-petsc-complex-64'
    },
    'cray-trilinos': {
        'buildable' : True,
        'variants' : "build_type=Release",
        'name': 'trilinos',
        'prefix' : True,
        'modules': 'cray-trilinos'
    },
    # 'intel-mkl-tbb': {
    #     'buildable' : True,
    #     'name': 'intel-mkl',
    #     'prefix' : '/opt/intel',
    #     'variants': "+ilp64 threads=tbb",
    # },
    # 'intel-mkl-openmp': {
    #     'buildable' : True,
    #     'name': 'intel-mkl',
    #     'prefix' : '/opt/intel',
    #     'variants': "+ilp64 threads=openmp",
    # },
    # 'intel-mkl-none': {
    #     'buildable' : True,
    #     'name': 'intel-mkl',
    #     'prefix' : '/opt/intel',
    #     'variants': "+ilp64 threads=none",
    # },
}

BLACKLISTED_PKG_MODULES = [
    'apr',
    'apr-util',
    'arpack-ng',
    'autoconf',
    'automake',
    'autotools',
    'bazel',
    'bdftopcf',
    'berkeleydb',
    'binutils',
    'bison',
    'byacc',
    'bzip2',
    'c3',
    'cairo',
    'coreutils',
    'cube',
    'cuda',
    'cudnn',
    'curl',
    'diffutils',
    'double-conversion',
    'doxygen',
    'eigen',
    'expat',
    'fftw',
    'findutils',
    'flex',
    'fltk',
    'font-util',
    'fontconfig',
    'fontsproto',
    'freetype',
    'funcsigs',
    'gc',
    'gdbm',
    'gettext',
    'gl2ps',
    'glib',
    'glpk',
    'gmake',
    'gmp',
    'gnutls',
    'go-boostrap',
    'gompi',
    'gperf',
    'graphicsmagick',
    'gts',
    'guile',
    'harfbuzz',
    'help2man',
    'hwloc',
    'icu4c',
    'inputproto',
    'ipython',
    'isl',
    'jasper',
    'junit',
    'kbproto',
    'lcms',
    'libarchive',
    'libbsd',
    'libcerf',
    'libdrm',
    'libedit',
    'libevent',
    'libffi',
    'libfontenc',
    'libgd',
    'libglu',
    'libiberty',
    'libiconv',
    'libinit',
    'libint',
    'libjpeg-turbo',
    'libmng',
    'libpciaccess',
    'libpng',
    'libpthread-stubs',
    'libqglviewer',
    'libreadline',
    'libsigsegv',
    'libsodium',
    'libtiff',
    'libtool',
    'libunistring',
    'libunwind',
    'libutempter',
    'libuv',
    'libx11',
    'libxau',
    'libxc',
    'libxcb',
    'libxdmcp',
    'libxfont',
    'libxml2',
    'libxshmfence',
    'libxsmm',
    'loki',
    'lz4',
    'lzo',
    'm4',
    'make',
    'mako',
    'mesa',
    'mkfontdir',
    'mkfontscale',
    'mock',
    'mpc',
    'mpfr',
    'mpich',
    'mxml',
    'nasm',
    'ncurses',
    'nettle',
    'nose-parameterized',
    'numactl',
    'opari2',
    'openpgm',
    'openssl',
    'otf2',
    'pcre',
    'pcre',
    'pcre2',
    'pdt',
    'perl',
    'perl-data-dumper',
    'pil',
    'pixman',
    'pkg-config',
    'pkgconf',
    'ploticus',
    'proj',
    'protobuf',
    'protobuf-core',
    'pygts',
    'pyqt',
    'python-bare',
    'python-xlib',
    'qrupdate',
    'qt',
    'readline',
    'rhash',
    'scons',
    'scotch',
    'serf',
    'sionlib',
    'sip',
    'sqlite',
    'swig',
    'szip',
    'tar',
    'tcl',
    'texinfo',
    'tk',
    'udunits',
    'util-linux',
    'util-macros',
    'wheel',
    'xcb-proto',
    'xextproto',
    'xproto',
    'xtrans',
    'xz',
    'yasm',
    'zeromq',
    'zlib'
]

MODULE_SUFFIXES = {
    'build_type=RelWithDebInfo': 'reldebinfo',
    'build_type=Release': 'release',
    '+cuda': 'cuda',
    '+cycle_subcounters': 'subcounters',
    '+openmp': 'omp',
    '+omp': 'omp',
    'threads=openmp': 'omp',
    'threads=tbb': 'tbb',
    '^intel-mkl': 'mkl',
    '^openblas': 'openblas',
    '^netlib-lapack': 'lapack',
    '^netlib-scalapack': 'scalapack',
    '+shared': 'shared',
    '+plumed': 'plumed',
    '+pic': 'pic',
    '+pmi': 'pmi',
    '+slurm': 'slurm',
    '+verbs': 'verbs',
    '+elpa': 'elpa',
    '+libxc': 'libxc',
    '+pexsi': 'pexsi',
    '+docs': 'docs',
    '^python@2': 'python2',
    '^python@3': 'python3'
}

MODULE_CONFIGS = {
    'modules' : {
        r'enable:' : ['tcl'],
        'lmod' : {
            'verbose': True,
            'core_compilers': [],
            'hierarchy': ['mpi', 'lapack'],
            'hash_length': 0,
            'blacklist': [],
            'all' : {
                'suffixes' : {},
                'environment': {
                    'set' : {
                        r'${PACKAGE}_ROOT': r'${PREFIX}'
                    }
                }
            },
            '^python': {
                'autoload': 'direct'
            },
        },
        'tcl' : {
            'verbose': True,
            'hash_length': 0,
            'blacklist': [],
            'all' : {
                'conflict' : [r'${PACKAGE}'],
                'suffixes' : {},
                'environment': {
                    'set' : {
                        r'${PACKAGE}_ROOT': r'${PREFIX}'
                    }
                },
            },
            r'^python': {
                'autoload': r'direct'
            },
            'projections' : {
                'all' : r'{name}/{version}-{compiler.name}-{compiler.version}',
                '^mpi' : r'{name}/{version}-{^mpi.name}-{^mpi.version}-{compiler.name}-{compiler.version}'
            }
        }
    }
}

SPACK_CONFIG = {
    'config' : {
        'build_stage' : [r'${XDG_RUNTIME_DIR}', r'$spack/.spack/var/stage'],
        'source_cache': r'$spack/.spack/var/cache/source',
        'misc_cache': r'$spack/.spack/var/cache/misc',
        'build_jobs': 8,
        'db_lock_timeout' : 20, # increasing time to allow CI to pass
    }
}
