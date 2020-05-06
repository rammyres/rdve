#!/usr/bin/env python3
from Eleitor import Eleitor
from Transacoes import Transacoes
from Criptografia import Criptografia
from Utilitarios import Utilitarios
from datetime import datetime, date
import os, json 

class Candidato(Eleitor):
    abrangencia = None
    cargo = None
    nome = None
    titulo = None
    numero = None
    assinatura = None
    timestamp = None
    # As chaves e endereços devem ser gerados depois da validação da requisição de candidatura
    # expedida a partir de um eleitor válido
    endereco = None 
    chavePrivada = None
    chavePublica = None

    def __init__(self, requisicao = None):
        self.auxCriptografica = Criptografia()
        self.Utilitarios = Utilitarios()
        if requisicao:
            self.importarDaRequisicao(requisicao)

    def importarDaRequisicao(self, requisicao):
        self.abrangencia = requisicao["abrangencia"]
        self.cargo = requisicao ["cargo"]
        self.nome = requisicao["nome"]
        self.titulo = requisicao["titulo"]
        self.numero = requisicao["numero"]
        self.assinatura = requisicao["assinatura"]
        self.timestamp = requisicao["timestamp"]
    
    def criarChavePrivada(self):
        if self.assinatura:
            self.chavePrivada = self.auxCriptografica.gerarChavePrivada()

    def criarEndereco(self):
        if self.chavePrivada:
            self.endereco = self.Utilitarios.gerarEndereco(self.chavePrivada)
        
    def criarTransacao(self):
        self.tCandidato = tCandidato(self.abrangencia, 
                                     self.cargo, 
                                     self.nome, 
                                     self.titulo, 
                                     self.numero,
                                     self.timestamp, 
                                     self.endereco,
                                     self.chavePublica)

    def __key(self):
        return (self.nome, self.titulo, self.endereco, self.numero, self.assinatura, self.timestamp)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented

class tCandidato(Transacoes):
    def __init__(self, abrangencia = None, cargo = None, nome = None, titulo = None, numero = None, timestamp = None, endereco = None, chavePublica = None):
        self.tipo = "Candidato"
        self.abrangencia = abrangencia
        self.cargo = cargo
        self.nome = nome
        self.titulo = titulo
        self.numero = numero
        self.timestamp = timestamp
        self.endereco = endereco
        self.chavePublica = chavePublica
        self.gerarHash()
    
    def dados(self):
        return "{}:{}:{}:{}:{}:{}:{}:{}".format(self.abrangencia, 
                                          self.cargo, 
                                          self.nome, 
                                          self.titulo, 
                                          self.numero, 
                                          self.timestamp, 
                                          self.endereco, 
                                          self.chavePublica)

    def serializar(self):
        return {"tipo": self.tipo, 
                "abrangencia": self.abrangencia, 
                "cargo": self.cargo,
                "nome": self.nome, 
                "titulo": self.titulo,
                "numero": self.numero,
                "timestamp": self.timestamp,
                "endereco": self.endereco,  
                "hashTransAnterior": self.hashTransAnterior, 
                "hash": self.Hash, 
                "assinatura": self.assinatura}

    def importarDicionario(self, dicionario):
        self.tipo = dicionario["tipo"]
        self.abrangencia = dicionario["abrangencia"]
        self.cargo = dicionario["cargo"]
        self.nome = dicionario["nome"]
        self.titulo = dicionario["titulo"]
        self.numero = dicionario["numero"]
        self.timestamp = dicionario["timestamp"]
        self.endereco = dicionario["endereco"]        
        self.hashTransAnterior = dicionario["hashTransAnterior"]
        self.Hash = dicionario["hash"]
        self.assinatura = dicionario["assinatura"]
        return self 

    def gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self.dados()).decode()