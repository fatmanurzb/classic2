# ============================================
# SIMPLE DES (MANUAL - EDUCATIONAL VERSION)
# ============================================

def xor(a, b):
    return [i ^ j for i, j in zip(a, b)]


def feistel_function(right, subkey):
    # Basit substitution + XOR
    return [(r + k) % 256 for r, k in zip(right, subkey)]


def generate_subkeys(key):
    key_bytes = [ord(c) for c in key.ljust(8)[:8]]
    return [
        key_bytes[i:] + key_bytes[:i]
        for i in range(4)
    ]


def pad(text):
    while len(text) % 8 != 0:
        text += chr(8 - (len(text) % 8))
    return text


def unpad(text):
    return text.rstrip(text[-1])


def encrypt(text, key):
    text = pad(text)
    subkeys = generate_subkeys(key)
    result = ""

    for i in range(0, len(text), 8):
        block = [ord(c) for c in text[i:i+8]]
        left, right = block[:4], block[4:]

        # 4 ROUND FEISTEL
        for r in range(4):
            temp = right
            f = feistel_function(right, subkeys[r])
            right = xor(left, f)
            left = temp

        result += "".join(chr(c) for c in left + right)

    return result


def decrypt(cipher, key):
    subkeys = generate_subkeys(key)
    result = ""

    for i in range(0, len(cipher), 8):
        block = [ord(c) for c in cipher[i:i+8]]
        left, right = block[:4], block[4:]

        for r in reversed(range(4)):
            temp = left
            f = feistel_function(left, subkeys[r])
            left = xor(right, f)
            right = temp

        result += "".join(chr(c) for c in left + right)

    return unpad(result)
