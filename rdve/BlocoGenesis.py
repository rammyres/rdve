#!/usr/bin/env python3
from hashlib import sha256
from datetime import datetime
from rdve.Erros import dataInferiorAoLimite
from Abrangencias import RegistroAbrangencias
from Utilitarios import hashArquivo
import json

class BlocoGenesis:
    nonce = 0
    Hash = ''
    abrangencias = RegistroAbrangencias()
    hashAbrangencias = None
    tipo_Eleicao = None
    alistamento_dataInicio = None
    alistamento_dataFim = None
    candidatura_dataInicio = None
    candidatura_dataFim = None
    dataVotacao = None

    def __init__(self, eleicao, tipo_Eleicao):
        self.tipo_Eleicao = tipo_Eleicao # Os seguintes tipos de eleições serão aceitos:
                                         # 1 para eleição nacional (presidente, governadores, deputados e senadores, abrangencia Nacional, 
                                         # com abrangencias nacionais e estaduais)
                                         # 2 para eleições municipal (prefeitos e vereadores), com abrangencias municipais
                                         # 3 para eleições extraordinarias nacionais (somente o presidente)
                                         # 4 para eleições extraordinarias estaduais (somente o governador)
                                         # 5 para eleições extraordinárias municipais (somente prefeito)
        self.eleicao = eleicao # Eleicação no formado AAAA.RR, onde RR é o sequencial indicativo de regularidade. Deve ser 1 para eleição 
                               # regular e a partir de 2 eleições extraordinárias. 
                               # Exemplo, eleição 2020.01

    def importarAbrangencias(self, arquivo):
        try:
            self.abrangencias.importarAbrangencias(arquivo)
            self.hashAbrangencias = hashArquivo(arquivo)
        except IOError:
            print("O arquivo de abrangências não existe. Um arquivo com as abrangências da eleição válido deve"\
                   "estar presente para gerar o blocogenesis")


    def definirPeriodoalistamento(self, dataInicio, dataFim):
        # A função deve ser chamada para definir o periodo de alistamento eleitoral, eleitores já existentes
        # também deverão ser importados durante esse periodo. As datas devem ser str, no formato AAAA-MM-DD        
        self.alistamento_dataInicio = str(datetime.strptime(dataInicio, "%Y-%m-%d"))
        self.alistamento_dataFim = str(datetime.strptime(dataFim, "%Y-%m-%d"))

    def definirPeriodoCandidaturas(self, dataInicio, dataFim):
        # A função deve ser chamada para definir o periodo de registro das candidaturas. 
        # A data deve ser str, no formamto AAAA-MM-DD
        self.candidatura_dataInicio = str(datetime.strptime(dataInicio, "%Y-%m-%d"))
        self.alistamento_dataFim = str(datetime.strptime(dataFim, "%Y-%m-%d"))

    def definirDataVotacao(self, data):
        # Define a data da votação do primeiro turno, um bloco de criação de segundo turno conterá
        # outra data para o segundo turno
        self.dataVotacao = str(datetime.strptime(data, "%Y-%m-%d"))

    def dados(self):
        # Retorna os dados de identificação do block genesis, principalmente para calculo do hash
        return "Genesis:{}:{}:{}:{}:{}:{}:{}:{}:{}".format(self.tipo_Eleicao, self.eleicao, self.nonce, self.hashAbrangencias, 
                                                        self.alistamento_dataInicio, self.alistamento_dataFim, 
                                                        self.candidatura_dataInicio, self.candidatura_dataFim,
                                                        self.dataVotacao)

    def criarHash(self):
        # Calcula o hash do bloco, usando os dados e o nonce. O hash tem dificuldade 
        _hash = ''
        while not _hash.startswith('00000'):
            _hash = sha256(self.dados().encode()).hexdigest()
            self.nonce += 1
        self.Hash = '0x{}'.format(_hash)

    def dicionario(self):
        # Retorna o bloco Gênesis serializado
        _dicionario = {"index": "0", 
                       "tipo":"Genesis",
                       "tipo_eleicao": self.tipo_Eleicao, 
                       "eleicao": self.eleicao, 
                       "nonce": self.nonce,
                       "hashAbrangencias": self.hashAbrangencias,
                       "alistamento_dataInicio": self.alistamento_dataInicio,
                       "alistamento_dataFim": self.alistamento_dataFim, 
                       "candidatura_dataInicio": self.candidatura_dataInicio, 
                       "cadidatura_dataFim": self.candidatura_dataFim,
                       "dataVotacao": self.dataVotacao,
                       "hash": self.Hash,
                       "registro_abrangencias": self.abrangencias.abrNacional.serializar()
                      }
        return _dicionario

    def criarBlocoGenesis(self):
        _arq = open("blockchain.json", "w", encoding="latin-1")
        json.dump(self.dicionario(), _arq, indent=4)
        _arq.close()