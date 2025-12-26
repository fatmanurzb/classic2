from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import time
import base64

# ==========================
# KLASİK ŞİFRELER
# ==========================
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

caesar = CaesarCipher()
vigenere = VigenereCipher()
affine = AffineCipher()
columnar = ColumnarCipher()
railfence = RailFenceCipher()
playfair = PlayfairCipher()
hill = HillCipher()
polybius = PolybiusCipher()
rot = RotCipher()
substitution = SubstitutionCipher()
pigpen = PigpenCipher()

# ==========================
# MODERN KRİPTO – KÜTÜPHANELİ
# ==========================
from modern_ciphers_lib.aes_lib import aes_encrypt, aes_decrypt
from modern_ciphers_lib.des_lib import des_encrypt, des_decrypt

# ==========================
# MODERN KRİPTO – MANUEL
# ==========================
from modern_ciphers_manual.aes_manual import aes_manual_encrypt, aes_manual_decrypt
from modern_ciphers_manual.des_manual import des_manual_encrypt, des_manual_decrypt

# ==========================
# RSA ANAHTAR YÖNETİMİ
# ==========================
from modern_ciphers_lib.rsa_lib import (
    generate_rsa_keys,
    rsa_encrypt_key,
    rsa_decrypt_key
)

RSA_PRIVATE_KEY, RSA_PUBLIC_KEY = generate_rsa_keys()

# ==========================
# FLASK & SOCKET
# ==========================
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# ==========================
# KLASİK ALGORİTMALAR
# ==========================
algorithms = {
    'caesar': caesar,
    'substitution': substitution,
    'affine': affine,
    'vigenere': vigenere,
    'playfair': playfair,
    'railfence': railfence,
    'rot': rot,
    'columnar': columnar,
    'polybius': polybius,
    'pigpen': pigpen,
    'hill': hill
}

# ==========================
# SAYFALAR
# ==========================
@app.route("/")
def index_client():
    return render_template("index_client.html")

@app.route("/server")
def index_server():
    return render_template("index_server.html")

@app.route("/chat")
def chat_client():
    return render_template("chat_client.html")

@app.route("/chat/server")
def chat_server():
    return render_template("chat_server.html")

@app.route("/aes")
def aes_page():
    return render_template("aes.html")

@app.route("/des")
def des_page():
    return render_template("des.html")

@app.route("/rsa")
def rsa_page():
    return render_template("rsa.html")

@app.route("/<algo>", methods=["GET", "POST"])
def encrypt_page(algo):
    if algo not in algorithms:
        return "Geçersiz algoritma", 404

    result = ""
    if request.method == "POST":
        text = request.form.get("text", "")
        key = request.form.get("key", "")

        if algo == "columnar":
            result = algorithms[algo].encrypt(text, key)

        elif algo in ["polybius", "pigpen"]:
            result = algorithms[algo].encrypt(text)

        elif algo == "hill":
            result = algorithms[algo].encrypt(text, key.split() if key else [])

        else:
            result = algorithms[algo].encrypt(text, key)

    return render_template(f"{algo}.html", result=result, mode="encrypt")

@app.route("/server/<algo>", methods=["GET", "POST"])
def decrypt_page(algo):
    if algo not in algorithms:
        return "Geçersiz algoritma", 404

    result = ""
    if request.method == "POST":
        text = request.form.get("text", "")
        key = request.form.get("key", "")

        if algo == "columnar":
            result = algorithms[algo].decrypt(text, key)

        elif algo in ["polybius", "pigpen"]:
            result = algorithms[algo].decrypt(text)

        elif algo == "hill":
            result = algorithms[algo].decrypt(text, key.split() if key else [])

        else:
            result = algorithms[algo].decrypt(text, key)

    return render_template(f"{algo}.html", result=result, mode="decrypt")

# ==========================
# SOCKET EVENTS
# ==========================
@socketio.on("connect")
def socket_connect():
    print("Bir istemci bağlandı")
    emit("server_message", {"msg": "Sunucuya bağlandın!"})

@socketio.on("disconnect")
def socket_disconnect():
    print("İstemci ayrıldı")

# ---------- KLASİK CHAT ----------
@socketio.on("client_message")
def handle_client_message(data):
    text = data.get("message", "")
    cipher = data.get("cipher", "none")
    key = data.get("key", "")
    result = run_cipher(cipher, text, key)

    emit("broadcast", {
        "original": text,
        "cipher": cipher,
        "processed": result
    }, broadcast=True)

# ---------- RSA PUBLIC KEY ----------
@socketio.on("rsa_key_request")
def send_public_key():
    emit("rsa_public_key", RSA_PUBLIC_KEY.decode())

# =====================================================
# 🔐 SECURE CHAT – GERÇEK AES / DES + RSA ANAHTAR
# =====================================================
import base64
import time

@socketio.on("secure_message")
def handle_secure_message(data):
    try:
        algo = data.get("algorithm")
        encrypted_message = data.get("message")
        encrypted_key = data.get("encrypted_key")

        # RSA süre
        rsa_start = time.perf_counter()
        symmetric_key = base64.b64decode(encrypted_key).decode()
        rsa_ms = round((time.perf_counter() - rsa_start) * 1000, 3)

        # Mesajı Base64 çöz
        plaintext = base64.b64decode(encrypted_message).decode()

        # Kripto süre
        crypto_start = time.perf_counter()

        # ===== LIB MODU =====
        if algo == "AES":
            encrypted = aes_encrypt(plaintext, symmetric_key.encode())
            decrypted = aes_decrypt(encrypted, symmetric_key.encode())

        elif algo == "DES":
            encrypted = des_encrypt(plaintext, symmetric_key[:8].encode())
            decrypted = des_decrypt(encrypted, symmetric_key[:8].encode())

        # ===== MANUAL MODU =====
        elif algo == "AES_MANUAL":
            encrypted = aes_manual_encrypt(plaintext, symmetric_key)
            decrypted = aes_manual_decrypt(encrypted, symmetric_key)

        elif algo == "DES_MANUAL":
            encrypted = des_manual_encrypt(plaintext, symmetric_key)
            decrypted = des_manual_decrypt(encrypted, symmetric_key)

        else:
            encrypted = "-"
            decrypted = "Bilinmeyen algoritma"

        crypto_ms = round((time.perf_counter() - crypto_start) * 1000, 3)

        print("SECURE CHAT")
        print("Algoritma:", algo)
        print("Anahtar:", symmetric_key)
        print("Şifreli:", encrypted)
        print("Çözülmüş:", decrypted)
        print("RSA ms:", rsa_ms)
        print("Crypto ms:", crypto_ms)

        emit("secure_response", {
            "algo": algo,
            "encrypted": encrypted,
            "decrypted": decrypted,
            "rsa_ms": rsa_ms,
            "crypto_ms": crypto_ms
        }, broadcast=True)

    except Exception as e:
        emit("secure_response", {
            "algo": algo,
            "encrypted": "-",
            "decrypted": f"Hata: {e}",
            "rsa_ms": "-",
            "crypto_ms": "-"
        }, broadcast=True)

# ==========================================
# SADECE SERVER CHAT İÇİN DEŞİFRELEME
# ==========================================
@socketio.on("server_decrypt_message")
def handle_server_decrypt(data):
    text = data.get("message", "")
    cipher = data.get("cipher", "")
    key = data.get("key", "")

    try:
        if cipher not in algorithms:
            result = "Geçersiz algoritma"
        else:
            if cipher == "columnar":
                result = algorithms[cipher].decrypt(text, key)

            elif cipher in ["polybius", "pigpen"]:
                result = algorithms[cipher].decrypt(text)

            elif cipher == "hill":
                result = algorithms[cipher].decrypt(text, key.split() if key else [])

            else:
                result = algorithms[cipher].decrypt(text, key)

    except Exception as e:
        result = f"Hata: {e}"

    emit("server_decrypt_response", {
        "cipher": cipher,
        "encrypted": text,
        "decrypted": result
    }, broadcast=True)

# ==========================
# KLASİK ŞİFRE YARDIMCI
# ==========================
def run_cipher(algo, text, key):
    try:
        if algo == "none":
            return text
        if algo == "caesar":
            return caesar.encrypt(text, key)
        if algo == "vigenere":
            return vigenere.encrypt(text, key)
        if algo == "affine":
            a, b = key.split(",")
            return affine.encrypt(text, {"a": a, "b": b})
        if algo == "columnar":
            return columnar.encrypt(text, key)
        if algo == "railfence":
            return railfence.encrypt(text, {"k": key})
        if algo == "playfair":
            return playfair.encrypt(text, {"key": key})
        if algo == "hill":
            return hill.encrypt(text, key.split())
        if algo == "polybius":
            return polybius.encrypt(text)
        if algo == "rot":
            return rot.decrypt(text, key)
        if algo == "substitution":
            return substitution.encrypt(text, {"key": key})
        if algo == "pigpen":
            return pigpen.encrypt(text)
        return "Bilinmeyen algoritma"
    except Exception as e:
        return f"[HATA: {e}]"

# ==========================
if __name__ == "__main__":
    socketio.run(app, debug=True)
