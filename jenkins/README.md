# Directory related to Jenkins

This directory contains files related to the Jenkins ci used in CSCS for regression, testing and production. The following files are present:

* `Machines.groovy:` Contains information for each machine at CSCS. Each machine is 
   defined as a groovy dictionary and a list of all the machine dictionaries is returned.

* `util.groovy:` Contains a number of common methods used in the Jenkins pipelines.

* `JenkinsfileRegressionEB:` This is the Jenkins pipeline script used for the regression Jenkins project.

* `JenkinsfileTestingEB:` This is the Jenkins pipeline script used for the testing Jenkins project.
