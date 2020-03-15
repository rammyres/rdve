from Transacoes import Transacoes
from erros import tipoDeTransacaoDesconhecido

class blocosDeTransacoes:
    bloco = []

    def inserir(self, transacao):
        
        if isinstance(transacao, Transacoes):
            if self.bloco and len(self.bloco)>0:
                transacao.hashTransAnterior = self.bloco[-1].Hash
                self.bloco.append(transacao)
            else:
                transacao.hashTransAnterior = '0'
                self.bloco.append(transacao)
        else: 
            raise tipoDeTransacaoDesconhecido

    def dados(self):
        d = []
        for b in self.bloco:
            d.append(b._dados())

        if len(d)%2 != 0:
            d.append('0:0')       
            
        return d
