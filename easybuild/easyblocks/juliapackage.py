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

@author: Kenneth Hoste (Ghent University)
@author: Samuel Omlin (CSCS)
@author: Victor Holanda (CSCS)
"""
import os
import shutil

#from easybuild.easyblocks.r import EXTS_FILTER_R_PACKAGES, EB_R
from easybuild.framework.easyconfig import CUSTOM
from easybuild.framework.extensioneasyblock import ExtensionEasyBlock
from easybuild.tools.build_log import EasyBuildError
from easybuild.tools.filetools import mkdir
from easybuild.tools.run import run_cmd, parse_log_for_error


class JuliaPackage(ExtensionEasyBlock):
    """
    Install an Julia package as a separate module, or as an extension.
    """

    def __init__(self, *args, **kwargs):
        """Initliaze RPackage-specific class variables."""

        super(JuliaPackage, self).__init__(*args, **kwargs)
        self.package_name = ""

    def patch_step(self, beginpath=None):
        pass

    def fetch_sources(self, sources=None, checksums=None):
        pass

    def extract_step(self):
        """Source should not be extracted."""
        pass

    def configure_step(self):
        """No configuration for installing Julia packages."""
        pass

    def build_step(self):
        """No separate build step for Julia packages."""
        pass

    def make_julia_cmd(self, prefix=None, remove=False):
        """Create a command to run in julia to install an julia package."""

        if not prefix:
            prefix = ''
        self.depot=prefix

        self.package_name = self.name
        names = self.package_name.split('.')
        if len(names) > 1:
            self.package_name = ''.join(names[:-1])
        print("package_name: %s" % self.package_name)

        install_opts = ""
        if self.cfg['installopts']:
            install_opts = self.cfg['installopts']
        else:
            install_opts = "name=\"%s\", version=\"%s\"" % (self.package_name, self.version)

        if remove:
            cmd = "%s export JULIA_DEPOT_PATH=%s && julia --eval 'using Pkg; Pkg.rm(PackageSpec(%s))'" % (self.cfg['preinstallopts'], self.depot, install_opts)
        else:
            cmd = "%s export JULIA_DEPOT_PATH=%s && julia --eval 'using Pkg; Pkg.add(PackageSpec(%s))'" % (self.cfg['preinstallopts'], self.depot, install_opts)

        self.log.debug("make_julia_cmd returns %s" % cmd)

        return cmd

    def install_step(self):
        """Install procedure for Julia packages."""

        cmd = self.make_julia_cmd(prefix=self.installdir, remove=False)
        cmdttdouterr, _ = run_cmd(cmd, log_all=True, simple=False, regexp=False)

        cmderrors = parse_log_for_error(cmdttdouterr, regExp="^ERROR:")
        if cmderrors:
            cmd = self.make_julia_cmd(prefix=self.installdir, remove=True)
            run_cmd(cmd, log_all=False, log_ok=False, simple=False, inp=stdin, regexp=False)
            raise EasyBuildError("Errors detected during installation of Julia package %s!", self.name)
        else:
            self.log.debug("Julia package %s installed succesfully" % self.name)


    def run(self):
        """Install Julia package as an extension."""
        self.install_step()


    def sanity_check_step(self, *args, **kwargs):
        """
        Custom sanity check for Julia packages
        """

        cmd = "export JULIA_DEPOT_PATH=%s && julia --eval 'import (\"%s\")'" % (self.depot, self.package_name)
        if 'CUDA' in self.package_name or 'CuArrays' in self.package_name:
            cmd = "export JULIA_DEPOT_PATH=%s && julia --eval 'using Pkg; Pkg.status(PackageSpec(\"%s\"))'" % (self.depot, self.package_name)

        cmdttdouterr, _ = run_cmd(cmd, log_all=True, simple=False, regexp=False)
        cmderrors = parse_log_for_error(cmdttdouterr, regExp="%s" % self.version)

        if cmderrors:
            return True

        return False
        #return super(JuliaPackage, self).sanity_check_step(EXTS_FILTER_R_PACKAGES, *args, **kwargs)

    #def make_module_extra(self):
    #    """Add install path to R_LIBS"""
    #    # prepend R_LIBS with install path
    #    extra = self.module_generator.prepend_paths("R_LIBS", [self.cfg['exts_subdir']])
    #    return super(RPackage, self).make_module_extra(extra)
