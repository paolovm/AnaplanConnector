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
#importList = {"I_List_CST_Maquinas":folder+"MAQUINAS.CSV","I_Dados_MAP.032.CST_Maquinas":None}
#importList =\
# [
# ["I_List_CCF4_UN_SKU", folder+"UNxSKU.txt", None],
# ["I_Dados_MAP.025.UNxSKU", None, None],
# ["I_Dados_STG.700.Carga Mg de Mkt PIS Embutido", folder+"mm.txt", [{"Line Item":"Valor Actual"}]],
# ["I_Dados_STG.700.Carga Mg de Mkt PIS Zero",None, [{"Line Item":"Valor Actual"}]],
# ["I_Dados_REC.200.Margem de Mercado - Real Base",None, [{"Line Item":"Valor Actual"}]],
# ["I_Dados_REC.200.Margem de Mercado - Real PIS/Cofins",None, [{"Line Item":"Valor Actual"}]],
# ["I_Dados_STG.001.Carga OPEX arquivo",folder+"OPEX.csv", [{"Line Item":"Valor Realizado Pós Rateio"}]],
# ["I_Dados_EBT.100.EBITDA - Real",None, [{"Line Item":"Valor Realizado Pós Rateio"}]]
#     ]
importList =\
[["I_Dados_STG.700.Carga Mg de Mkt PIS Embutido", folder+"mm.txt", {"Line Item":"Valor Actual"}],
["I_Dados_STG.700.Carga Mg de Mkt PIS Zero",folder+"mm.txt", {"Line Item":"Valor Actual"}],
["I_Dados_REC.200.Margem de Mercado - Real Base",None, {"Line Item":"Valor Actual"}],
["I_Dados_REC.200.Margem de Mercado - Real PIS/Cofins",None, {"Line Item":"Valor Actual"}],
["I_Dados_STG.001.Carga OPEX arquivo",folder+"OPEX.csv", {"Line Item":"Valor Realizado Pós Rateio"}],
["I_Dados_EBT.100.EBITDA - Real",None, {"Line Item":"Valor Realizado Pós Rateio"}]]


####### DEFINICAO DE IMPORT #######

####### DEFINICAO DE PROCESSOS #######
# processlist = lista de processos
#processName = {"Testing Process":[{"Version":"Actual","Period":"Aug 20"}]}
#processName = {"Testing Process 2":None}
####### DEFINICAO DE PROCESSOS #######
# processlist = lista de processos
processList =[]
#processList =\
#[
#["Testing Process 2",{"Version":"Actual","Period":"Aug 20"}]
#]
#processList=[["Carga Centro de Custo e Unidades",None]]


# Execucao do script
def main():
    try:
        # execucao caller
        exec= executionControl.main(user, pwd, model, importList, processList)
    except:
        print("998 - An exception occurred.")



if __name__ == '__main__':
    main()


