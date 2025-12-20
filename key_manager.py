from Crypto.PublicKey import RSA

# RSA anahtar çifti üret (2048 bit)
_key = RSA.generate(2048)

PRIVATE_KEY = _key.export_key()
PUBLIC_KEY = _key.publickey().export_key()
