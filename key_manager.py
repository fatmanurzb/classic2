from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

key = RSA.generate(2048)

PRIVATE_KEY = key.export_key()
PUBLIC_KEY = key.publickey().export_key()

def rsa_encrypt_key(sym_key: bytes) -> str:
    cipher = PKCS1_OAEP.new(RSA.import_key(PUBLIC_KEY))
    encrypted = cipher.encrypt(sym_key)
    return base64.b64encode(encrypted).decode()

def rsa_decrypt_key(enc_key_b64: str) -> bytes:
    cipher = PKCS1_OAEP.new(RSA.import_key(PRIVATE_KEY))
    enc_key = base64.b64decode(enc_key_b64)
    return cipher.decrypt(enc_key)
