help([[

Description
===========
Production EasyBuild @ CSCS

More information
================
 - Homepage: https://github.com/eth-cscs/production/wiki
]])

whatis([===[Description: Production EasyBuild @ CSCS  ]===])
whatis([===[Homepage: https://github.com/eth-cscs/production/wiki]===])
conflict("EasyBuild-custom")

-- EasyBuild-custom SETUP 
local eb_config_dir="/apps/common/UES/jenkins/production/easybuild"
local eb_module_dir="/apps/common/UES/easybuild"
local eb_root_dir="/apps/common/UES/jenkins/easybuild/software/EasyBuild-custom/cscs"
local eb_runtime_dir=os.getenv("SCRATCH") or pathJoin("/tmp", os.getenv("USER"))
local eb_source_dir="/apps/common/UES/easybuild/sources"
setenv("EBROOTEASYBUILDMINCUSTOM", eb_root_dir)
setenv("EBVERSIONEASYBUILDMINCUSTOM", "cscs")
setenv("EBDEVELEASYBUILDMINCUSTOM", pathJoin(eb_root_dir, "/easybuild/EasyBuild-custom-cscs-easybuild-devel"))

--[[ 
 EB_CUSTOM_REPOSITORY defines the following variables:
 * XDG_CONFIG_DIRS
 * EASYBUILD_ROBOT_PATHS
 * EASYBUILD_INCLUDE_EASYBLOCKS
 * EASYBUILD_EXTERNAL_MODULES_METADATA (see section SYSTEM SPECIFIC)
--]]
local eb_custom_repository=os.getenv("EB_CUSTOM_REPOSITORY") or eb_config_dir
setenv("XDG_CONFIG_DIRS", eb_custom_repository)
setenv("EASYBUILD_ROBOT_PATHS", pathJoin(eb_custom_repository, "easyconfigs/:"))
setenv("EASYBUILD_INCLUDE_EASYBLOCKS", pathJoin(eb_custom_repository, "easyblocks/*.py"))

--[[ 
 XDG_RUNTIME_DIR defines the following variables:
 * EASYBUILD_BUILDPATH
 * EASYBUILD_TMPDIR
--]]
local xdg_runtime_dir=os.getenv("XDG_RUNTIME_DIR") or eb_runtime_dir
if not os.getenv("EASYBUILD_BUILDPATH") then
	setenv("EASYBUILD_BUILDPATH", pathJoin(xdg_runtime_dir, "build"))
end
if not os.getenv("EASYBUILD_TMPDIR") then
	setenv("EASYBUILD_TMPDIR", pathJoin(xdg_runtime_dir, "tmp"))
end

-- EASYBUILD_SOURCEPATH: use eb_source_dir if writable, otherwise $HOME/sources
if not os.getenv("EASYBUILD_SOURCEPATH") then
	if subprocess("test -w " .. eb_source_dir .. " ; echo $?") < "1" then
		setenv("EASYBUILD_SOURCEPATH", eb_source_dir)
	else
		setenv("EASYBUILD_SOURCEPATH", pathJoin(os.getenv("HOME"),"sources"))
	end
end

-- SYSTEM SPECIFIC (Cray with Lmod)
local system=os.getenv("LMOD_SYSTEM_NAME") or os.getenv("CLUSTER_NAME")
if system == "eiger" then
	setenv("EASYBUILD_EXTERNAL_MODULES_METADATA", pathJoin(eb_custom_repository, "cpe_external_modules_metadata-21.04.cfg"))
elseif system == "pilatus" then
	setenv("EASYBUILD_EXTERNAL_MODULES_METADATA", pathJoin(eb_custom_repository, "cpe_external_modules_metadata-21.05.cfg"))
else
	LmodError("System ", system, " is currently unsupported\n")
end
setenv("EASYBUILD_MODULE_NAMING_SCHEME","HierarchicalMNS")
setenv("EASYBUILD_MODULE_SYNTAX","Lua")
setenv("EASYBUILD_MODULES_TOOL","Lmod")
setenv("EASYBUILD_OPTARCH",os.getenv("CRAY_CPU_TARGET"))
setenv("EASYBUILD_RECURSIVE_MODULE_UNLOAD","0")

--[[ 
 EASYBUILD_PREFIX defines the following variable:
 * EASYBUILD_INSTALLPATH
--]]
if not os.getenv("EASYBUILD_PREFIX") then
	setenv("EASYBUILD_PREFIX", pathJoin(os.getenv("HOME"),"easybuild", system))
end
setenv("EASYBUILD_INSTALLPATH", os.getenv("EASYBUILD_PREFIX"))

-- add folder with already installed modules to the MODULEPATH
prepend_path("MODULEPATH", pathJoin(os.getenv("EASYBUILD_INSTALLPATH"), "modules/all"))

-- add EasyBuild module folder to MODULEPATH and load EasyBuild
prepend_path("MODULEPATH", pathJoin(eb_module_dir, "modules/all"))
load("EasyBuild")
