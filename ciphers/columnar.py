# ciphers/columnar.py
import math

def _key_order(key: str):
    indexed = sorted([(ch, i) for i, ch in enumerate(key)], key=lambda x: (x[0], x[1]))
    order = [None] * len(key)
    for rank, (_, orig_i) in enumerate(indexed):
        order[orig_i] = rank
    return order

def encrypt(plaintext: str, key: str):
    if not key:
        return "Anahtar gerekli!"
    text = ''.join(plaintext.split())  # boşlukları kaldır
    cols = len(key)
    rows = math.ceil(len(text) / cols)
    matrix = [['X'] * cols for _ in range(rows)]
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx < len(text):
                matrix[r][c] = text[idx]
                idx += 1
    order = _key_order(key)
    cols_by_rank = sorted(range(cols), key=lambda i: order[i])
    ciphertext = ''
    for c in cols_by_rank:
        for r in range(rows):
            ciphertext += matrix[r][c]
    return ciphertext

def decrypt(ciphertext: str, key: str):
    if not key:
        return "Anahtar gerekli!"
    cols = len(key)
    rows = math.ceil(len(ciphertext) / cols)
    order = _key_order(key)
    col_lens = [rows] * cols
    cols_by_rank = sorted(range(cols), key=lambda i: order[i])
    start = 0
    col_strings = [None] * cols
    for c in cols_by_rank:
        l = col_lens[c]
        col_strings[c] = ciphertext[start:start+l]
        start += l
    plaintext = ''
    for r in range(rows):
        for c in range(cols):
            if r < len(col_strings[c]):
                plaintext += col_strings[c][r]
    return plaintext.rstrip('X')
