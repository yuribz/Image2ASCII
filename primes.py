bound = 1000000

count = 0

i = 2

while i <= bound:
    is_prime = True
    for j in range(2, int(i ** (1/2))):
        if (i % j == 0):
            is_prime = False
            break
    if is_prime:
        count += 1
    i += 1

print(f"Found %d primes!", count)