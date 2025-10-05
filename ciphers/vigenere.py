def encrypt(text, params):
    key = params.get('key', '')
    if not key:
        return "Hata: Lütfen bir anahtar girin."

    key = key.upper()
    result = ''
    key_index = 0

    for char in text:
        if char.isalpha():
            k = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + k) % 26 + base)
            key_index += 1
        else:
            result += char

    return result


def decrypt(text, params):
    key = params.get('key', '')
    if not key:
        return "Hata: Lütfen bir anahtar girin."

    key = key.upper()
    result = ''
    key_index = 0

    for char in text:
        if char.isalpha():
            k = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - k) % 26 + base)
            key_index += 1
        else:
            result += char

    return result
