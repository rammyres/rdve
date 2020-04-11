import json 
from hashlib import sha256
from pymerkle import MerkleTree

class Secao: 
    def __init__(self, zona, numero, nome):
        self.zona = zona
        self.numero = numero
        self.nome = nome

    def dicionario(self):
        return {"zona": self.zona, "secao": self.numero, "nome": self.nome}

class Zona:
    secoes = []

    def __init__(self, abrEstadual, numero):
        self.abrEstadual = abrEstadual
        self.numero = numero

    def inserirSecao(self, secao_):
        if isinstance(secao_, Secao):
            self.secoes.append(secao_)

    def dicionario(self):
        _dicionarios = []
        for _s in self.secoes:
            if(_s.zona == self.numero):
                _d = {"secao": _s.numero, "nome": _s.nome}
                _dicionarios.append(_d)
        return {"zona": self.numero, "secoes": _dicionarios}

class abrNacional:
    def __init__(self):
        self.nome = "BRASIL"
        self.numero = "1"
        
    def dicionario(self):
        return {self.numero: self.nome}

class abrEstadual:
    zonas = []
    def __init__(self, nome, sequencial):
        self.nome = nome
        self.numero = "3{:0>2d}".format(sequencial)

    def incluirZona(self, numero):
        _zona = Zona(self.numero, numero)
        self.zonas.append(_zona)

    def dicionario(self):
        _dicionarios = []
        for _z in self.zonas:
            if _z.abrEstadual == self.numero:
                _d = _z.dicionario()
                _dicionarios.append(_d)
        return {"abrEstadual": self.numero, "zonas": _dicionarios}

class abrMunicipal: 
    secoes = []

    def __init__(self, nome, sequencial):
        self.nome = nome
        self.numero = "5{:0>4d}".format(sequencial)

    def incluirSecao(self, secao_):
        if isinstance(secao_, Secao):
            self.secoes.append(secao_)

    def dicionario(self):
        _dicionarios = []
        for _secao in self.secoes:
            _dicionario = _secao.dicionario()
            _dicionarios.append(_dicionario)
        return {"abrMunicipal": self.numero, "nome": self.nome, "secoes": _dicionarios}

class BlocoAbrangencias:
    hashBlocoAnterior = ''
    Hash = ''

# Cria o bloco de abrangencias que é contíguo ao bloco Gênesis e define quais municipios, zonas
# e seções participarão da eleição.
    def __init__(self, tipo_deEleicao, eleicao):
        _arq = open("blockchain.json", "r")
        _bloco = json.load(_arq)
        _arq.close()

        for _b in _bloco:
            if _b["index"] == "1" and _b["tipo"] == "Genesis":
                self.hashBlocoAnterior = _b["hash"]
            if _b["tipo"] == "abrangencias":
                self.importarDicionario(_b)        

        if tipo_deEleicao == 1: 
            # Cria a abrangencia nacional e abrangencias estaduais para inclusão das zonas abrangidas
            self.abrangenciaNacional = abrNacional()
            self.abrangenciaisEstaduais = []
            self.sequencialEstado = 1
        if tipo_deEleicao == 2:
            # Cria as abrangencias onde serão eleitos prefeitos e vereadores
            self.abrangenciasMunicipais = []
            self.sequencialMunicipio = 1
        if tipo_deEleicao == 3:
            # Cria a abrangencia nacional, para eleição-tampão de presidente
            self.abrangenciaNacional = abrNacional()
        if tipo_deEleicao == 4:
            # Cria abrangencia estadual para eleição-tampão de governador
            self.abrangenciaEstadual = None
            self.sequencialEstado = 1
        if tipo_deEleicao == 5:
            # Cria a abrangencia municipal, para eleição tampão de prefeito
            self.abrangenciaMunicipal = None
            self.sequencialMunicipio = 1
        self.tipo_deEleicao = tipo_deEleicao
        self.eleicao = eleicao

    def incluirAbrEstadual(self, nome, sequencial):
        if self.abrangenciaisEstaduais:
            _abrEstadual = abrEstadual(nome, sequencial)
            self.abrangenciaisEstaduais.append(_abrEstadual)
            self.sequencialEstado += 1
    
    def definirMunicipio(self, nome, sequencial):
        self.abrangenciaMunicipal = abrMunicipal(nome, self.sequencialMunicipio)
    
    def definirEstado(self, nome, sequencial):
        self.abragenciaEstadual = abrEstadual(nome, sequencial)

    