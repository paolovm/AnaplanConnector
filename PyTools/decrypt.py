from cryptography.fernet import Fernet

def pwdDecrypt(pwdfile, key):
    cipher_suite = Fernet(key)
    with open(pwdfile, 'rb') as file_object:
        for line in file_object:
            encryptedpwd = line
    uncipher_text = (cipher_suite.decrypt(encryptedpwd))
    encryptStr = bytes(uncipher_text).decode("utf-8") #convert to string
    return(encryptStr)


pwdfile='mssqltip_bytes.bin'
key= b'ck5UFW9QZzpQe-oNXwiRJm3AQsf2HwUWlY_RjzDM5t0='
#

if __name__ == '__main__':
    pwdDecrypt(pwdfile, key)