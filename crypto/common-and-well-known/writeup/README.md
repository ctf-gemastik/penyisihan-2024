# Writeup
In one round of `gen`, we can get $ch$, $e$, $s$, $ee$. Modulus $n$ and $key$ will be the same in each connection. And, $a$ and $b$ is generated separately. We can see that:

$$s = a \cdot key + b \mod ch$$

$$ e_i = a_i^{ee_i} \mod n $$

To recover the flag, we need to recover $key$. To recover $key$, we can see that we can get it from the first equation even if we don't know $b$ because it is the basic setup for LWE (learning with errors) problem. To do that, first, we need to recover $a$. We can recover it by performing common modulus attack because the $a$ and $n$ is the same for every `gen`, but the exponent $ee$ will be different. Knowing that, we can generate enough $s$ with different $a$ and $b$ and solve the LWE problem.

References:
- https://hackmd.io/@hakatashi/B1OM7HFVI
- https://11dimensions.moe/archives/267
- https://crypto.stackexchange.com/questions/16283/how-to-use-common-modulus-attack