from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

def des_encrypt(plaintext: str, key: bytes) -> str:
    if len(key) != 8:
        raise ValueError("DES key must be exactly 8 bytes")

    iv = get_random_bytes(8)
    cipher = DES.new(key, DES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), 8))

    return base64.b64encode(iv + ciphertext).decode()


def des_decrypt(ciphertext_b64: str, key: bytes) -> str:
    if len(key) != 8:
        raise ValueError("DES key must be exactly 8 bytes")

    raw = base64.b64decode(ciphertext_b64)
    iv = raw[:8]
    ciphertext = raw[8:]

    cipher = DES.new(key, DES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), 8)

    return plaintext.decode()
