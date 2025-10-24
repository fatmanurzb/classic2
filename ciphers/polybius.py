# ciphers/polybius.py

poly = [
    ['A','B','C','D','E'],
    ['F','G','H','I','K'],
    ['L','M','N','O','P'],
    ['Q','R','S','T','U'],
    ['V','W','X','Y','Z']
]

char_to_code = {}
code_to_char = {}
for r in range(5):
    for c in range(5):
        ch = poly[r][c]
        code = f"{r+1}{c+1}"
        char_to_code[ch] = code
        code_to_char[code] = ch
char_to_code['J'] = char_to_code['I']

def encrypt(text: str):
    out = []
    for ch in text.upper():
        if ch.isalpha():
            out.append(char_to_code.get(ch, ''))
    return ' '.join(out)

def decrypt(code_str: str):
    digits = ''.join(code_str.split())
    if len(digits) % 2 != 0:
        return "Geçersiz kod uzunluğu!"
    out = []
    for i in range(0, len(digits), 2):
        pair = digits[i:i+2]
        ch = code_to_char.get(pair, '')
        out.append(ch)
    return ''.join(out)
