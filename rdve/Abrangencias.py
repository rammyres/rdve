import json 
from hashlib import sha256
from pymerkle import MerkleTree
from collections import OrderedDict

class Secao: 
    def __init__(self, idZona, numero, nome):
        self.idSecao = "{}.{:04d}".format(idZona, numero)
        self.nome = nome

    def dicionario(self):
        return {"secao": self.idSecao, "nome": self.nome}

    def importarDicionario(self, dicionario):
        if "secao" in dicionario.keys():
            _tSecao = Secao(dicionario["idSecao"][:6], dicionario["idSecao"][-4:], dicionario["nome"])
            return _tSecao

class Zona:
    secoes = []

    def __init__(self, uf, numero):
        self.idZona = "{}{:04d}".format(uf, numero)
        
    def inserirSecao(self, secao_):
        if isinstance(secao_, Secao):
            self.secoes.append(secao_)

    def dicionario(self):
        _dicionarios = []
        for _s in self.secoes:
            if(_s.idZona == self.idZona):
                _d = {"secao": _s.idSecao, "nome": _s.nome}
                _dicionarios.append(_d)
        return {"zona": self.idZona, "secoes": _dicionarios}

class abrNacional:
    abrEstaduais = []
    def __init__(self):
        self.nome = "BRASIL"
        self.idAbr = "BR"

    def incluirAbrEstadual(self, abrangenciaEstadual):
        if isinstance(abrangenciaEstadual, abrEstadual):
            self.abrEstaduais.append(abrangenciaEstadual)
        
    def dicionario(self):
        _dicionarios = []
        for _e in self.abrEstaduais:
            _dicionarios.append(_e.dicionario())
        return {self.idAbr: self.nome, "abrEstaduais": _dicionarios}

class abrEstadual:
    zonas = []
    abrMunicipais = []
    seq = 1
    def __init__(self, nome, uf):
        self.nome = nome
        self.UF = uf

    def incluirZona(self, numero):
        _zona = Zona(self.UF, self.seq)
        self.zonas.append(_zona)
        self.seq += 1

    def incluirAbrMunicipal(self, abrMunicipal):
        self.abrMunicipais.append(abrMunicipal)

    def dicionario(self):
        _dicionariosZ = []
        _dicionariosM = []
        for _z in self.zonas:
            if _z.idZona.startswith(self.UF):
                _dicionariosZ.append(_z.dicionario())
        for _abrM in self.abrMunicipais:
            _dicionariosM.append(_abrM.dicionario())
        return {"abrEstadual": self.UF, "estado": self.nome, "zonas": _dicionariosZ, "abrMunicipais": _dicionariosM}


class abrMunicipal: 
    secoes = []

    def __init__(self, uf, sequencial, nome): #TODO
        self.nome = nome
        self.idMunicipio = "{}.{:04d}".format(uf,sequencial)

    def incluirSecao(self, secao_):
        if isinstance(secao_, Secao):
            self.secoes.append(secao_)

    def dicionario(self):
        _dicionarios = []
        for _secao in self.secoes:
            _dicionarios.append(_secao.dicionario())
        return {"abrMunicipal": self.idMunicipio, "nome": self.nome, "secoes": _dicionarios}

class BlocoAbrangencias:
    def __init__(self, tipo_deEleicao, eleicao):
        self.tipo_deEleicao = tipo_deEleicao
        self.eleicao = eleicao
        self.abrNacional_ = abrNacional()

    def exportarAbrangencias(self, arquivo):
        _arq = open(arquivo, "w")

        json.dump({"eleicao": self.eleicao, 
                   "tipo_deEleicao":self.tipo_deEleicao,
                   "bloco_abrangencias": self.abrNacional_.dicionario()}, 
                   _arq, indent=4)

        _arq.close()

    def importarAbrangencias(self, arquivo):
        _arq = open(arquivo, "r")

        dicionarios = json.load(_arq)

        _arq.close()

        self.tipo_deEleicao = dicionarios["tipo_deEleicao"]
        self.eleicao = dicionarios["eleicao"]
        
        for _dE in dicionarios["bloco_abrangencias"]:
            _tAbrEstadual = abrEstadual(_dE["estado"], _dE["abrEstadual"])

            for _dZ in _dE["zonas"]:
                _tZona = Zona(_dZ["idZona"][:2], _dZ["idZona"][-4:])

                for _dS in _dZ["secoes"]:
                    _tSecao =  Secao(_dS["idSecao"][:6], _dS["idSecao"][-4:], _dS["nome"])
                    _tZona.inserirSecao(_tSecao)

                _tAbrEstadual.incluirZona(_tZona)

            for _dAM in _dE["abrMunicipais"]:
                _tAbrMunicipal = abrMunicipal(_dAM["idMunicipio"][:2], _dAM["idMunicipio"][-4:], _dAM["nome"])
                for _dS in _dAM["secoes"]:
                    _tSecao =  Secao(_dS["idSecao"][:6], _dS["idSecao"][-4:], _dS["nome"])
                    _tAbrMunicipal.incluirSecao(_tSecao)
                _tAbrEstadual.incluirAbrMunicipal(_tAbrMunicipal)
            
            self.abrNacional_.incluirAbrEstadual(_tAbrEstadual)
