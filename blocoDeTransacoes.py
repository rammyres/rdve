from Transacoes import Transacoes, Voto, Eleitor, Candidato
from erros import tipoDeTransacaoDesconhecido, listaDeDicioariosVazia
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
        
        dicionario = {"transacoes":dicionarios}

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

    def validaSequencia(self):
        for i in range(len(self)):
            if len(self) == 1 and self[i].hashTransAnterior == '0':
                return True
            elif len(self) > 1 and i > 0 and self[i].hashTransAnterior != self[i-1].Hash:
                return False
            return True

    def exportar(self):
        dicionarios = []
        for dados in self:
            dicionarios.append(dados._dicionario())
        
        dicionario = {"transacoes":dicionarios}
        arquivo = open("blocofinal.json", "w+")
        
        json.dump(dicionario, arquivo, indent=4)

    
    def dicionarios(self):
        dicionarios = []
        for dados in self:
            dicionarios.append(dados._dicionario())
        
        dicionario = {"transacoes":dicionarios}

        return dicionario

    def importarDicionarios(self, listaDeDicionarios):
        if len(listaDeDicionarios)<1:
            raise listaDeDicioariosVazia
        else:
            for d in listaDeDicionarios:
                if d["tipo"] == "Eleitor":
                    t = Eleitor(9, d["nome"], d["titulo"], d["endereco"], d["dataDoAlistamento"], d["timestamp"], d["aleatorio"])
                elif d["tipo"] == "Candidato":
                    t = Candidato(9, ["nome"], d["titulo"], d["endereco"], d["numero"], d["processo"], d["aleatorio"], d["timestamp"])
                elif d["tipo"] == "Voto":
                    t = Voto(9, d["numero"], d["aleatorio"])
                self.inserir(t)