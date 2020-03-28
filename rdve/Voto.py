from Transacoes import Transacoes
from ecdsa import SECP256k1, VerifyingKey
import codecs, os

class Voto:
    assinatura = ''
    def __init__(self, numero = None, enderecoDeOrigem = None, chavePrivada=None, aletorio = None, assinatura = None):
        if numero and enderecoDeOrigem:
            self.numero = numero
            self.enderecoDeOrigem = enderecoDeOrigem
            self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
            self.tVoto = tVoto(self.numero, self.aleatorio, self.enderecoDeOrigem, self.aleatorio, self.assinatura)

    def importarDicionario(self, dicionario):
        self.numero = dicionario["numero"]
        self.enderecoDeOrigem = dicionario["enderecoDeOrigem"] 
        self.aleatorio = dicionario["aleatorio"]
        self.assinatura = dicionario["assinatura"]
        
    def importarVoto(self, numero, enderecoDeOrigem, aletorio, assinatura):
        self.numero = numero
        self.enderecoDeOrigem = enderecoDeOrigem
        self.aleatorio = aletorio
        self.assinatura = assinatura

    def verificarAssinatura(self, dados, assinatura, chavePublica):
        _vk = VerifyingKey.from_string(chavePublica)
        return _vk.verify(assinatura, dados.encode())
    
    def dados(self):
        return "{}:{}:{}:{}".format(self.numero, self.aleatorio, self.enderecoDeOrigem, self.assinatura)

class tVoto(Transacoes):
    def __init__(self, numero, aleatorio, enderecoDeOrigem, aletorio, assinatura = None):
        self.tipo = "Voto"
        self.numero = numero
        self.enderecoDeOrigem = enderecoDeOrigem
        self.aleatorio = aletorio
        self.assinatura = assinatura

    def _dados(self):
        return "{}:{}:{}:{}:{}".format(self.numero, self.aleatorio, self.enderecoDeOrigem, self.assinatura, self.hashTransAnterior)

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