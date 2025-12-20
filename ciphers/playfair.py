from .base import BaseCipher


class PlayfairCipher(BaseCipher):

    def _generate_matrix(self, key):
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

        return [matrix[i:i + 5] for i in range(0, 25, 5)]

    def _prepare_text(self, text):
        text = text.upper().replace('J', 'I')
        prepared = ""
        i = 0

        while i < len(text):
            a = text[i]
            b = text[i + 1] if i + 1 < len(text) else ""

            if not a.isalpha():
                i += 1
                continue

            if b and b.isalpha():
                if a == b:
                    prepared += a + "X"
                    i += 1
                else:
                    prepared += a + b
                    i += 2
            else:
                prepared += a
                i += 1

        if len(prepared) % 2 != 0:
            prepared += "X"

        return prepared

    def _find_position(self, matrix, char):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == char:
                    return r, c
                
        raise ValueError(f"Playfair matrisinde karakter bulunamadı: {char}")

    def encrypt(self, text, key=None):
        if not key:
            return "Hata: Lütfen bir anahtar girin."

        matrix = self._generate_matrix(key)
        text = self._prepare_text(text)
        result = ""

        try:
            for i in range(0, len(text), 2):
                a, b = text[i], text[i + 1]
                r1, c1 = self._find_position(matrix, a)
                r2, c2 = self._find_position(matrix, b)

                if r1 == r2:
                    result += matrix[r1][(c1 + 1) % 5]
                    result += matrix[r2][(c2 + 1) % 5]

                elif c1 == c2:
                    result += matrix[(r1 + 1) % 5][c1]
                    result += matrix[(r2 + 1) % 5][c2]

                else:
                    result += matrix[r1][c2]
                    result += matrix[r2][c1]

            return result

        except ValueError as e:
            return f"Hata: {e}"

    def decrypt(self, text, key=None):
        if not key:
            return "Hata: Lütfen bir anahtar girin."

        matrix = self._generate_matrix(key)
        result = ""

        try:
            for i in range(0, len(text), 2):
                a, b = text[i], text[i + 1]
                r1, c1 = self._find_position(matrix, a)
                r2, c2 = self._find_position(matrix, b)

                if r1 == r2:
                    result += matrix[r1][(c1 - 1) % 5]
                    result += matrix[r2][(c2 - 1) % 5]

                elif c1 == c2:
                    result += matrix[(r1 - 1) % 5][c1]
                    result += matrix[(r2 - 1) % 5][c2]

                else:
                    result += matrix[r1][c2]
                    result += matrix[r2][c1]

            return result

        except ValueError as e:
            return f"Hata: {e}"
