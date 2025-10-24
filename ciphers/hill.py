# ciphers/hill.py
# 2x2 Hill Cipher (mod 26)

def _egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = _egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def _modinv(a, m):
    g, x, _ = _egcd(a, m)
    if g != 1:
        raise ValueError("Ters mod 26 bulunamadı!")
    return x % m

def _prepare(text):
    s = ''.join(c for c in text.upper() if c.isalpha())
    if len(s) % 2 != 0:
        s += 'X'
    return s

def encrypt(text, key_list):
    s = _prepare(text)
    try:
        a,b,c,d = map(int, key_list)
    except:
        return "Anahtar hatalı! (4 sayı girin)"
    out = []
    for i in range(0, len(s), 2):
        x = ord(s[i]) - 65
        y = ord(s[i+1]) - 65
        r1 = (a*x + b*y) % 26
        r2 = (c*x + d*y) % 26
        out.append(chr(r1 + 65))
        out.append(chr(r2 + 65))
    return ''.join(out)

def decrypt(cipher, key_list):
    try:
        a,b,c,d = map(int, key_list)
    except:
        return "Anahtar hatalı! (4 sayı girin)"
    det = (a*d - b*c) % 26
    try:
        det_inv = _modinv(det, 26)
    except ValueError:
        return "Anahtar matrisinin tersi yok!"
    inv = [(d*det_inv)%26, (-b*det_inv)%26, (-c*det_inv)%26, (a*det_inv)%26]
    out = []
    for i in range(0, len(cipher), 2):
        x = ord(cipher[i]) - 65
        y = ord(cipher[i+1]) - 65
        r1 = (inv[0]*x + inv[1]*y) % 26
        r2 = (inv[2]*x + inv[3]*y) % 26
        out.append(chr(r1 + 65))
        out.append(chr(r2 + 65))
    return ''.join(out)
