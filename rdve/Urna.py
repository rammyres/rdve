from Transacoes import TransacoesEnderecaveis
from datetime import datetime, date

class tUrna(TransacoesEnderecaveis):
    endereco = None

    def __init__(self, modo, zona, secao, saldoInicial, endereco = None, timestamp = None, hashTransAnterior = None, Hash = None):
        
        if modo == 1:
            self.tipo = "Urna"
            self.zona = zona
            self.secao = secao
            self.saldo = saldoInicial
            self.timestamp = datetime.timestamp(datetime.now().timestamp())
            self.endereco = self.gerarEndereco()
        
        elif modo == 9:
            self.tipo = "Urna"
            self.zona = zona
            self.secao = secao
            self.saldo = saldoInicial
            self.timestamp = timestamp
            self.endereco = endereco
    
    def __key(self):
        return (self.zona, self.secao, self.timestamp, self.endereco, self.hashTransAnterior, self.Hash)
    
    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented

    def _dados(self):
        return '{}:{}:{}:{}:{}:{}'.format(self.tipo, self.zona, self.secao, self.saldo, self.timestamp, self.endereco)
    
    def _gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self._dados()).decode()
    
    def _dicionario(self):
        if self.Hash:
            return {"tipo": self.tipo, "zona": self.zona, "secao": self.secao, "saldoInicial": self.saldo,
                    "endereco": self.endereco, "timestamp": self.timestamp, "assinatura": self.assinatura, 
                    "hashTransAnterior": self.hashTransAnterior, "hash": self.Hash}
        else:
            return {"tipo": self.tipo, "zona": self.zona, "secao": self.secao, "saldoInicial": self.saldo,
                    "endereco": self.endereco, "timestamp": self.timestamp, "assinatura": self.assinatura, 
                    "hashTransAnterior": self.hashTransAnterior}