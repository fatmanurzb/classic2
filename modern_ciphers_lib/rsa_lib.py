from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# RSA anahtar çifti üret (2048 bit)
_key = RSA.generate(2048)

PRIVATE_KEY = _key.export_key()
PUBLIC_KEY = _key.publickey().export_key()

def rsa_encrypt_key(sym_key: bytes, public_key: bytes) -> str:
    """
    Simetrik anahtarı RSA public key ile şifreler.
    Geriye base64 encoded string döner.
    """
    try:
        rsa_key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        encrypted = cipher.encrypt(sym_key)
        return base64.b64encode(encrypted).decode()

    except Exception as e:
        raise ValueError(f"RSA encrypt hatası: {e}")


def rsa_decrypt_key(enc_key: str, private_key: bytes) -> bytes:
    """
    RSA ile şifrelenmiş (base64) simetrik anahtarı çözer.
    Geriye bytes döner.
    """
    try:
        rsa_key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        decoded = base64.b64decode(enc_key)
        return cipher.decrypt(decoded)

    except Exception as e:
        raise ValueError(f"RSA decrypt hatası: {e}")
