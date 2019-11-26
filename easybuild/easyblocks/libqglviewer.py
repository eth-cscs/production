from easybuild.easyblocks.generic.configuremake import ConfigureMake
from easybuild.tools.run import run_cmd
from easybuild.tools.modules import get_software_root

class libqglviewer(ConfigureMake):

   def configure_step(self):
        """
        Configure and 
        Test if Qt module is loaded
        """
        if not get_software_root('Qt'):
            raise EasyBuildError("Qt module not loaded")

        cmd = "%(preconfigopts)s qmake PREFIX=%(installdir)s %(configopts)s" % {
            'preconfigopts': self.cfg['preconfigopts'],
            'installdir': self.installdir,
            'configopts': self.cfg['configopts'],
        }

        (out, _) = run_cmd(cmd, log_all=True, simple=False)
