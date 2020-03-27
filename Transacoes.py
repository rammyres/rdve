import codecs, os, ecdsa, base58, binascii, hashlib
from erros import processoDeAssinaturaInvalido
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


class tUrna(TransacoesEnderecaveis):
    endereco = None

    def __init__(self, modo, zona, secao, saldoInicial, endereco = None, timestamp = None, hashTransAnterior = None, Hash = None):
        
        if modo == 1:
            self.tipo = "Urna"
            self.zona = zona
            self.secao = secao
            self.saldo = saldoInicial
            self.timestamp = datetime.timestamp(datetime.now().timestamp())
            self.endereco = self.gerarEndereco()
        
        elif modo == 9:
            self.tipo = "Urna"
            self.zona = zona
            self.secao = secao
            self.saldo = saldoInicial
            self.timestamp = timestamp
            self.endereco = endereco
    
    def __key(self):
        return (self.zona, self.secao, self.timestamp, self.endereco, self.hashTransAnterior, self.Hash)
    
    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented

    def _dados(self):
        return '{}:{}:{}:{}:{}:{}'.format(self.tipo, self.zona, self.secao, self.saldo, self.timestamp, self.endereco)
    
    def _gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self._dados()).decode()
    
    def _dicionario(self):
        if self.Hash:
            return {"tipo": self.tipo, "zona": self.zona, "secao": self.secao, "saldoInicial": self.saldo,
                    "endereco": self.endereco, "timestamp": self.timestamp, "assinatura": self.assinatura, 
                    "hashTransAnterior": self.hashTransAnterior, "hash": self.Hash}
        else:
            return {"tipo": self.tipo, "zona": self.zona, "secao": self.secao, "saldoInicial": self.saldo,
                    "endereco": self.endereco, "timestamp": self.timestamp, "assinatura": self.assinatura, 
                    "hashTransAnterior": self.hashTransAnterior}


    
class tVoto(Transacoes):
    def __init__(self, modo, numero, enderecoDeOrigem, chavePrivada=None, aletorio = None, assinatura = None):
        if modo == 1:
            self.tipo = "Voto"
            self.numero = numero
            self.enderecoDeOrigem = enderecoDeOrigem
            self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
                
        elif modo == 9:
            self.tipo = "Voto"
            self.numero = numero
            self.enderecoDeOrigem = enderecoDeOrigem
            self.aleatorio = aletorio
            self.assinatura = assinatura
    
    def _dados(self):
        return "{}:{}:{}:{}:{}:{}".format(self.tipo, self.numero, self.aleatorio, self.enderecoDeOrigem, self.hashTransAnterior, self.assinatura)

    def _dicionario(self):
        if self.Hash:
            return {"tipo": self.tipo, "numero": self.numero, "aleatorio": self.aleatorio, "hash": self.Hash, "enderecoDeOrigem":self.enderecoDeOrigem,
                    "hashTransAnterior": self.hashTransAnterior, "assinatura": self.assinatura}
        else:
            return {"tipo": self.tipo, "numero": self.numero, "aleatorio": self.aleatorio, "enderecoDeOrigem":self.enderecoDeOrigem,
                    "hashTransAnterior": self.hashTransAnterior, "assinatura": self.assinatura}

    def _gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self._dados()).decode()

    def __key(self):
        return(self.tipo, self.numero, self.aleatorio, self.hashTransAnterior, self.assinatura)
    
    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
            
        return NotImplemented