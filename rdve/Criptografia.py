import os, ecdsa, base58, binascii, hashlib, io, qrcode
from ecdsa import SigningKey, VerifyingKey, curves, SECP256k1
from Cryptodome.Protocol.KDF import scrypt
from AES import CifrarComAES

class Criptografia:

    def gerarChavePrivada(self):
        _sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        return _sk

    def exportarChavePrivada(self, chave, arquivo):
        _arq = open(arquivo, "wb")
        _arq.write(chave.to_pem())
        _arq.close()

    def gerarChavePublica(self, chavePrivada):
        if isinstance(chavePrivada, io.IOBase):
            _arq = open(chavePrivada, "rb")
            _sk = SigningKey.from_pem(_arq.read())
        elif isinstance(chavePrivada, str):
            _sk = SigningKey.from_pem(bytearray.fromhex(chavePrivada))
        _vk = _sk.verifying_key
        return _vk
        
    def exportarChavePublica(self, chavePublica, arquivo):
        try:
            _arq = open(arquivo, "rb")
        except IOError:
            print("Arquivo inexistente")
        finally:
            _arq.close()

    def importarChavePrivada(self, chave):
        try:
            if isinstance(chave, io.IOBase):
                _arq = open(chave, "rb")
                chavePrivada = SigningKey.from_pem(_arq.read())
            elif isinstance(chave, str):
                chavePrivada = SigningKey.from_string(bytearray.fromhex(chave))
            return chavePrivada
        except IOError:
            print("Arquivo inexistente")
        finally:
            _arq.close()

    def importarChavePublica(self, chave):
        try:
            if isinstance(chave, io.IOBase):
                _arq = open(chave, "rb")
                chavePublica = VerifyingKey.from_pem(_arq.read())
            elif isinstance(chave, str):
                chavePublica = VerifyingKey.from_string(bytearray.fromhex(chave))
            return chavePublica
        except IOError:
            print("Arquivo inexistente")
        finally:
            _arq.close()

    def ripemd160(self, x):
        d = hashlib.new('ripemd160')
        d.update(x)
        return d

    def hashSenha(self, senha, sal):
        _s = scrypt(senha.encode(), sal, 32, N=2**16, r=8, p=8)
        return _s
        
    def encriptarChaveAES(self, chave, senha, sal):
        chaveAES = self.hashSenha(senha, sal)
        cifrador = CifrarComAES(chaveAES)
        chaveCifrada = cifrador.criptografar(chave)
        return chaveCifrada



