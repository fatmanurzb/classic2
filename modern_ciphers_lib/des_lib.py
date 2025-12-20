from Crypto.Cipher import DES
import base64

def generate_key():
    return b"8bytekey"  # 8 byte

def des_encrypt(msg, key):
    cipher = DES.new(key, DES.MODE_ECB)
    padded = msg + " " * (8 - len(msg) % 8)
    return base64.b64encode(cipher.encrypt(padded.encode())).decode()

def des_decrypt(enc_msg, key):
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.decrypt(base64.b64decode(enc_msg)).decode().strip()
