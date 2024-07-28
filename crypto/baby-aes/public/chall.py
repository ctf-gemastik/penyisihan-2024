#!/usr/local/bin/python

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

def encrypt(key, pt):
	cipher = AES.new(key, AES.MODE_CBC)
	ct = cipher.decrypt(pad(pt, 16))
	return cipher.iv + ct

print(f'Welcome to the AES CBC Machine')
print(f'Give me some input, and I will encrypt it for you')

with open('flag.txt', 'rb') as f:
    flag = f.read().strip()
assert len(flag) == 67

key = os.urandom(16)
out = encrypt(key, flag)
print(f'This is the example of the encryption result: {out.hex()}')
while True:
    msg = bytes.fromhex(input('Give me your message: '))
    print(f'Encryption result: {encrypt(key, msg).hex()}')
