from flask import Flask, render_template,request
from flask_socketio import SocketIO, emit
from ciphers import caesar, substitution, affine, vigenere, playfair, railfence, rot
from ciphers import columnar, polybius, pigpen, hill  # yeni cipher modülleri
# ==========================
# MODERN KRİPTO (YENİ)
# ==========================
from modern_ciphers_lib import aes_lib, des_lib, rsa_lib
from modern_ciphers_manuel import aes_manuel, des_manuel
from key_manager import PRIVATE_KEY, PUBLIC_KEY


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# ==========================
#  TÜM ŞİFRELEME ALGORİTMALARI
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



# ============================================================
#  1) CLIENT - SERVER CHAT SAYFALARI (SOCKET)
# ============================================================

@app.route('/')
def index_client():
    return render_template('index_client.html')

@app.route('/server')
def index_server():
    return render_template('index_server.html')

@app.route('/chat')
def chat_client():
    return render_template('chat_client.html')

@app.route('/chat/server')
def chat_server():
    return render_template('chat_server.html')



# =======================
# SOCKET: MESAJ AL / GÖNDER
# =======================

@socketio.on("connect")
def socket_connect():
    print("Bir istemci bağlandı")
    emit("server_message", {"msg": "Sunucuya bağlandın!"})


@socketio.on("client_message")
def handle_message(data):
    """
    data = {
        "message": "...",
        "cipher": "caesar",
        "key": "...",
    }
    """
    text = data.get("message", "")
    cipher = data.get("cipher", "none")
    key = data.get("key", "")

    # Şifreleme çalıştır
    processed = run_cipher(cipher, text, key)

    emit("broadcast", {
        "original": text,
        "cipher": cipher,
        "processed": processed,
        "key": key
    }, broadcast=True)

@socketio.on("secure_message")
def handle_secure_message(data):
    """
    data = {
        "algorithm": "AES" | "DES" | "AES_MANUAL" | "DES_MANUAL",
        "encrypted_key": "...",   # RSA ile şifreli
        "message": "..."
    }
    """

    algo = data.get("algorithm")
    enc_key = data.get("encrypted_key")
    message = data.get("message")

    # RSA ile anahtarı çöz
    sym_key = rsa_lib.decrypt_key(enc_key, PRIVATE_KEY)

    # Mesajı çöz
    if algo == "AES":
        plain = aes_lib.decrypt(message, sym_key)

    elif algo == "DES":
        plain = des_lib.decrypt(message, sym_key[:8])

    elif algo == "AES_MANUAL":
        plain = aes_manuel.decrypt(message, sym_key.decode())

    elif algo == "DES_MANUAL":
        plain = des_manuel.decrypt(message, sym_key.decode())

    else:
        plain = "[Bilinmeyen algoritma]"

    print("🔓 ÇÖZÜLMÜŞ MESAJ:", plain)

    # ACK gönder
    emit("secure_response", {
        "status": "OK",
        "decrypted": plain
    }, broadcast=True)

@socketio.on("disconnect")
def socket_disconnect():
    print("İstemci ayrıldı")


@socketio.on("rsa_key_request")
def send_public_key():
    emit("rsa_public_key", PUBLIC_KEY.decode())


# ============================================================
#  2) BÜTÜN ŞİFRELEME / DEŞİFRELEME SAYFALARI (ÖNCEKİ KODUN)
# ============================================================

@app.route('/<algo>', methods=['GET', 'POST'])
def encrypt_page(algo):
    if algo not in algorithms:
        return "Geçersiz algoritma", 404

    result = ''

    if request.method == 'POST':
        text = request.form.get('text', '')
        key = request.form.get('key', '')
        a = request.form.get('a', '')
        b = request.form.get('b', '')
        k = request.form.get('k', '')
        shift = request.form.get('shift', '')
        n = request.form.get('n', '')

        params = {'key': key, 'a': a, 'b': b, 'k': k, 'shift': shift, 'n': n}

        if algo == 'columnar':
            result = algorithms[algo].encrypt(text, key)

        elif algo == 'polybius':
            result = algorithms[algo].encrypt(text)

        elif algo == 'pigpen':
            result = algorithms[algo].encrypt(text)

        elif algo == 'hill':
            key_values = key.split() if key else []
            result = algorithms[algo].encrypt(text, key_values)

        else:
            result = algorithms[algo].encrypt(text, params)

    return render_template(f"{algo}.html", result=result, mode="encrypt")


@app.route('/server/<algo>', methods=['GET', 'POST'])
def decrypt_page(algo):
    if algo not in algorithms:
        return "Geçersiz algoritma", 404

    result = ''

    if request.method == 'POST':
        text = request.form.get('text', '')
        key = request.form.get('key', '')
        a = request.form.get('a', '')
        b = request.form.get('b', '')
        k = request.form.get('k', '')
        shift = request.form.get('shift', '')
        n = request.form.get('n', '')

        params = {'key': key, 'a': a, 'b': b, 'k': k, 'shift': shift, 'n': n}

        if algo == 'columnar':
            result = algorithms[algo].decrypt(text, key)

        elif algo == 'polybius':
            result = algorithms[algo].decrypt(text)

        elif algo == 'pigpen':
            result = algorithms[algo].decrypt(text)

        elif algo == 'hill':
            key_values = key.split() if key else []
            result = algorithms[algo].decrypt(text, key_values)

        else:
            result = algorithms[algo].decrypt(text, params)

    return render_template(f"{algo}.html", result=result, mode="decrypt")

@app.route("/aes", methods=["GET", "POST"])
def aes_page():
    result = ""
    if request.method == "POST":
        text = request.form["text"]
        key = request.form["key"].encode()
        result = aes_lib.encrypt(text, key)
    return render_template("aes.html", result=result)


@app.route("/des", methods=["GET", "POST"])
def des_page():
    result = ""
    if request.method == "POST":
        text = request.form["text"]
        key = request.form["key"].encode()
        result = des_lib.encrypt(text, key)
    return render_template("des.html", result=result)


@app.route("/rsa", methods=["GET", "POST"])
def rsa_page():
    encrypted = ""
    if request.method == "POST":
        key = request.form["key"].encode()
        encrypted = rsa_lib.encrypt_key(key, PUBLIC_KEY)
    return render_template("rsa.html", encrypted=encrypted)


# ============================================================
#  ORTAK ŞİFRELEME FONKSİYONU — Socket için
# ============================================================

def run_cipher(algo, text, key):
    if algo == "none":
        return text

    try:
        if algo == "caesar":
            shift = int(key) if key else 3
            return caesar.encrypt(text, {"shift": shift})

        if algo == "vigenere":
            return vigenere.encrypt(text, {"key": key})

        if algo == "affine":
            a, b = (5,8)
            if "," in key:
                a, b = map(int, key.split(","))
            return affine.encrypt(text, {"a": a, "b": b})

        if algo == "columnar":
            return columnar.encrypt(text, key)

        if algo == "railfence":
            return railfence.encrypt(text, {"n": key})

        if algo == "playfair":
            return playfair.encrypt(text, {"key": key})

        if algo == "hill":
            return hill.encrypt(text, key.split())

        if algo == "polybius":
            return polybius.encrypt(text)

        if algo == "rot":
            return rot.encrypt(text, {})

        if algo == "substitution":
            return substitution.encrypt(text, {"key": key})

        if algo == "pigpen":
            return pigpen.encrypt(text)

    except Exception as e:
        return f"[HATA: {e}]"

    return text



# ============================================================

if __name__ == "__main__":
    socketio.run(app, debug=True)
