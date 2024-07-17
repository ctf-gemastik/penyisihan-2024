# Writeup

## TL;DR
- Create disassembler for the VM
- There is common anti debug that will slightly modify the SBOX and key
- Found that the algorithm looks like RC4 with flow flattening
- There is added XOR instruction in RC4 algorithm that make the current value will affect the next value (chained)
- Modified part of RC4 only added XOR instruction and different SBOX
- Compare function utilize substraction to validate each ciphertext value
`actual_ciphertext[i] - x === y`
- i == index, x value is different for each index and index is not in order
- To get the flag , participants need to find the order of index and its value, create RC4 algorithm with defined SBOX then add XOR instruction with the previous ciphertext at the end of the decrypt function