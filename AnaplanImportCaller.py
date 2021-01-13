import sys
sys.path.insert(1, 'PyTools/')
import dataAcquisition
import decrypt

# Anaplan Credentials
model = "Planning"
user = "paolovm3@yahoo.com.br"
pwdFile='PyTools/mssqltip_bytes.bin'
pwdKey='ck5UFW9QZzpQe-oNXwiRJm3AQsf2HwUWlY_RjzDM5t0='

# Folder with files
folder = "C:/Users/paolo.malafaia/Dropbox (Personal)/Flexthink/Py Scripts/VigmaPy/"

# ----------- IMPORT DEFINITION -----------
dataList =\
[
["sku.csv", folder+'sku.csv'],
["ska.csv",folder+'ska.csv']
]
# ----------- END IMPORT DEFINITION -----------

# ----------- IMPORT DEFINITION -----------
importList =\
[
]
# ----------- END IMPORT DEFINITION -----------



# ----------- PROCESS DEFINITION ---------
#processList=[["Carga Centro de Custo e Unidades", {}]]
processList=[["Testing Process",{}]]
#processList=[]
# ----------- END PROCESS DEFINITION -----------


# ----------- SCRIPT DEFINITION ----------
def main():
    # caller
    pwd = decrypt.pwdDecrypt(pwdFile,pwdKey)
    exec= dataAcquisition.main(user, pwd, model, dataList, importList, processList)
# ----------- END SCRIPT DEFINITION ----------



# ----------- SCRIPT EXECUTION ----------
if __name__ == '__main__':
    main()
# ----------- END SCRIPT EXECUTION ----------

