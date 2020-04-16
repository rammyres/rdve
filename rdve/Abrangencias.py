import json
from collections import OrderedDict 
from hashlib import sha256

class Secao(OrderedDict): 
    def __init__(self, idZona, numero, nome):
        self.idZona = idZona
        self.idSecao = "{}.{:04d}".format(idZona, numero)
        self.nome = nome
        self.dicionario= {"idZona": idZona, "idSecao": self.idSecao, "nome": nome}

    def serializar(self):
        return self.dicionario

class Zona:
    secoes = []
    def __init__(self, uf, numero):
        self.uf = uf
        self.idZona = "{}Z{:04d}".format(uf, int(numero))
        self.seqS = 1
        
    def inserirSecao(self, secao_):
        if isinstance(secao_, Secao):
            self.secoes.append(secao_)
    
    def incluirSecao(self, nome):
        _tSecao = Secao(self.idZona, self.seqS, nome)
        self.secoes.append(_tSecao)

    def serializar(self):
        _dicionarios = []
        for _s in self.secoes:
            _dicionarios.append(_s.serializar())
        return {"idZona": self.idZona, "secoes": _dicionarios}

class abrNacional:
    abrEstaduais = []
    def __init__(self):
        self.id = "BR"
        self.nome = "BRASIL"

    def inserirAbrEstadual(self, abrangenciaEstadual):
        if isinstance(abrangenciaEstadual, abrEstadual):
            self.abrEstaduais.append(abrangenciaEstadual)
    
    def incluirAbrEstadual(self, nome, uf):
        _tAbrEstadual = abrEstadual(nome, uf)
        self.inserirAbrEstadual(_tAbrEstadual)

    def indexEstadoPorUF(self, uf):
        for x in range(len(self.abrEstaduais)):
            if self.abrEstaduais[x].uf == uf:
                return x
        
    def serializar(self):
        _dicionarios = []
        for _e in self.abrEstaduais:
            _dicionarios.append(_e.serializar())
        return {"BR":"BRASIL", "abrEstaduais": _dicionarios}

class abrEstadual:
    zonas = []
    abrMunicipais = []
    seqM = 1

    def __init__(self, nome, uf):
        self.uf = str.upper(uf)
        self.nome = str.upper(nome)

    def inserirZona(self, zona_):
        if isinstance(zona_, Zona):
            self.zonas.append(zona_)
    
    def incluirZona(self, numero):
        _zona = Zona(self.uf, numero)
        self.zonas.append(_zona)


    def inserirAbrMunicipal(self, abrMunicipal_):
        if isinstance(abrMunicipal_, abrMunicipal):
            self.abrMunicipais.append(abrMunicipal_)
            self.seqM = int(abrMunicipal_.idMunicipio[3:7])
            self.seqM += 1

    def incluirAbrMunicipal(self, nome, seq = None):
        if not seq: 
            _tAbrMunicipal = abrMunicipal(self.uf, self.seqM, nome)
        else:
            _tAbrMunicipal = abrMunicipal(self.uf, seq, nome)
            self.seqM = seq
        self.abrMunicipais.append(_tAbrMunicipal)
        self.seqM += 1

    def indexMunicipioPorId(self, id):
        for x in range(len(self.abrMunicipais)):
            if self.abrMunicipais[x].idMunicipio == id:
                return x
        return -1
    
    def indexZonaPorId(self, id):
        for x in range(len(self.zonas)):
            if self.zonas[x].idZona == id:
                return x
        return -1

    def serializar(self):
        _dicionariosZ = []
        _dicionariosM = []
        for _z in self.zonas:
            if _z.idZona.startswith(self.uf):
                _dicionariosZ.append(_z.serializar())
        for _abrM in self.abrMunicipais:
            if _abrM.idMunicipio.startswith(self.uf):
                _dicionariosM.append(_abrM.serializar())
        return {"abrEstadual": self.uf, "estado": self.nome, "zonas": _dicionariosZ, "abrMunicipais": _dicionariosM}


class abrMunicipal: 
    secoes = []
    seqS = 1

    def __init__(self, uf, sequencial, nome):
        self.idMunicipio = "{}M{:04d}".format(uf, int(sequencial))
        self.nome = str.upper(nome)

    def inserirSecao(self, secao_):
        if isinstance(secao_, Secao):
            self.secoes.append(secao_)

    def indexSecaoPorId(self, id):
        for x in range(len(self.secoes)):
            if self.secoes[x].idSecao == id:
                return x
        return -1

    def serializar(self):
        _dicionarios = []
        for _secao in self.secoes:
            _dicionarios.append(_secao.serializar())
        return {"idMunicipio": self.idMunicipio, "nome": self.nome, "secoes": _dicionarios}

class RegistroAbrangencias:
    def __init__(self):
        self.abrNacional = abrNacional()

    def exportarAbrangencias(self, arquivo):
        _arq = open(arquivo, "w")

        json.dump({"registro_abrangencias": self.abrNacional.serializar()}, _arq, indent=4)

        _arq.close()

    def listarAbrangencias(self, tipo, UF = None):
        _tAbr = []
        if tipo == 1: # Retorna uma lista de abrangências estaduais
            for _abr in self.abrNacional.abrEstaduais:
                _t = {"UF": _abr.uf, "nome": _abr.nome}
                _tAbr.append(_t)
        if tipo == 2 and UF: # Retorna uma lista das abrangnencias municipais existentes
                             # na UF apontada
            for _abrE in self.abrNacional.abrEstaduais:
                if _abrE.uf == UF: 
                    for _abrM in _abrE.abrMunicipais:
                        if _abrM.idMunicipio[:2] == UF:
                            _tAbr.append({"ID Municipio": _abrM.idMunicipio, "Nome": _abrM.nome})
        if tipo == 3 and UF: #Retorna as zonas existentes na UF apontada
            for _abrE in self.abrNacional.abrEstaduais:
                if _abrE.uf == UF:
                    for _abrZ in _abrE:
                        if _abrZ[:2] == UF:
                            _tAbr.append({"ID Zona": _abrZ.idZona, "Numero": _abrZ.numero})

        return _tAbr

    def importarAbrangencias(self, arquivo):
        _arq = open(arquivo, "r")

        dicionarios = json.load(_arq)

        _arq.close()

        for _dE in dicionarios["registro_abrangencias"]["abrEstaduais"]:
            _tAbrEstadual = abrEstadual(_dE["estado"], _dE["abrEstadual"])

            for _dZ in _dE["zonas"]:
                _tZona = Zona(_dZ["idZona"][:2], _dZ["idZona"][-4:])
                for _dS in _dZ["secoes"]:
                    _tSecao =  Secao(_dS["idSecao"][:6], _dS["idSecao"][-4:], _dS["nome"])
                    _tZona.inserirSecao(_tSecao)
                _tAbrEstadual.inserirZona(_tZona)

            for _dAM in _dE["abrMunicipais"]:
                if _dAM["idMunicipio"][:2] == _tAbrEstadual.uf:
                    print("{} - {}".format(_dAM["idMunicipio"][:2], _tAbrEstadual.uf))
                    _tAbrMunicipal = abrMunicipal(_dAM["idMunicipio"][:2], _dAM["idMunicipio"][-4:], _dAM["nome"])
                    for _dS in _dAM["secoes"]:
                        _tSecao =  Secao(_dS["idSecao"][:6], _dS["idSecao"][-4:], _dS["nome"])
                        _tAbrMunicipal.inserirSecao(_tSecao)
                    _tAbrEstadual.inserirAbrMunicipal(_tAbrMunicipal)
            
            self.abrNacional.inserirAbrEstadual(_tAbrEstadual)
