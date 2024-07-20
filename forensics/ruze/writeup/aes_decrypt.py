from Crypto.Cipher import AES

file = open("/mnt/c/Users/GreySyafiqKusuma/CTF/shared-folder/seccreettttt_credentialll_confidentalll_moodd_booossteerrrr.pdf","rb").read()
key = b"ea0aaa5d53dddfe1"
iv = file[0:16]
data = file[16:]

cipher = AES.new(key, AES.MODE_CBC, iv)
dec_data = cipher.decrypt(data)

res = open("/mnt/c/Users/GreySyafiqKusuma/CTF/shared-folder/res.pdf","wb")
res.write(dec_data)
res.close()