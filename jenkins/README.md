# Directory related to Jenkins

This directory contains files related to the Jenkins ci used in CSCS for regression, testing and production. The following files are present:

* `Machines.groovy:` Contains information for each machine at CSCS. Each machine is defined as a groovy dictionary and a list of all the machine dictionaries is returned. The following dictionary keys are provided:

    * `name`: the name of the machine
    * `archs`: the list of supported architectures (empty list if none)
    * `toolkits`: the list of supported toolkits
    * `toolkitVersions`: the list of supported toolkit versions
    * `unusePath`: colon separated string containing the paths to unuse for regression (empty string if none)

* `util.groovy:` Contains a number of common methods used in the Jenkins pipelines.

* `JenkinsfileRegressionEB:` This is the Jenkins pipeline script used for the regression Jenkins project.

* `JenkinsfileTestingEB:` This is the Jenkins pipeline script used for the testing Jenkins project.
