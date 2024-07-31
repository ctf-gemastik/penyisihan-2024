from pwn import *
import string
import itertools

r = remote('localhost', '10004')

def oracle(msg):
    r.sendlineafter(b'Give me your message: ', msg.hex().encode())
    r.recvuntil(b'Encryption result: ')
    result = bytes.fromhex(r.recvline().strip().decode())
    return result[:16], result[16:]

# Retrieve encrypted flag
r.recvuntil(b'result: ')
out = bytes.fromhex(r.recvline().strip().decode())
iv = out[:16]
enc_flag = out[16:]

num_blocks = len(enc_flag) // 16
print(f'{num_blocks = }')
blocks = [enc_flag[i:i+16] for i in range(0, len(enc_flag), 16)]
assert len(blocks) == num_blocks

# Brute-force last block
# Notes that the flag's length is 67, which mean the last block of the padded flag
# is guaranteed to be b'xx}'+b'\xd'*13
# We just need to bruteforce 2 chars
recovered_pts = []
for ch1, ch2 in itertools.product(string.printable, repeat=2):
    msg = f"{ch1}{ch2}}}".encode()
    iv, enc_msg = oracle(msg)
    block_enc_res = xor(iv, enc_msg)
    recovered_pt = xor(block_enc_res, blocks[-1])

    # If the msg that we brute-force is correct, the recovered_pt
    if all(chr(byte) in string.printable for byte in recovered_pt):
        print(f"Possible last block: {recovered_pt}")
        recovered_pts += [recovered_pt, msg]
        break

# Now we have recover the last two block, recovering the rest is trivial
# We can simply recover block per block from behind
for _ in range(num_blocks-2):
    last_recovered_pt = recovered_pts[0]
    iv, enc_msg = oracle(last_recovered_pt)
    new_recovered_pt = xor(xor(iv, enc_msg)[:16], blocks[-len(recovered_pts)])
    recovered_pts = [new_recovered_pt] + recovered_pts

# Flag is finally recovered
print(f"flag: {b''.join(recovered_pts)}")
r.close()
