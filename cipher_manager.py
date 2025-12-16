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


def encrypt_message(cipher, text, key):
    cipher = cipher.lower()

    if cipher == "none":
        return text

    try:
        if cipher == "caesar":
            shift = int(key) if key else 3
            return CaesarCipher(shift).encrypt(text)

        if cipher == "vigenere":
            return VigenereCipher(key).encrypt(text)

        if cipher == "affine":
            a, b = map(int, key.split(",")) if "," in key else (5, 8)
            return AffineCipher(a, b).encrypt(text)

        if cipher == "columnar":
            return ColumnarCipher(key).encrypt(text)

        if cipher == "railfence":
            rails = int(key) if key else 3
            return RailFenceCipher(rails).encrypt(text)

        if cipher == "playfair":
            return PlayfairCipher(key).encrypt(text)

        if cipher == "hill":
            return HillCipher(key).encrypt(text)

        if cipher == "polybius":
            return PolybiusCipher().encrypt(text)

        if cipher == "rot":
            return RotCipher().encrypt(text)

        if cipher == "substitution":
            return SubstitutionCipher(key).encrypt(text)

        if cipher == "pigpen":
            return PigpenCipher().encrypt(text)

    except Exception as e:
        return f"[Şifreleme Hatası: {e}]"

    return text
