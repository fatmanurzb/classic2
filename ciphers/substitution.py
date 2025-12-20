import string
from .base import BaseCipher


class SubstitutionCipher(BaseCipher):

    def _validate_key(self, key):
        if not key or not isinstance(key, str) or len(key) != 26:
            return None
        return key.upper()

    def encrypt(self, text, key=None):
        key = self._validate_key(key)
        if key is None:
            return "Hata: Lütfen 26 harfli geçerli bir anahtar girin."

        alphabet = string.ascii_uppercase
        result = ""

        for char in text:
            if char.isalpha():
                is_upper = char.isupper()
                idx = alphabet.index(char.upper())
                enc_char = key[idx]
                result += enc_char if is_upper else enc_char.lower()
            else:
                result += char

        return result

    def decrypt(self, text, key=None):
        key = self._validate_key(key)
        if key is None:
            return "Hata: Lütfen 26 harfli geçerli bir anahtar girin."

        alphabet = string.ascii_uppercase
        result = ""

        for char in text:
            if char.isalpha():
                is_upper = char.isupper()
                idx = key.index(char.upper())
                dec_char = alphabet[idx]
                result += dec_char if is_upper else dec_char.lower()
            else:
                result += char

        return result
