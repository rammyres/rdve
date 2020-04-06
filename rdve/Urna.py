#!/usr/bin/env python3
from Transacoes import Transacoes
from Erros import urnaSemEndereco, hashDoBlocoDeCedulasInvalido
from Voto import Voto
from Eleitor import Eleitor
from Candidato import Candidato
from Cedulas import Cedulas
from BlocosDeTransacoes import blocosDeTransacoesFinal, blocosDeTransacoesIntermediario
from datetime import datetime, date
from BoletimDeUrna import boletimDeUrna
from Utilitarios import gerarEndereco, gerarChavePrivada, importarChavePrivada
from ecdsa import SigningKey, SECP256k1
from pymerkle import hashing
import math, random, json

class Urna:
    zona = None
    secao = None
    saldoInicial = None
    timestamp = None
    endereco = None
    chavePrivada = None
    cadidatos = []
    cedulas = Cedulas()

    def __init__(self, eleicao = None, abrangencia = None, zona = None, secao = None, saldoInicial = None, endereco = None):
        self.eleicao = eleicao
        self.abrangencia = abrangencia
        self.zona = zona
        self.secao = secao
        self.saldo = saldoInicial
        self.timestamp = datetime.timestamp(datetime.now().timestamp())
        self.boletimDeUrna = boletimDeUrna(eleicao, abrangencia, endereco, zona, secao, self.endereco)

    def iniciarUrna(self, eleicao, abrangencia, zona, secao, saldoInicial, endereco, timestamp):
        self.eleicao = eleicao
        self.abrangencia = abrangencia
        self.zona = zona
        self.secao = secao
        self.saldo = saldoInicial
        self.timestamp = timestamp
        self.endereco = endereco
    
    def gerarChavePrivada(self, arquivo):
        gerarChavePrivada(arquivo)
        self.chavePrivada = importarChavePrivada(arquivo)

    def gerarEndereco(self, arquivo):
        if self.chavePrivada:
            self.endereco = gerarEndereco(arquivo)
        else:
            raise urnaSemEndereco

    def criarTransacao(self):
        if self.endereco:
            self.tUrna = tUrna(self.eleicao, self.abrangencia, self.zona, self.secao, self.saldo, self.cedulas, self.cedulas.hash_raiz, self.timestamp, self.endereco)

    def dados(self):
        return(self.eleicao, self.abrangencia, self.zona, self.secao, self.saldo, self.timestamp, self.endereco)

    def carregarDicionario(self, dicionario):
        if dicionario["tipo"] == "Urna":
            self.iniciarUrna(dicionario["eleicao"], dicionario["abrangencia"], dicionario["zona"], dicionario["secao"], dicionario["saldoInicial"], dicionario["endereco"], dicionario["timestamp"])
            self.cedulas.importarDicionario(dicionario["cedulas"])
        if dicionario["tipo"] == "Candidato":
            if dicionario["abrangencia"] == self.abrangencia and dicionario["eleicao"] == self.eleicao:
                candidato = (dicionario["numero"], dicionario["nome"], dicionario["endereco"])
                self.cadidatos.append(candidato)

    def exportarBlocosIntermediarios(self):
        for x in range(len(self.votosNaoProcessados)):
            self.votosNaoProcessados[x].exportar("tmp/bloco{}.json".format(x))
    
    def criarPoolDeVotacao(self):
        self.votosNaoProcessados = []
        _n = math.ceil(math.log2(self.saldoInicial))
        self.exportarBlocosIntermediarios()
        
        for x in range (_n):
            lista = blocosDeTransacoesIntermediario()
            self.votosNaoProcessados.append(lista)

    def assinarVoto(self, voto):
        assinatura = self.chavePrivada.sign(voto.dados().encode())
        return assinatura 

    def sorteiaCedula(self):
        if len(self.cedulas)>0:
            random.shuffle(self.cedulas)
            return self.cedulas.pop()

    def gerarVoto(self, numero):
        v = Voto(self.eleicao, self.abrangencia, numero, self.sorteiaCedula().retornaIdCedula, self.endereco)
        v.assinatura = self.assinarVoto(v)
        return v
        
    def votar(self, voto):
        random.shuffle(self.votosNaoProcessados)
        self.votosNaoProcessados[0].inserir(voto)
        self.exportarBlocosIntermediarios()

    def prepararVotosParaApuracao(self):
        self.votosAProcessar = blocosDeTransacoesFinal()

        for x in range(len(self.votosNaoProcessados)):
            random.shuffle(self.votosNaoProcessados)
            if self.votosNaoProcessados[0]:
                random.shuffle(self.votosNaoProcessados[0])
                v = self.votosNaoProcessados[0].pop()
                self.votosAProcessar.inserir(v)

    def exportarDicionario(self):
        _dicionario = {"zona": self.zona, "secao": self.secao, "saldoInicial": self.saldoInicial, "votos": self.votosAProcessar,
                        "timestamp": self.timestamp, "endereco": self.endereco, "hashRaiz": self.cedulas.hash_raiz, 
                        "cedulas": self.cedulas.dicionarios()}
        return _dicionario
    
    def __key(self):
        return (self.eleicao, self.abrangencia, self.zona, self.secao, self.timestamp, self.endereco)
    
    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented


class tUrna(Transacoes):
    # O objetivo da transação urna (tUrna) é emitir um objeto serializável para cadastro de *novas* urnas. 
    # O objeto, persistido como json pode ser importado, juntamente com sua chave privada na urna funcional.
    # A saida da coleta de votos será feita como um objeto BoletimDeUrna, que conterá transações Voto (tVoto)
    # que serão emitidos ou capturados pelas transações 

    def __init__(self, eleicao, abrangencia, zona, secao, saldo, cedulas, hash_raiz_cedulas, timestamp, endereco):
        self.tipo = "Urna"
        self.eleicao = eleicao
        self.abrangencia = abrangencia
        self.zona = zona
        self.secao = secao
        self.saldo = saldo
        self.timestamp = timestamp
        self.endereco = endereco
        self.cedulas = cedulas
        self.hashRaiz = hash_raiz_cedulas
        self.gerarHash()
    
    def dados(self):
        return '{}:{}:{}:{}:{}:{}:{}:{}:{}'.format(self.tipo, self.eleicao, self.abrangencia, self.zona, self.secao, 
                                                    self.saldo, self.timestamp, self.endereco, self.cedulas.hash_raiz)

    def gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self.dados()).decode()
    
    def dicionario(self):
        return {"tipo": self.tipo, "eleicao": self.eleicao, "abrangencia": self.abrangencia, "zona": self.zona, "secao": self.secao, 
                "saldoInicial": self.saldo, "endereco": self.endereco, "timestamp": self.timestamp, "assinatura": self.assinatura,
                "cedulas": self.cedulas.dicionarios(), "hashRaiz": self.hashRaiz, "hash": self.Hash}

    def gerarObjeto(self):
        _urna = Urna(self.eleicao, self.abrangencia, self.zona, self.secao, self.saldo, self.endereco)
        return _urna

    def importarDicionario(self, dicionario):
        self.tipo = dicionario["tipo"]
        self.eleicao = dicionario["eleicao"]
        self.abrangencia = dicionario["abrangencia"]
        self.zona = dicionario["zona"]
        self.secao = dicionario["secao"]
        self.saldo = dicionario["saldo"]
        self.timestamp = dicionario["timestamp"]
        self.endereco = dicionario["endereco"]
        self.Hash = dicionario["hash"]        
        self.hashRaiz = dicionario["hashRaiz"]
        self.cedulas.importarDicionario(dicionario["celulas"])
        self.cedulas.calcularArvoreDeMerkle()
        if self.hashRaiz != self.cedulas.arvoreDeMerkle.rootHash:
            raise hashDoBlocoDeCedulasInvalido
        
        return self

    def importarCedulas(self, dicCedulas_):
        if isinstance(dicCedulas_, Cedulas):
            self.cedulas.importarDicionario(dicCedulas_["cedulas"])

class BlocoUrna:
    
    def __init__(self, tUrna):
        if isinstance(tUrna, tUrna):
            self.index = None
            self.tUrna = tUrna
            self.Hash = None   
            self.HashBlocoAnterior = None

    def dados(self):
        return '{}:{}:{}:{}:{}:{}:{}:{}:{}'.format(self.tUrna.tipo, self.tUrna.eleicao, self.tUrna.abrangencia, self.tUrna.zona, self.tUrna.secao, 
                                                   self.tUrna.saldo, self.tUrna.timestamp, self.tUrna.endereco, self.tUrna.cedulas.hash_raiz)

    def calcularHash(self):
        gerador = hashing.HashMachine()
        _hash = ''
        while not _hash.startswith("00000"):
            _hash = gerador.hash(self.dados())
        self.Hash = _hash

    
    def serializarBloco(self):
        return {"index": self.index, "urna": self.tUrna.dicionario(), "hashBlocoAnterior": self.HashBlocoAnterior, "hash": self.Hash}

    def exportarBloco(self, arquivo):
        _arq = open(arquivo, "w")
        json.dump(self.serializarBloco(), _arq, indent=4)
        _arq.close()

    def importarBloco(self, dicionario):
        _tUrna = dicionario["urna"]

    def importarJson(self, arquivo):
        _tArq = open(arquivo, "r")
        _tDicionario = json.load(_tArq)
        _tArq.close()
        self.importarBloco(_tDicionario)
        _tUrna = tUrna.importarDicionario(_tDicionario["urna"])
        _tUrna.importarCedulas(_tDicionario["urna"])
        return _tUrna