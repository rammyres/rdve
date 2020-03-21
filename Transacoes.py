import ecdsa, codecs, os
from hashlib import sha256
from datetime import time
from datetime import datetime
from pymerkle.hashing import HashMachine

class Transacoes:

    hashTransAnterior = '0'
    assinatura = 'assinatura'
    Hash = None
    gerador = HashMachine()

class Eleitor(Transacoes):

    def __init__(self, modo, nome, titulo, endereco, dataDoAlistamento, timestamp = None, aleatorio = None):
        
        if modo == 1:
            self.tipo = "Eleitor"
            self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
            self.timestamp = datetime.timestamp(datetime.now().timestamp())
            self.nome = nome
            self.titulo = titulo
            self.endereco = endereco
            self.dataDoAlistamento = dataDoAlistamento
        
        elif modo == 9:
            self.tipo = "Eleitor"
            self.aleatorio = aleatorio
            self.timestamp = timestamp
            self.nome = nome
            self.titulo = titulo
            self.endereco = endereco
            self.dataDoAlistamento = dataDoAlistamento
            
    
    def __key(self):
        return (self.aleatorio, self.timestamp, self.nome, self.titulo, self.endereco, self.dataDoAlistamento, 
                self.Hash, self.hashTransAnterior, self.assinatura)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented

    def _dados(self):
        return "{}:{}:{}:{}:{}:{}:{}:{}:{}".format(self.tipo, self.aleatorio, self.nome, self.titulo, self.endereco, 
                                                self.dataDoAlistamento, self.timestamp, self.hashTransAnterior, 
                                                self.assinatura)


    def _dicionario(self):
        return {"tipo": self.tipo, "aleatorio": self.aleatorio, "nome": self.nome, "titulo": self.titulo,
                "endereco": self.endereco, "dataDoAlistamento": self.dataDoAlistamento,
                "timestamp": self.timestamp, "hashTransAnterior": self.hashTransAnterior, 
                "assinatura": self.assinatura}
    
    def _gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self._dados()).decode()

class Candidato(Eleitor):
    def __init__(self, modo, nome, titulo, endereco, numero, processo, aleatorio = None, timestamp = None):
        
        if modo == 1:
            self.tipo = "Candidato"
            self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
            self.timestamp = datetime.timestamp(datetime.now().timestamp())
            self.nome = nome
            self.titulo = titulo
            self.endereco = endereco
            self.numero = numero
            self.processo = processo
        
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
    
class Voto(Transacoes):
    def __init__(self, modo, numero, aletorio = None):
        if modo == 1:
            self.tipo = "Voto"
            self.numero = numero
            self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
        
        elif modo == 9:
            self.tipo = "Voto"
            self.numero = numero
            self.aleatorio = aletorio
    
    def _dados(self):
        return "{}:{}:{}:{}:{}".format(self.tipo, self.numero, self.aleatorio, self.assinatura, self.hashTransAnterior)

    def _dicionario(self):
        if self.Hash:
            return {"tipo": self.tipo, "numero": self.numero, "aleatorio": self.aleatorio, "hash": self.Hash, 
                    "hashTransAnterior": self.hashTransAnterior, "assinatura": self.assinatura}
        else:
            return {"tipo": self.tipo, "numero": self.numero, "aleatorio": self.aleatorio, 
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