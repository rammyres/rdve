#!/usr/bin/env python3
from Transacoes import Transacoes
from ecdsa import SECP256k1, VerifyingKey
import codecs, os

class Voto:
    assinatura = ''
    def __init__(self, eleicao = None, abrangencia = None, numero = None, idCedula = None, enderecoDeOrigem = None, assinatura = None):
        if numero and enderecoDeOrigem:
            self.eleicao = eleicao 
            self.abrangencia = abrangencia
            self.numero = numero
            self.enderecoDeOrigem = enderecoDeOrigem
            self.idCedula = idCedula

    def definirIdCedula(self, idCedula):
        self.idCedula = idCedula
    
    def importarVoto(self, eleicao, abrangencia, numero, enderecoDeOrigem, idCedula, assinatura):
        self.eleicao = eleicao
        self.abrangencia = abrangencia
        self.numero = numero
        self.enderecoDeOrigem = enderecoDeOrigem
        self.idCedula = idCedula
        self.assinatura = assinatura
    
    def importarDicionario(self, dicionario):
        self.importarVoto(dicionario["eleicao"], dicionario['abrangencia'], dicionario["numero"], dicionario["enderecoDeOrigem"], 
                                    dicionario["idCedula"], dicionario["assinatura"])        
        
    def criarTransacao(self):
        self.tVoto = tVoto(self.eleicao, self.abrangencia, self.numero, self.idCedula, self.enderecoDeOrigem, self.assinatura)

    def verificarAssinatura(self, dados, assinatura, chavePublica):
        _vk = VerifyingKey.from_string(chavePublica)
        return _vk.verify(assinatura, dados.encode())
    
    def dados(self):
        return "{}:{}:{}:{}:{}:{}".format(self.eleicao, self.abrangencia, self.numero, self.idCedula, self.enderecoDeOrigem, self.assinatura)

class tVoto(Transacoes):
    def __init__(self, eleicao, abrangencia, numero, idCedula, enderecoDeOrigem, assinatura = None):
        self.tipo = "Voto"
        self.eleicao = eleicao
        self.abrangencia = abrangencia
        self.numero = numero
        self.enderecoDeOrigem = enderecoDeOrigem
        self.idCedula = idCedula
        self.assinatura = assinatura

    def dados(self):
        return "{}:{}:{}:{}:{}".format(self.numero, self.idCedula, self.enderecoDeOrigem, self.assinatura, self.hashTransAnterior)

    def dicionario(self):
        if self.Hash:
            return {"tipo": self.tipo, "numero": self.numero, "idCedula": self.idCedula, "hash": self.Hash, "enderecoDeOrigem":self.enderecoDeOrigem,
                    "hashTransAnterior": self.hashTransAnterior, "assinatura": self.assinatura}
        else:
            return {"tipo": self.tipo, "numero": self.numero, "idCedula": self.idCedula, "enderecoDeOrigem":self.enderecoDeOrigem,
                    "hashTransAnterior": self.hashTransAnterior, "assinatura": self.assinatura}

    def gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self.dados()).decode()

    def importarDicionario(self, dicionario):
        self.tipo = dicionario["tipo"]
        self.eleicao = dicionario["eleicao"]
        self.abrangencia = dicionario["abrangencia"]
        self.numero = dicionario["numero"]
        self.enderecoDeOrigem = dicionario["enderecoDeOrigem"]
        self.idCedula = dicionario["idCedula"]
        self.assinatura = dicionario["assinatura"]
        self.hashTransAnterior = dicionario["hashTransAnterior"]
        self.Hash = dicionario["hash"]
        
        return self

    def gerarObjeto(self):
        _voto = Voto(self.eleicao, self.abrangencia, self.numero, self.idCedula, self.enderecoDeOrigem, self.assinatura)
        return _voto

    def __key(self):
        return(self.tipo, self.numero, self.idCedula, self.hashTransAnterior, self.assinatura)
    
    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
            
        return NotImplemented