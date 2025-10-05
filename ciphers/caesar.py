def encrypt(text, params):
    try:
        shift = int(params.get('shift', 3))
    except (ValueError, TypeError):
        return "Hata: Lütfen geçerli bir shift sayısı girin."

    result = ''
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def decrypt(text, params):
    try:
        shift = int(params.get('shift', 3))
    except (ValueError, TypeError):
        return "Hata: Lütfen geçerli bir shift sayısı girin."

    # decrypt için shift negatif
    return encrypt(text, {'shift': -shift})
