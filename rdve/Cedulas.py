import os, codecs, json
from pymerkle import hashing
from Transacoes import Transacoes
from Erros import saldoInconsistente, enderecoDaUrnaNulo
from pymerkle import MerkleTree
from uuid import uuid4

class _Cedula:
    idCedula = None

    def __init__(self, idCedula = None):
        if idCedula:
            self.idCedula = idCedula

    def criarCedula(self):
        self.idCedula = uuid4()
    
    def retornIdCedula(self):
        return self.idCedula

class Cedulas(list):
    endUrna = None
    _saldo = None
    arvoreDeMerkle = MerkleTree()
    hash_raiz = None 

    @property
    def saldo(self, saldo):
        return self._saldo

    @saldo.setter
    def saldo(self, saldo):
        if len(self)+1 != saldo:
            raise saldoInconsistente
        else:
            self._saldo = saldo

    def __init__(self, endUrna = None):
        if endUrna:
            self.endUrna = endUrna
           
    def definirEndereco(self, endUrna):
        self.endUrna = endUrna
        
    def inserir(self, _cedula):
        if isinstance(_cedula, _Cedula):
            self.append(_cedula)
            self.saldo += 1
            self.arvoreDeMerkle.update(_cedula.idCedula)

    def criarCedulas(self, saldo):
        if not self.endUrna:
            raise enderecoDaUrnaNulo
        for x in range(saldo):
            _Cedula = _Cedula()
            _Cedula.criarCedula()
            self.inserir(_Cedula)

    def dicionarios(self):
        if not self.hash_raiz:
            self.calcularArvoreDeMerkle()
            self.hash_raiz = self.arvoreDeMerkle.rootHash
        if len(self)>0:
            _dicionarios = []
            for _cedula in self:
                _dicionario = {"idCedula": _cedula.idCedula}
                _dicionarios.append(_dicionario)
            
            return {"endUrna": self.endUrna, "cedulas":_dicionarios, "hash_raiz": self.hash_raiz}
        else:
            return None

    def _idsCedulas(self):
        _dados = []
        for _c in self:
            _dados.append(_c.retornaIdCedula)
        
    def calcularArvoreDeMerkle(self):
        for _id in self._idsCedulas():
            self.arvoreDeMerkle.update(_id)

    def importarDicionario(self, dicionarios):
        endUrna = dicionarios["endUrna"]
        for _dicionario in dicionarios["cedulas"]:
            _cedula = _Cedula()
            _cedula.endUrna = endUrna
            _cedula.idCedula = _dicionario["idCedula"]
            self.inserir(_cedula)         

    def criarTransacao(self):
        self.tCedulas = tCedulas(self)

class tCedulas(Transacoes):
    def __init__(self, cedulas):
        if isinstance(cedulas, Cedulas):
            self.endUrna = cedulas.endUrna
            self.cedulas = []
            for _cedula in cedulas:
                self.cedulas.append(_cedula)
            self.arvoreDeMerkle = MerkleTree()
            for _cedula in cedulas:
                self.arvoreDeMerkle.update(_cedula.idCedula)
            self.hash_raiz = self.arvoreDeMerkle.rootHash

    def dados(self):
        return "{}:{}:{}".format(self.endUrna, len(self.cedulas), self.hash_raiz)

    def gerarHash(self):
        gerador = hashing.HashMachine()
        self.Hash = gerador.hash(self.dados())

    def dicionarios(self):
        _ds = []
        for _c in self.cedulas:
            _d = {"idCedula": _c.idCedula}
            _ds.append(_d)

        return {"endUrna": self.endUrna, "cedulas":_ds}

    def importarDicionario(self, dicionario):
        self.endUrna = dicionario["endUrna"]

        for _d in dicionario["celulas"]:
            _c = _Cedula
            _c.idCedula = _d["idCelula"]

    def exportarDicionario(self, arquivo):
        _arq = open(arquivo, "w")
        json.dump(self.dicionarios(), _arq, indent=4)
        _arq.close()