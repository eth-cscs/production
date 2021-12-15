##
# Copyright 2014-2021 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
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
CrayNvidia toolchain: Cray compilers (Nvidia) and MPI via Cray compiler drivers (PrgEnv-nvidia) without LibSci
:author: Luca Marsella (CSCS)
"""
from easybuild.toolchains.compiler.craype import CrayPENvidia
from easybuild.toolchains.mpi.craympich import CrayMPICH
from easybuild.tools.toolchain.toolchain import SYSTEM_TOOLCHAIN_NAME


class CrayNvidia(CrayPENvidia, CrayMPICH):
    """Compiler toolchain for Cray Programming Environment and Cray Compiling Environment (Nvidia) (PrgEnv-nvidia)."""
    NAME = 'CrayNvidia'
    SUBTOOLCHAIN = SYSTEM_TOOLCHAIN_NAME
