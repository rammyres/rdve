import os, codecs, json
from pymerkle import hashing
from Transacoes import Transacoes
from Erros import saldoInconsistente, enderecoDaUrnaNulo, excedeMaxVotos
from pymerkle import MerkleTree
from uuid import uuid4

class Cedula:
    idCedula = None

    def __init__(self, tipoEleicao, eleicao, idCedula = None, maxVotos = None):     

        if idCedula and tipoEleicao and maxVotos:
            self.idCedula = idCedula
            self.tipoEleicao = tipoEleicao
            self.eleicao = eleicao
            self.maxVotos = maxVotos
        else:
            self.criarCedula(tipoEleicao)

    def criarCedula(self, tipoEleicao):
        self.idCedula = uuid4()

        if tipoEleicao == "1":
            self.maxVotos = 5
        elif tipoEleicao == "2":
            self.maxVotos == 2
        elif tipoEleicao == "3" or tipoEleicao == "4" or tipoEleicao == "5":
            self.maxVotos == 1
        else:
            raise excedeMaxVotos("Numero de votos superior ao máximo permitido para a cédula")   
    
    def importarDicionario(self, dicionario):
        _cedula = Cedula(dicionario["tipoEleicao"], dicionario["eleicao"], dicionario["idCedula"], dicionario["maxVotos"])
        return _cedula
    
    def serializar(self):
        return {"tipoEleicao": self.tipoEleicao, 
                "eleicao": self.eleicao, 
                "idCedula":self.idCedula, 
                "maxVotos": self.maxVotos}

class Cedulas(list):
    endUrna = None

    def __init__(self, endUrna = None):
        if endUrna:
            self.endUrna = endUrna
           
    def definirEndereco(self, endUrna):
        self.endUrna = endUrna
        
    def inserir(self, _cedula):
        if isinstance(_cedula, Cedula):
            self.append(_cedula)

    def criarCedulas(self, saldo):
        if not self.endUrna:
            raise enderecoDaUrnaNulo
        for _ in range(saldo):
            _Cedula = _Cedula()
            _Cedula.criarCedula()
            self.inserir(_Cedula)

    def serializar(self):
        if len(self)>0:
            _dicionarios = []
            for _cedula in self:
                _dicionario = _cedula.serializar()
                _dicionarios.append(_dicionario)
            return {"cedulas":_dicionarios}
        else:
            return None

    def _idsCedulas(self):
        _dados = []
        for _c in self:
            _dados.append(_c.retornaIdCedula)
        
    def importarDicionario(self, dicionarios):
        self.endUrna = dicionarios["endUrna"]
        for _dicionario in dicionarios["cedulas"]:
            _cedula = Cedula(_dicionario["tipoEleicao"],
                             _dicionario["eleicao"], 
                             _dicionario["idCedula"],
                             _dicionario["maxVotos"])
            self.inserir(_cedula)