# ============================================
# SIMPLE AES (MANUAL - EDUCATIONAL VERSION)
# ============================================

# Basit S-Box (gerçek AES S-box DEĞİL)
S_BOX = {
    i: (i * 7 + 3) % 256 for i in range(256)
}

INV_S_BOX = {v: k for k, v in S_BOX.items()}


def sub_bytes(block):
    return [S_BOX[b] for b in block]


def inv_sub_bytes(block):
    return [INV_S_BOX[b] for b in block]


def shift_rows(block):
    # 4x4 matris varsayımı (AES mantığı)
    return [
        block[0],  block[1],  block[2],  block[3],
        block[5],  block[6],  block[7],  block[4],
        block[10], block[11], block[8],  block[9],
        block[15], block[12], block[13], block[14]
    ]


def inv_shift_rows(block):
    return [
        block[0],  block[1],  block[2],  block[3],
        block[7],  block[4],  block[5],  block[6],
        block[10], block[11], block[8],  block[9],
        block[13], block[14], block[15], block[12]
    ]


def add_round_key(block, key):
    return [b ^ k for b, k in zip(block, key)]


def pad(text):
    while len(text) % 16 != 0:
        text += chr(16 - (len(text) % 16))
    return text


def unpad(text):
    return text.rstrip(text[-1])


def aes_manual_encrypt(text, key):
    """
    text: string
    key: string (16 byte önerilir)
    """

    text = pad(text)

    key_bytes = [ord(c) for c in key.ljust(16)[:16]]
    result = ""

    for i in range(0, len(text), 16):
        block = [ord(c) for c in text[i:i+16]]

        # 4 ROUND (sadeleştirilmiş)
        for _ in range(4):
            block = sub_bytes(block)
            block = shift_rows(block)
            block = add_round_key(block, key_bytes)

        result += "".join(chr(b) for b in block)

    return result


def aes_manual_decrypt(cipher, key):
    key_bytes = [ord(c) for c in key.ljust(16)[:16]]
    result = ""

    for i in range(0, len(cipher), 16):
        block = [ord(c) for c in cipher[i:i+16]]

        for _ in range(4):
            block = add_round_key(block, key_bytes)
            block = inv_shift_rows(block)
            block = inv_sub_bytes(block)

        result += "".join(chr(b) for b in block)

    return unpad(result)
