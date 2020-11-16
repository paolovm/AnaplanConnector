import base64
import requests
from requests.exceptions import HTTPError
import json
import anaplanLib
import sendemail
from AnaplanConnection import AnaplanConnection

urlAuth = "https://auth.anaplan.com/token/authenticate"
urlStem = "https://api.anaplan.com/2/0"
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
    def executeImport(cls, conn, importFile, contentToSend):
        tokenValue = conn.authorization
        workspaceId = conn.workspaceGuid
        modelId = conn.modelGuid
        # Get the list of imports and choose one with the importId and the datasourceId
        print ("IMPORT001 - Retrieving the list of imports")
        importInfos = cls.getImportInfo(tokenValue, workspaceId, modelId, importFile)
        print ("IMPORT002 - Import and Datasource ID retrieved. See below:")
        importId = importInfos[0]
        datasourceId = importInfos[1]
        # Send the data to Anaplan to update datasource
        print("IMPORT003 - Evaluating data to send to Anaplan")
        if (contentToSend != None):
            sendData = cls.sendData(tokenValue, workspaceId, modelId, datasourceId, 1, contentToSend)
            print("IMPORT004 - Data Sent")
        else:
            print("IMPORT004 - No Data to send")
        # # Trigger the import
        print("IMPORT005 - Executing the Import")
        executeImport = cls.importTrigger(tokenValue, workspaceId, modelId, importId)
        print("IMPORT006 - Import Triggered")
        # # Get the status of the import
        print("IMPORT007 - Checking status of import")
        checkStatusImport = cls.check_status(tokenValue, workspaceId, modelId, importId,
                                                  executeImport)
        print("IMPORT008 - Status Retrieved")
        emailSubject = "Anaplan Execution - " + importFile
        emailText = checkStatusImport
        sendemail.sendEmail(emailSubject,emailText)
#        print(checkStatusImport)

    @classmethod
    def executeProcess(cls, conn, processName, **params):
        tokenValue = conn.authorization
        workspaceId = conn.workspaceGuid
        modelId = conn.modelGuid
        # Get the list of imports and choose one with the importId and the datasourceId
        print("PROC001 - Retrieving the list of imports")
        processInfos = cls.getProcessInfo(tokenValue, workspaceId, modelId, processName)
        processId = processInfos
        print("PROC002 - Import ID retrieved. See below:")
        # # Trigger the import
        print("PROC003 - Executing the Process")
        executeImport = anaplanLib.execute_action_with_parameters(conn, processId, 3, **params)
        print("PROC004 - Process Executed")
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
        #print("009.1 - Telling Anaplan it will receive one chunk")
        headers = {'Authorization': 'AnaplanAuthToken %s' % token, 'Content-Type': 'application/json'}
        data = json.dumps({'id': fileId, "chunkCount": chunkCount})
        response = requests.post(
            urlStem + "/workspaces/" + wsId + "/models/" + modelId + "/files/" + fileId,
            headers=headers,
            data=data
        )
        #print("009.2 - Told Anaplan it will receive one chunk")
        ## Now let's send the file
        headers2 = {'Authorization': 'AnaplanAuthToken %s' % token, 'Content-Type': 'application/octet-stream'}
        #print("009.3 - Put command starting")
        response2 = requests.put(
            urlStem + "/workspaces/" + wsId + "/models/" + modelId + "/files/" + fileId + "/chunks/" + str(
            chunkCount - 1)
            ,
            headers=headers2,
            data=content
        )
        #print("009.4 - Put command finished")
        status_code = response2.status_code
        return status_code

    @classmethod
    def importTrigger(cls, token, wsId, modelId, importId):
        # Finally we trigger the import
        headers = {'Authorization': 'AnaplanAuthToken %s' % token, 'Content-Type': 'application/json'}
        data = json.dumps({'localeName': "en_US"})
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
    def check_status(cls, token, wsId, modelId, importId, taskId):
        # ===========================================================================
        # This function monitors the status of Anaplan action. Once complete it returns
        # the JSON text of the response.
        # ===========================================================================
        post_header = {'Authorization': 'AnaplanAuthToken %s' % token, 'Content-Type': 'application/json'}
        while True:
            try:
                headers = {'Authorization': 'AnaplanAuthToken %s' % token, 'Content-Type': 'application/json'}
                get_status = requests.get(
                    urlStem + "/workspaces/" + wsId + "/models/" + modelId + "/imports/" + importId + "/tasks/" + taskId,
                    headers=headers)
                get_status.raise_for_status()
            except HTTPError as e:
                raise HTTPError(e)
            status = json.loads(get_status.text)
            status = status["task"]["taskState"]
            if status == "COMPLETE":
                results = json.loads(get_status.text)
                results = results["task"]
                break
        return parse_task_response(results, token, wsId, modelId, importId, taskId, post_header)

def parse_task_response(results, token, wsId, modelId, importId, taskId, post_header):
    #===========================================================================
    # This function reads the JSON results of the completed Anaplan task and returns
    # the job details.
    #===========================================================================
    '''
    :param results: JSON dump of the results of an Anaplan action
    '''
    job_status = results["currentStep"]
#    print(job_status)
    failure_alert = str(results["result"]["failureDumpAvailable"])
    if job_status == "Failed.":
        error_message = str(results["result"]["details"][0]["localMessageText"])
#        print("The task has failed to run due to an error: " + error_message)
        return "The task has failed to run due to an error: " + error_message
    else:
        if failure_alert == "True":
            try:
                dump = requests.get(urlStem + "/workspaces/" + wsId + "/models/" + modelId + "/imports/" + importId + "/tasks/" + taskId + '/' + "dump", headers=post_header)
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
                            dump = requests.get(urlStem + "/workspaces/" + wsId + "/models/" + modelId + "/imports/" + importId + "/tasks/" + taskId + '/' + "dumps" + '/' + object_id,  headers=post_header)
                            dump.raise_for_status()
                        except HTTPError as e:
                            raise HTTPError(e)
                        report = "Error dump for " + object_id + '\n' + dump.text
                        anaplan_process_dump += report
                        failure_details = failure_details + local_message
            if anaplan_process_dump != "":
#                print("The requested job is " + job_status)
                return load_detail + '\n' + "Details:" + '\n' + error_detail + '\n' + "Failure dump(s):" + '\n' + anaplan_process_dump
            else:
#                print("The requested job is " + job_status)
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
#                        print("The requested job is " + job_status)
                        return "Failure Dump Available: " + failure_alert + ", Successful: " + success_report + '\n' + "Load details:" + '\n' + load + '\n' + load_detail + '\n' + "Failure dump:" + '\n' + dump
                    else:
#                        print("The requested job is " + job_status)
                        return "Failure Dump Available: " + failure_alert + ", Successful: " + success_report + '\n' + "Load details:" + '\n' + load + '\n' + load_detail

def convertbase64(connectString):
    cred64 = base64.b64encode(bytes(connectString, 'UTF-8')).decode('utf-8')
    return cred64

