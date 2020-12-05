# Importando outras bibliotecas do Python
from anaplanTools import anaplanImport as anaplan



def singleFileImport(conn, datasourceName, fileLocation, **params):
    print("execution control 7")
    data_content=None
    if (fileLocation != None):
        with open(fileLocation, "rt",encoding="latin-1") as f:
            data_content = f.read()
        f.close()
        # execucao do subprocesso de import
    anaplanImport = anaplan().sendFile(conn, datasourceName, data_content)
#    print("999 - Import Complete")

# funcao para execucao de imports
def singleImportAction(conn, importName, **params):
    # execucao do subprocesso de import.
    anaplanImport = anaplan().executeImport(conn, importName, **params)


# funcao para execucao de processo
def singleProcessExecution(conn, processName, **params):
    # execucao do subprocesso de import.
    anaplanImport = anaplan().executeProcess(conn, processName, **params)
#    print("999 - Process Complete")




def main(user, pwd, model, dataList, importList, processList):
    # conectar ao Anaplan
    conn= anaplan().connectToAnaplanModel(user, pwd, model)
    # data post
    for eachData in dataList:
        datasourceName = eachData[0]
        fileLocation = eachData[1]
        singleFileImport(conn, datasourceName, fileLocation)
    # execucao de imports
    for eachImport in importList:
        importAction = eachImport[0]
        importParams = eachImport[1]
        singleImportAction(conn, importAction, **importParams)
    # execucao de processes
    for eachprocess in processList:
        processAction = eachprocess[0]
        processParams = eachprocess[1]
        singleProcessExecution(conn, processAction, **processParams)



