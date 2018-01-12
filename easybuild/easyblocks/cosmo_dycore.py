"""
EasyBuild support for building and installing the COSMO C++ dynamical core

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


class EB_COSMO_DYCORE(CMakeMake):
    """Support for building/installing the COSMO C++ dynamical core."""

    @staticmethod
    def extra_options():
        extra_vars = {
            'enable_cuda': [False, "Enable CUDA backend (-DCUDA_BACKEND=ON)", CUSTOM],
        }
        return CMakeMake.extra_options(extra_vars)

    def __init__(self, *args, **kwargs):
        super(EB_COSMO_DYCORE, self).__init__(*args, **kwargs)
        self.lib_subdir = ''
        self.pre_env = ''

    def configure_step(self):
        
        self.cfg.update('configopts', "-DCMAKE_BUILD_TYPE=Release")


        if self.cfg['enable_cuda']:
            self.cfg.update('configopts', "-DCUDA_BACKEND=ON")
        else:
            self.cfg.update('configopts', "-DCUDA_BACKEND=OFF")

        out = super(EB_COSMO_DYCORE, self).configure_step()

