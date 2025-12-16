from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def generate_key():
    return get_random_bytes(16)  # AES-128

def encrypt(msg, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode())
    return base64.b64encode(cipher.nonce + ciphertext).decode()

def decrypt(enc_msg, key):
    raw = base64.b64decode(enc_msg)
    nonce = raw[:16]
    ciphertext = raw[16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode()
