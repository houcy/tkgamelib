import timeit, math

PRIMES = [2,3]

def isprime(n):
    max_fac = int(math.sqrt(n))
    for i in PRIMES:
        if i > max_fac:
            return True
        if n % i == 0:
            return False
    i += 1
    while i < max_fac:
        if n % i == 0:
            return False
        i += 1
    return True

def cache_primes(n):
    """Cache primes up to n"""
    global PRIMES
    
    PRIMES = [2,3]
    for i in range(5, n, 2):
        if isprime(i):
            PRIMES.append(i)

def gap(m, n, g):
    last_prime = None
    primes = []
    if m % 2 == 0:
        m += 1
        if m == 2:
            last_prime = 2
            
    for i in range(m, n, 2):
        if isprime(i):
            if last_prime and i-last_prime == 2:
                primes.append([last_prime, i])
            else:
                last_prime = i
    return primes

cache_primes(100)
print("Cached", len(PRIMES), "primes")
for n in [1000, 10000, 100000]:
    print("Calculating", n)
    t = timeit.timeit('gap(2, %s, 2)' % n, number=5, globals=globals())
    print(t)

"""
Cached  25  primes
Calculating 1000
0.004577650001010625
Calculating 10000
0.03998120899996138
Calculating 100000
1.9685105070020654
"""

"""
Cached 168 primes
Calculating 1000
0.004807772002095589
Calculating 10000
0.058558840999467066
Calculating 100000
0.8301851750002243
"""
