# CSCS Production Repository

This is the CSCS Production Repository on the GitHub, with the list of CSCS production builds and [EasyBuild](https://hpcugent.github.io/easybuild) configuration files.
Please check the [CSCS User Portal](https://user.cscs.ch) for details on how to use the [EasyBuild framework at CSCS](https://user.cscs.ch/scientific_computing/code_compilation/easybuild_framework).

# Contributing back

## How to submit a pull request:

1. Add the EasyBuild configuration files to a __new branch__, including __all the required dependencies__
1. Create and __assign yourself a pull request__ following this policy for the title:
    * the title __must match a supported system__ in the list `daint dom fulen kesch leone monch`, otherwise the build will fail immediately. The system names __have to be enclosed in square brackets__ to be distinguished from the actual pull request title and be parsed by the corresponding Jenkins project.
    * if the title matches `WIP` ("Work In Progress"), then the test build will be aborted immediately, as work in progress is not supposed to be tested.
    * Dom and Piz Daint can test both software stacks `-gpu`and `-mc` at once:
        1. if the title matches only `${system}-gpu` or `${system}-mc`, only that software stack will be used:
            * `[dom-gpu] NAMD` will build using `-gpu`, `[dom-mc] NAMD` will use `-mc`.
        1. if the title matches both or none, then both will be used, one after another in a loop:
            * `[dom] NAMD` will build using both `-gpu` and `-mc` in a loop.
            * `[dom-gpu,dom-mc] NAMD` will do the same.
1. The CSCS Jenkins project `TestingEB` will test the build of new EasyBuild recipes with respect to the master. The corresponding pipeline of `TestingEB` is contained in the `jenkins/JenkinsfileTestingEB` script.
1. If the build is successful, you should __ask for a review__: the pull request will only be merged when approved.
1. In order to re-trigger the testing of the pull request without committing a change, add the comment `retest this please` which will notify the `TestingEB` Jenkins project.
1. (CSCS only) for production builds, please update the appropriate production build list [here](https://github.com/eth-cscs/production/tree/master/jenkins-builds).
