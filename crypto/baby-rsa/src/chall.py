from Crypto.Util.number import getPrime, inverse

p, q, e = getPrime(1337), getPrime(1337), 0x10001
n, d = p*q, inverse(e, (p-1)*(q-1))

assert (((p-1)*(q-1))%e != 0) and (1337 == pow(1337, e*d, n))

FLAG = open('flag.txt', 'rb').read().strip()
cFLAG = pow(int.from_bytes(FLAG, 'big') , e, n)

print('Welcome to RSA Machine...')
print(f'Here is the public key    :', hex(n))
print(f'Here is the encrypted flag:', hex(cFLAG))

while True:
    try:
        c = input('Give me your encrypted value, and I will decrypt it for free: ')
        c = int(c, 16)
        dFLAG = pow(c, d, n).to_bytes(n.bit_length()//8, 'big')
        dFLAG = 'You get rickrolled lmao'
        print(f'Here is your decrypted value: {dFLAG}')
    except:
        print('Urghhhhhhh...')