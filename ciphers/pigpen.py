# ciphers/pigpen.py
# Gerçek semboller yerine ASCII karakterlerle temsil

_map = {
 'A':'!', 'B':'@', 'C':'#', 'D':'$', 'E':'%',
 'F':'^', 'G':'&', 'H':'*', 'I':'(', 'J':')',
 'K':'-','L':'=','M':'+','N':'[','O':']',
 'P':'{','Q':'}','R':';','S':':','T':'<',
 'U':'>','V':'?','W':'/','X':'//','Y':'|','Z':'~'
}
_rev = {v:k for k,v in _map.items()}

def encrypt(text: str):
    out = []
    for ch in text.upper():
        if ch.isalpha():
            out.append(_map.get(ch, ''))
    return ''.join(out)

def decrypt(ciphertext: str):
    out = []
    for ch in ciphertext:
        out.append(_rev.get(ch, ''))
    return ''.join(out)
