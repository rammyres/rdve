import ecdsa, codecs, os
from hashlib import sha256
from datetime import time

class Transacoes:

    hashTransAnterior = None
    assinatura = ''

class Eleitor(Transacoes):

    nome = None
    titulo = None
    endereco = None 
    dataDoAlistamento = None 

    def __key(self):
        return (self.nome, self.titulo, self.endereco)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented

    def __init__(self, nome, titulo, endereco):
        
        self.nome = nome
        self.titulo = titulo
        self.endereco = endereco

class Candidato(Eleitor):

    numero = None
    processo = None
    valido = None
    timestamp = None

    def __key(self):
        return (self.nome, self.titulo, self.endereco, self.numero, self.processo, self.timestamp)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented

    def __init__(self, nome, titulo, endereco, numero, processo):
        
        self.nome = nome
        self.titulo = titulo
        self.endereco = endereco
        self.numero = numero
        self.processo = processo
    
class Voto(Transacoes):
    def __init__(self, numero):
        self.numero = numero
        self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
        self._gerarHash()
    
    def _dados(self):
        return "{}:{}".format(self.numero, self.aleatorio)

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