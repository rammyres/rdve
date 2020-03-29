#!/usr/bin/env python3

from hashlib import sha256
from pymerkle.hashing import HashMachine
from datetime import date, datetime
import json

class BlocoGenesis:
    abrangencias = {}
    Hash = None

    def __init__(self, eleicao):
        self.eleicao = eleicao # Eleicação no formado AAAATT, onde TT é o turno,
                               # exemplo, eleição 202001

    def definirDataVotacao(self, data):
        self.dataVotacao = data
    
    def carregarAbrangencia(self):
        _abr = open("abrangencias.json", "r")
        self.abrangencias = json.load(_abr)
        _abr.close()

    def dados(self):
        hashAbrangencias = sha256()
        tamanho = 65536
        with open("abrangencias.json", "rb") as _abr:
            _abr_b = _abr.read(tamanho)
            while len(_abr_b)>0:
                hashAbrangencias.update(_abr_b)
                _abr_b = _abr.read(tamanho)
        return "Genesis:{}:{}".format(self.dataVotacao, hashAbrangencias)

    def criarHash(self):
        gerardorDeHash = HashMachine()
        self.Hash = gerardorDeHash.hash(self.dados().encode()).decode()

    def dicionario(self):
        _dicionario = {"Genesis":{"eleicao": self.eleicao, 
                                  "dataVotacao": self.dataVotacao, 
                                  "hash": self.criarHash()}
                                  }
        return _dicionario

    def criarBlocoGenesis(self):
        _arq = open("blockchain.json", "w")
        json.dump(self.dicionario(), _arq, indent=4)
        _arq.close()