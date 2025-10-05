import string

def encrypt(text, params):
    key = params.get('key', '')
    if not key or len(key) != 26:
        return "Hata: Lütfen 26 harfli geçerli bir anahtar girin."

    key = key.upper()
    alphabet = string.ascii_uppercase
    result = ''

    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            idx = alphabet.index(char.upper())
            enc_char = key[idx]
            result += enc_char if is_upper else enc_char.lower()
        else:
            result += char

    return result


def decrypt(text, params):
    key = params.get('key', '')
    if not key or len(key) != 26:
        return "Hata: Lütfen 26 harfli geçerli bir anahtar girin."

    key = key.upper()
    alphabet = string.ascii_uppercase
    result = ''

    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            idx = key.index(char.upper())
            dec_char = alphabet[idx]
            result += dec_char if is_upper else dec_char.lower()
        else:
            result += char

    return result
