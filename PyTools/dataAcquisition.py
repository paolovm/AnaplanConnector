# Importando outras bibliotecas do Python
from anaplanTools import anaplanImport as anaplan



def singleFileImport(conn, importName, fileLocation, **params):
    print("execution control 7")
    data_content=None
    if (fileLocation != None):
        with open(fileLocation, "rt",encoding="latin-1") as f:
            data_content = f.read()
        f.close()
        # execucao do subprocesso de import
    anaplanImport = anaplan().executeImport(conn, importName, data_content, **params)
#    print("999 - Import Complete")




# funcao para execucao de processo
def singleProcessExecution(conn, processName, **params):
    # execucao do subprocesso de import.
    anaplanImport = anaplan().executeProcess(conn, processName, **params)
#    print("999 - Process Complete")




def main(user, pwd, model, importList, processList):
    # conectar ao Anaplan
    conn= anaplan().connectToAnaplanModel(user, pwd, model)
    # execucao de imports
    for eachImport in importList:
        importAction=eachImport[0]
        importFile = eachImport[1]
        importParams = eachImport[2]
        singleFileImport(conn, importAction, importFile , **importParams)
    # execucao de processes
    for eachprocess in processList:
        processAction = eachprocess[0]
        processParams = eachprocess[1]
        singleProcessExecution(conn, processAction, **processParams)



