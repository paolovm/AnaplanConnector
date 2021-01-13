from cryptography.fernet import Fernet
import getpass


def encryptPwd(pwd,key,file):
    cipher_suite = Fernet(key)
    ciphered_text = cipher_suite.encrypt(pwd)   #required to be bytes
    with open(file, 'wb') as file_object:
        file_object.write(ciphered_text)
    unciphered_text = (cipher_suite.decrypt(ciphered_text))
    print("Password Stored in encrypted file")

key= b'ck5UFW9QZzpQe-oNXwiRJm3AQsf2HwUWlY_RjzDM5t0='
pwd = input("Please type your password:").encode()
#pwd = getpass.getpass(prompt='Password: ', stream=None)
file='mssqltip_bytes.bin'

encryptPwd(pwd,key,file)