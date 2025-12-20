from .base import BaseCipher


class VigenereCipher(BaseCipher):

    def _validate_key(self, key):
        if not key or not isinstance(key, str):
            return None
        return key.upper()

    def encrypt(self, text, key=None):
        key = self._validate_key(key)
        if key is None:
            return "Hata: Lütfen bir anahtar girin."

        result = ""
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

    def decrypt(self, text, key=None):
        key = self._validate_key(key)
        if key is None:
            return "Hata: Lütfen bir anahtar girin."

        result = ""
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
