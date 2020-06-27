#!/usr/bin/env python3
from Transacoes import Transacoes
from Erros import urnaSemEndereco, hashDoBlocoDeCedulasInvalido, votoNulo, candidatoInvalido, eleitorInvalido,\
                  votosNaoPreparadosParaApuracao, tipoDeOperadorInvalido
from Eleitor import Eleitor
from Candidato import Candidato
from Cedulas import Cedulas
from CedulasEmVotacao import CedulasEmVotacao
from BlocosDeTransacoes import registroTransitorio, registroFinal
from saldoInicial import saldoInicial, saldosIniciais
from datetime import datetime, date
from BoletimDeUrna import boletimDeUrna
from Criptografia import Criptografia
from pymerkle import MerkleTree, hashing
from OperadoresDeUrna import Operadores
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

class eleitorValido:
    def __init__(self, nome, titulo, endereco):
        if nome == None or titulo == None or endereco == None:
            raise eleitorInvalido
        else: 
            self.nome = nome
            self.titulo = titulo
            self.endereco = endereco

    def retornaEnderecoPeloTitulo(self, titulo):
        if self.titulo == titulo:
            return self.endereco
        else:
            return None

class Urna:    

    def __init__(self, eleicao = None, abrangencia = None, zona = None, secao = None, saldosIniciais = None, endereco = None):
        self.eleicao = eleicao
        self.abrangencia = abrangencia
        self.zona = zona
        self.secao = secao
        self.saldosIniciais = saldosIniciais()
        self.endereco = endereco
        self.chavePrivada = None
        self.arvoreDeMerkle = MerkleTree()
        self.operadores = Operadores()
        self.cripto = Criptografia()    
        self.cedulasEmVotacao = CedulasEmVotacao()
        self.tmpVotos = []
        self.candidatos = []
        self.eleitores = []
        self.timestamp = datetime.timestamp(datetime.now().timestamp())
  
    def dados(self):
        return(self.eleicao, self.abrangencia, self.zona, self.secao, self.saldosIniciais.dados(), self.timestamp, self.endereco)

    def exportaRegistrosIntermediarios(self):
        for x in range(len(self.votosNaoProcessados)):
            self.votosNaoProcessados[x].exportar("tmp/bloco{}.json".format(x))
    
    def criarPoolDeVotacao(self):
        self.votosNaoProcessados = []
        _n = math.ceil(math.log2(len(self.cedulasEmVotacao)))
        self.exportaRegistrosIntermediarios()
        
        for _ in range (_n):
            lista = registroTransitorio()
            self.votosNaoProcessados.append(lista)

    def assinarCedula(self, voto):
        assinatura = self.chavePrivada.sign(voto.dados().encode())
        return assinatura 

    def sorteiaCedula(self):
        if len(self.cedulasEmVotacao)>0:
            random.shuffle(self.cedulasEmVotacao)
            return self.cedulasEmVotacao[0].pop()

    def gerarVoto(self, numero):
        for candidato in self.candidatos:
            if candidato.numero == numero:
                v = Voto(numero, candidato.endereco)
                return v
            else:
                return None

    def limparVotos(self):
        if self.tmpVotos:
            self.tmpVotos.clear()
            
    def votar(self, votos):
        _tmpCedula = self.sorteiaCedula()
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
    
    def importarSaldosIniciais(self, dictSaldos):
        for _dict in dictSaldos:
            _saldo = saldoInicial(_dict["idCargo"])
            _saldo.incrementarSaldo(int(_dict["saldo"]))
            self.saldosIniciais.inserir(_saldo)

    def importarEleitores(self, dictEleitores):
        for _e in dictEleitores:
            _eleitor = eleitorValido(_e["nome"],
                                    _e["titulo"],
                                    _e["endereco"])
            self.eleitores.append(_eleitor)
    
    def importarCandidatos(self, dictCandidatos):
        for _c in dictCandidatos:
            _candidato = candidatoValido(_c["nome"],
                                        _c["numero"],
                                        _c["endereco"])
            self.candidatos.append(_candidato)
        

    def importarUrna(self, dicionario):
        self.eleicao = dicionario["eleicao"]
        self.abrangencia = dicionario["abrangencia"]
        self.zona = dicionario["zona"]
        self.secao = dicionario["secao"]
        self.endereco = dicionario["endereco"]
        self.importarSaldosIniciais(dicionario["saldosIniciais"])
        self.timestamp = dicionario["timestamp"]
        self.nonce = dicionario["nonce"]
        self.hashRaiz = dicionario["hashRaiz"]
        self.Hash = dicionario["hash"]
        self.cedulasEmVotacao.importarCedulasEmBranco(dicionario["cedulas"])
        self.importarEleitores(dicionario["eleitores"])
        self.importarCandidatos(dicionario["candidatos"])
        self.operadores.importar(dicionario["operadores"])
                