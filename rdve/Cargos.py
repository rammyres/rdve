from Abrangencias import abrNacional, abrEstadual, abrMunicipal
from Erros import abrangenciaInvalida

class Cargo:
    idCargo = None
    descricao = None
    
    def __init__(self, idAbrangencia, sequencial, descricao):
        self.idCargo = "{}.{}".format(idAbrangencia, sequencial)
        self.descricao = descricao

class Cargos(list):
    abrangencias = []
    seqC = 1

    def __init__(self):
        self.abrangencias.append({"BR": "BRASIL"})

    def validarAbrangencias(self, abrangencia):
        if abrangencia == "BR":
            return True

        for _abrE in self.abrangencias:
            if _abrE.uf == abrangencia:
                return True
            else:
                for _abrM in _abrE.abrMunicipais:
                    if abrangencia == _abrM.idMunicipio:
                        return True
        else:
            return False

    def importarAbrangenias(self, dicionario):
        for _dE in dicionario:
            _tAbrEstadual = abrEstadual(_dE["estado"], _dE["abrEstadual"])

            for _dAM in _dE["abrMunicipais"]:
                if _dAM["idMunicipio"][:2] == _tAbrEstadual.uf:
                    _tAbrMunicipal = abrMunicipal(_dAM["idMunicipio"][:2], _dAM["idMunicipio"][-4:], _dAM["nome"])
    
                    _tAbrEstadual.inserirAbrMunicipal(_tAbrMunicipal)
            
            self.abrangencias.append(_tAbrEstadual)

    def inserir(self, cargo):
        if isinstance(cargo, Cargo):
            if self.validarAbrangencias(cargo.idAbrangencia):
                self.append(cargo)
            else:
                raise abrangenciaInvalida
        else:
            raise abrangenciaInvalida

    def incluir(self, idAbrangencia, descricao):
        _tCargo = Cargo(idAbrangencia, self.seqC, descricao)
        self.inserir(_tCargo)
        self.seqC += 1

    def serializar(self):
        _dicionarios = []
        for _c in self:
            _dicionarios.append({"idCargo": _c.idCargo, "descricao": _c.descricao})

        return {"cargos": _dicionarios}

    def importar(self, dicionario):
        for _c in dicionario["cargos"]:
            _id = _c["idCargo"].split(".")
            _tCargo = Cargo(_id[0], _id[1], _c["nome"])
            self.inserir(_tCargo)       