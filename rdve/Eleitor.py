#!/usr/bin/env python3
from Transacoes import Transacoes
from datetime import datetime, date
from Utilitarios import gerarChavePrivada, gerarChavePublica, gerarEndereco, importarChavePublica
import codecs, os 

class Eleitor:

    def __init__(self, nome = None, titulo = None, endereco = None, timestamp = None):
        self.timestamp = datetime.timestamp(datetime.now().timestamp())
        self.nome = nome
        self.titulo = titulo
        gerarChavePrivada("eleitor{}.pem".format(titulo))
        gerarChavePublica("eleitor{}.pem".format(titulo))
        self.endereco = gerarEndereco("eleitor{}.pem".format(titulo))
        self.chavePublica = importarChavePublica(("pub-eleitor{}.pem".format(titulo))).to_string()
        self.tEleitor = tEleitor(self.nome, self.titulo, self.endereco, self.timestamp)
        
    def importarEleitor(self, nome, titulo, endereco, timestamp):
        self.timestamp = timestamp
        self.nome = nome
        self.titulo = titulo
        self.endereco = endereco

    def importarDicionario(self, dicionario):
        self.importarEleitor(dicionario["nome"], dicionario["titulo"], dicionario["endereco"], dicionario["timestamp"])

    def dados(self):
        return (self.nome, self.titulo, self.endereco, self.timestamp)

class tEleitor(Transacoes):
    assinatura = None

    def __init__(self, nome, titulo, endereco, timestamp, assinatura = None):
        self.tipo = "Eleitor"
        self.nome = nome 
        self.titulo = titulo
        self.endereco = endereco
        self.timestamp = timestamp
        self.assinatura = assinatura

    def _dados(self):
        if self.Hash:
            return "{}:{}:{}:{}:{}:{}:{}:{}".format(self.tipo, self.nome, self.titulo, self.endereco, self.timestamp, self.assinatura, self.hashTransAnterior, 
                                                    self.Hash)
        else:
            return "{}:{}:{}:{}:{}:{}:{}".format(self.tipo, self.nome, self.titulo, self.endereco, self.timestamp, self.assinatura, self.hashTransAnterior)

    def __key(self):
        return (self.timestamp, self.nome, self.titulo, self.endereco, self.Hash, self.hashTransAnterior, self.assinatura)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented

    def _dicionario(self):
        return {"tipo": self.tipo, "nome": self.nome, "titulo": self.titulo, "endereco": self.endereco, "timestamp": self.timestamp, 
                "assinatura": self.assinatura, "hash": self.Hash, "hashTransAnterior": self.hashTransAnterior}
    
    def gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self._dados()).decode()