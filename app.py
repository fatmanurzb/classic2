from flask import Flask, render_template, request
from ciphers import caesar, substitution, affine, vigenere, playfair, railfence, rot

app = Flask(__name__)

algorithms = {
    'caesar': caesar,
    'substitution': substitution,
    'affine': affine,
    'vigenere': vigenere,
    'playfair': playfair,
    'railfence': railfence,
    'rot': rot
}

# Ana sayfa - şifreleme
@app.route('/')
def index_client():
    return render_template('index_client.html')

# Sunucu - deşifreleme
@app.route('/server')
def index_server():
    return render_template('index_server.html')

# Şifreleme sayfaları (GET ve POST)
@app.route('/<algo>', methods=['GET', 'POST'])
def encrypt_page(algo):
    if algo not in algorithms:
        return "Geçersiz algoritma", 404

    result = ''
    if request.method == 'POST':
        text = request.form['text']
        key = request.form.get('key', '')
        a = request.form.get('a', '')
        b = request.form.get('b', '')
        k = request.form.get('k', '')
        shift = request.form.get('shift', '')
        n = request.form.get('n', '')

        # Algoritmaya göre parametreleri geçir
        params = {'key': key, 'a': a, 'b': b, 'k': k, 'shift': shift, 'n': n}
        result = algorithms[algo].encrypt(text, params)

    return render_template(f'{algo}.html', result=result, mode='encrypt')

# Deşifreleme sayfaları (GET ve POST)
@app.route('/server/<algo>', methods=['GET', 'POST'])
def decrypt_page(algo):
    if algo not in algorithms:
        return "Geçersiz algoritma", 404

    result = ''
    if request.method == 'POST':
        text = request.form['text']
        key = request.form.get('key', '')
        a = request.form.get('a', '')
        b = request.form.get('b', '')
        k = request.form.get('k', '')
        shift = request.form.get('shift', '')
        n = request.form.get('n', '')

        params = {'key': key, 'a': a, 'b': b, 'k': k, 'shift': shift, 'n': n}
        result = algorithms[algo].decrypt(text, params)

    return render_template(f'{algo}.html', result=result, mode='decrypt')

if __name__ == "__main__":
    app.run(debug=True)
