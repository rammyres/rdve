import json
from collections import OrderedDict 
from hashlib import sha256

class Secao(OrderedDict): 
    def __init__(self, idZona, numero, nome):
        self.update({"idZona": idZona, "idSecao": "{}.{:04d}".format(idZona, numero), "nome": nome})

    def serializar(self):
        return self

class Zona(OrderedDict):
    secoes = []

    def __init__(self, uf, numero):
        self.update({"idZona": "{}Z{:04d}".format(uf, numero)})
        
    def inserirSecao(self, secao_):
        if isinstance(secao_, Secao):
            self.secoes.append(secao_)

    def serializar(self):
        _dicionarios = []
        for _s in self.secoes:
            if(_s["idZona"]==self["idZona"]):
                _dicionarios.append(_s.serializar())
        return {"idZona": self["idZona"], "secoes": _dicionarios}

class abrNacional(OrderedDict):
    abrEstaduais = []
    def __init__(self):
        self.update({"BR":"BRASIL"})

    def incluirAbrEstadual(self, abrangenciaEstadual):
        if isinstance(abrangenciaEstadual, abrEstadual):
            self.abrEstaduais.append(abrangenciaEstadual)
        
    def serializar(self):
        _dicionarios = []
        for _e in self.abrEstaduais:
            _dicionarios.append(_e.serializar())
        return {"BR": self["BR"], "abrEstaduais": _dicionarios}

class abrEstadual(OrderedDict):
    zonas = []
    abrMunicipais = []
    seqM = 1

    def __init__(self, nome, uf):
        self.update({"UF": uf, "nome": nome})

    def incluirZona(self, numero):
        _zona = Zona(self["UF"], numero)
        self.zonas.append(_zona)

    def inserirAbrMunicipal(self, abrMunicipal_):
        if isinstance(abrMunicipal_, abrMunicipal):
            self.abrMunicipais.append(abrMunicipal_)
            self.seqM = int(abrMunicipal_["idMunicipio"][3:7])
            self.seqM += 1

    def incluirAbrMunicipal(self, nome, seq = None):
        if not seq: 
            _tAbrMunicipal = abrMunicipal(self["UF"], self.seqM, nome)
        else:
            _tAbrMunicipal = abrMunicipal(self["UF"], seq, nome)
            self.seqM = seq
        self.abrMunicipais.append(_tAbrMunicipal)
        self.seqM += 1

    def serializar(self):
        _dicionariosZ = []
        _dicionariosM = []
        for _z in self.zonas:
            if _z.idZona.startswith(self["UF"]):
                _dicionariosZ.append(_z.dicionario())
        for _abrM in self.abrMunicipais:
            _dicionariosM.append(_abrM.dicionario())
        return {"abrEstadual": self["UF"], "estado": self["nome"], "zonas": _dicionariosZ, "abrMunicipais": _dicionariosM}


class abrMunicipal(OrderedDict): 
    secoes = []

    def __init__(self, uf, sequencial, nome): 
        self.update({"idMunicipio": "{}M{:04d}".format(uf,sequencial), "nome": nome})

    def incluirSecao(self, secao_):
        if isinstance(secao_, Secao):
            self.secoes.append(secao_)

    def serializar(self):
        _dicionarios = []
        for _secao in self.secoes:
            _dicionarios.append(_secao.serializar())
        return {"abrMunicipal": self["idMunicipio"], "nome": self["nome"], "secoes": _dicionarios}

class RegistroAbrangencias:
    def __init__(self):
        self.abrNacional_ = abrNacional()

    def exportarAbrangencias(self, arquivo):
        _arq = open(arquivo, "w")

        json.dump({"registro_abrangencias": self.abrNacional_.serializar()}, _arq, indent=4)

        _arq.close()

    def listarAbrangencias(self, tipo, UF = None):
        _tAbr = []
        if tipo == 1:
            for _abr in self.abrNacional_.abrEstaduais:
                _t = {"UF": _abr["UF"], "nome": _abr["nome"]}
                _tAbr.append(_t)
        if tipo == 2 and UF:
            for _abrE in self.abrNacional_.abrEstaduais:
                if _abrE["UF"] == UF:
                    _tAbr = [{"ID Municipio": _abrM["idMunicipio"], "Nome": _abrM["nome"]} 
                            for _abrM in self.abrNacional_.abrEstaduais if _abrM["idMunicipio"][:2] == UF]

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
