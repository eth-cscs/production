String[] getMachineConfiguration(String message, String machine, String[] archs) {
    if (archs.size() == 0)
        return ['']
    def validArchs = []
    for (architecture in archs) {
        def machineWithArch = ".*${machine}-${architecture}.*"
        if (message ==~ machineWithArch)
            validArchs.add(architecture) 
    }
    return validArchs.empty ? archs : validArchs
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

return this
