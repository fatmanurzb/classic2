from .base import BaseCipher


class RotCipher(BaseCipher):

    def _get_n(self, key):
        try:
            n = int(key)
            if n <= 0:
                return None
            return n
        except (ValueError, TypeError):
            return None

    def encrypt(self, text, key=None):
        n = self._get_n(key)
        if n is None:
            return "Hata: Lütfen geçerli bir yatay uzunluk girin."

        text = text.replace(" ", "")
        total_len = len(text)
        rows = (total_len + n - 1) // n

        matrix = [['*'] * n for _ in range(rows)]

        idx = 0
        top, left = 0, 0
        bottom, right = rows - 1, n - 1

        # Saat yönünde spiral doldurma
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

        return ''.join(''.join(row) for row in matrix)

    def decrypt(self, text, key=None):
        n = self._get_n(key)
        if n is None:
            return "Hata: Lütfen geçerli bir yatay uzunluk girin."

        total_len = len(text)
        rows = (total_len + n - 1) // n

        matrix = [['*'] * n for _ in range(rows)]

        idx = 0
        for r in range(rows):
            for c in range(n):
                if idx < total_len:
                    matrix[r][c] = text[idx]
                    idx += 1

        result = []
        top, left = 0, 0
        bottom, right = rows - 1, n - 1

        # Saat yönünün tersine spiral okuma
        while top <= bottom and left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1

            for i in range(left, right + 1):
                result.append(matrix[bottom][i])
            bottom -= 1

            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][right])
            right -= 1

            for i in range(right, left - 1, -1):
                result.append(matrix[top][i])
            top += 1

        return ''.join(result)
