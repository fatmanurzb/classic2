from flask import Flask, render_template, request
from ciphers import caesar, substitution, affine, vigenere, playfair, railfence, rot
from ciphers import columnar, polybius, pigpen, hill  # yeni eklenen cipher modülleri

app = Flask(__name__)

# Tüm algoritmalar burada birleştirildi
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

# Ana sayfa - Şifreleme
@app.route('/')
def index_client():
    return render_template('index_client.html')

# Sunucu - Deşifreleme
@app.route('/server')
def index_server():
    return render_template('index_server.html')

# Şifreleme sayfaları (GET & POST)
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

    return render_template(f'{algo}.html', result=result, mode='encrypt')

# Deşifreleme sayfaları (GET & POST)
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

    return render_template(f'{algo}.html', result=result, mode='decrypt')

if __name__ == "__main__":
    app.run(debug=True)
