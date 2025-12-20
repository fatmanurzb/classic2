# cipher_manager.py
from ciphers.caesar import CaesarCipher
from ciphers.vigenere import VigenereCipher
from ciphers.affine import AffineCipher
from ciphers.columnar import ColumnarCipher
from ciphers.railfence import RailFenceCipher
from ciphers.playfair import PlayfairCipher
from ciphers.hill import HillCipher
from ciphers.polybius import PolybiusCipher
from ciphers.rot import RotCipher
from ciphers.substitution import SubstitutionCipher
from ciphers.pigpen import PigpenCipher


class CipherManager:

    def __init__(self):
        self.ciphers = {
            "caesar": CaesarCipher(),
            "vigenere": VigenereCipher(),
            "affine": AffineCipher(),
            "columnar": ColumnarCipher(),
            "railfance": RailFenceCipher(),
            "playfair": PlayfairCipher(),
            "hill": HillCipher(),
            "polybius": PolybiusCipher(),
            "rot": RotCipher(),
            "substitution": SubstitutionCipher(),
            "pigpen": PigpenCipher(),
    }

    def encrypt(self, algo, text, key=None):
        if algo not in self.ciphers:
            raise ValueError("Geçersiz algoritma")
        return self.ciphers[algo].encrypt(text, key)

    def decrypt(self, algo, text, key=None):
        if algo not in self.ciphers:
            raise ValueError("Geçersiz algoritma")
        return self.ciphers[algo].decrypt(text, key)