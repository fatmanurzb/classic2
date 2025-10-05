def modinv(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def encrypt(text, params):
    try:
        a = int(params['a'])
        b = int(params['b'])
    except (KeyError, ValueError):
        return "Hata: Lütfen a ve b için geçerli sayılar girin."

    if modinv(a, 26) is None:
        return "Hata: a ile 26 aralarında asal olmalı"

    result = ''
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((a * (ord(char) - base) + b) % 26 + base)
        else:
            result += char
    return result

def decrypt(text, params):
    try:
        a = int(params['a'])
        b = int(params['b'])
    except (KeyError, ValueError):
        return "Hata: Lütfen a ve b için geçerli sayılar girin."

    a_inv = modinv(a, 26)
    if a_inv is None:
        return "Hata: a ile 26 aralarında asal olmalı"

    result = ''
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((a_inv * ((ord(char) - base) - b)) % 26 + base)
        else:
            result += char
    return result
