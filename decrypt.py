from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

import glob
import os

try:
    # 대칭키 RSA로 복호화
    file_in = open('enc_symmetric_key.bin', 'rb')
    private_key = RSA.import_key(open('private.pem').read())
    enc_file_key = file_in.read(private_key.size_in_bytes())
    cipher_rsa = PKCS1_OAEP.new(private_key)
    file_key = cipher_rsa.decrypt(enc_file_key)

    # .enc 모두 가져오기
    data_list = glob.glob('*.enc')

    # iv 읽기
    file_in = open('iv.bin', 'rb')
    iv = b64decode(file_in.read())
    file_in.close()

    cipher = AES.new(file_key, AES.MODE_CBC, iv)
    iter = 0

    for data_file in data_list:
        # 파일명 추출
        file_basename = os.path.splitext(data_file)[0]

        # .enc 읽기
        file_in = open(data_file, 'rb')
        ct = b64decode(file_in.read())
        file_in.close()

        # AES 복호화
        pt = unpad(cipher.decrypt(ct), AES.block_size)        
            
        # 복호화한 파일 생성
        file_out = open('dec_' + file_basename + '.txt', 'wb')
        file_out.write(pt)
        file_out.close()
except ValueError:
    print('Incorrect decryption')
except KeyError:
    print('Incorrect Key')