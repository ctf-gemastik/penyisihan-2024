from pwn import *
from Crypto.Util.number import inverse
from binascii import unhexlify
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

conn = remote('localhost', '10002')

exec(conn.recvuntil(b'\n'))

print(f'{n = }')

ch = []
ee = []
s = []
e = []
m = 32

for i in range(m):
    print(f'{i = }')
    for j in range(2):
        conn.sendlineafter(b'> ', b'cheese')

        ch_i, ee_i, s_i, e_i = eval(conn.recvuntil(b'\n')[:-1])

        ch.append(ch_i)
        ee.append(ee_i)
        s.append(s_i)
        e.append(e_i)

    conn.sendlineafter(b'> ', b'')

conn.sendlineafter(b'> ', b'flag')
iv = conn.recvuntil(b'\n').strip()
flag = conn.recvuntil(b'\n').strip()
conn.close()

def extendedGcd(a, b):
    if (a == 0):
        return (b, 0, 1)
    x, y, z = extendedGcd(b % a, a)
    return (x, z - (b // a) * y, y)

def mul(a, b):
    global n
    return ((a % n) * (b % n)) % n

a = []
b = []
for i in range(m):
    idx = 2 * i
    a_i = []

    ee_1 = ee[idx]
    ee_2 = ee[idx + 1]
    e_1 = e[idx]
    e_2 = e[idx + 1]
    for j in range(len(e_1)):
        gcd, s1, s2 = extendedGcd(ee_1[j], ee_2[j])
        c1 = e_1[j]
        c2 = e_2[j]
        if (s1 < 0):
            c1 = inverse(c1, n)
        if (s2 < 0):
            c2 = inverse(c2, n)
        a_i.append(mul(pow(c1, abs(s1), n), pow(c2, abs(s2), n)))

    a.append(a_i)
    b.append(s[idx])

q = ch[0]
n = len(a[0])

from sage.modules.free_module_integer import IntegerLattice

def Babai_closest_vector(M, G, target):
    small = target
    for _ in range(1):
        for i in reversed(range(M.nrows())):
            c = ((small * G[i]) / (G[i] * G[i])).round()
            small -= M[i] * c
    return target - small


A = matrix(ZZ, m + n, m)
for i in range(m):
    A[i, i] = q
for x in range(m):
    for y in range(n):
        A[m + y, x] = a[x][y]

lattice = IntegerLattice(A, lll_reduce=True)
gram = lattice.reduced_basis.gram_schmidt()[0]
target = vector(ZZ, b)
res = Babai_closest_vector(lattice.reduced_basis, gram, target)

print(f"Closest Vector: {res}")

R = IntegerModRing(q)
M = Matrix(R, a)
key = M.solve_right(res)

cipher = AES.new(bytes(key), AES.MODE_CBC, unhexlify(iv))
flag = unpad(cipher.decrypt(unhexlify(flag)), AES.block_size).decode()
print(f'{flag = }')