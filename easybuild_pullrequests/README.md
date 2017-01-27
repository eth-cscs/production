# EasyBuild: review process

You can share your .eb recipes by making a pull request in github.

## Github Pull Request (PR)

The first step is to create a pull request
(https://github.com/eth-cscs/production/compare) by comparing the master branch
with your branch.

## Jenkins build
Then, the jenkins plugin will test/review your commits as explained in
[ghprb-plugin](https://github.com/jenkinsci/ghprb-plugin/blob/master/README.md):

```
 "ok to test" to accept this pull request for testing
 "test this please" for a one time test run
 "add to whitelist" to add the author to the whitelist
```

* A succesfull build will show `check passed` in github with a link to the
jenkins build log, for instance [build number 85](https://jenkins.cscs.ch/job/ProductionEBtestingPR-gpu/85/label=daint103/console).

* The full list of pull requests is [here](https://github.com/eth-cscs/production/pulls).
