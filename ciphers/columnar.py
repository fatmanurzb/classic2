import math
from typing import Optional
from .base import BaseCipher


class ColumnarCipher(BaseCipher):

    def _key_order(self, key: str):
        """
        Anahtar harflerine göre sütun sıralaması üretir.
        Örn: ZEBRA -> [4,1,3,2,0]
        """
        return sorted(range(len(key)), key=lambda i: (key[i], i))

    def encrypt(self, text: str, key: Optional[str] = None):
        if not key:
            return "Anahtar gerekli!"

        key = key.upper()
        text = ''.join(text.split())

        cols = len(key)
        rows = math.ceil(len(text) / cols)

        # Matris oluştur
        matrix = [['X'] * cols for _ in range(rows)]

        idx = 0
        for r in range(rows):
            for c in range(cols):
                if idx < len(text):
                    matrix[r][c] = text[idx]
                    idx += 1

        # Sütunları anahtar sırasına göre oku
        order = self._key_order(key)
        ciphertext = ""

        for c in order:
            for r in range(rows):
                ciphertext += matrix[r][c]

        return ciphertext

    def decrypt(self, text: str, key: Optional[str] = None):
        if not key:
            return "Anahtar gerekli!"

        key = key.upper()
        cols = len(key)
        rows = math.ceil(len(text) / cols)

        order = self._key_order(key)

        # Her sütunun alacağı karakter sayısı
        full_cols = len(text) % cols
        col_lengths = [rows] * cols
        if full_cols != 0:
            for i in range(cols):
                if order.index(i) >= full_cols:
                    col_lengths[i] -= 1

        # Sütunları doldur
        columns = [''] * cols
        idx = 0
        for c in order:
            length = col_lengths[c]
            columns[c] = text[idx:idx + length]
            idx += length

        # Satır satır oku
        plaintext = ""
        for r in range(rows):
            for c in range(cols):
                if r < len(columns[c]):
                    plaintext += columns[c][r]

        return plaintext.rstrip('X')
