def generate_matrix(key):
    key = key.upper().replace('J', 'I')
    matrix = []
    used = set()
    for char in key:
        if char.isalpha() and char not in used:
            matrix.append(char)
            used.add(char)
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in used:
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def prepare_text(text, encrypting=True):
    text = text.upper().replace('J','I')
    prepared = ''
    i = 0
    while i < len(text):
        char1 = text[i]
        char2 = ''
        if i+1 < len(text):
            char2 = text[i+1]
        if char1.isalpha():
            if char2.isalpha():
                if char1 == char2:
                    prepared += char1 + 'X'
                    i += 1
                else:
                    prepared += char1 + char2
                    i += 2
            else:
                prepared += char1
                i += 1
        else:
            i += 1
    if len(prepared) % 2 != 0:
        prepared += 'X'
    return prepared

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return i, j
    return None

def encrypt(text, params):
    key = params.get('key', '')
    if not key:
        return "Hata: Lütfen bir anahtar girin."

    matrix = generate_matrix(key)
    text = prepare_text(text)
    result = ''

    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:
            result += matrix[row1][(col1+1)%5] + matrix[row2][(col2+1)%5]
        elif col1 == col2:
            result += matrix[(row1+1)%5][col1] + matrix[(row2+1)%5][col2]
        else:
            result += matrix[row1][col2] + matrix[row2][col1]

    return result

def decrypt(text, params):
    key = params.get('key', '')
    if not key:
        return "Hata: Lütfen bir anahtar girin."

    matrix = generate_matrix(key)
    text = prepare_text(text, encrypting=False)
    result = ''

    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:
            result += matrix[row1][(col1-1)%5] + matrix[row2][(col2-1)%5]
        elif col1 == col2:
            result += matrix[(row1-1)%5][col1] + matrix[(row2-1)%5][col2]
        else:
            result += matrix[row1][col2] + matrix[row2][col1]

    return result
