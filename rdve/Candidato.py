from _eleitor import Eleitor
from datetime import datetime, date
import codecs, os 

class Candidato(Eleitor):
    def __init__(self, modo, nome, titulo, numero, processo, endereco = None, aleatorio = None, timestamp = None):
        
        if modo == 1:
            self.tipo = "Candidato"
            self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
            self.timestamp = datetime.timestamp(datetime.now().timestamp())
            self.nome = nome
            self.titulo = titulo
            self.numero = numero
            self.processo = processo
            self.endereco = self.gerarEndereco()
        
        elif modo == 9:
            self.tipo = "Candidato"
            self.aleatorio = aleatorio
            self.timestamp = timestamp
            self.nome = nome
            self.titulo = titulo
            self.endereco = endereco
            self.numero = numero
            self.processo = processo

    def __key(self):
        return (self.tipo, self.aleatorio, self.nome, self.titulo, self.endereco, self.numero, 
                self.processo, self.timestamp, self.hashTransAnterior, self.assinatura)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented
    
    def _dados(self):
        return "{}:{}:{}:{}:{}:{}:{}:{}:{}:{}".format(self.tipo, self.aleatorio, self.nome, self.titulo, self.endereco, 
                                                self.numero, self.processo, self.timestamp, self.hashTransAnterior, 
                                                self.assinatura)

    def _dicionario(self):
        if self.Hash:
            return {"tipo": self.tipo, "aleatorio": self.aleatorio, "nome": self.nome, "titulo": self.titulo,
                   "endereco": self.endereco, "numero": self.processo, "timestamp": self.timestamp,
                    "hashTransAnterior": self.hashTransAnterior, "hash": self.Hash, "assinatura": self.assinatura}
        else:
            return {"tipo": self.tipo, "aleatorio": self.aleatorio, "nome": self.nome, "titulo": self.titulo,
                    "endereco": self.endereco, "numero": self.processo, "timestamp": self.timestamp,
                    "hashTransAnterior": self.hashTransAnterior, "assinatura": self.assinatura}

    def _gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self._dados()).decode()
