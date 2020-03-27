from Transacoes import Transacoes
import codecs, os

class Voto(Transacoes):
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