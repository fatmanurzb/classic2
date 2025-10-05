def encrypt(text, params):
    try:
        n = int(params['n'])  # kullanıcı girişi zorunlu
    except (KeyError, ValueError, TypeError):
        return "Hata: Lütfen geçerli bir yatay uzunluk girin."

    if n <= 0:
        return "Hata: Yatay uzunluk pozitif olmalı."

    text = text.replace(" ", "")  # boşlukları kaldır
    total_len = len(text)
    rows = (total_len + n - 1) // n
    matrix = [['*' for _ in range(n)] for _ in range(rows)]

    idx = 0
    top, left = 0, 0
    bottom, right = rows - 1, n - 1

    while top <= bottom and left <= right:
        for i in range(left, right + 1):
            if idx < total_len:
                matrix[top][i] = text[idx]
                idx += 1
        top += 1
        for i in range(top, bottom + 1):
            if idx < total_len:
                matrix[i][right] = text[idx]
                idx += 1
        right -= 1
        for i in range(right, left - 1, -1):
            if idx < total_len:
                matrix[bottom][i] = text[idx]
                idx += 1
        bottom -= 1
        for i in range(bottom, top - 1, -1):
            if idx < total_len:
                matrix[i][left] = text[idx]
                idx += 1
        left += 1

    result = ''.join(''.join(row) for row in matrix)
    return result


def decrypt(text, params):
    try:
        n = int(params['n'])
    except (KeyError, ValueError, TypeError):
        return "Hata: Lütfen geçerli bir yatay uzunluk girin."

    if n <= 0:
        return "Hata: Yatay uzunluk pozitif olmalı."

    total_len = len(text)
    rows = (total_len + n - 1) // n
    matrix = [['*' for _ in range(n)] for _ in range(rows)]

    idx = 0
    for r in range(rows):
        for c in range(n):
            if idx < total_len:
                matrix[r][c] = text[idx]
                idx += 1

    result = ''
    top, left = 0, 0
    bottom, right = rows - 1, n - 1

    while top <= bottom and left <= right:
        # saat yönünün tersine spiral okuma
        for i in range(bottom, top - 1, -1):
            result += matrix[i][left]
        left += 1
        for i in range(left, right + 1):
            result += matrix[bottom][i]
        bottom -= 1
        for i in range(bottom, top - 1, -1):
            result += matrix[i][right]
        right -= 1
        for i in range(right, left - 1, -1):
            result += matrix[top][i]
        top += 1

    return result
