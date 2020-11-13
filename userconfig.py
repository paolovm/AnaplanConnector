# Importando outras bibliotecas do Python
import trigger

# Credenciais para acessar o Anaplan
model = "Planning"
user = "paolovm3@yahoo.com.br"
pwd = "Number28"

# Configuracoes de arquivos, imports e processes
# importlist = dicionario com nome do import + arquivo base
# processlist = lista de processos
folder = "Dados/"
importList = {"Asset Price from quotes.csv": folder+"quotes.csv"}
processName = []


# Execucao do script
def main():
    try:
        # execucao caller
        exec= trigger.main(user, pwd, model, importList, processName)
    except:
        print("998 - An exception occurred.")



if __name__ == '__main__':
    main()


