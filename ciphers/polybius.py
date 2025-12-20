from .base import BaseCipher


class PolybiusCipher(BaseCipher):

    def __init__(self):
        self.poly = [
            ['A','B','C','D','E'],
            ['F','G','H','I','K'],
            ['L','M','N','O','P'],
            ['Q','R','S','T','U'],
            ['V','W','X','Y','Z']
        ]

        self.char_to_code = {}
        self.code_to_char = {}

        for r in range(5):
            for c in range(5):
                ch = self.poly[r][c]
                code = f"{r+1}{c+1}"
                self.char_to_code[ch] = code
                self.code_to_char[code] = ch

        # J → I kuralı
        self.char_to_code['J'] = self.char_to_code['I']

    def encrypt(self, text, key=None):
        out = []
        for ch in text.upper():
            if ch.isalpha():
                out.append(self.char_to_code.get(ch, ''))
        return " ".join(out)

    def decrypt(self, text, key=None):
        digits = ''.join(text.split())

        if len(digits) % 2 != 0:
            return "Hata: Geçersiz Polybius kod uzunluğu!"

        out = []
        for i in range(0, len(digits), 2):
            pair = digits[i:i+2]
            out.append(self.code_to_char.get(pair, ''))

        return "".join(out)
