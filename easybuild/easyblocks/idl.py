# This file is part of JSC's public easybuild repository 
# (https://github.com/easybuilders/jsc)
# adapted by Luca Marsella (CSCS)
"""
EasyBlock for IDL installation
@author: Sebastian Luehrs (FZJ)
"""
import os
import shutil

from easybuild.framework.easyblock import EasyBlock
from easybuild.tools.build_log import EasyBuildError
from easybuild.framework.easyconfig import CUSTOM
from easybuild.tools.run import run_cmd

class EB_IDL(EasyBlock):
    """Support for installing IDL.
    Just unpack the sources in the install dir
    """

    @staticmethod
    def extra_options(extra_vars=None):
        """Extra easyconfig parameters specific to IDL easyblock."""
        extra_vars = EasyBlock.extra_options(extra_vars)
        extra_vars.update({
            'answer_file': [None, "Install answer file to be used", CUSTOM]
        })
        return extra_vars

    def configure_step(self):
        """No configuration, this is binary software"""
        pass

    def build_step(self):
        """No compilation, this is binary software"""
        pass

    def install_step(self):
        """
        Run IDL install.sh
        """

        if self.cfg['answer_file'] is None:
            file_handle = open('idl_answer_file',"w")
            file_handle.write("""y
""")
            file_handle.write("""%s
""" % (self.installdir))
            file_handle.write("""y
""")
            file_handle.write("""n
""")
            file_handle.write("""y
""")
            file_handle.write("""n
""")
            file_handle.write("""y
""")
            file_handle.write("""n
""")
            file_handle.close()
            self.cfg['answer_file'] = 'idl_answer_file'

        cmd = "./install.sh -s < %s" % (self.cfg['answer_file'])
        cmd = ' '.join([self.cfg['preinstallopts'], cmd,                       \
                        self.cfg['installopts']])
        self.log.info("Installing %s using command '%s'..." % (self.name, cmd))
        run_cmd(cmd, log_all=True, simple=True)

    def make_module_extra(self):
        """Add the bin directory to the PATH."""

        txt = self.module_generator.prepend_paths("PATH", ['idl/bin'])
#        txt += self.module_generator.prepend_paths(                            \
#                  "LD_LIBRARY_PATH", ['idl/bin/bin.linux.x86_64',              \
#                  'idl/bin/bin.linux.x86_64/dm/lib',                           \
#                  'idl/idlde/bin.linux.x86_64/jre/lib/amd64',                  \
#                  'idl/idlde/bin.linux.x86_64/jre/lib/amd64/server',           \
#                  'idl/idlde/bin.linux.x86_64/jre/lib/amd64/xawt'])
        txt += super(EB_IDL, self).make_module_extra()
        self.log.debug("make_module_extra added this: %s" % txt)
        return txt
