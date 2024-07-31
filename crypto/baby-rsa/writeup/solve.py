from pwn import *
from Crypto.Util.number import *

r = remote('localhost', '10044')

e = 0x10001
r.recvuntil(b': ')
n = int(r.recvline().strip(), 16)
max_bytes = n.bit_length()//8
r.recvuntil(b': ')
cFLAG = int(r.recvline().strip(), 16)

print(f'{n = }')
print(f'{max_bytes = }')
print(f'{cFLAG = }')

def oracle(val, debug=False):
    r.sendlineafter(b'free: ', hex(val).encode())
    out = r.recvline().strip()
    if debug:
        print(out)
    if b'decrypted' in out:
        return True
    return False

# Find flag length
for i in range(0, max_bytes, 1):
    val = cFLAG*pow((2**8)**i, e, n)
    status = oracle(val)
    if not status:
        print(i, 'error')
        len_flag = (max_bytes - (i-1))
        break
print(f'{len_flag = }')
pause()

low = (2**8)**(max_bytes - len_flag)
high = (2**8)**(max_bytes - len_flag + 1)
i = 0
while low < high:
    mid = (high + low) // 2
    out = oracle(cFLAG*pow(mid, e, n))
    print(f'{out = }')
    if out:
        low = mid + 1
    else:
        high = mid
    print(f'Range: {high - low}')
    print(f'{high = }')
    print(f'{low = }')
    i += 1
    print(f'-----')

print()
print(f'Total calls: {i}')
mid = low-1
for k in range(1000):
    flag = (((2**8)**max_bytes) + k*n) // mid
    flag = long_to_bytes(flag)
    print(k, flag)
    if b'gemastik' in flag:
        exit()
