# -*-coding:utf-8-*-
from Crypto.PublicKey import RSA

text = "Test Text"
pub_key = RSA.importKey(open(r"D:\id_rsa.pub").read())
x = pub_key.encrypt(text.encode(encoding="utf-8"), '1234'.encode(encoding="utf-8"))

pri_key = RSA.importKey(open(r"D:\id_rsa").read())
decrypted_text = pri_key.decrypt(x[0])
decrypted_text = decrypted_text.decode(encoding="utf-8")
print(decrypted_text)

print(text==decrypted_text)