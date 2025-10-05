def encrypt(text, params):
    try:
        k = int(params.get('k', 2))
    except (ValueError, TypeError):
        k = 2  # boş veya geçersizse default

    if k <= 1:
        return text

    rail = [''] * k
    dir_down = False
    row = 0

    for char in text:
        rail[row] += char
        if row == 0 or row == k - 1:
            dir_down = not dir_down
        row += 1 if dir_down else -1

    return ''.join(rail)


def decrypt(cipher, params):
    try:
        k = int(params.get('k', 2))
    except (ValueError, TypeError):
        k = 2

    if k <= 1:
        return cipher

    n = len(cipher)
    rail = [['\n'] * n for _ in range(k)]
    dir_down = None
    row, col = 0, 0

    # İşaretleme
    for i in range(n):
        if row == 0:
            dir_down = True
        elif row == k - 1:
            dir_down = False
        rail[row][i] = '*'
        row += 1 if dir_down else -1

    # Harfleri yerleştirme
    index = 0
    for i in range(k):
        for j in range(n):
            if rail[i][j] == '*' and index < n:
                rail[i][j] = cipher[index]
                index += 1

    # Okuma
    result = ''
    row, col = 0, 0
    for i in range(n):
        result += rail[row][col]
        if row == 0:
            dir_down = True
        elif row == k - 1:
            dir_down = False
        row += 1 if dir_down else -1
        col += 1

    return result
