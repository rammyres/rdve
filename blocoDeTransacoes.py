from Transacoes import Transacoes
from erros import tipoDeTransacaoDesconhecido

class blocosDeTransacoes(list):

    def inserir(self, transacao):
        
        if isinstance(transacao, Transacoes):
            if self and len(self)>0:
                transacao.hashTransAnterior = self[-1].Hash
                self.append(transacao)
            else:
                transacao.hashTransAnterior = '0'
                self.append(transacao)
        else: 
            raise tipoDeTransacaoDesconhecido

    def dados(self):
        d = []
        for b in self:
            d.append(b._dados())

        if len(d)%2 != 0:
            d.append({'0':'0'})       
            
        return d
