from blocoDeTransacoes import blocosDeTransacoesFinal, blocosDeTransacoesIntermediario
from erros import deveSerBlocoDeTransacaoFinal, quantidadeMenorQueUm, tipoDeTransacaoDesconhecido, sequenciaDeHashesInvalida
from pymerkle import MerkleTree
from Transacoes import Transacoes, Voto, Eleitor, Candidato
import utilitarios
import json, os

class Bloco:
    def __init__(self, urnaID, transacoes):

        if len(transacoes) == 0:
            raise quantidadeMenorQueUm
        elif isinstance(transacoes, blocosDeTransacoesFinal):
            for transacao in transacoes:
                if isinstance(transacao, Transacoes):
                    pass
                else:
                    raise tipoDeTransacaoDesconhecido
        else: 
            raise deveSerBlocoDeTransacaoFinal

        if transacoes.validarSequencia():
            self.arvoreDeMerkle = MerkleTree(*transacoes)
            self.transacoes = transacoes
            self.urnaID = urnaID
        else:
            raise sequenciaDeHashesInvalida

    def exportar(self, arquivo):
        persistencia = open(arquivo, "w")

        json.dump({"urnaID":self.urnaID, "arvoreDeMerkle": self.arvoreDeMerkle, "transacoes": self.transacoes},
                    persistencia, indent=4)

        persistencia.close()

    def importar(self, arquivo):
        _persistencia = open(arquivo, "r")

        _bloco = json.load(_persistencia)

        _tUrnaID = _bloco["urnaID"]
        _tArvore = _bloco["arvoreDeMerkle"]
        _tTransacoes = _bloco["transacoes"]

        _tArvoreJson = open("tmp.json", "w")
        json.dump(_tArvore, _tArvoreJson)

        _tArvoreMerkle = MerkleTree.loadFromFile("tmp.json")

        rBloco = Bloco(_tUrnaID, _tTransacoes)
        rBloco.arvoreDeMerkle = _tArvoreMerkle

        utilitarios.remover_seguramente(_tArvoreJson, 5)
        
        _persistencia.close()

        return rBloco