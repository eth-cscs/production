"""
EasyBuild support for building and installing STELLA, implemented as an easyblock

@author: Hannes Vogt (CSCS)
"""
import glob
import os
import re
import shutil
from distutils.version import LooseVersion

import easybuild.tools.environment as env
import easybuild.tools.toolchain as toolchain
from easybuild.easyblocks.generic.configuremake import ConfigureMake
from easybuild.easyblocks.generic.cmakemake import CMakeMake
from easybuild.framework.easyconfig import CUSTOM
from easybuild.tools.build_log import EasyBuildError
from easybuild.tools.filetools import download_file, extract_file, which
from easybuild.tools.modules import get_software_libdir, get_software_root, get_software_version
from easybuild.tools.run import run_cmd
from easybuild.tools.systemtools import get_platform_name , get_shared_lib_ext


class EB_STELLA(CMakeMake):
    """Support for building/installing STELLA."""

    @staticmethod
    def extra_options():
        extra_vars = {
#            'single_precision': [False, "Build with single precision enabled (-DSINGLEPRECISION=ON)", CUSTOM],
            'enable_cuda': [False, "Enable CUDA backend (-DCUDA_BACKEND=ON)", CUSTOM],
            'cuda_compute_capability': ['sm_60', "CUDA compute capability (if CUDA backend enabled)", CUSTOM],
            'ksize': [60, "Compile-time k-size hint", CUSTOM],
            'kflat': [11, "k-level that defines the split between flat and terrain coordinates", CUSTOM],
            'enable_openmp': [False, "Enable OpenMP backend (-DENABLE_OPENMP)", CUSTOM],
            'use_gcl': [True, "Use GCL", CUSTOM],
        }
        return CMakeMake.extra_options(extra_vars)

    def __init__(self, *args, **kwargs):
        """Initialize STELLA-specific variables."""
        super(EB_STELLA, self).__init__(*args, **kwargs)
        self.lib_subdir = ''
        self.pre_env = ''

    def configure_step(self):
        """Custom configuration procedure for STELLA: set configure options for configure or cmake."""
        # build a release build
        self.cfg.update('configopts', "-DCMAKE_BUILD_TYPE=Release")


        if "float" in self.cfg['versionsuffix']:
            self.cfg.update('configopts', "-DSINGLEPRECISION=ON")
        else:
            self.cfg.update('configopts', "-DSINGLEPRECISION=OFF")

        if self.cfg['enable_cuda']:
            self.cfg.update('configopts', "-DCUDA_BACKEND=ON")
            self.cfg.update('configopts', "-DCUDA_COMPUTE_CAPABILITY=%s" % self.cfg['cuda_compute_capability'])
        else:
            self.cfg.update('configopts', "-DCUDA_BACKEND=OFF")

        self.cfg.update('configopts', "-DSTELLA_KSIZE=%d -DSTELLA_KFLAT=%d" % (self.cfg['ksize'], self.cfg['kflat']))


        if self.cfg['enable_openmp']:
            self.cfg.update('configopts', "-DENABLE_OPENMP=ON")
        else:
            self.cfg.update('configopts', "-DENABLE_OPENMP=OFF")

        if self.cfg['use_gcl']:
            self.cfg.update('configopts', "-DGCL=ON")
        else:
            self.cfg.update('configopts', "-DGCL=OFF")

        out = super(EB_STELLA, self).configure_step()

