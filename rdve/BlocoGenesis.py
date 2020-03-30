#!/usr/bin/env python3
from hashlib import sha256
from pymerkle.hashing import HashMachine
from datetime import datetime
from rdve.Erros import dataInferiorAoLimite
import json

class BlocoGenesis:
    abrangencias = {}
    hashAbrangencias = None
    _dataVotacao = None
    Hash = None

    def __init__(self, eleicao, dataVotacao):
        self.eleicao = eleicao # Eleicação no formado AAAATT, onde TT é o turno,
                               # exemplo, eleição 202001
        self.dataVotacao = dataVotacao

    @property
    def dataVotacao(self):
        return self._dataVotacao

    @dataVotacao.setter
    def dataVotacao(self, dataVotacao):
        _tDataVotacao = datetime.strptime(dataVotacao, "%Y-%m-%d")
        if _tDataVotacao <= datetime.today():
            raise dataInferiorAoLimite
        self._dataVotacao = dataVotacao

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
        self.hashAbrangencias = hashAbrangencias.hexdigest()
        return "Genesis:{}:{}".format(self.dataVotacao, hashAbrangencias)

    def criarHash(self):
        gerardorDeHash = HashMachine()
        self.Hash = gerardorDeHash.hash(self.dados().encode()).decode()

    def dicionario(self):
        _dicionario = {"index": "0", "tipo":"Genesis",
                        "bloco":{"eleicao": self.eleicao, 
                                  "abrangencias":self.abrangencias,
                                  "hashAbrangencias": self.hashAbrangencias,
                                  "dataVotacao": self.dataVotacao, 
                                  "hash": self.Hash}
                                  }
        return _dicionario

    def criarBlocoGenesis(self):
        _arq = open("blockchain.json", "w", encoding="latin-1")
        json.dump(self.dicionario(), _arq, indent=4)
        _arq.close()