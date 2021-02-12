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
    def patternStart = /.*\[.*/
    def patternEnd = /.*\].*/
    for (architecture in archs) {
        def machineWithArch = "$patternStart$machine-$architecture$patternEnd"
        if (message ==~ machineWithArch)
            validArchs.add(architecture)
    }
    return validArchs.isEmpty() ? archs : validArchs
}

/**
* Checks if as message contains a given machine.
*
* @param message The actual message.
* @param machine The machine.
* @return A boolean indicating whether there is a match.
*/
boolean machineCheck(String message, String machine) {
    def patternStart = /.*\[.*(\b/
    def patternEnd = /(-\S+)?\b).*\].*/
    def machinePattern = "$patternStart$machine$patternEnd"
    return message ==~ machinePattern
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

/**
* Notifies Slack about the result of the current build.
*/
void notifySlackFinish() {
   def resultColor
   if (currentBuild.result == "SUCCESS")
       resultColor = '#239B56'
   else
       resultColor = '#E74C3C'

   slackSend(color: resultColor,
             message: "Job ${env.JOB_NAME} [${env.BUILD_NUMBER}] finished with result: *${currentBuild.result}* (<${env.BUILD_URL}|Open>)")
}

/**
* Create a Jira task for an EasyBuild recipe that failed to build:
*
* @param projkey Jira project key (only project members can create issues)
* @param recipe EasyBuild recipe that failed to build
* @param machine Computing system where the recipe failed to build (machineLabel)
*/
void failedJiraTask(String projkey, String recipe, String machine) {

   def title = "${recipe} failed on ${machine}"
   def content = "EasyBuild recipe ${recipe} failed to build on ${machine} in Jenkins job ${env.JOB_NAME} [${env.BUILD_NUMBER}] (job result: *${currentBuild.result}*)"
   def issue = [fields: [ project: [key: projkey ],
                          summary: title,
                          description: content,
                          issuetype: [name: 'Task']]]
   def newIssue = jiraNewIssue issue: issue, site: 'JIRA_SITE'
}

/**
* Create a Jira Service Desk ticket with custom message:
* - issuetype: 'Service Request' or 'Incident'
* - customfield_11102 (Service): 'Atlassian', 'Compute at Piz Daint', 'JFrog', 'JupyterHub' or 'KeyCloak'
* - customfield_11103 (System): 'Alps', 'Dom', 'Piz Daint', 'Tsa' or other services of the JIRA_SITE
* - assignee: list with information of the person in charge, like [name:'lucamar']
* - customfield_10401 (Watchers): list with information of watchers, like [[name:'bignamic'], [name:'manitart']]
* 
* @param subject Subject of the Jira Service Desk ticket appended to [${machine}]
* @param machine Computing system where the build took place (machineLabel)
* @param message Content of the Jira Service Desk ticket prepended to Jenkins job details
* @param priority Priority of the ticket: Blocker, High, Medium, Low
* @param queue Queue where the Jira Service Desk ticket will be dispatched
*/
void createJiraSD(String subject, String machine, String message, String priority, String queue){

   def system
   def systems = [
       [name:'Alps', label:'eiger'],
       [name:'Dom', label:'dom'],
       [name:'Piz Daint', label:'daint'], 
       [name:'Tsa', label:'tsa']
   ]
   systems.each { item ->
       if(machine.contains(item.label)) system = item.name
   }

   def title = "[${machine}] ${subject}"
   def content = "${message} \nJenkins job ${env.JOB_NAME} [${env.BUILD_NUMBER}] (job result: *${currentBuild.result}*)"
   def ticket = [fields: [ project: [key:'SD'],
                          summary: title,
                          description: content,
                          issuetype: [name:'Incident'],
                          priority: [name:priority],
                          customfield_10802: [value:queue],
                          customfield_11102: 'Compute at Piz Daint',
                          customfield_11103: system]]
   def newIssue = jiraNewIssue issue: ticket, site: 'JIRA_SITE'
}
