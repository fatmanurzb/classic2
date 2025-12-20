from .base import BaseCipher

class CaesarCipher(BaseCipher):

    def encrypt(self, text, key=None):
        shift = int(key) if key else 3
        result = ""

        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += char

        return result

    def decrypt(self, text, key=None):
        shift = int(key) if key else 3
        return self.encrypt(text, -shift)
