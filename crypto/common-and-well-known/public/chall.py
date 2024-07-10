from Crypto.Util.number import getPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from os import urandom

p = getPrime(256)
q = getPrime(256)
n = p * q
ch = getPrime(128)

def gen(key):
    global ch, a, b
    ee = [getPrime(24) for i in range(len(key))]
    s = sum([(a[i] * key[i] + b) % ch for i in range(len(key))]) % ch
    e = [pow(a[i], ee[i], n) for i in range(len(key))]

    return (ch, ee, s, e)

def gen_a_b(key):
    global a, b
    a = [getPrime(256) for i in range(len(key))]
    b = getPrime(32)

def main():
    f = open('flag.txt', 'rb')
    flag = f.read()
    f.close()
    key = urandom(AES.key_size[0])

    print(f'{n = }')
    gen_a_b(key)
    while True:
        print('Say cheese 🧀')
        choice = input('> ')
        if choice == 'cheese':
            print(gen(key))
        elif choice == 'flag':
            iv = urandom(AES.block_size)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            print(iv.hex())
            print(cipher.encrypt(pad(flag, AES.block_size)).hex())
            exit(0)
        else:
            gen_a_b(key)


if __name__ == '__main__':
    main()