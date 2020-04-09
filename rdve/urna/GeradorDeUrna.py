from rdve.Cedulas import Cedulas
from rdve.Erros import saldoInconsistente
from rdve.Candidato import Candidato, tCandidato
from rdve.Eleitor import Eleitor, tEleitor
from rdve.Utilitarios import gerarChavePublica, gerarChavePrivada, gerarEndereco, importarChavePublica
from pymerkle import hashing
from datetime import datetime

class regEleitor:
    endereco = None
    saldo = None

    def __init__(self, endereco, titulo):
        self.endereco = endereco
        self.titulo = titulo

class regCandidato:
    endereco = None
    saldo = None

    def __init__(self, numero, abrangencia, endereco, nome):
        self.nome = nome
        self.numero = numero
        self.abrangencia = abrangencia
        self.endereco = endereco
        self.saldo = 0

class GeradorDeUrna:
    eleicao = None
    abrangencia = None
    zona = None
    secao = None
    saldoInicial = None
    timestamp = None
    endereco = None
    chavePublica = None
    candidatos = []
    eleitores = []
    cedulas = Cedulas()
    
    def __init__(self, eleicao, zona, secao):
        self.eleicao = eleicao
        self.zona = zona
        self.secao = secao
        self.timestamp = datetime.utcnow().timestamp()
        self.saldoInicial = 0

    def incluirEleitor(self, eleitor_):
        if isinstance(eleitor_, tEleitor):
            _tEleitor = regEleitor(eleitor_.endereco, eleitor_.titulo)
            self.eleitores.append(_tEleitor)
            self.saldoInicial += 1
    
    def serializarEleitores(self):
        _dicionarios = []
        for _eleitor in self.eleitores:
            _dicionario = {"endereco": _eleitor.endereco, "titulo": _eleitor.titulo}
            _dicionarios.append(_dicionario)
        return  _dicionarios

    def importarEleitor(self, dEleitor_):
        if dEleitor_["tipo"] == "eleitor":
            _e = tEleitor.importarDicionario(dEleitor_)
            self.incluirEleitor(_e)

    def incluirCandidato(self, candidato_):
        if isinstance(candidato_, tCandidato):
            _tCandidato = regCandidato(candidato_.numero, candidato_.abrangencia, candidato_.endereco, candidato_.nome)
            self.candidatos.append(_tCandidato)

    def importarCandidato(self, candidato_):
        if candidato_["tipo"] == "candidato":
            _c = tCandidato.importarDicionario(candidato_)
            self.incluirCandidato(_c)

    def serializarCandidatos(self):
        _dicionarios = []
        for _candidato in self.candidatos:
            _dicionario = {
                            "numero": _candidato.numero, 
                            "abrangencia": _candidato.abrangencia, 
                            "endereco": _candidato.endereco, 
                            "nome": _candidato.nome, 
                            "saldo": _candidato.saldo
                            }
            _dicionarios.append(_dicionario)
        return _dicionarios
    
    def gerarCedulas(self):
        if len(self.candidatos)>0 and len(self.eleitores)>0:
            self.cedulas.criarCedulas(self.saldoInicial)
        else:
            raise saldoInconsistente

    def gerarChavePrivada(self):
        gerarChavePrivada("tmp/PrivUrnaZona{}Secao{}.pem".format(self.zona, self.secao))

    def gerarChavePublica(self):
        gerarChavePublica("tmp/PrivUrnaZona{}Secao{}.pem".format(self.zona, self.secao))
        self.chavePublica = importarChavePublica("tmp/PubUrnaZona{}Secao{}.pem".format(self.zona, self.secao))

    def gerarEndereco(self):
        if self.chavePublica:
            self.endereco = gerarEndereco("tmp/PrivUrnaZona{}Secao{}.pem".format(self.zona, self.secao))

    def dados(self):
        return "{}{}{}{}{}{}".format(self.eleicao, self.zona, self.secao, self.endereco, self.saldoInicial, self.cedulas.hash_raiz)

    def calcularHash(self):
        gerador = hashing.HashMachine()
        _hash = ''
        while not _hash.startswith('00000'):
            _hash = gerador.hash(self.dados())
        return _hash

    def dicionario(self):
        return {
                "tipo": "urna", 
                "eleicao": self.eleicao, 
                "zona": self.zona, 
                "secao": self.secao, 
                "saldoInicial": self.saldoInicial,
                "endereco": self.endereco, 
                "timestamp": self.timestamp, 
                "cedulas": self.cedulas.dicionarios(), 
                "hashRaiz": self.cedulas.hash_raiz, 
                "eleitores": self.serializarEleitores(), 
                "candidatos": self.serializarCandidatos()
                }            