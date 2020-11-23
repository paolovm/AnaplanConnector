import sys
sys.path.insert(1, 'PyTools/')
import dataAcquisition

# Anaplan Credentials
model = "Planning"
user = "paolovm3@yahoo.com.br"
pwd = "Number28"


# Folder with files
folder = "Data/"


# ----------- IMPORT DEFINITION -----------
importList =\
[
["Asset Month Price from sku.csv", 'C:/Users/paolo.malafaia/Dropbox (Personal)/Flexthink/Py Scripts/VigmaPy/sku.csv', {}],
["Asset Month Price from ska.csv",'C:/Users/paolo.malafaia/Dropbox (Personal)/Flexthink/Py Scripts/VigmaPy/ska.csv',{}]
]
# ----------- END IMPORT DEFINITION -----------



# ----------- PROCESS DEFINITION ---------
#processList=[["Carga Centro de Custo e Unidades", {}]]
processList=[]
# ----------- END PROCESS DEFINITION -----------


# ----------- SCRIPT DEFINITION ----------
def main():
    # caller
    exec= dataAcquisition.main(user, pwd, model, importList, processList)
# ----------- END SCRIPT DEFINITION ----------



# ----------- SCRIPT EXECUTION ----------
if __name__ == '__main__':
    main()
# ----------- END SCRIPT EXECUTION ----------

