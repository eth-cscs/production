##
# Copyright 2009-2016 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# Flemish Research Foundation (FWO) (http://www.fwo.be/en)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBuild support for building and installing HPCG, implemented as an easyblock

@author: Kenneth Hoste (Ghent University)
"""
import os
import shutil

from easybuild.easyblocks.generic.configuremake import ConfigureMake
from easybuild.tools.build_log import EasyBuildError
from easybuild.tools.filetools import mkdir
from easybuild.tools.run import run_cmd


class hpcg3(ConfigureMake):
    """Support for building/installing HPCG."""

    def configure_step(self):
        """Custom configuration procedure for HPCG."""

        mkdir("obj")
        # configure with most generic configuration available, i.e. hybrid
        # this is not specific to GCC or OpenMP, we take full control over that via $CXX and $CXXFLAGS
        cmd = "../configure MPI_GCC_OMP"
        run_cmd(cmd, log_all=True, simple=True, log_ok=True, path='obj')

    def build_step(self):
        """Run build in build subdirectory."""
        cxx = os.environ['CXX']
        cxxflags = os.environ['CXXFLAGS']
        cmd = "make CXX='%s' CXXFLAGS='$(HPCG_DEFS) %s -DMPICH_IGNORE_CXX_SEEK'" % (cxx, cxxflags)
        run_cmd(cmd, log_all=True, simple=True, log_ok=True, path='obj')

    def install_step(self):
        """Custom install procedure for HPCG."""
        objbindir = os.path.join(self.cfg['start_dir'], 'obj', 'bin')
        bindir = os.path.join(self.installdir, 'bin')
        try:
            shutil.copytree(objbindir, bindir)
        except OSError as err:
            raise EasyBuildError("Failed to copy HPCG files to %s: %s", bindir, err)

    def sanity_check_step(self):
        """Custom sanity check for HPCG."""
        custom_paths = {
            'files': ['bin/xhpcg', 'bin/hpcg.dat'],
            'dirs': [],
        }
        super(hpcg3, self).sanity_check_step(custom_paths=custom_paths)
