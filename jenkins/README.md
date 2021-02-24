# Directory related to Jenkins

This directory contains files related to the Jenkins ci used in CSCS for regression, testing and production.
The following files are present:

* `Machines.groovy:` Contains information for each machine at CSCS. Each machine is defined as a groovy dictionary and a list of all the machine dictionaries is returned.
The following dictionary keys are provided:

    * `name`: the name of the machine
    * `archs`: the list of supported architectures (empty list if none)
    * `cpus` : the number of cpu cores per architecture (single number if `archs` is an empty list)
    * `buildPath`: the path used as EASYBUILD_BUILDPATH for production
    * `unusePath`: colon separated string containing the paths to unuse for regression (empty string if none)
    * `modulesProduction`: the modules path to use
    * `prefixProduction`: the prefix path for EasyBuild

* `util.groovy:` Contains a number of common methods used in the Jenkins pipelines.

* `JenkinsfileReBuildEB:` This is the Jenkins pipeline script used for the regression Jenkins project.

* `JenkinsfileTestingEB:` This is the Jenkins pipeline script used for the testing Jenkins project.

* `JenkinsfileProductionEB:` This is the Jenkins pipeline script used for the production Jenkins project.

* `JenkinsfileUpdateEB:` This is the Jenkins pipeline script used for the update Jenkins project.
