from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import glob
import os

file_key = get_random_bytes(16)

rsa_key = RSA.generate(2048)
private_key = rsa_key.export_key()
file_out = open('private.pem', 'wb')
file_out.write(private_key)
file_out.close()

public_key = rsa_key.publickey().export_key()
file_out = open('receiver.pem', 'wb')
file_out.write(public_key)
file_out.close()

# .txt 모두 파일 가져오기
data_list = glob.glob('*.txt')

# 대칭키를 RSA 2048로 암호화
file_out = open('enc_symmetric_key.bin', 'wb')
public_key = RSA.import_key(open("receiver.pem").read())
cipher_rsa =  PKCS1_OAEP.new(public_key)
enc_file_key = cipher_rsa.encrypt(file_key)
file_out.write(enc_file_key)
file_out.close()

# 파일을 AES로 암호화하기 위한 과정
cipher = AES.new(file_key, AES.MODE_CBC)
iv = b64encode(cipher.iv)

# iv를 파일로 저장
file_out = open('iv.bin', 'wb')
file_out.write(iv)
file_out.close()

for data_file in data_list:
    # 파일명 추출
    file_basename = os.path.splitext(data_file)[0]

    # 파일 읽어오기
    file_in = open(data_file, 'rb')
    data = file_in.read()
    file_in.close()

    # 파일을 AES로 암호화
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    ct = b64encode(ct_bytes)

    file_out = open(file_basename + '.enc', 'wb')
    file_out.write(ct)
    file_out.close()