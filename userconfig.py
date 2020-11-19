# Importando outras bibliotecas do Python
import dataAcquisition

# Credenciais para acessar o Anaplan
model = "Planning"
user = "paolovm3@yahoo.com.br"
pwd = "Number28"

# Configuracoes de arquivos, imports e processes
folder = "Dados/"

####### DEFINICAO DE IMPORT #######
# importlist = cada import eh uma lista com IMPORT NAME , ARQUIVO , PARAMETROS
# importList =\
#     [
#     ["I_Dados_STG.700.Carga Mg de Mkt PIS Embutido", folder+"mm.txt", [{"Line Item":"Valor Actual"}]],
#     ["I_Dados_STG.700.Carga Mg de Mkt PIS Zero",None, [{"Line Item":"Valor Actual"}]],
#     ["I_Dados_REC.200.Margem de Mercado - Real Base",None, [{"Line Item":"Valor Actual"}]],
#     ["I_Dados_REC.200.Margem de Mercado - Real PIS/Cofins",None, [{"Line Item":"Valor Actual"}]]
#     ]

# importList =\
# [
# ["Asset Price from quotes.csv", folder+"quotes.csv", None],
# ["Asset Price from quotes.csv", folder+"quotes.csv", None]
# ]
importList=[]
####### DEFINICAO DE IMPORT #######


####### DEFINICAO DE PROCESSOS #######
# processlist = lista de processos
processName =\
[
["Testing Process 2",{"Version":"Actual","Period":"Aug 20"}]
]
#processName = {"Testing Process 2":None}
####### DEFINICAO DE PROCESSOS #######


# Execucao do script
def main():
    try:
        # execucao caller
        exec= dataAcquisition.main(user, pwd, model, importList, processName)
    except:
        print("998 - An exception occurred.")



if __name__ == '__main__':
    main()


