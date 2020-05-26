#!/usr/bin/env python3
from BlocosDeTransacoes import blocosDeTransacoesFinal, blocosDeTransacoesIntermediario
from Erros import deveSerBlocoDeTransacaoFinal, quantidadeMenorQueUm, tipoDeTransacaoDesconhecido, sequenciaDeHashesInvalida, \
                  arvoreDeMerkleInvalida, registroSemTransacoes, excedeMaxVotos, cedulaNaoAssinada, cedulaSemVotos
from pymerkle import MerkleTree
from collections import OrderedDict 
from Transacoes import Transacoes
from Voto import Voto
from Candidato import Candidato
from Eleitor import Eleitor
from Cedulas import Cedula
from Utilitarios import Utilitarios
from hashlib import sha256
import json, os

class CedulaPreenchida(Cedula):
    votos = []
    assinatura = None
    Hash = None

    def __init__(self, dicionario_cedula):
        self.idCedula = dicionario_cedula["idCedula"]
        self.tipoEleicao = dicionario_cedula["tipoEleicao"]
        self.maxVotos = int(dicionario_cedula["maxVotos"])

    def inserirVotos(self, votos):
        if isinstance(votos, list):
            for v in votos:
                self._inserirVoto(v)

    def _inserirVoto(self, voto):
        # A classe vai verificar se o voto segue os votos contidos 
        # contém as chaves certas
        if len(self.votos) <= self.maxVotos:
            if len(voto.keys)>2:
                if voto.keys()[0] == "enderecoDestino" and voto.keys()[1] == "quantidade":
                    self.votos.append(voto)
        else:
            raise excedeMaxVotos("Numero de votos superior ao máximo permitido para a cédula")   

    def importarVotos(self, dicionario):
        self.votos = [v for v in dicionario["votos"]]

    def dadosCedula(self):
        if not self.votos:
            raise cedulaSemVotos
        else:
            for x in range(len(self.votos)):
                _vs = "{}:{}:".format(_vs, self.votos(x))

        return "{}{}{}{}".format(self.idCedula, self.tipoEleicao, self.maxVotos, _vs[:-1])

    def gerarHash(self):
        if self.assinatura:
            _hash = sha256(self.dadosCedula().encode())
        else:
            raise cedulaNaoAssinada

    def dicionario_votos(self):
        if self.votos:
            _d = [v for v in self.votos]
            return _d
        else:
            raise cedulaSemVotos

    def serializar(self):
        if len(self.votos) == self.maxVotos and self.assinatura and self.Hash:
            return {"idCedula": self.idCedula, 
                    "tipoEleicao": self.tipoEleicao, 
                    "maxVotos": self.maxVotos,
                    "votos": self.dicionario_votos(),
                    "assinatura": self.assinatura,
                    "hash": self.Hash}

    

class boletimDeUrna:
    eleicao = None
    endereco = None
    abrangencia = None
    zona = None
    secao = None
    _arvoreDeMerkle = None
    votos = None 

    @property
    def arvoreDeMerkle(self):
        return self._arvoreDeMerkle

    @arvoreDeMerkle.setter
    def arvoreDeMerkle(self, arvore):
        if not self.votos:
            raise registroSemTransacoes
        _tArvore = MerkleTree(*self.transacoes.dados())
        if arvore != _tArvore:
            raise arvoreDeMerkleInvalida
        else:
            self._arvoreDeMerkle = arvore    

    def __init__(self, eleicao, abrangencia, endereco, zona, secao, blocoTF=None, arvore = None):

        if blocoTF != None:
            if len(blocoTF.dados()) == 0:
                raise quantidadeMenorQueUm
            elif isinstance(blocoTF, blocosDeTransacoesFinal):
                for transacao in blocoTF:
                    if isinstance(transacao, Transacoes):
                        pass
                    else:
                        raise tipoDeTransacaoDesconhecido
                if blocoTF.validaSequencia():
                    _tArvore = MerkleTree(*blocoTF.dados())
                    if arvore:
                        if arvore != _tArvore:
                            raise arvoreDeMerkleInvalida
                    self.votos = blocoTF
                    self.arvoreDeMerkle = _tArvore
                    self.abrangencia = abrangencia
                    self.endereco = endereco
                    self.zona = zona
                    self.secao = secao 
                    self.eleicao = eleicao

                else:
                    raise sequenciaDeHashesInvalida
            else: 
                raise deveSerBlocoDeTransacaoFinal

    def cabecalho(self):
        return {"eleicao": self.eleicao, "endereco": self.endereco, "abrangencia": self.abrangencia, "zona": self.zona, "secao": self.secao}
    
    def receberVotos(self, _blocoFinal):
        self.transacoes = _blocoFinal
        self.arvoreDeMerkle = MerkleTree(*self.transacoes.dados())

    def dicionario(self): 
        return {"cabecalho": self.cabecalho(), "arvoreDeMerkle": self.arvoreDeMerkle.serialize(), "transacoes": self.transacoes.dicionarios()}

    def exportar(self, arquivo):
        _persistencia = open(arquivo, "w")

        json.dump(self.dicionario, _persistencia, indent=4)

        _persistencia.close()

    def importarDicionario(self, dicionario):
        util = Utilitarios()

        _tArvore = dicionario["arvoreDeMerkle"]
        _tTransacoesDict = OrderedDict()
        _tTransacoesDict = dicionario["transacoes"]

        _tTransacoes = blocosDeTransacoesFinal()
        _tTransacoes.importarDicionarios(_tTransacoesDict["transacoes"])

        _tArvoreJson = open("tmp.json", "w")
        json.dump(_tArvore, _tArvoreJson)
        _tArvoreJson.close()

        _tArvoreMerkle = MerkleTree.loadFromFile("tmp.json")

        if _tArvoreMerkle != MerkleTree(*_tTransacoes.dados()):
            raise arvoreDeMerkleInvalida

        self.transacoes = _tTransacoes
        self.arvoreDeMerkle = _tArvoreMerkle

        _tArvoreJson = open("tmp.json", "w")
        util.remover_seguramente("tmp.json", 5)
        _tArvoreJson.close()
        
        return self