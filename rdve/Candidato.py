#!/usr/bin/env python3
from Eleitor import Eleitor
from Transacoes import Transacoes
from Utilitarios import gerarChavePrivada, gerarChavePublica, gerarEndereco
from datetime import datetime, date
import codecs, os 

class Candidato(Eleitor):
    def __init__(self, abrangencia = None, nome = None, titulo = None, cargo = None, numero = None, 
                 processo = None, endereco = None, timestamp = None):
        self.abrangencia = abrangencia
        self.nome = nome
        self.titulo = titulo
        self.cargo = cargo
        self.abrangencia = abrangencia
        self.timestamp = datetime.timestamp(datetime.now().timestamp())     
        self.numero = numero
        self.processo = processo
        gerarChavePrivada("candidato{}.pem".format(self.processo))
        gerarChavePublica("candidato{}.pem".format(self.processo))
        self.endereco = gerarEndereco("candidato{}.pem".format(self.processo))
        
    def importarCandidato(self, abrangencia, nome, titulo, cargo, numero, processo, endereco, timestamp):
        self.abrangencia = abrangencia
        self.nome = nome
        self.titulo = titulo
        self.endereco = endereco
        self.numero = numero
        self.processo = processo
        self.timestamp = timestamp

    def criarTransacao(self):
        self.tCandidato = tCandidato(self.abrangencia, self.nome, self.titulo, self.cargo, self.numero, self.processo, self.endereco, self.timestamp)

    def __key(self):
        return (self.nome, self.titulo, self.endereco, self.numero, self.processo, self.timestamp)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented

class tCandidato(Transacoes):
    def __init__(self, abrangencia, nome, titulo, cargo, numero, processo, endereco, timestamp):
        self.tipo = "Candidato"
        self.abrangencia = abrangencia
        self.cargo = cargo 
        self.nome = nome
        self.titulo = titulo
        self.numero = numero
        self.processo = processo
        self.endereco = endereco
        self.timestamp = timestamp
        self.gerarHash()
    
    def dados(self):
        return "{}:{}:{}:{}:{}:{}".format(self.nome, self.titulo, self.endereco, self.numero, self.processo, self.timestamp)

    def dicionario(self):
        return {"tipo": self.tipo, "abrangencia": self.abrangencia, "nome": self.nome, "titulo": self.titulo,
                "endereco": self.endereco, "numero": self.processo, "timestamp": self.timestamp,
                "hashTransAnterior": self.hashTransAnterior, "hash": self.Hash, "assinatura": self.assinatura}

    def importarDicionario(self, dicionario):
        self.tipo = dicionario["tipo"]
        self.abrangencia = dicionario["abrangencia"]
        self.cargo = dicionario["cargo"]
        self.nome = dicionario["nome"]
        self.titulo = dicionario["titulo"]
        self.numero = dicionario["numero"]
        self.processo = dicionario["processo"]
        self.endereco = dicionario["endereco"]
        self.timestamp = dicionario["timestamp"]
        self.hashTransAnterior = dicionario["hashTransAnterior"]
        self.Hash = dicionario["hash"]
        return self 

    def gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self.dados()).decode()

    def gerarObjeto(self):
        _candidato = Candidato(self.abrangencia, self.nome, self.titulo, self.cargo, self.numero, self.processo, self.endereco, self.timestamp)
        return _candidato