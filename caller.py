# Importando outras bibliotecas do Python
import base64
import json
import requests
import os
import child
from child import anaplanImport as anaplan

#Credenciais para acessar o Anaplan
model = "Planning"
user = "paolovm3@yahoo.com.br"
pwd = "Number28"


#DEFINIR RELACAO IMPORT/ARQUIVOS EM PARES PARA EXECUTAR A MAIN EM LOOP
# Lista de Imports a serem executados com nome assim como na tab de actions do Anaplan
importName = "Asset Price from quotes.csv"

# Localizacao dos arquivos associados com os imports
fileLocation= "quotes.csv"

# Lista de Processes a serem executados com nome assim como na tab de actions do Anaplan
processName = "Testing Process"

# comentario extra para testar git
#
def main():
    try:
        # leitura do arquivo
        with open(fileLocation, "rt") as f:
                data_content=f.read()
        f.close()
        print("001 - Data Content Retrieved. See below:")
        print("002 - Anaplan Import Script Starting")

        # execucao do subprocesso de import
        anaplanImport = anaplan().executeImport(user, pwd, model, importName, processName, data_content)
        print("999 - Execution Complete")

    except:
        print("998 - An exception occurred.")


if __name__ == '__main__':
    main()
