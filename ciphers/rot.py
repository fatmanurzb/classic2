class RotCipher:
    def __init__(self):
        pass

    def encrypt(self, text: str, n: int):
        if not isinstance(n, int) or n <= 0:
            return "Hata: Lütfen geçerli bir yatay uzunluk girin."

        text = text.replace(" ", "")
        total_len = len(text)
        rows = (total_len + n - 1) // n  # satır sayısı
        matrix = [[''] * n for _ in range(rows)]

        idx = 0
        top, left = 0, 0
        bottom, right = rows - 1, n - 1

        # Saat yönünde spiral doldurma
        while idx < total_len:
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

        # Matrisi satır satır birleştirip döndür
        return ''.join(''.join(cell for cell in row if cell) for row in matrix)

    def decrypt(self, text: str, n: int):
        if not isinstance(n, int) or n <= 0:
            return "Hata: Lütfen geçerli bir yatay uzunluk girin."

        total_len = len(text)
        rows = (total_len + n - 1) // n
        matrix = [[''] * n for _ in range(rows)]

        # Spiral sırayla indeksleri belirle
        indices = []
        top, left = 0, 0
        bottom, right = rows - 1, n - 1

        while len(indices) < total_len:
            for i in range(left, right + 1):
                if len(indices) < total_len:
                    indices.append((top, i))
            top += 1

            for i in range(top, bottom + 1):
                if len(indices) < total_len:
                    indices.append((i, right))
            right -= 1

            for i in range(right, left - 1, -1):
                if len(indices) < total_len:
                    indices.append((bottom, i))
            bottom -= 1

            for i in range(bottom, top - 1, -1):
                if len(indices) < total_len:
                    indices.append((i, left))
            left += 1

        # Texti matrise spiral sırayla yerleştir
        for idx, (r, c) in enumerate(indices):
            matrix[r][c] = text[idx]

        # Matrisi satır satır oku
        result = ''.join(matrix[r][c] for r in range(rows) for c in range(n) if matrix[r][c])
        return result


