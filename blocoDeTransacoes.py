from Transacoes import Transacoes
from erros import tipoDeTransacaoDesconhecido
import json

class blocosDeTransacoesIntermediario(list):

    def inserir(self, transacao):
        
        if isinstance(transacao, Transacoes):
            self.append(transacao)
        else: 
            raise tipoDeTransacaoDesconhecido            

    def dados(self):
        d = []
        for b in self:
            d.append(b._dados())
            
        return d

    def exportar(self, arquivo):
        dicionarios = []
        for dados in self:
            dicionarios.append({dados._dicionaros})
        
        dicionario = {"transacoes":dicionarios}
        arquivo = open(arquivo, "w+")
        
        json.dump(dicionario, arquivo)

    def importar(self, arquivo):
        arq = open(arquivo, "r+")

        json.load(arq)
    
    def dicionarios(self):
        dicionarios = []
        for dados in self:
            dicionarios.append(dados._dicionario())
        
        dicionario = {"blocos":dicionarios}

        return dicionario

class blocosDeTransacoesFinal(list):

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
            d.append('0:0')
            
        return d

    def exportar(self):
        dicionarios = []
        for dados in self:
            dicionarios.append({dados._dicionaros})
        
        dicionario = {"blocos":dicionarios}
        arquivo = open("blocofinal.json", "w+")

        
        json.dump(dicionario, arquivo)
    
    def dicionarios(self):
        dicionarios = []
        for dados in self:
            dicionarios.append(dados._dicionario())
        
        dicionario = {"blocos":dicionarios}

        return dicionario