from .base import BaseCipher


class RailFenceCipher(BaseCipher):

    def _get_k(self, key):
        try:
            k = int(key)
            if k <= 1:
                return 1
            return k
        except (ValueError, TypeError):
            return 2  # default

    def encrypt(self, text, key=None):
        k = self._get_k(key)

        if k <= 1:
            return text

        rail = [''] * k
        row = 0
        dir_down = False

        for ch in text:
            rail[row] += ch

            if row == 0 or row == k - 1:
                dir_down = not dir_down

            row += 1 if dir_down else -1

        return ''.join(rail)

    def decrypt(self, text, key=None):
        k = self._get_k(key)

        if k <= 1:
            return text

        n = len(text)
        rail = [['\n'] * n for _ in range(k)]

        row = 0
        dir_down = None

        # Zikzak işaretleme
        for col in range(n):
            if row == 0:
                dir_down = True
            elif row == k - 1:
                dir_down = False

            rail[row][col] = '*'
            row += 1 if dir_down else -1

        # Harfleri yerleştir
        index = 0
        for i in range(k):
            for j in range(n):
                if rail[i][j] == '*' and index < n:
                    rail[i][j] = text[index]
                    index += 1

        # Okuma
        result = []
        row = 0
        for col in range(n):
            result.append(rail[row][col])

            if row == 0:
                dir_down = True
            elif row == k - 1:
                dir_down = False

            row += 1 if dir_down else -1

        return ''.join(result)
