from .base import BaseCipher

class PigpenCipher(BaseCipher):
    def __init__(self):
        self._map = {
            'A':'!', 'B':'@', 'C':'#', 'D':'$', 'E':'%',
            'F':'^', 'G':'&', 'H':'*', 'I':'(', 'J':')',
            'K':'-','L':'=','M':'+','N':'[','O':']',
            'P':'{','Q':'}','R':';','S':':','T':'<',
            'U':'>','V':'?','W':'/','X':'//','Y':'|','Z':'~'
        }
        self._rev = {v: k for k, v in self._map.items()}

    def encrypt(self, text, key=None):
        out = []
        for ch in text.upper():
            if ch.isalpha():
                out.append(self._map.get(ch, ''))
            else:
                out.append(ch)
        return ''.join(out)

    def decrypt(self, text, key=None):
        out = []
        for ch in text:
            out.append(self._rev.get(ch, ch))
        return ''.join(out)
