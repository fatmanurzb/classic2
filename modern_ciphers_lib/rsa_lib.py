from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generate_keys():
    key = RSA.generate(2048)
    return key.export_key(), key.publickey().export_key()

def encrypt_key(sym_key, public_key):
    pub = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(pub)
    return base64.b64encode(cipher.encrypt(sym_key)).decode()

def decrypt_key(enc_key, private_key):
    priv = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(priv)
    return cipher.decrypt(base64.b64decode(enc_key))
