from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

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
# MODERN KRİPTO - KÜTÜPHANELİ
# ==========================
from modern_ciphers_lib.aes_lib import aes_encrypt, aes_decrypt
from modern_ciphers_lib.des_lib import des_encrypt, des_decrypt

# ==========================
# MODERN KRİPTO - MANUEL
# ==========================
from modern_ciphers_manual.aes_manual import aes_manual_encrypt, aes_manual_decrypt
from modern_ciphers_manual.des_manual import des_manual_encrypt, des_manual_decrypt

# ==========================
# RSA ANAHTAR YÖNETİMİ
# ==========================
from key_manager import PUBLIC_KEY, PRIVATE_KEY

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
@app.route("/aes", methods=["GET", "POST"])
def aes_page():
    return render_template("aes.html")

@app.route("/des", methods=["GET", "POST"])
def des_page():
    return render_template("des.html")

@app.route("/rsa", methods=["GET", "POST"])
def rsa_page():
    return render_template("rsa.html")


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
    emit("rsa_public_key", PUBLIC_KEY.decode())

# ---------- SECURE CHAT (DEMO UYUMLU) ----------
@socketio.on("secure_message")
def handle_secure_message(data):
    algo = data.get("algorithm")
    encrypted_message = data.get("message")
    symmetric_key = data.get("encrypted_key")

    try:
        if algo == "AES":
            decrypted = aes_decrypt(encrypted_message, symmetric_key.encode())

        elif algo == "DES":
            decrypted = des_decrypt(encrypted_message, symmetric_key[:8].encode())

        elif algo == "AES_MANUAL":
            decrypted = aes_manual_decrypt(encrypted_message, symmetric_key)

        elif algo == "DES_MANUAL":
            decrypted = des_manual_decrypt(encrypted_message, symmetric_key)

        else:
            decrypted = "Bilinmeyen algoritma"

    except Exception as e:
        decrypted = f"Hata: {e}"

    print("ÇÖZÜLMÜŞ MESAJ:", decrypted)

    emit("secure_response", {
        "status": "OK",
        "decrypted": decrypted
    }, broadcast=True)

# ==========================
# KLASİK ŞİFRE SAYFALARI
# ==========================
@app.route("/<algo>", methods=["GET", "POST"])
def encrypt_page(algo):
    if algo not in algorithms:
        return "Geçersiz algoritma", 404

    result = ""
    if request.method == "POST":
        text = request.form.get("text", "")
        key = request.form.get("key", "")
        params = request.form.to_dict()

        if algo == "columnar":
            result = algorithms[algo].encrypt(text, key)
        elif algo in ["polybius", "pigpen"]:
            result = algorithms[algo].encrypt(text)
        elif algo == "hill":
            result = algorithms[algo].encrypt(text, key.split())
        else:
            result = algorithms[algo].encrypt(text, params)

    return render_template(f"{algo}.html", result=result, mode="encrypt")

@app.route("/server/<algo>", methods=["GET", "POST"])
def decrypt_page(algo):
    if algo not in algorithms:
        return "Geçersiz algoritma", 404

    result = ""
    if request.method == "POST":
        text = request.form.get("text", "")
        key = request.form.get("key", "")
        params = request.form.to_dict()

        if algo == "columnar":
            result = algorithms[algo].decrypt(text, key)
        elif algo in ["polybius", "pigpen"]:
            result = algorithms[algo].decrypt(text)
        elif algo == "hill":
            result = algorithms[algo].decrypt(text, key.split())
        else:
            result = algorithms[algo].decrypt(text, params)

    return render_template(f"{algo}.html", result=result, mode="decrypt")

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
            if key and "," in key:
                a, b = key.split(",")
                return affine.encrypt(text, {"a": a, "b": b})
            return "Hata: Affine için a,b formatında anahtar girin"

        if algo == "columnar":
            return columnar.encrypt(text, key)

        if algo == "railfence":
            return railfence.encrypt(text, {"k": key})

        if algo == "playfair":
            return playfair.encrypt(text, {"key": key})

        if algo == "hill":
            return hill.encrypt(text, key.split() if key else [])

        if algo == "polybius":
            return polybius.encrypt(text)

        if algo == "rot":
            return rot.encrypt(text)

        if algo == "substitution":
            return substitution.encrypt(text, {"key": key})

        if algo == "pigpen":
            return pigpen.encrypt(text)

        return "Bilinmeyen algoritma"

    except Exception as e:
        return f"[HATA: {e}]"

if __name__ == "__main__":
    socketio.run(app, debug=True)
