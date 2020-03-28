from Transacoes import Transacoes
from Voto import Voto
from Eleitor import Eleitor
from Candidato import Candidato
from BlocosDeTransacoes import blocosDeTransacoesFinal, blocosDeTransacoesIntermediario
from datetime import datetime, date
from BoletimDeUrna import boletimDeUrna
from Utilitarios import gerarEndereco, importarChavePrivada
from ecdsa import SigningKey, SECP256k1
import math, random

class Urna:
    zona = None
    secao = None
    saldoInicial = None
    timestamp = None
    endereco = None
    chavePrivada = None
    cadidatos = []

    def __init__(self, zona = None, secao = None, saldoInicial = None, endereco = None):
        self.zona = zona
        self.secao = secao
        self.saldo = saldoInicial
        self.timestamp = datetime.timestamp(datetime.now().timestamp())
        self.endereco = endereco
        self.boletimDeUrna = boletimDeUrna(zona, secao, self.endereco)
        self.chavePrivada = importarChavePrivada("tmp/Zona{}Secao{}.pem".format(self.zona, self.secao))
        self.transacaoUrna = tUrna(self.zona, self.secao, self.saldo, self.timestamp, self.endereco)

    def iniciarUrna(self, zona, secao, saldoInicial, endereco, timestamp):
        self.tipo = "Urna"
        self.zona = zona
        self.secao = secao
        self.saldo = saldoInicial
        self.timestamp = timestamp
        self.endereco = endereco

    def dados(self):
        return(self.zona, self.secao, self.saldo, self.timestamp, self.endereco)

    def carregarDicionario(self, dicionario):
        if dicionario["tipo"] == "Urna":
            self.iniciarUrna(dicionario["zona"], dicionario["secao"], dicionario["saldoInicial"], dicionario["endereco"], dicionario["timestamp"])
        if dicionario["tipo"] == "Candidato":
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

    def gerarVoto(self, numero):
        v = Voto(numero, self.endereco)
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
        _dicionario = {"tipo": self.tipo, "zona": self.zona, "secao": self.secao, "saldoInicial": self.saldoInicial, "votos": self.votosAProcessar,
                        "timestamp": self.timestamp, "endereco": self.endereco}
        return _dicionario
    
    def __key(self):
        return (self.zona, self.secao, self.timestamp, self.endereco)
    
    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented


class tUrna(Transacoes):

    def __init__(self, zona, secao, saldo, timestamp, endereco):
        self.tipo = "Urna"
        self.zona = zona
        self.secao = secao
        self.saldo = saldo
        self.timestamp = timestamp
        self.endereco = endereco
        self._gerarHash()
    
    def _dados(self):
        return '{}:{}:{}:{}:{}:{}'.format(self.tipo, self.zona, self.secao, self.saldo, self.timestamp, self.endereco)

    def _gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self._dados()).decode()
    
    def _dicionario(self):
        return {"tipo": self.tipo, "zona": self.zona, "secao": self.secao, "saldoInicial": self.saldo,
                "endereco": self.endereco, "timestamp": self.timestamp, "assinatura": self.assinatura, 
                "hashTransAnterior": self.hashTransAnterior, "hash": self.Hash}