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


    def get_environment_folder(self):
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
            user_depot_path = os.path.join('~', '.julia', self.version, self.get_environment_folder())
        else:
            arch = systemtools.get_cpu_architecture()
            cpu_family = systemtools.get_cpu_family()
            user_depot_path = os.path.join('~', '.julia', self.version, self.get_environment_folder())
        return user_depot_path

    def __init__(self, *args, **kwargs):
        super(EB_Julia, self).__init__(*args, **kwargs)

        self.user_depot = self.get_user_depot_path()
        local_share_depot = os.path.join(self.installdir, 'local', 'share', 'julia')
        share_depot = os.path.join(self.installdir, 'share', 'julia')
        self.std_depots = ':'.join([local_share_depot, share_depot])
        self.julia_depot_path = ':'.join([self.user_depot, self.std_depots])
        self.admin_depots = os.path.join(self.installdir, 'extensions')

        self.julia_project = os.path.join(self.user_depot, "environments", '-'.join([self.version, self.get_environment_folder()]))

        self.user_load_path = '@:@#.#.#-%s' % self.get_environment_folder()
        self.std_load_paths = '@stdlib'
        self.julia_load_path = ':'.join([self.user_load_path, self.std_load_paths])
        self.admin_load_path = os.path.join(self.admin_depots, "environments", '-'.join([self.version, self.get_environment_folder()]))

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

    def install_step(self, *args, **kwargs):
        """Install procedure for Julia"""

        super(EB_Julia, self).install_step(*args, **kwargs)
        txt = """
## Read EB environment variables

if haskey(ENV, "EBJULIA_ADMIN_LOAD_PATH")
    ADMIN_LOAD_PATH = split(ENV["EBJULIA_ADMIN_LOAD_PATH"],':')
else
    ADMIN_LOAD_PATH = []
end

if haskey(ENV, "EBJULIA_STD_LOAD_PATH")
    STD_LOAD_PATH = split(ENV["EBJULIA_STD_LOAD_PATH"],':')
else
    STD_LOAD_PATH = []
end

if haskey(ENV, "EBJULIA_ADMIN_DEPOT_PATH")
    ADMIN_DEPOT_PATH = split(ENV["EBJULIA_ADMIN_DEPOT_PATH"],':')
else
    ADMIN_DEPOT_PATH = []
end

if haskey(ENV, "EBJULIA_STD_DEPOT_PATH")
    STD_DEPOT_PATH = split(ENV["EBJULIA_STD_DEPOT_PATH"],':')
else
    STD_DEPOT_PATH = []
end


## Inject the admin paths, except if paths empty (or only "@" for LOAD_PATH) or all entries in std path.
if !( isempty(LOAD_PATH) || isempty(DEPOT_PATH) || (length(LOAD_PATH)==1 && LOAD_PATH[1]=="@") ||
      all([entry in STD_LOAD_PATH for entry in LOAD_PATH]) || all([entry in STD_DEPOT_PATH for entry in DEPOT_PATH]) )

    ## Inject the admin load path into the LOAD_PATH

    # Empty the LOAD_PATH, separating load path into user and std load path.
    user_load_path = []
    std_load_path = []
    while !isempty(LOAD_PATH)
        entry = popfirst!(LOAD_PATH)
        if entry in STD_LOAD_PATH
            push!(std_load_path, entry)
        else
            push!(user_load_path, entry)
        end
    end

    # Add user load path to LOAD_PATH
    while !isempty(user_load_path)
        entry = popfirst!(user_load_path)
        push!(LOAD_PATH, entry)
    end

    # Add admin load path to LOAD_PATH
    while !isempty(ADMIN_LOAD_PATH)
        entry = popfirst!(ADMIN_LOAD_PATH)
        push!(LOAD_PATH, entry)
    end

    # Add std load path to LOAD_PATH
    while !isempty(std_load_path)
        entry = popfirst!(std_load_path)
        push!(LOAD_PATH, entry)
    end


    ## Inject the admin depot path into the DEPOT_PATH

    # Empty the DEPOT_PATH, separating depots into user and std depots.
    user_depot_path = []
    std_depot_path = []
    while !isempty(DEPOT_PATH)
        depot = popfirst!(DEPOT_PATH)
        if depot in STD_DEPOT_PATH
            push!(std_depot_path, depot)
        else
            push!(user_depot_path, depot)
        end
    end

    # Add user depots to DEPOT_PATH
    while !isempty(user_depot_path)
        depot = popfirst!(user_depot_path)
        push!(DEPOT_PATH, depot)
    end

    # Add admin depots to DEPOT_PATH
    while !isempty(ADMIN_DEPOT_PATH)
        depot = popfirst!(ADMIN_DEPOT_PATH)
        push!(DEPOT_PATH, depot)
    end

    # Add std depots to DEPOT_PATH
    while !isempty(std_depot_path)
        depot = popfirst!(std_depot_path)
        push!(DEPOT_PATH, depot)
    end

end

        """
        with open(os.path.join(self.installdir, 'etc', 'julia', 'startup.jl'), 'w') as startup_file:
            startup_file.write(txt)
            startup_file.close()

    def make_module_extra(self, *args, **kwargs):
        txt = super(EB_Julia, self).make_module_extra(*args, **kwargs)

        txt += self.module_generator.set_environment('JULIA_PROJECT', self.julia_project)
        txt += self.module_generator.set_environment('JULIA_DEPOT_PATH', self.julia_depot_path)
        txt += self.module_generator.set_environment('EBJULIA_USER_DEPOT_PATH', self.user_depot)
        txt += self.module_generator.set_environment('EBJULIA_ADMIN_DEPOT_PATH', self.admin_depots)
        txt += self.module_generator.set_environment('EBJULIA_STD_DEPOT_PATH', self.std_depots)


        txt += self.module_generator.set_environment('JULIA_LOAD_PATH', self.julia_load_path)
        txt += self.module_generator.set_environment('EBJULIA_USER_LOAD_PATH', self.user_load_path)
        txt += self.module_generator.set_environment('EBJULIA_ADMIN_LOAD_PATH', self.admin_load_path)
        txt += self.module_generator.set_environment('EBJULIA_STD_LOAD_PATH', self.std_load_paths)

        txt += self.module_generator.set_environment('EBJULIA_ENV_NAME', '-'.join([self.version, self.get_environment_folder()]))

        return txt

