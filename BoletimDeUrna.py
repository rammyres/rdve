from blocoDeTransacoes import blocosDeTransacoesFinal, blocosDeTransacoesIntermediario
from erros import deveSerBlocoDeTransacaoFinal, quantidadeMenorQueUm, tipoDeTransacaoDesconhecido, sequenciaDeHashesInvalida, \
                  arvoreDeMerkleInvalida, registroSemTransacoes
from pymerkle import MerkleTree
from collections import OrderedDict 
from rdve import Transacoes, Voto, Eleitor, Candidato, Urna
import utilitarios
import json, os

class registroDeVotacao:
        _arvoreDeMerkle = None
        transacoes = None 

        @property
        def arvoreDeMerkle(self):
            return self._arvoreDeMerkle

        @arvoreDeMerkle.setter
        def arvoreDeMerkle(self, arvore):
            if not self.transacoes:
                raise registroSemTransacoes
            _tArvore = MerkleTree(*self.transacoes.dados())
            if arvore != _tArvore:
                raise arvoreDeMerkleInvalida
            else:
                self._arvoreDeMerkle = arvore    

        def __init__(self, zona, secao, endereco=None, blocoTF=None, arvore = None):

            if blocoTF != None:
                if len(blocoTF.dados()) == 0:
                    raise quantidadeMenorQueUm
                elif isinstance(blocoTF, blocosDeTransacoesFinal):
                    for transacao in blocoTF:
                        if isinstance(transacao, Transacoes):
                            pass
                        else:
                            raise tipoDeTransacaoDesconhecido
                    if blocoTF.validaSequencia():
                        _tArvore = MerkleTree(*blocoTF.dados())
                        if arvore:
                            if arvore != _tArvore:
                                raise arvoreDeMerkleInvalida
                        self.transacoes = blocoTF
                        self.arvoreDeMerkle = _tArvore

                    else:
                        raise sequenciaDeHashesInvalida
                else: 
                    raise deveSerBlocoDeTransacaoFinal
            
        def exportar(self, arquivo):
            _persistencia = open(arquivo, "w")

            json.dump({"urnaID":self.urnaID, "arvoreDeMerkle": self.arvoreDeMerkle.serialize(), "transacoes": self.transacoes.dicionarios()},
                        _persistencia, indent=4)

            _persistencia.close()

        def importar(self, arquivo):
            _persistencia = open(arquivo, "r")

            _bloco = json.load(_persistencia)

            _tUrnaID = _bloco["urnaID"]
            _tArvore = _bloco["arvoreDeMerkle"]
            _tTransacoesDict = OrderedDict()
            _tTransacoesDict = _bloco["transacoes"]

            _tTransacoes = blocosDeTransacoesFinal()
            _tTransacoes.importarDicionarios(_tTransacoesDict["transacoes"])

            _tArvoreJson = open("tmp.json", "w")
            json.dump(_tArvore, _tArvoreJson, indent=4)
            _tArvoreJson.close()

            _tArvoreMerkle = MerkleTree.loadFromFile("tmp.json")

            if _tArvoreMerkle != MerkleTree(*_tTransacoes.dados()):
                raise arvoreDeMerkleInvalida

            self.urnaID = _tUrnaID
            self.transacoes = _tTransacoes
            self.arvoreDeMerkle = _tArvoreMerkle

            _tArvoreJson = open("tmp.json", "w")
            utilitarios.remover_seguramente("tmp.json", 5)
            _tArvoreJson.close()
            
            _persistencia.close()




    