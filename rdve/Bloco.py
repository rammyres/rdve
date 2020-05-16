#!/usr/bin/env python3

from Transacoes import Transacoes
from Eleitor import tEleitor
from Candidato import tCandidato
from hashlib import sha256
from pymerkle import MerkleTree, hashing
from Erros import arvoreDeMerkleInvalida, tipoDeTransacaoDesconhecido, registroSemTransacoes, listaDeTransacoesVazia
import json

class listaDeTransacoes(list):
    
    def inserir(self, transacao):
        if isinstance(transacao, Transacoes):
            if len(self)<1:
                self.append(transacao)
            else:
                transacao.hashTransAnterior = self[len(self)-1].Hash
                self.append(transacao)
        else:
            raise tipoDeTransacaoDesconhecido
    
    def dados(self):
        _dados = []
        for d in self:
            _dados.append(d.dados())
        return _dados

    def dicionarios(self):
        if len(self)<1:
            raise listaDeTransacoesVazia
        _dicionarios = []
        for d in self:
            _dicionarios.append(d.dicionario())
        return _dicionarios

class Bloco: 
    index = None
    Hash_raiz = None
    Hash = None 
    Nonce = 1
    HashBlocoAnterior = None

    @property
    def arvoreDeMerkle(self):
        return self._arvoreDeMerkle

    @arvoreDeMerkle.setter
    def arvoreDeMerkle(self, arvore):
        if not self.transacoes:
            raise registroSemTransacoes
        _tArvore = MerkleTree(*self.transacoes.dados())
        if arvore != _tArvore:
            raise arvoreDeMerkleInvalida
        else:
            self._arvoreDeMerkle = arvore    

    def __init__(self, transacoes = None, arvoreDeMerkle = None):
        if transacoes and arvoreDeMerkle:
            self.transacoes = transacoes
            self.arvoreDeMerkle = arvoreDeMerkle
            self.Hash_raiz = self.arvoreDeMerkle.rootHash
        else:
            self.transacoes = listaDeTransacoes()

    def calcularArvoreDeMerkle(self):
        if len(self.transacoes)<1:
            raise listaDeTransacoesVazia
        else:
            self.arvoreDeMerkle = MerkleTree(*self.transacoes.dados())
            self.Hash_raiz = self.arvoreDeMerkle.rootHash
            
    def atualizarIndex(self, index):
        self.index = index

    def calcularHash(self):
        #gerador = hashing.HashMachine()
        _hash = ''
        while not _hash.startswith('00000000'):
            _dados = "{}{}{}".format(self.HashBlocoAnterior, self.Hash_raiz, self.Nonce)
            #_hash = gerador.hash(_dados)
            _hash = sha256(_dados.encode).hexdigest()
            self.Nonce += 1
        self.Hash = _hash

    def serializarBloco(self):
        if not self.arvoreDeMerkle:
            self.calcularArvoreDeMerkle()
        if not self.Hash:
            self.calcularHash()
        if self.transacoes and self.arvoreDeMerkle:
            _d = {"index": self.index, 
                  "HashBlocoAnterior": self.HashBlocoAnterior,
                  "Hash": self.Hash,
                  "Hash_raiz": self.Hash_raiz,
                  "arvoreDeMerkle": self.arvoreDeMerkle.serialize(),
                  "transacoes": self.transacoes.dicionarios()}
        else:
            raise listaDeTransacoesVazia

        return _d

    def exportarBloco(self, arquivo):
        if self.transacoes and self.arvoreDeMerkle:
            try:
                _arq = open(arquivo, "w")
                json.dump(self.serializarBloco(), _arq, indent=4)
            except IOError:
                return False
            return True

        