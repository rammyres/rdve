'''
    Esta classe abstrai o mecanismo que gera um bloco urna. Considerando a dimensão do bloco, a abordagem 
    adotada passou a ser um bloco por urna, ao contrário de várias urnas em um bloco. A classe exportar
    um dicionário que pode ser exportado no objeto genérico "bloco", sem a necessidade de herança. 
'''

from Cedulas import Cedulas
from Transacoes import Transacoes
from Erros import saldoInconsistente, hashDoBlocoDeCedulasInvalido
from Candidato import Candidato, tCandidato
from Eleitor import Eleitor, tEleitor
from Criptografia import Criptografia
from Utilitarios import Utilitarios
from pymerkle import MerkleTree, hashing
from datetime import datetime
import json

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
    auxCriptografia = Criptografia()
    util = Utilitarios()
    eleicao = None
    idSecao = None
    zona = None
    secao = None
    saldoInicial = None
    nonce = None
    timestamp = None
    endereco = None
    chavePublica = None
    arvoreDeMerkle = MerkleTree()
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
            _e = tEleitor(dEleitor_["nome"], 
                          dEleitor_["titulo"], 
                          dEleitor_["endereco"], 
                          dEleitor_["chavePublica"], 
                          dEleitor_["aleatorio"], 
                          dEleitor_["timestamp"], 
                          dEleitor_["assinatura"])
            self.incluirEleitor(_e)

    def incluirCandidato(self, candidato_):
        if isinstance(candidato_, tCandidato):
            _tCandidato = regCandidato(candidato_.numero, candidato_.abrangencia, candidato_.endereco, candidato_.nome)
            self.candidatos.append(_tCandidato)

    def importarCandidato(self, candidato_):
        if candidato_["tipo"] == "candidato":
            _c = tCandidato(candidato_["abrangencia"], candidato_["nome"], candidato_["titulo"], candidato_["cargo"],
                            candidato_["numero"], candidato_["processo"], candidato_["endereco"], candidato_["timestamp"])
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

    def gerarChaves(self):
        _sk = self.auxCriptografia.gerarChavePrivada()
        self.auxCriptografia.exportarChavePrivada(_sk, "tmp/PrivUrnaZona{}Secao{}.pem".format(self.zona, self.secao))
        self.chavePublica = _sk.verifying_key

    def gerarEndereco(self):
        if self.chavePublica:
            self.endereco = self.util.gerarEndereco("tmp/PrivUrnaZona{}Secao{}.pem".format(self.zona, self.secao))

    def dados(self):
        return "{}{}{}{}{}{}{}".format(self.eleicao, self.zona, self.secao, self.endereco, self.saldoInicial, self.nonce, self.arvoreDeMerkle.rootHash)

    def calcularArvoreDeMerkle(self):
        for _c in self.cedulas:
            self.arvoreDeMerkle.update(_c.retornaIdCedula())
        for _e in self.eleitores:
            self.arvoreDeMerkle.update(_e.dados())
        for _cD in self.candidatos:
            self.arvoreDeMerkle.update(_cD.dados())

    def importarCedulas(self, dicCedulas_):
        if isinstance(dicCedulas_, Cedulas):
            self.cedulas.importarDicionario(dicCedulas_["cedulas"])

    def calcularHash(self):
        self.nonce = 0
        gerador = hashing.HashMachine()
        _hash = ''
        while not _hash.startswith('00000'):
            _hash = gerador.hash(self.dados())
            self.nonce+=1
        return _hash

    def serializar(self):
        return {
                "eleicao": self.eleicao, 
                "zona": self.zona, 
                "secao": self.secao, 
                "endereco": self.endereco, 
                "saldoInicial": self.saldoInicial,                
                "timestamp": self.timestamp,
                "nonce": self.nonce,
                "hashRaiz": self.arvoreDeMerkle.rootHash,
                "hash": self.calcularHash(),
                "arvoreDeMerkle": self.arvoreDeMerkle.serialize(),
                "cedulas": self.cedulas.serializar(), 
                "eleitores": self.serializarEleitores(), 
                "candidatos": self.serializarCandidatos()
                }