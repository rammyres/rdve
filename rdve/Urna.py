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
from Criptografia import Criptografia
from pymerkle import hashing
import math, random, json

class Urna:
    cripto = Criptografia()
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
        
        for _ in range (_n):
            lista = blocosDeTransacoesIntermediario()
            self.votosNaoProcessados.append(lista)

    def assinarCedula(self, voto):
        assinatura = self.chavePrivada.sign(voto.dados().encode())
        return assinatura 

    def sorteiaCedula(self):
        if len(self.cedulas)>0:
            random.shuffle(self.cedulas)
            return self.cedulas.pop()

    def gerarVoto(self, numero):
        if isinstance(votos, list):
            cedula.voto
        v = Voto(self.eleicao, self.abrangencia, numero, self.sorteiaCedula().retornaIdCedula, self.endereco)
        v.assinatura = self.assinarVoto(v)
        return v
        
    def votar(self, voto):
        random.shuffle(self.votosNaoProcessados)
        self.votosNaoProcessados[0].inserir(voto)
        self.exportarBlocosIntermediarios()

    def prepararVotosParaApuracao(self):
        self.votosAProcessar = blocosDeTransacoesFinal()

        for _ in range(len(self.votosNaoProcessados)):
            random.shuffle(self.votosNaoProcessados)
            if self.votosNaoProcessados[0]:
                random.shuffle(self.votosNaoProcessados[0])
                v = self.votosNaoProcessados[0].pop()
                self.votosAProcessar.inserir(v)