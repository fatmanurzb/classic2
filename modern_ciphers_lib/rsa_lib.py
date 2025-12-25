from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Anahtar üret
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def rsa_encrypt_key(aes_key: bytes, public_key_bytes: bytes) -> str:
    public_key = RSA.import_key(public_key_bytes)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted = cipher.encrypt(aes_key)
    return base64.b64encode(encrypted).decode()


def rsa_decrypt_key(encrypted_key_b64: str, private_key_bytes: bytes) -> bytes:
    private_key = RSA.import_key(private_key_bytes)
    cipher = PKCS1_OAEP.new(private_key)
    decrypted = cipher.decrypt(base64.b64decode(encrypted_key_b64))
    return decrypted
