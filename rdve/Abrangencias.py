''' 
    Abstrai como classes as principais entidades existentes nas eleições do Brasil. 
    A principal diferença nos métodos inserir e incluir das classes abaixo é que a
    os métodos inserir recebem um objeto instanciado como parametro e o insere na 
    lista, enquanto os métodos incluir recebem os dados para instanciar um novo
    objeto e então fazer a inserção.
'''
import json
from collections import OrderedDict 
from hashlib import sha256
from Erros import abragenciaDuplicada

# Abstrai a seção eleitoral. A seção é o local onde a urna é instalada. É habitual que uma zona possa encompassar mais 
# de um municipio em regiões de cidades muito pequenas e um município grande possa emcompassar mais de uma zona, então
# as seções terão as duas vinculações, com uma classe-pai zona e uma classe-mãe seção, herdando somente seus identifi-
# cadores. 
class Secao(OrderedDict): 
    def __init__(self, idZona, idMunicipio, numero, nome):
        self.idZona = idZona
        self.idMunicipio = idMunicipio
        self.idSecao = "{}.{:04d}".format(idZona, int(numero)) # A id da seção segue o seguinte formato: UUZNNNN.SSSS, onde 
                                                               # UU é a sigla do estado, ZNNNN a zona e SSSS o sequencial 
                                                               # da seção
        self.nome = nome        

    def serializar(self):
        # Retorna o conteúdo da classe como um objeto dicionário serializável.
        dicionario= {"idZona": self.idZona, "idMunicipio": self.idMunicipio, "idSecao": self.idSecao, "nome": self.nome}
        return dicionario

# Abstrai a zona eleitoral, que norlamente se vincula diretamente ao TRE estadual (neste projeto uma abrangência estadual,
# conforme especificação mais adiante)
class Zona:
    secoes = [] # Cria a lista de seções vinculadas a zona 
    def __init__(self, uf, numero):
        self.uf = uf
        self.idZona = "{}Z{:04d}".format(uf, int(numero)) # A id da zona segue o seguinte formato: UUZNNNN, onde UU é a 
                                                          # sigla do estado onde a zona se localiza, Z indicativo de zona
                                                          # e NNNN é sequencial da zona
        self.seqS = 1 # Sequencial da seção, pode ser ignorado caso a operação seja de importação

    def validarSecao(self, secao_):
        # Valida a seção apresentada, para evitar inclusão duplicada, comparando a seção
        # com todas as seções já existentes no objeto
        for _s in self.secoes:
            if _s.idZona == self.idZona:
                if secao_.idSecao == _s.idSecao or _s.nome == secao_.nome:
                    raise abragenciaDuplicada

    def inserirSecao(self, secao_):
        # Insere a seção na lista de seções, caso ela não seja duplicada
        if isinstance(secao_, Secao):
            self.validarSecao(secao_)
            self.secoes.append(secao_)
    
    def incluirSecao(self, nome, idMunicipio):
        # Inclui uma nova seção, que será inserida na lista de seções do objeto 
        _tSecao = Secao(self.idZona, idMunicipio, self.seqS, nome)
        self.secoes.append(_tSecao)

    def serializar(self):
        # Retorna um objeto dicionário serializável, contendo os dados do objeto 
        _dicionarios = []
        _dicionarios.clear() # Evita que a seção recupere dados de outra zona
        for _s in self.secoes: # Coleta os dados das seções para incporar ao dicionáio da zona
            if _s.idZona == self.idZona:
                _dicionarios.append(_s.serializar())
        return {"idZona": self.idZona, "secoes": _dicionarios}

# A abrangência nacional é uma abrangência geral, que contem os estados e um dicionário especial
# contendo a id BR e o nome Brasil
class abrNacional: 
    abrEstaduais = [] # Cria a lista de abrangencias estaduais do país 
    def __init__(self):
        self.id = "BR"
        self.nome = "BRASIL"

    def inserirAbrEstadual(self, abrangenciaEstadual):
        # Insere uma abrangência estadual instanciada, caso não exista outra
        # igual na lista 
        if isinstance(abrangenciaEstadual, abrEstadual):
            self.validarEstado(abrangenciaEstadual)
            self.abrEstaduais.append(abrangenciaEstadual)
    
    def incluirAbrEstadual(self, nome, uf):
        # Instancia uma abrangência estadual a partir dos parametros e 
        # chama o método para inseri-la na lista de abrangencias do objeto
        _tAbrEstadual = abrEstadual(nome, uf)
        self.inserirAbrEstadual(_tAbrEstadual)

    def indexEstadoPorUF(self, uf):
        # Procura a sigla do estado (UF) na lista de abrangencias e retorna seu indice
        for x in range(len(self.abrEstaduais)):
            if self.abrEstaduais[x].uf == uf:
                return x
    
    def removerEstado(self, uf):
        # Remove o estado, caso ele seja encontrado na lista
        try:
            self.abrEstaduais.pop(self.indexEstadoPorUF(uf))
            return True
        except IndexError:
            return False
        except TypeError:
            return False

    def validarEstado(self, abrEstadual_):
        # Verificar se a abrangencia já se encontra na lista 
        for _e in self.abrEstaduais:
            if abrEstadual_.uf == _e.uf or abrEstadual_.nome == _e.nome:
                raise abragenciaDuplicada
        
    def serializar(self):
        _dicionarios = []
        for _e in self.abrEstaduais:
            _dicionarios.append(_e.serializar())
        saida = {"BR":"BRASIL", "abrEstaduais": _dicionarios} 
        return saida

class abrEstadual:
    # Abstrai uma abrangencia estadual. No mundo real normalmente são TREs, entretanto,
    # para simplificar, os dados são limitados a identificação do estado (nome e sigla, identificada por uf).
    # O objeto terá uma lista de zonas e uma lista de municipios (abrangencias municipais), que podem ou não 
    # se sobrepor. 
    zonas = []  # Lista de zonas do estado
    abrMunicipais = [] # lista de municiṕios do estado
    seqM = 1 # sequencial da lista de municipios
    seqZ = 1 # sequencial da lista de zonas

    def __init__(self, nome, uf):
        self.uf = str.upper(uf) # UF é basicamente a sigla do estado
        self.nome = str.upper(nome)

    # A partir deste ponto uma lista de metodos para validaão das zonas e abrangencias municipais se segue
    # A ideia é separar os métodos referentes as zonas e municipios. As funções são basicamente as mesmas.
    # Os métodos validar verificar se a abrangencia já existe nas listas, os incluir criam uma nova ins-
    # tancia de abrangencia (municipio ou zona) e a incluem nas listas, is inserir inserem objetos de 
    # abrangencias instanciados nas listas e os remover removem as abrangencia, se a id for localizada. 
    
    def validarZona(self, zona_):
        for _z in self.zonas:
            if zona_.idZona == _z.idZona:
                raise abragenciaDuplicada

    def inserirZona(self, zona_):
        self.validarZona(zona_)
        if isinstance(zona_, Zona):
            self.zonas.append(zona_)
    
    def incluirZona(self):
        _zona = Zona(self.uf, self.seqZ)
        self.inserirZona(_zona)
        self.seqZ += 1

    def indexZonaPorId(self, id):
        for x in range(len(self.zonas)):
            if self.zonas[x].idZona == id:
                return x
        return -1
    
    def removerZona(self, id):
        try:            
            self.zonas.pop(self.indexZonaPorId(id))
            return True
        except IndexError:
            return False
    
    def validarMunicipio(self, abrMunicipal_):
        for _m in self.abrMunicipais:
            if _m.idMunicipio == abrMunicipal_.idMunicipio or _m.nome == abrMunicipal_.nome:
                raise abragenciaDuplicada

    def inserirAbrMunicipal(self, abrMunicipal_):
        if isinstance(abrMunicipal_, abrMunicipal):
            self.validarMunicipio(abrMunicipal_)
            self.abrMunicipais.append(abrMunicipal_)
            self.seqM = int(abrMunicipal_.idMunicipio[3:7])
            self.seqM += 1

    def incluirAbrMunicipal(self, nome, seq = None):
        if not seq: 
            _tAbrMunicipal = abrMunicipal(self.uf, self.seqM, nome)
        else:
            _tAbrMunicipal = abrMunicipal(self.uf, seq, nome)
            self.seqM = seq
        self.inserirAbrMunicipal(_tAbrMunicipal)

    def indexMunicipioPorId(self, id):
        for x in range(len(self.abrMunicipais)):
            if self.abrMunicipais[x].idMunicipio == id:
                return x
        return -1
    
    def removerMunicipio(self, id):
        try:
            self.abrMunicipais.pop(self.indexMunicipioPorId(id))
            return True
        except IndexError:
            return False
        except TypeError:
            return False

    def serializar(self):
        _dicionariosZ = []
        _dicionariosM = []
        _dicionariosM.clear()
        _dicionariosZ.clear()
        for _z in self.zonas:
            if _z.idZona.startswith(self.uf):
                _dicionariosZ.append(_z.serializar())
        for _abrM in self.abrMunicipais:
            if _abrM.idMunicipio.startswith(self.uf):
                _dicionariosM.append(_abrM.serializar())
        saida = {"abrEstadual": self.uf, "estado": self.nome, "zonas": _dicionariosZ, "abrMunicipais": _dicionariosM}
        print(saida)
        return saida


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

    def removerSecao(self, id):
        try:
            self.secoes.pop(self.indexSecaoPorId(id))
            return True
        except IndexError:
            return False
        except TypeError:
            return False

    def serializar(self):
        _dicionarios = []
        _dicionarios.clear()
        for _secao in self.secoes:
            if _secao.idSecao[:2] == self.idMunicipio[:2] and _secao.idMunicipio == self.idMunicipio:
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
                    for _abrZ in _abrE.zonas:
                        if _abrZ.idZona[:2] == UF:
                            _tAbr.append({"ID Zona": _abrZ.idZona, "Descrição": "{}ª zona eleitoral".format(_abrZ.idZona[-4:])})

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
                    _tSecao =  Secao(_dS["idSecao"][:6], _dS["idMunicipio"], _dS["idSecao"][-4:], _dS["nome"])
                    _tZona.inserirSecao(_tSecao)
                _tAbrEstadual.inserirZona(_tZona)

            for _dAM in _dE["abrMunicipais"]:
                if _dAM["idMunicipio"][:2] == _tAbrEstadual.uf:
                    _tAbrMunicipal = abrMunicipal(_dAM["idMunicipio"][:2], _dAM["idMunicipio"][-4:], _dAM["nome"])
                    for _dS in _dAM["secoes"]:
                        _tSecao =  Secao(_dS["idSecao"][:6], _dS["idMunicipio"], _dS["idSecao"][-4:], _dS["nome"])
                        _tAbrMunicipal.inserirSecao(_tSecao)
                    _tAbrEstadual.inserirAbrMunicipal(_tAbrMunicipal)
            
            self.abrNacional.inserirAbrEstadual(_tAbrEstadual)
