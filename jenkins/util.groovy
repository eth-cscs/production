/**
* Extracts the machine configurations from the given message.
* If no architectures are specified, the method returns an array
* containing only an empty string. In case no valid configurations
* are found the method returns the given array of architectures. 
*
* @param message The message.
* @param machine The name of the machine.
* @param archs A String array of the valid machine architectures.
* @return An array of Strings with the valid configurations. 
*/
String[] getMachineConfiguration(String message, String machine, String[] archs) {
    if (archs.size() == 0)
        return ['']
    def validArchs = []
    for (architecture in archs) {
        def machineWithArch = "\\[.*${machine}-${architecture}.*\\]"
        if (message ==~ machineWithArch)
            validArchs.add(architecture) 
    }
    return validArchs.empty ? archs : validArchs
}

/**
* Checks if as message contains a given machine.
*
* @param message The actual message.
* @param machine The machine.
* @return A boolean indicating whether there is a match.
*/
boolean machineCheck(String message, String machine) {
    def machinePattern = "\\[.*${machine}.*\\]"
    return message ==~ machinePattern? true : false 
}

/**
* Checks if the given message contains the WIP abbreviation.
*
* @param message The actual message.
* @return A boolean indicating if WIP is found.
*/
boolean checkWorkInProgress(String message) {
    if (message ==~ /.*WIP.*/) {
        return true
    }
    
    return false
}

/**
* Checks if the filename is valid for any of the given toolkits.
* 
* @param toolkits An array of Strings containing the toolkit name-version.
* @param filename The name of the file for the check.
* return A boolean indicating whether the given filename corresponds
* to a valid toolkit.
*/
boolean checkToolkits(String[] toolkits, String filename) {
    for (kit in toolkits) {
        if (filename ==~ "\\S+$kit\\S+")
            return true
    }
    return false
}
return this
