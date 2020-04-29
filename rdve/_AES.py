import sys
import base64
from Cryptodome.Cipher import AES


class CifrarComAES(object):
    def __init__(self, key):
        self.bs = 16
        self.cipher = AES.new(key, AES.MODE_ECB)

    def criptografar(self, raw):
        raw = self._pad(raw)
        encrypted = self.cipher.encrypt(raw)
        encoded = base64.b64encode(encrypted)
        return str(encoded, 'utf-8')

    def decriptar(self, raw):
        decoded = base64.b64decode(raw)
        decrypted = self.cipher.decrypt(decoded)
        return str(self._unpad(decrypted), 'utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]