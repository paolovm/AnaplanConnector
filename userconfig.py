# Importando outras bibliotecas do Python
import executionControl

# Credenciais para acessar o Anaplan
model = "Planning"
user = "paolovm3@yahoo.com.br"
pwd = "Number28"

# Configuracoes de arquivos, imports e processes
folder = "Dados/"

####### DEFINICAO DE IMPORT #######
# importlist = dicionario com nome do import + arquivo base
#importList = {"Asset Price from quotes.csv": folder+"quotes.csv"}
#importList = {"Asset Price from quotes.csv": None}
importList = {}
####### DEFINICAO DE IMPORT #######


####### DEFINICAO DE PROCESSOS #######
# processlist = lista de processos
#processName = {"Testing Process":[{"Version":"Actual","Period":"Aug 20"}]}
processName = {"Testing Process 2":None}
####### DEFINICAO DE PROCESSOS #######


# Execucao do script
def main():
    try:
        # execucao caller
        exec= executionControl.main(user, pwd, model, importList, processName)
    except:
        print("998 - An exception occurred.")



if __name__ == '__main__':
    main()


