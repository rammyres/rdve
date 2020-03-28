#!/usr/bin/env python3
from Transacoes import Transacoes
from ecdsa import SECP256k1, VerifyingKey
import codecs, os

class Voto:
    assinatura = ''
    def __init__(self, eleicao = None, abrangencia = None, numero = None, enderecoDeOrigem = None, chavePrivada=None, aletorio = None, assinatura = None):
        if numero and enderecoDeOrigem:
            self.eleicao = eleicao 
            self.abrangencia = abrangencia
            self.numero = numero
            self.enderecoDeOrigem = enderecoDeOrigem
            self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
    
    def importarVoto(self, eleicao, abrangencia, numero, enderecoDeOrigem, aletorio, assinatura):
        self.eleicao = eleicao
        self.abrangencia = abrangencia
        self.numero = numero
        self.enderecoDeOrigem = enderecoDeOrigem
        self.aleatorio = aletorio
        self.assinatura = assinatura
    
    def importarDicionario(self, dicionario):
        self.importarVoto(dicionario["eleicao"], dicionario['abrangencia'], dicionario["numero"], dicionario["enderecoDeOrigem"], 
                                    dicionario["aleatorio"], dicionario["assinatura"])        
    
    
    def gerarTransacao(self):
        self.tVoto = tVoto(self.eleicao, self.abrangencia, self.numero, self.aleatorio, self.enderecoDeOrigem, self.assinatura)

    def verificarAssinatura(self, dados, assinatura, chavePublica):
        _vk = VerifyingKey.from_string(chavePublica)
        return _vk.verify(assinatura, dados.encode())
    
    def dados(self):
        return "{}:{}:{}:{}:{}:{}".format(self.eleicao, self.abrangencia, self.numero, self.aleatorio, self.enderecoDeOrigem, self.assinatura)

class tVoto(Transacoes):
    def __init__(self, eleicao, abrangencia, numero, aleatorio, enderecoDeOrigem, aletorio, assinatura = None):
        self.tipo = "Voto"
        self.eleicao = eleicao
        self.abrangencia = abrangencia
        self.numero = numero
        self.enderecoDeOrigem = enderecoDeOrigem
        self.aleatorio = aletorio
        self.assinatura = assinatura

    def _dados(self):
        return "{}:{}:{}:{}:{}".format(self.numero, self.aleatorio, self.enderecoDeOrigem, self.assinatura, self.hashTransAnterior)

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