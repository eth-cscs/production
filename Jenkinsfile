#!/usr/bin/env groovy

/*
enum Machine {
    DOM("dom"),
    DAINT("daint")

    private final name

    Machine(String machineName) {
        name = machineName
    }
    
    String toString() {
        return name
    }
}
*/

enum MachineConfiguration {
    MC("mc"),
    GPU("gpu"),
    BOTH("gpu mc")
    
    private final configuration

    MachineConfiguration(String conf) {
        configuration = conf
    }

    String toString() {
        return configuration
    }
}

MachineConfiguration getMachineConfiguration(String message, String machine) {
    def machinePattern = ".*${machine}.*"
    def machineGPU = ".*${machine}-gpu.*"
    def machineMC = ".*${machine}-mc.*"

    if (message ==~ machineGPU) {
        if (message ==~ machineMC) {
            return MachineConfiguration.BOTH
        }
        else {
            return MachineConfiguration.GPU
        }
    }
    else if (message ==~ machineMC) {
        return MachineCongiguration.MC
    }
     
    return MachineConfiguration.BOTH
}

boolean machineCheck(String message, String machine) {
    def machinePattern = ".*${machine}.*"
    
    return message ==~ machinePattern? true : false 
}

boolean checkWorkInProgress(String message) {
    if (message ==~ /.*WIP.*/) {
        return true
    }
    
    return false
}


/*-------------------------------------------------------------------
------------------------- STAGES ------------------------------------ 
-------------------------------------------------------------------*/

def builds = [:]

stage("Initialization") {
    if (checkWorkInProgress(env.ghprbPullTitle)) {
        println "Work in progress, aborting..."
        return 
    }
}

def machineList = ["dom"] //, "daint", "leone", "kesch", "monch"]

stage("Testing") {
    for (m in machineList) {
        def machine = m 
        def pullRequestMessage = env.ghprbPullTitle
        def runForMachine = machineCheck(pullRequestMessage, machine)

        if (runForMachine) {
            println "Machine ${machine} is added to stage"

            builds[machine] = {
                node(machine) {
                    println "Hello from machine ${machine}"     
                    def scmVars = checkout scm
                    def commitHash = scmVars.GIT_COMMIT   
                    def project_name = env.JOB_BASE_NAME.trim() 
                    
                    /*------------------------- SYSTEM SPECIFIC SETUP --------------------------
                     * look within the production script for additional system specific setup */
    
                    def command = ""
                    def unuse_path = ""
                    def arch_list = ""
                    switch (machine) {
                        case 'daint':
                            command = "srun -u --constraint=ARCH --job-name=${project_name} --time=24:00:00"
                            unuse_path = "$APPS/UES/jenkins/6.0.UP02/ARCH/easybuild/modules/all"
                            arch_list = getMachineConfiguration(pullRequestMessage, machine).toString() 
                            break
                        case 'dom':
                            command = "srun -u --constraint=ARCH --job-name=${project_name} --time=24:00:00"
                            unuse_path = "$APPS/UES/jenkins/6.0.UP04/ARCH/easybuild/modules/all"
                            arch_list = getMachineConfiguration(pullRequestMessage, machine).toString() 
                            break
                        case 'kesch':
                            unuse_path = "$APPS/UES/RH7.3_PE17.02/modules/all/"
                            break
                        case 'leone':
                            unuse_path = "$APPS/UES/PrgEnv-gnu-2016b"
                            break
                        case 'monch':
                            unuse_path = "$APPS/UES/jenkins/RH6.9-17.06/easybuild/modules/all/"
                            break
                        default:
                            break
                    }
    
                    withEnv(["GIT_COMMIT=${commitHash[0..6]}",
                             "system=${machine}",
                             "command=${command}",
                             "unuse_path=${unuse_path}",
                             "arch_list=${arch_list}",
                             "project_name=${project_name}"]) {

                        sh '''#!/bin/bash -l
                              PREFIX="$SCRATCH/${project_name}"
                              EASYBUILD_TMPDIR=${PREFIX}/tmp
                              EASYBUILD_SOURCE_PATH=${PREFIX}/sources 
                              status=0
    
                              if [ -d $PREFIX ]; then
                                  rm -rf $PREFIX/*
                              else 
                                  mkdir $PREFIX
                              fi
    
                              offlist="a/Amber c/CPMD n/NAMD n/NCL u/UDUNITS v/VASP v/Visit"
                              pushd $HOME
                              for item in ${offlist}; do 
                                  cp --parents -r sources/$item $PREFIX
                              done
                         
                              pwd

                              # --- BUILD ---
                              if [[ "$system" =~ "daint" || "$system" =~ "dom" ]]; then
                                  for ARCH in ${arch_list}; do
                                      linkname="${system}-${ARCH}"
                                      ${command/ARCH/$ARCH} $PWD/jenkins-builds/production.sh --arch=$ARCH --list=$PWD/jenkins-builds/${linkname} --prefix=${PREFIX}/${ARCH} --unuse=${unuse_path/ARCH/$ARCH} --xalt=no
                                      status=$[status+$?]
                                      echo $linkname
                                  done
                              else
                                  linkname=${system}
                                  $command $PWD/jenkins-builds/production.sh --list=$PWD/rjenkins-builds/${linkname} --prefix=$PREFIX --unuse=${unuse_path}
                                  status=$[status+$?]
                                  echo $linkname
                              fi 
                              exit ${status}
                        '''
                    }
                }
            }
        }   
        else {
            println "Machine ${machine} was not added to stage"
        }
    }
    parallel builds
}
