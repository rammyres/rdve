from BoletimDeUrna import registroDeVotacao
from pymerkle.hashing import HashMachine
from datetime import datetime
from blocoDeTransacoes import blocosDeTransacoesIntermediario, blocosDeTransacoesFinal

class Bloco:
    indice = None
    nonce = None
    gerador = HashMachine()
    timestamp = None
    hashUltBloco = None
    _hash = None

class BlocoGenesis(Bloco):

    tipo = "Genesis"
    registroEleitoral = (datetime.date(), datetime.date())
    registroDeCandidatos = (datetime.date(), datetime.date())
    dataVotacao = datetime.date()

    @property
    def Hash(self):
        return self._hash

    @Hash.setter
    def Hash(self, hash_):
        _hash = self.gerador.hash("{}{}".format(self.timestamp, self.hashUltBloco))
        if hash_ == _hash:
            self._hash = hash_

class BlocoDeVotacao(Bloco):
    tipo = "Votacao"
    boletim = None
    
    @property
    def Hash(self):
        return self._hash

    @Hash.setter
    def Hash(self, hash_):
        _hash = self.gerador.hash("{}{}{}{}".format(self.timestamp, self.hashUltBloco, self.nonce, self.boletim.Hash))
        if hash_ == _hash:
            self._hash = hash_

    def _dadosParaHash(self):
        if self:
            return "{}{}{}".format(self.timestamp, self.hashUltBloco, self.boletim.Hash)

    def _computarHash(self):
        if not self.boletim:
            self.nonce = 0 
            while True:
                self.Hash = self.gerador.hash(self._dadosParaHash)
                if self.Hash.startswith('00000000'):
                    break
                self.nonce += 1