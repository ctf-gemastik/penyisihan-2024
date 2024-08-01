# Writeup

The first thing to notice is that in the `encrypt` function, instead of using the AES-CBC `encrypt` method, it uses the AES-CBC `decrypt` method. If we carefully examine how AES-CBC decryption works, we will notice that it is quite similar to AES-ECB. If you're able to guess the last block of plaintext, you will be able to easily decrypt all the other blocks.

We observed that the flag's length is 67, which means the last block of the padded flag is guaranteed to be `b'xx}' + b'\xd'*13`, where `xx` is a combination of two possible characters. We can easily brute-force this to recover the correct intermediate bytes.

After we recover the last block's intermediate bytes, we can simply XOR the retrieved ciphertext block with the corresponding intermediate bytes. This will produce the previous ciphertext block. We can then continue to backtrack until we have recovered all of the plaintext.
