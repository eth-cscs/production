##
# Copyright 2009-2017 Ghent University
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
EasyBuild support for building and installing the Rmpi R library, implemented as an easyblock

@author: Stijn De Weirdt (Ghent University)
@author: Dries Verdegem (Ghent University)
@author: Kenneth Hoste (Ghent University)
@author: Jens Timmerman (Ghent University)
@author: Toon Willems (Ghent University)
@author: Balazs Hajgato (Vrije Universiteit Brussel)
@author: Guilherme Peretti-Pezzi (CSCS)
"""
import easybuild.tools.toolchain as toolchain
from distutils.version import LooseVersion
from easybuild.easyblocks.generic.rpackage import RPackage

import os

def make_R_install_option(opt, values, cmdline=False):
    """
    Make option list for install.packages, to specify in R environment.
    """
    txt = ""
    if values:
        if cmdline:
            txt = " --%s=\"%s" % (opt, values[0])
        else:
            txt = "%s=c(\"%s" % (opt, values[0])
        for i in values[1:]:
            txt += " %s" % i
        if cmdline:
            txt += "\""
        else:
            txt += "\")"
    return txt


class EB_Rmpi(RPackage):
    """Build and install Rmpi R library."""
    def make_cmdline_cmd(self, prefix=None):
        """Create a command line to install an R package."""
        self.configureargs = [
            "--with-Rmpi-include=%s/include " % os.environ['MPICH_DIR'], #%self.toolchain.get_variable('MPICH_DIR'),
            "--with-Rmpi-libpath=%s/lib " % os.environ['MPICH_DIR'], #%self.toolchain.get_variable('MPICH_DIR'),
            "--with-Rmpi-type=CRAY",
        ]
        confvars = ""
        if self.configurevars:
            confvars = make_R_install_option("configure-vars", self.configurevars, cmdline=True)
        confargs = ""
        if self.configureargs:
            confargs = make_R_install_option("configure-args", self.configureargs, cmdline=True)

        if prefix:
            prefix = '--library=%s' % prefix
        else:
            prefix = ''

        if self.patches:
            loc = self.ext_dir
        else:
            loc = self.ext_src
        cmd = "R CMD INSTALL %s %s %s %s --no-clean-on-error --no-test-load" % (loc, confargs, confvars, prefix)

        self.log.debug("make_cmdline_cmd returns %s" % cmd)
        return cmd, None
