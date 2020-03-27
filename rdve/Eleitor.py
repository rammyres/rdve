from _transacoes import TransacoesEnderecaveis
from datetime import datetime, date
import codecs, os 

class Eleitor(TransacoesEnderecaveis):

    def __init__(self, modo, nome, titulo, dataDoAlistamento, endereco = None, timestamp = None, aleatorio = None, Hash = None):
        
        if modo == 1:
            self.tipo = "Eleitor"
            self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
            self.timestamp = datetime.timestamp(datetime.now().timestamp())
            self.nome = nome
            self.titulo = titulo
            self.dataDoAlistamento = dataDoAlistamento
            self.endereco = self.gerarEndereco()
        
        elif modo == 9:
            self.tipo = "Eleitor"
            self.aleatorio = aleatorio
            self.timestamp = timestamp
            self.nome = nome
            self.titulo = titulo
            self.endereco = endereco
            self.dataDoAlistamento = dataDoAlistamento
            self.Hash = Hash
                
    def __key(self):
        return (self.aleatorio, self.timestamp, self.nome, self.titulo, self.endereco, self.dataDoAlistamento, 
                self.Hash, self.hashTransAnterior, self.assinatura)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented

    def _dados(self):
        return "{}:{}:{}:{}:{}:{}:{}:{}:{}".format(self.tipo, self.aleatorio, self.nome, self.titulo, self.endereco, 
                                                self.dataDoAlistamento, self.timestamp, self.hashTransAnterior, 
                                                self.assinatura)


    def _dicionario(self):
        return {"tipo": self.tipo, "aleatorio": self.aleatorio, "nome": self.nome, "titulo": self.titulo, "endereco": self.endereco, 
                "dataDoAlistamento": self.dataDoAlistamento, "timestamp": self.timestamp, "hashTransAnterior": self.hashTransAnterior, 
                "assinatura": self.assinatura}
    
    def _gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self._dados()).decode()