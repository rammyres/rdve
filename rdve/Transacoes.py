import codecs, os, ecdsa, base58, binascii, hashlib
from Erros import processoDeAssinaturaInvalido
from ecdsa import SigningKey, curves, SECP256k1
from datetime import time, date, datetime
from pymerkle.hashing import HashMachine

class Transacoes:

    hashTransAnterior = '0'
    assinatura = None
    Hash = None
    gerador = HashMachine()

    def assinar(self, dados = None, chavePrivada = None):
        if dados == None or chavePrivada == None:
            raise processoDeAssinaturaInvalido 
        
        assinatura = chavePrivada.sign(dados.encode())
        assinaturaStr = codecs.encode(assinatura, 'hex').decode()
        
        return assinaturaStr
    
    def verificarAssinatura(self, assinatura, chavePublica):
        return chavePublica.verify(assinatura, chavePublica)


class TransacoesEnderecaveis(Transacoes):
    def ripemd160(self, x):
        d = hashlib.new('ripemd160')
        d.update(x)
        return d

    def gerarEndereco(self):
        # generate private key , uncompressed WIF starts with "5"
        chavePrivada = os.urandom(32)
        #chaveCompleta = '80' + binascii.hexlify(chavePrivada).decode()
        #sha256a = hashlib.sha256(binascii.unhexlify(chaveCompleta)).hexdigest()
        #sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
        #WIF = base58.b58encode(binascii.unhexlify(chaveCompleta+sha256b[:8]))
        
        # get public key , uncompressed address starts with "1"
        sk = ecdsa.SigningKey.from_string(chavePrivada, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        chavePublica = '04' + binascii.hexlify(vk.to_string()).decode()
        hash160 = self.ripemd160(hashlib.sha256(binascii.unhexlify(chavePublica)).digest()).digest()
        enderecoPublico_a = b"\x00" + hash160
        checksum = hashlib.sha256(hashlib.sha256(enderecoPublico_a).digest()).digest()[:4]
        enderecoPublico_b = base58.b58encode(enderecoPublico_a + checksum)

        return enderecoPublico_b.decode()
