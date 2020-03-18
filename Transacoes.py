import ecdsa, codecs, os
from hashlib import sha256
from datetime import time
from datetime import datetime

class Transacoes:

    hashTransAnterior = '0'
    assinatura = ''

    def importarDadosBasicos(self, hashTransAnterior, assinatura):
        self.hashTransAnterior = hashTransAnterior
        self.assinatura = assinatura

class Eleitor(Transacoes):

    def __init__(self, nome, titulo, endereco, dataDoAlistamento):

        self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
        self.timestamp = datetime.timestamp(datetime.now().timestamp())
        self.nome = nome
        self.titulo = titulo
        self.endereco = endereco
        self.dataDoAlistamento = dataDoAlistamento
        
    def _importarEleitor(self, dicionario):
        self.importarDadosBasicos(dicionario["hashTransAnterior"], dicionario["assinatura"])
        self.aleatorio = dicionario["aleatorio"]
        self.timestamp = dicionario["timestamp"]
        self.nome = dicionario["nome"]
        self.titulo = dicionario["titulo"]
        self.endereco = dicionario["endereco"]
        self.dataDoAlistamento = dicionario["dataDoAlistamento"]
        self.Hash = dicionario["hash"]

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
        return "{}:{}:{}:{}:{}:{}:{}:{}".format(self.aleatorio, self.nome, self.titulo, self.endereco, 
                                             self.dataDoAlistamento, self.timestamp, self.hashTransAnterior, 
                                             self.assinatura)

    def _dicionario(self):
        return {"aleatorio": self.aleatorio, "nome": self.nome, "titulo": self.titulo,
                "endereco": self.endereco, "dataDoAlistamento": self.dataDoAlistamento,
                "timestamp": self.timestamp, "hashTransAnterior": self.hashTransAnterior, 
                "assinatura": self.assinatura}

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

    def _importarCandidato(self, dicionario):
        self.importarDadosBasicos(dicionario["hashTransAnterior"], dicionario["assinatura"])
        self.aleatorio = dicionario["aleatorio"]
        self.timestamp = dicionario["timestamp"]
        self.nome = dicionario["nome"]
        self.titulo = dicionario["titulo"]
        self.endereco = dicionario["endereco"]
        self.numero = dicionario["numero"]
        self.processo = dicionario["processo"]
        self.Hash = dicionario["hash"]

        return self

    def __key(self):
        return (self.aleatorio, self.nome, self.titulo, self.endereco, self.numero, 
                self.processo, self.timestamp, self.hashTransAnterior, self.assinatura)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented
    
    def _dados(self):
        return "{}:{}:{}:{}:{}:{}:{}:{}:{}".format(self.aleatorio, self.nome, self.titulo, self.endereco, 
                                             self.numero, self.processo, self.timestamp, self.hashTransAnterior, 
                                             self.assinatura)

    def _dicionario(self):
        return {"aleatorio": self.aleatorio, "nome": self.nome, "titulo": self.titulo,
                "endereco": self.endereco, "numero": self.processo, "timestamp": self.timestamp,
                "hashTransAnterior": self.hashTransAnterior, "assinatura": self.assinatura}

    def _gerarHash(self):        
        self.Hash = sha256(self._dados().encode()).hexdigest()
    
class Voto(Transacoes):
    def __init__(self, numero):
        self.numero = numero
        self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
        self._gerarHash()

    def _importarVoto(self, dicionario):
        self.importarDadosBasicos(dicionario["hashTransAnterior"], dicionario["assinatura"])
        self.numero = dicionario["voto"]
        self.aleatorio = dicionario["aleatorio"]
        self.Hash = dicionario["hash"]

        return self
    
    def _dados(self):
        return "{}:{}".format(self.numero, self.aleatorio)

    def _dicionario(self):
        return {"numero": self.numero, "aleatorio": self.aleatorio, "hash": self.Hash, "hashTransAnterior": self.hashTransAnterior, 
                "assinatura": self.assinatura}

    def _gerarHash(self):        
        self.Hash = sha256(self._dados().encode()).hexdigest()

    def __key(self):
        return(self.numero, self.aleatorio, self.hashTransAnterior, self.assinatura)
    
    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
            
        return NotImplemented