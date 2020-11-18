# Importando outras bibliotecas do Python
import executionControl

# Credenciais para acessar o Anaplan
model = "PLANNING DEV"
user = "paolo.malafaia@flexthink.com.au"
pwd = "Number28"

# Configuracoes de arquivos, imports e processes
folder = "Dados/"

# -----------DEFINICAO DE IMPORT -----------
# importlist = dicionario com nome do import + arquivo base

# importList = {"I_List_CST_Maquinas":folder+"MAQUINAS.CSV","I_Dados_MAP.032.CST_Maquinas":None}

# importList =\
# [
# ["I_List_CCF4_UN_SKU", folder+"UNxSKU.txt", {}],
# ["I_Dados_MAP.025.UNxSKU", None, {}],
# ["I_Dados_STG.700.Carga Mg de Mkt PIS Embutido", folder+"mm.txt", {"Line Item":"Valor Actual"}],
# ["I_Dados_STG.700.Carga Mg de Mkt PIS Zero",folder+"mm.txt", {"Line Item":"Valor Actual"}],
# ["I_Dados_REC.200.Margem de Mercado - Real Base",None, {"Line Item":"Valor Actual"}],
# ["I_Dados_REC.200.Margem de Mercado - Real PIS/Cofins",None, {"Line Item":"Valor Actual"}],
# ["I_Dados_STG.001.Carga OPEX arquivo",folder+"OPEX.csv", {"Line Item":"Valor Realizado Pós Rateio"}],
# ["I_Dados_EBT.100.EBITDA - Real",None, {"Line Item":"Valor Realizado Pós Rateio"}]
#      ]

importList = [["I_Dados_MAP.002.UN Resultado", None, {}]]
# ----------- DEFINICAO DE IMPORT -----------




# ----------- DEFINICAO DE PROCESSOS ---------


#processList=[["Carga Centro de Custo e Unidades", {}]]
processList=[]
# ----------- DEFINICAO DE PROCESSOS -----------


# Execucao do script
def main():
    try:
        # execucao caller
        exec= executionControl.main(user, pwd, model, importList, processList)
    except:
        print("998 - An exception occurred.")



if __name__ == '__main__':
    main()


