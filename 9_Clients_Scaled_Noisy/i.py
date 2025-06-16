def power(b, p, m):
    b %= m
    if p == 0:
        return 1
    j = power(b, p // 2, m)
    j = (j * j) % m
    if p % 2 == 1:
        j = (j * b) % m
    return j

def mod_inv(a, m):
    origin_m = m
    y, x = 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x += origin_m
    return x

# ---------- Parameters ----------
p = 1009  # large prime
g = 11         # generator
x = 5                     # small private key
h = power(g, x, p)        # public key

# ---------- Helper Functions ----------
def encode_signed(m, p):
    return m % (p - 1)

def decode_signed(m_encoded, p):
    return m_encoded if m_encoded <= (p - 1) // 2 else m_encoded - (p - 1)

# ---------- Encrypt / Decrypt ----------
def encrypt_additive(m, h, g, p, y=7):
    m_enc = encode_signed(m, p)
    c1 = power(g, y, p)
    s = power(h, y, p)
    c2 = (power(g, m_enc, p) * s) % p
    return c1, c2

def decrypt_additive(ciphertext, x, p, g):
    c1, c2 = ciphertext
    s = power(c1, x, p)
    s_inv = mod_inv(s, p)
    m_encoded = (c2 * s_inv) % p
    for m in range(p - 1):
        if power(g, m, p) == m_encoded:
            return decode_signed(m, p)
    return None

# ---------- Encrypt Messages ----------
m1 = 99
m2 = 99
print(f"Original m1 + m2: {(m1 + m2) % (p - 1)}")

# Encrypt
c1 = encrypt_additive(m1, h, g, p)
c2 = encrypt_additive(m2, h, g, p)

# ---------- Homomorphic Addition ----------
c_add = ((c1[0] * c2[0]) % p, (c1[1] * c2[1]) % p)

# ---------- Decrypt Result ----------
m_total = decrypt_additive(c_add, x, p, g)

print(f"Decrypted m1 + m2: {m_total if m_total is not None else 'Decryption failed'}")
