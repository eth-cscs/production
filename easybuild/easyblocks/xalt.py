##
# Copyright 2009-2019 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# Flemish Research Foundation (FWO) (http://www.fwo.be/en)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# https://github.com/easybuilders/easybuild
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
EasyBuild support for building and installing XALT, implemented as an easyblock

@author: Victor Holanda (CSCS)
"""

import os

from easybuild.easyblocks.generic.configuremake import ConfigureMake


# This class only exists because one needs to remove the pattern xalt/version
# from the XALT configuration
# If not, applications compiled with a version of XALT will not be tracked if
# XALT is upgraded
class EB_xalt(ConfigureMake):
    """
    XALT easyblock
    """

    def configure_step(self, util=False):

        # change temporarily the installdir
        self.original_installdir = self.installdir
        self.installdir = os.path.dirname(os.path.dirname(self.installdir))

        super(EB_xalt, self).configure_step()

        # revert back to the original installdir
        self.installdir = self.original_installdir
