# Importando outras bibliotecas do Python
from Oldcaller import caller

# Credenciais para acessar o Anaplan
model = "PLANNING DEV"
user = "paolo.malafaia@flexthink.com.au"
pwd = "Number28"
folder = "D:/Planning-LOC/PYTHON/Dados/"

# DEFINIR RELACAO IMPORT/ARQUIVOS EM PARES PARA EXECUTAR A MAIN EM LOOP
importList = {"I_List_CST_Maquinas": folder+"MAQUINAS.CSV","I_Dados_MAP.032.CST_Maquinas": folder+"MAQUINAS.CSV"}

# Lista de Processes a serem executados com nome assim como na tab de actions do Anaplan
processName = []
# "Testing Process 2"]

# funcao para Import de arquivo


def importSequence(conn, importName, fileLocation):
    with open(fileLocation, "rt") as f:
        data_content = f.read()
    f.close()
    # execucao do subprocesso de import
    anaplanImport = anaplan().executeImport(conn, importName, data_content)
#    print("999 - Import Complete")

# funcao para execucao de processo
def processSequence(conn, processName):
    # execucao do subprocesso de import
    anaplanImport = anaplan().executeProcess(conn, processName)
#    print("999 - Process Complete")


def main():
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


