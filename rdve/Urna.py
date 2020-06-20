#!/usr/bin/env python3
from Transacoes import Transacoes
from Erros import urnaSemEndereco, hashDoBlocoDeCedulasInvalido, votoNulo, candidatoInvalido, votosNaoPreparadosParaApuracao, tipoDeOperadorInvalido
from Eleitor import Eleitor
from Candidato import Candidato
from Cedulas import Cedulas
from CedulaPreenchida import CedulaPreenchida
from BlocosDeTransacoes import registroTransitorio, registroFinal
from datetime import datetime, date
from BoletimDeUrna import boletimDeUrna
from Criptografia import Criptografia
from pymerkle import hashing
import math, random, json


class Voto:
    def __init__(self, numero, enderecoDestino):
        if numero == None or enderecoDestino == None:
            raise votoNulo("Endereço ou numero não informados")
        else:
            self.numero = numero
            self.enderecoDestino = enderecoDestino

    def serializar(self):
        return {"numero":self.numero, "enderecoDestino": self.enderecoDestino, "qtd": 1}

class candidatoValido:
    def __init__(self, nome, numero, endereco):
        if nome == None or numero == None or endereco == None:
            raise candidatoInvalido("Nome, numero ou endereço de destino do candidato inválido")
        else:
            self.nome = nome
            self.numero = numero
            self.endereco = endereco
    
    def retornaEnderecoPeloNumero(self, numero):
        if self.numero == numero:
            return self.endereco
        else:
            return None

class Urna:
    operadores = Operadores()
    cripto = Criptografia()
    zona = None
    secao = None
    saldoInicial = None
    timestamp = None
    endereco = None
    chavePrivada = None
    cadidatos = []
    cedulas = Cedulas()
    tmpVotos = []

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

    def exportaRegistrosIntermediarios(self):
        for x in range(len(self.votosNaoProcessados)):
            self.votosNaoProcessados[x].exportar("tmp/bloco{}.json".format(x))
    
    def criarPoolDeVotacao(self):
        self.votosNaoProcessados = []
        _n = math.ceil(math.log2(self.saldoInicial))
        self.exportaRegistrosIntermediarios()
        
        for _ in range (_n):
            lista = registroTransitorio()
            self.votosNaoProcessados.append(lista)

    def assinarCedula(self, voto):
        assinatura = self.chavePrivada.sign(voto.dados().encode())
        return assinatura 

    def sorteiaCedula(self):
        if len(self.cedulas)>0:
            random.shuffle(self.cedulas)
            return self.cedulas.pop()

    def gerarVoto(self, numero):
        for candidato in self.cadidatos:
            if candidato.numero == numero:
                v = Voto(numero, candidato.endereco)
                return v
            else:
                return None

    def limparVotos(self):
        if self.tmpVotos:
            self.tmpVotos.clear()
            
    def votar(self, votos):
        random.shuffle(self.cedulas)
        _tmpIdCedula = self.cedulas[0].pop()
        _tmpCedula = CedulaPreenchida(_tmpIdCedula)
        _tmpCedula.inserirVotos(votos)
        random.shuffle(self.votosNaoProcessados)
        self.votosNaoProcessados[0].inserir(_tmpCedula)
        self.exportaRegistrosIntermediarios()
        self.limparVotos()

    def prepararVotosParaApuracao(self):
        self.votosAProcessar = registroFinal()

        for _ in range(len(self.votosNaoProcessados)):
            random.shuffle(self.votosNaoProcessados)
            if self.votosNaoProcessados[0]:
                random.shuffle(self.votosNaoProcessados[0])
                v = self.votosNaoProcessados[0].pop()
                self.votosAProcessar.inserir(v)
    
    def exportarRegistroFinal(self, *arquivos):
        if self.votosAProcessar:
            for x in arquivos:
                self.votosAProcessar.exportar(x)
        else:
            raise votosNaoPreparadosParaApuracao("Os votos não estão preparados para apuração")