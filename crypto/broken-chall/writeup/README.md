# Writeup

## Observation

The first thing to observe is that the challenge seems impossible to solve because the decryption result is always replaced with a hardcoded string. However, there is actually an oracle based on the `to_bytes` function. The `to_bytes` function tries to convert a given number to its bytes representation based on the specified length, which in this case is `n.bit_length() // 8`. According to the documentation, if the specified number has more bits than `n`, it will raise an overflow error. This trick allows us to use this as an `oracle` for the encryption.

## RSA Properties

Remember that RSA has properties where if you have `pow(m, e, n)`, you can easily multiply it with `pow(x, e, n)` to produce the encryption of `pow(m * x, e, n)`. This means we can extend the flag by multiplying it with any number, which can trigger the error.

## Steps to Solve
### Determine the Length of the Flag

The first step is to determine the length of the flag. Observe that the max bytes of the message is `n.bit_length() // 8`, which should be around 334 bytes. With high probability, if we try to extend the flag by shifting it by one byte (multiplying the flag with $2^{8*i}$ where $i$ is the number of bytes shifted), and if we get an error, it is very likely because the length of the flag plus the shifted bytes is already higher than $334$ bytes (which means that $mx \mod n$ is higher than $2^{334}-1$). This means if, after shifting it by $10$, the oracle returns an error, the length of the flag should be $334 - 10 - 1 = 323$.

### Find the Largest Number $x$

After knowing the length of the flag, the next step is to find the largest number $x$ such that $mx \mod n \leq 2^{8*334}$. Based on the length of the flag, we know that the range of $x$ must be between $2^{8(\text{max bytes}-\text{len flag})}$ and $2^{8(\text{max bytes}-\text{len flag}+1)}$. We can use binary search to find $x$.

### Brute-Force the Correct $k$

After finding $x$, observe that $mx - kn \leq 2^{8*334}$. Since $k$ is small, we can brute-force it to find the correct $k$, which will produce the correct $m$ by calculating,
$$m \leq \frac{2^{8*334} + kn}{x}$$
where $m$ is the flag.