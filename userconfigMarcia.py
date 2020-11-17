# Importando outras bibliotecas do Python
import executionControl

# Credenciais para acessar o Anaplan
model = "PLANNING DEV"
user = "paolo.malafaia@flexthink.com.au"
pwd = "Number28"

# Configuracoes de arquivos, imports e processes
folder = "D:/Planning-LOC/PYTHON/Dados/"

####### DEFINICAO DE IMPORT #######
# importlist = dicionario com nome do import + arquivo base
#importList = {"Asset Price from quotes.csv": folder+"quotes.csv"}
#importList = {"Asset Price from quotes.csv": None}
importList = {"I_List_CST_Maquinas":folder+"MAQUINAS.CSV","I_Dados_MAP.032.CST_Maquinas":None}
importList =
[
["I_Dados_STG.700.Carga Mg de Mkt PIS Embutido", folder+"mm.txt", [{"Line Item":"Valor Actual"}]],
["I_Dados_STG.700.Carga Mg de Mkt PIS Zero",None, [{"Line Item":"Valor Actual"}]],
["I_Dados_REC.200.Margem de Mercado - Real Base",None, [{"Line Item":"Valor Actual"}]],
["I_Dados_REC.200.Margem de Mercado - Real PIS/Cofins",None, [{"Line Item":"Valor Actual"}]]
    ]

####### DEFINICAO DE IMPORT #######

####### DEFINICAO DE PROCESSOS #######
# processlist = lista de processos
#processName = {"Testing Process":[{"Version":"Actual","Period":"Aug 20"}]}
#processName = {"Testing Process 2":None}
####### DEFINICAO DE PROCESSOS #######
processName = {}

# Execucao do script
def main():
    try:
        # execucao caller
        exec= executionControl.main(user, pwd, model, importList, processName)
    except:
        print("998 - An exception occurred.")



if __name__ == '__main__':
    main()


