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
EasyBuild support for building and installing Julia packages, implemented as an easyblock

@author: Victor Holanda (CSCS)
@author: Samuel Omlin (CSCS)
"""
import os
import shutil
import socket

from easybuild.tools.config import build_option
from easybuild.framework.easyconfig import CUSTOM
from easybuild.easyblocks.generic.packedbinary import PackedBinary
from easybuild.tools.build_log import EasyBuildError
from easybuild.tools.filetools import mkdir
from easybuild.tools.run import run_cmd, parse_log_for_error
from easybuild.tools import systemtools


class EB_Julia(PackedBinary):
    """
    Install an Julia package as a separate module, or as an extension.
    """
    @staticmethod
    def extra_options(extra_vars=None):
        extra_vars = {
            'arch_name': [None, "Change julia's Project.toml pathname", CUSTOM],
        }
        return PackedBinary.extra_options(extra_vars)


    def get_environment_path(self):
        env_path = ''

        hostname = socket.gethostname()
        hostname_short = ''.join(c for c in hostname if not c.isdigit())

        if self.cfg['arch_name']:
            env_path = '-'.join([hostname_short, self.cfg['arch_name']])
            return env_path

        optarch = build_option('optarch') or None
        if optarch:
            env_path = '-'.join([hostname_short, optarch])
        else:
            arch = systemtools.get_cpu_architecture()
            cpu_family = systemtools.get_cpu_family()
            env_path = '-'.join([hostname_short, cpu_family, arch])
        return env_path

    def get_user_depot_path(self):
        user_depot_path = ''

        hostname = socket.gethostname()
        hostname_short = ''.join(c for c in hostname if not c.isdigit())

        optarch = build_option('optarch') or None
        if optarch:
            user_depot_path = os.path.join('~', '.julia', self.version, self.get_environment_path())
        else:
            arch = systemtools.get_cpu_architecture()
            cpu_family = systemtools.get_cpu_family()
            user_depot_path = os.path.join('~', '.julia', self.version, self.get_environment_path())
        return user_depot_path

    def __init__(self, *args, **kwargs):
        """Initliaze RPackage-specific class variables."""
        super(EB_Julia, self).__init__(*args, **kwargs)

        user_depot = self.get_user_depot_path()
        local_share_depot = os.path.join(self.installdir, 'local', 'share', 'julia')
        share_depot = os.path.join(self.installdir, 'share', 'julia')
        extensions_depot = os.path.join(self.installdir, 'extensions')

        self.depot_path = ':'.join([user_depot, extensions_depot, local_share_depot, share_depot])
        self.julia_project = os.path.join(user_depot, "environments", '-'.join([self.version, self.get_environment_path()]))
        self.julia_load_path = '@:@#.#.#-%s:@stdlib' % self.get_environment_path()

    def sanity_check_step(self):
        """Custom sanity check for Julia."""

        custom_paths = {
            'files': [os.path.join('bin', 'julia'), 'LICENSE.md'],
            'dirs': ['bin', 'include', 'lib', 'share'],
        }
        custom_commands = [
            "julia --version",
            "julia --eval '1+2'",
        ]

        super(EB_Julia, self).sanity_check_step(custom_paths=custom_paths, custom_commands=custom_commands)

    def make_module_extra(self, *args, **kwargs):
        txt = super(EB_Julia, self).make_module_extra(*args, **kwargs)

        txt += self.module_generator.set_environment('JULIA_DEPOT_PATH', self.depot_path)
        txt += self.module_generator.set_environment('JULIA_PROJECT', self.julia_project)
        txt += self.module_generator.set_environment('JULIA_LOAD_PATH', self.julia_load_path)
        txt += self.module_generator.set_environment('EBJULIA_ENV_NAME', '-'.join([self.version, self.get_environment_path()]))
        return txt

