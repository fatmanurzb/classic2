from .base import BaseCipher

class AffineCipher(BaseCipher):

    def modinv(self, a: int, m: int):
        for i in range(1, m):
            if (a * i) % m == 1:
                return i
        return None

    def encrypt(self, text, key=None):
        if not isinstance(key, dict):
            return "Hata: a ve b parametreleri eksik"

        a_val = key.get("a")
        b_val = key.get("b")

        if a_val is None or b_val is None:
            return "Hata: a ve b zorunludur"

        try:
            a = int(a_val)
            b = int(b_val)
        except ValueError:
            return "Hata: a ve b sayısal olmalı"

        if self.modinv(a, 26) is None:
            return "Hata: a ile 26 aralarında asal olmalı"

        result = ""
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((a * (ord(char) - base) + b) % 26 + base)
            else:
                result += char

        return result

    def decrypt(self, text, key=None):
        if not isinstance(key, dict):
            return "Hata: a ve b parametreleri eksik"

        a_val = key.get("a")
        b_val = key.get("b")

        if a_val is None or b_val is None:
            return "Hata: a ve b zorunludur"

        try:
            a = int(a_val)
            b = int(b_val)
        except ValueError:
            return "Hata: a ve b sayısal olmalı"

        a_inv = self.modinv(a, 26)
        if a_inv is None:
            return "Hata: a ile 26 aralarında asal olmalı"

        result = ""
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((a_inv * ((ord(char) - base) - b)) % 26 + base)
            else:
                result += char

        return result
