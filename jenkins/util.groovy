/*
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

/*
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

/*
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

/*
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

/*
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

/*
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
   def newIssue = jiraNewIssue issue: issue, site: 'JIRA_SITE', failOnError: false
}

/*
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
   def newIssue = jiraNewIssue issue: ticket, site: 'JIRA_SITE', failOnError: false
}

/*
* Create a Jira Issue with custom message:
* - assignee: list with information of the person in charge, like [name:'lucamar']
* - customfield_10101: Epic link (only for issuetype 'Task')
* - customfield_10103: Epic name (only for issuetype 'Epic')
* 
* @param issuetype Type of Jira issue ('Epic' or 'Task')
* @param machine Computing system where the build took place (machineLabel)
* @param subject Subject of the Jira Issue appended to [${machine}]
* @param message Content of the Jira Issue prepended to Jenkins job details
* @param priority Priority of the issue: Blocker, High, Medium, Low
* @param project Project where the Jira Issue will be created
*/
void createJiraIssue(String issuetype, String machine, String subject, String message, String priority, String project){

   def title = "[${machine}] ${subject}"
   def content = "${message} \nJenkins job ${env.JOB_NAME} [${env.BUILD_NUMBER}] (job result: *${currentBuild.result}*)"
   def ticket = [fields: [ project: [key: project],
                          summary: title,
                          description: content,
                          issuetype: [name:issuetype],
                          priority: [name:priority],
                          components:[[name:'Software Installation']],
                          labels: ['Production','Software']]]
   def newIssue = jiraNewIssue issue: ticket, site: 'JIRA_SITE', failOnError: false
}

/*
* Search a Jira Issue:
* 
* @param subject Subject of the Jira Issue appended to [${machine}]
* @param machine Computing system where the build took place (machineLabel)
* @param pe Target Programming Environment of the build (params.pe_target)
* @param project Project where the Jira Issue has been be created
*/
String[] searchJiraIssue(String subject, String machine, String pe, String project){

   def search = jiraJqlSearch jql: "project = '$project' AND summary ~ '*$subject*' AND summary ~ '*$machine*' AND summary ~ '*$pe*'", fields: ['status'], maxResults: 1, site: 'JIRA_SITE', failOnError: false

   if(search.successful && search.data.issues) {
       //  key and status of the Jira issues matched by the search 
       def key = search.data.issues[0].key
       def status = search.data.issues.fields.status[0].name
       return [key, status]
   } else {
       return null
   }
}

/*
* Add comment to a Jira Issue:
* 
* @param message Comment to the Jira Issue prepended to Jenkins job details
* @param key     Jira Issue key
*/
void commentJiraIssue(String message, String key){

   def content = [body: "${message} \nJenkins job ${env.JOB_NAME} [${env.BUILD_NUMBER}] (job result: *${currentBuild.result}*)"]
   def commentIssue = jiraAddComment idOrKey: key, input: content, site: 'JIRA_SITE', failOnError: false
}
