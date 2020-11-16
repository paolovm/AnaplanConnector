# Importando outras bibliotecas do Python
from child import anaplanImport as anaplan



def singleFileImport(conn, importName, fileLocation):
    data_content=None
    if (fileLocation != None):
        with open(fileLocation, "rt") as f:
            data_content = f.read()
        f.close()
        # execucao do subprocesso de import
    anaplanImport = anaplan().executeImport(conn, importName, data_content)
#    print("999 - Import Complete")




# funcao para execucao de processo
def singleProcessExecution(conn, processName):
    # execucao do subprocesso de import
    anaplanImport = anaplan().executeProcess(conn, processName)
#    print("999 - Process Complete")




def main(user, pwd, model, importList, processName):
    print("running main"+user+pwd+model)
    try:
        # conectar ao Anaplan
        conn= anaplan().connectToAnaplanModel(user, pwd, model)
        # execucao de imports
        for importAction, importFile in importList.items():
            singleFileImport(conn, importAction, importFile)
        # execucao de processes
        for each_process in processName:
            singleProcessExecution(conn, each_process)
    except:
        print("998 - An exception occurred.")



if __name__ == '__main__':
    main()


