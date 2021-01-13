import base64
import requests
from requests.exceptions import HTTPError
import json
import sendemail
from anaplanConnection import AnaplanConnection

#===============================================================================
# Defining global variables
#===============================================================================

urlAuth = "https://auth.anaplan.com/token/authenticate"
urlStem = "https://api.anaplan.com/2/0"
__base_url__ = "https://api.anaplan.com/2/0/workspaces"
__post_body__ = {
            "localeName":"en_US"
        }

class anaplanImport(object):

    @classmethod
    def connectToAnaplanModel(cls, email, password, modelName):
        # Get the token
        print("CONN01 - Anaplan Connection starting")
        tokenValue = cls.getTokenBasicAuth(email, password)
        print("CONN02 - Anaplan Token Value Retrieved")
        # Get the list of models and choose one
        print ("CONN03 - Getting Ws and Model IDs")
        modelInfos = cls.getWsModelIds(tokenValue, modelName)
        modelId = modelInfos[0]
        workspaceId = modelInfos[1]
        print("CONN04 - Workspace and Model ID Retrieved")
        conn = AnaplanConnection(tokenValue, workspaceId, modelId)
        return conn

    @classmethod
    def sendFile(cls, conn, datasourceName, contentToSend, **params):
        tokenValue = conn.authorization
        workspaceId = conn.workspaceGuid
        modelId = conn.modelGuid
        # Get the list of imports and choose one with the importId and the datasourceId
        print ('DATA001 - %s - Retrieving the list of imports' %(datasourceName))
        datasourceId = cls.getDatasourceInfo(tokenValue, workspaceId, modelId, datasourceName)
        print ("DATA002 - %s - Import and Datasource ID retrieved" %(datasourceName))
        # Send the data to Anaplan to update datasource
        print("DATA003 - %s - Evaluating data to send to Anaplan" %(datasourceName))
        if (contentToSend != None):
            sendData = cls.sendData(tokenValue, workspaceId, modelId, datasourceId, 1, contentToSend)
            print("DATA004 - %s - Data Sent" %(datasourceName))
        else:
            print("DATA004 - %s - No Data to send" %(datasourceName))

    @classmethod
    def executeImport(cls, conn, importFile, **params):
        tokenValue = conn.authorization
        workspaceId = conn.workspaceGuid
        modelId = conn.modelGuid
        # Get the list of imports and choose one with the importId and the datasourceId
        print ('IMPORT001 - %s - Retrieving the list of imports' %(importFile))
        importInfos = cls.getImportInfo(tokenValue, workspaceId, modelId, importFile)
        print ("IMPORT002 - %s - Import ID retrieved" %(importFile))
        importId = importInfos[0]
        # # Trigger the import
        print("IMPORT005 - %s - Executing the Import" %(importFile))
        executeImport = cls.importTrigger(tokenValue, workspaceId, modelId, importId, **params)
        print("IMPORT006 - %s - Import Triggered" %(importFile))
        # # Get the status of the import
        print("IMPORT007 - %s - Checking status of import" %(importFile))
        url = urlStem + "/workspaces/" + workspaceId + "/models/" + modelId + "/imports/" + importId + "/tasks"
        post_header = {'Authorization': 'AnaplanAuthToken %s' % tokenValue, 'Content-Type': 'application/json'}
        checkStatusImport = check_status(url, executeImport,post_header)
        print("IMPORT008 - %s - Status Retrieved" %(importFile))
        emailSubject = "Anaplan Execution - " + importFile
        emailText = checkStatusImport
        sendemail.sendEmail(emailSubject,emailText)

    @classmethod
    def executeProcess(cls, conn, processName, **params):
        tokenValue = conn.authorization
        workspaceId = conn.workspaceGuid
        modelId = conn.modelGuid
        # Get the list of imports and choose one with the importId and the datasourceId
        print("PROC001 - %s - Retrieving the list of imports" %(processName))
        processInfos = cls.getProcessInfo(tokenValue, workspaceId, modelId, processName)
        processId = processInfos
        print("PROC002 - %s - Import ID retrieved. See below:" %(processName))
        # # Trigger the import
        print("PROC003 - %s - Executing the Process" %(processName))
        print(params)
        executeImport = cls.execute_action_with_parameters(conn, processId, 3, **params)
        print("PROC004 - %s - Process Executed" %(processName))
        # # Get the status of the import
        emailSubject = "Anaplan Execution - " + processName
        emailText = executeImport
        sendemail.sendEmail(emailSubject, emailText)

    @classmethod
    def getTokenBasicAuth(cls, email, password):
        # Get the token
        cred64 = convertbase64(email + ":" + password)
        headers = {'Authorization': 'Basic %s' % cred64}
        rawResponse = requests.post(
            urlAuth,
            headers=headers
        )
        jsonResponse = json.loads(rawResponse.content)
        tokenValue = jsonResponse["tokenInfo"]["tokenValue"]
        return tokenValue

    @classmethod
    def getWsModelIds(cls, token, modelName):
        # Get the list of models and choose one with the model id and the workspaceId
        headers = {'Authorization': 'AnaplanAuthToken %s' % token}
        response = requests.get(
            urlStem + "/models",
            headers=headers
        )
        jsonResponse = json.loads(response.content)
        modelsArray = jsonResponse["models"]
        modelInfo = [model for model in modelsArray if model['name'] == modelName]
        modelId = modelInfo[0]["id"]
        wsId = modelInfo[0]["currentWorkspaceId"]
        return modelId, wsId

    @classmethod
    def getImportInfo(cls, token, wsId, modelId, importName):
        # Get the list of imports and choose one with the importId and the datasourceId
        headers = {'Authorization': 'AnaplanAuthToken %s' % token, 'Content-Type': 'application/json'}
        response = requests.get(
            urlStem + "/workspaces/" + wsId + "/models/" + modelId + "/imports",
            headers=headers
        )
        jsonResponse = json.loads(response.content)
        importsArray = jsonResponse["imports"]
        importsInfo = [importInfo for importInfo in importsArray if importInfo['name'] == importName]
        importId = importsInfo[0]["id"]
        datasourceId = importsInfo[0]["importDataSourceId"]
        return importId, datasourceId

    @classmethod
    def getDatasourceInfo(cls, token, wsId, modelId, dataSourceName):
        # Get the list of imports and choose one with the importId and the datasourceId
        headers = {'Authorization': 'AnaplanAuthToken %s' % token, 'Content-Type': 'application/json'}
        response = requests.get(
            urlStem + "/workspaces/" + wsId + "/models/" + modelId + "/files",
            headers=headers
        )
        jsonResponse = json.loads(response.content)
        filesArray = jsonResponse["files"]
        importsInfo = [importInfo for importInfo in filesArray if importInfo['name'] == dataSourceName]
        datasourceId = importsInfo[0]["id"]
        return datasourceId

    @classmethod
    def getProcessInfo(cls, token, wsId, modelId, processName):
        # Get the list of processes and choose one with the processId
        headers = {'Authorization': 'AnaplanAuthToken %s' % token, 'Content-Type': 'application/json'}
        response = requests.get(
            urlStem + "/workspaces/" + wsId + "/models/" + modelId + "/processes",
            headers=headers
        )

        jsonResponse = json.loads(response.content)
        processesArray = jsonResponse["processes"]
        processesInfo = [processInfo for processInfo in processesArray if processInfo['name'] == processName]
        processId = processesInfo[0]["id"]

        return processId

    @classmethod
    def sendData(cls, token, wsId, modelId, fileId, chunkCount, content):
        # Send the data to Anaplan to update datasource
        ## First, tell Anaplan API's server it will receive one chunk
        print("009.1 - Telling Anaplan it will receive one chunk")
        headers = {'Authorization': 'AnaplanAuthToken %s' % token, 'Content-Type': 'application/json'}
        data = json.dumps({'id': fileId, "chunkCount": chunkCount})
        response = requests.post(
            urlStem + "/workspaces/" + wsId + "/models/" + modelId + "/files/" + fileId,
            headers=headers,
            data=data
        )
        print("009.2 - Told Anaplan it will receive one chunk")
        ## Now let's send the file
        headers2 = {'Authorization': 'AnaplanAuthToken %s' % token, 'Content-Type': 'application/octet-stream'}
        print("009.3 - Put command starting")
        response2 = requests.put(
            urlStem + "/workspaces/" + wsId + "/models/" + modelId + "/files/" + fileId + "/chunks/" + str(
            chunkCount - 1)
            ,
            headers=headers2,
            data=content
        )
        print("009.4 - Put command finished")
        status_code = response2.status_code
        return status_code

    @classmethod
    def importTrigger(cls, token, wsId, modelId, importId, **params):
        # adding post body/parameters:
        post_body = {'localeName': 'en_US'}

        if len(params) == 0:
            pass
        elif len(params) > 1:
            paramsbody = []
            for key, value in params.items():
                paramstemp = {'entityType': key, 'entityName': value}
                paramsbody.append(paramstemp)
            post_body['mappingParameters'] = paramsbody
        else:
            for key, value in params.items():
                #            body += "{\"entityType\":\"" + key + "\"" + ","+ "\"entityName\":\"" + value + "\"}"
                paramsbody = [{'entityType': key, 'entityName': value}]
            post_body['mappingParameters'] = paramsbody


        # Finally we trigger the import
        headers = {'Authorization': 'AnaplanAuthToken %s' % token, 'Content-Type': 'application/json'}
        data = json.dumps(post_body)
        response = requests.post(
            urlStem + "/workspaces/" + wsId + "/models/" + modelId + "/imports/" + importId + "/tasks/",
            headers=headers,
            data=data
        )
        # Get the taskId
        jsonResponse = json.loads(response.content)
        taskId = jsonResponse["task"]["taskId"]
        return taskId

    @classmethod
    def execute_action_with_parameters(cls, conn, actionId, retryCount, **params):
        '''
        :param conn: AnaplanConnection object which contains authorization string, workspace ID, and model ID
        :param actionId: ID of the action in the Anaplan model
        :param retryCount: The number of times to attempt to retry the action if it fails
        '''
        # ===========================================================================
        # This function reads the ID of the desired import or process to run with
        # mapping parameters declared, POSTs the task to the Anaplan API to execute
        # the action, then monitors the status until complete.
        # ===========================================================================
        authorization = conn.authorization
        workspaceGuid = conn.workspaceGuid
        modelGuid = conn.modelGuid

        post_header = {'Authorization': 'AnaplanAuthToken %s' % authorization, 'Content-Type': 'application/json'}
        post_body = {'localeName': 'en_US'}

        if len(params) == 0:
            pass
        elif len(params) > 1:
            paramsbody = []
            for key, value in params.items():
                paramstemp = {'entityType': key, 'entityName': value}
                paramsbody.append(paramstemp)
            post_body['mappingParameters'] = paramsbody
        else:
            for key, value in params.items():
                #            body += "{\"entityType\":\"" + key + "\"" + ","+ "\"entityName\":\"" + value + "\"}"
                paramsbody = [{'entityType': key, 'entityName': value}]
            post_body['mappingParameters'] = paramsbody

        if actionId[:3] == "112":
            print("Running action " + actionId)
            url = __base_url__ + "/" + workspaceGuid + "/models/" + modelGuid + "/imports/" + actionId + "/tasks"
            taskId = cls.run_action_with_parameters(url, post_header, retryCount, post_body)
            return check_status(url, taskId, post_header)
        elif actionId[:3] == "118":
            print("Running action " + actionId)
            url = __base_url__ + "/" + workspaceGuid + "/models/" + modelGuid + "/processes/" + actionId + "/tasks"
            taskId = cls.run_action_with_parameters(url, post_header, retryCount, post_body)
            # taskId = run_action(url, post_header, retryCount)
            return check_status(url, taskId, post_header)
        else:
            print("Incorrect action ID provided! Only imports and processes may be executed with parameters.")

    @classmethod
    def run_action_with_parameters(cls,url, post_header, retryCount, post_body):
        '''
        @param url: POST URL for Anaplan action
        @param post_header: Authorization header string
        @param retryCount: Number of times to retry executino of the action
        '''
        # ===========================================================================
        # This function executes the Anaplan import or process with mapping parameters,
        # if there is a server error it will wait, and retry a number of times
        # defined by the user. Once the task is successfully created, the task ID is returned.
        # ===========================================================================
        state = 0
        sleepTime = 10
        while True:
            try:
                run_action = requests.post(url, headers=post_header, json=post_body)
                run_action.raise_for_status()
            except HTTPError as e:
                raise HTTPError(e)
            if run_action.status_code != 200 and state < retryCount:
                sleep(sleepTime)
                try:
                    run_action = requests.post(url, headers=post_header, json=post_body)
                    run_action.raise_for_status()
                except HTTPError as e:
                    raise HTTPError(e)
                state += 1
                sleepTime = sleepTime * 1.5
            else:
                break
        taskId = json.loads(run_action.text)
        taskId = taskId["task"]
        return taskId["taskId"]

def parse_task_response(results, url, taskId, post_header):
    '''
    :param results: JSON dump of the results of an Anaplan action
    '''
    # ===========================================================================
    # This function reads the JSON results of the completed Anaplan task and returns
    # the job details.
    # ===========================================================================
    job_status = results["currentStep"]
    failure_alert = str(results["result"]["failureDumpAvailable"])

    if job_status == "Failed.":
        error_message = str(results["result"]["details"][0]["localMessageText"])
        print("The task has failed to run due to an error: " + error_message)
        return "The task has failed to run due to an error: " + error_message
    else:
        if failure_alert == "True":
            try:
                dump = requests.get(url + "/" + taskId + '/' + "dump", headers=post_header)
                dump.raise_for_status()
            except HTTPError as e:
                raise HTTPError(e)
            dump = dump.text
        success_report = str(results["result"]["successful"])
        if 'details' not in results["result"]:
            anaplan_process_dump = ""
            error_detail = ""
            load_detail = ""
            failure_details = ""
            for nestedResults in results["result"]["nestedResults"]:
                process_subfailure = str(nestedResults["failureDumpAvailable"])
                object_id = str(nestedResults["objectId"])
                load_detail = load_detail + "Process action " + object_id + " completed. Failure: " + process_subfailure + '\n'
                if process_subfailure == "True":
                    local_message = str(nestedResults["details"][0]["localMessageText"])
                    details = nestedResults["details"][0]["values"]
                    for i in details:
                        error_detail = error_detail + i + '\n'
                    try:
                        dump = requests.get(url + "/" + taskId + '/' + "dumps" + '/' + object_id, headers=post_header)
                        dump.raise_for_status()
                    except HTTPError as e:
                        raise HTTPError(e)
                    report = "Error dump for " + object_id + '\n' + dump.text
                    anaplan_process_dump += report
                    failure_details = failure_details + local_message
            if anaplan_process_dump != "":
                # print("The requested job is " + job_status)
                return load_detail + '\n' + "Details:" + '\n' + error_detail + '\n' + "Failure dump(s):" + '\n' + anaplan_process_dump
            else:
                # print("The requested job is " + job_status)
                return load_detail
        else:
            if "details" in results["result"]:
                if str(results["result"]["details"][0]["type"]) == "exportSucceeded":
                    size = results["result"]["details"][0]["values"][1]
                    name = results["result"]["details"][0]["values"][5]
                    return "Export complete! Files size: " + str(size) + " bytes. File name: " + str(name)
                else:
                    load = str(results["result"]["details"][0]["localMessageText"])
                    load_detail = ""
                    for i in results["result"]["details"][0]["values"]:
                        load_detail = load_detail + i + '\n'
                    if failure_alert == "True":
                        # print("The requested job is " + job_status)
                        return "Failure Dump Available: " + failure_alert + ", Successful: " + success_report + '\n' + "Load details:" + '\n' + load + '\n' + load_detail + '\n' + "Failure dump:" + '\n' + dump
                    else:
                        # print("The requested job is " + job_status)
                        return "Failure Dump Available: " + failure_alert + ", Successful: " + success_report + '\n' + "Load details:" + '\n' + load + '\n' + load_detail

def check_status(url, taskId, post_header):
    '''
    @param url: Anaplan task URL
    @param taskId: ID of the Anaplan task executed
    @param post_header: Authorization header value
    '''
    # ===========================================================================
    # This function monitors the status of Anaplan action. Once complete it returns
    # the JSON text of the response.
    # ===========================================================================
    while True:
        try:
            get_status = requests.get(url + "/" + taskId, headers=post_header)
            get_status.raise_for_status()
        except HTTPError as e:
            raise HTTPError(e)
        status = json.loads(get_status.text)
        status = status["task"]["taskState"]
        if status == "COMPLETE":
            results = json.loads(get_status.text)
            results = results["task"]
            break

    return parse_task_response(results, url, taskId, post_header)

def convertbase64(connectString):
    cred64 = base64.b64encode(bytes(connectString, 'UTF-8')).decode('utf-8')
    return cred64

