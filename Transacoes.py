import ecdsa, codecs, os
from hashlib import sha256
from datetime import time
from datetime import datetime

class Transacoes:

    hashTransAnterior = None
    assinatura = ''

class Eleitor(Transacoes):

    def __init__(self, nome, titulo, endereco, dataDoAlistamento):

        self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
        self.nome = nome
        self.titulo = titulo
        self.endereco = endereco
        self.dataDoAlistamento = dataDoAlistamento
        self.timestamp = datetime.timestamp(datetime.now().timestamp())

    def __key(self):
        return (self.nome, self.titulo, self.endereco)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented

    def _dados(self):
        return "{}:{}:{}:{}:{}:{}".format(self.aleatorio, self.nome, self.titulo, self.endereco, 
                                             self.dataDoAlistamento, self.timestamp)

    def _dicionario(self):
        return {"aleatorio": self.aleatorio, "nome": self.nome, "titulo": self.titulo,
                "endereco": self.endereco, "dataDoAlistamento": self.dataDoAlistamento,
                "timestamp": self.timestamp}

    def _gerarHash(self):        
        self.Hash = sha256(self._dados().encode()).hexdigest()

class Candidato(Eleitor):
    def __init__(self, nome, titulo, endereco, numero, processo):
        
        self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
        self.timestamp = datetime.timestamp(datetime.now().timestamp())
        self.nome = nome
        self.titulo = titulo
        self.endereco = endereco
        self.numero = numero
        self.processo = processo

    def __key(self):
        return (self.aleatorio, self.nome, self.titulo, self.endereco, self.numero, self.processo, self.timestamp)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented
    
    def _dados(self):
        return "{}:{}:{}:{}:{}:{}:{}".format(self.aleatorio, self.nome, self.titulo, self.endereco, 
                                             self.numero, self.processo, self.timestamp)

    def _dicionario(self):
        return {"aleatorio": self.aleatorio, "nome": self.nome, "titulo": self.titulo,
                "endereco": self.endereco, "numero": self.processo, "timestamp": self.timestamp}

    def _gerarHash(self):        
        self.Hash = sha256(self._dados().encode()).hexdigest()
    
class Voto(Transacoes):
    def __init__(self, numero):
        self.numero = numero
        self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
        self._gerarHash()
    
    def _dados(self):
        return "{}:{}".format(self.numero, self.aleatorio)

    def _dicionario(self):
        return {"numero": self.numero, "aleatorio": self.aleatorio}

    def _gerarHash(self):        
        self.Hash = sha256(self._dados().encode()).hexdigest()

    def __key(self):
        return(self.numero, self.aleatorio)
    
    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
            
        return NotImplemented