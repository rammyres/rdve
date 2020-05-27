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