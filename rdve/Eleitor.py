from Transacoes import Transacoes
from datetime import datetime, date
from Utilitarios import gerarChavePrivada, gerarChavePublica, gerarEndereco, importarChavePublica
import codecs, os 

class Eleitor:

    def __init__(self, nome = None, titulo = None, endereco = None, timestamp = None, aleatorio = None, Hash = None):
        self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
        self.timestamp = datetime.timestamp(datetime.now().timestamp())
        self.nome = nome
        self.titulo = titulo
        gerarChavePrivada("eleitor{}.pem".format(titulo))
        gerarChavePublica("eleitor{}.pem".format(titulo))
        self.endereco = gerarEndereco("eleitor{}.pem".format(titulo))
        self.chavePublica = importarChavePublica(("pub-eleitor{}.pem".format(titulo))).to_string()
        self.tEleitor = tEleitor(self.nome, self.titulo, self.endereco, self.aleatorio, self.timestamp)
        
    def importarEleitor(self, nome, titulo, endereco, timestamp, aleatorio):
        self.aleatorio = aleatorio
        self.timestamp = timestamp
        self.nome = nome
        self.titulo = titulo
        self.endereco = endereco

    def importarDicionario(self, dicionario):
        self.importarEleitor(dicionario["nome"], dicionario["titulo"], dicionario["endereco"], dicionario["timestamp"], dicionario["aleatorio"])

class tEleitor(Transacoes):
    assinatura = None

    def __init__(self, nome, titulo, endereco, aleatorio, timestamp, assinatura = None):
        self.tipo = "Eleitor"
        self.nome = nome 
        self.titulo = titulo
        self.endereco = endereco
        self.aleatorio = aleatorio
        self.timestamp = timestamp
        self.assinatura = assinatura

    def _dados(self):
        return "{}:{}:{}:{}:{}:{}:{}:{}".format(self.tipo, self.aleatorio, self.nome, self.titulo, self.endereco, self.timestamp, self.hashTransAnterior, 
                                                    self.assinatura)

    def __key(self):
        return (self.aleatorio, self.timestamp, self.nome, self.titulo, self.endereco, 
                self.Hash, self.hashTransAnterior, self.assinatura)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented

    def _dados(self):
        return "{}:{}:{}:{}:{}:{}".format(self.aleatorio, self.nome, self.titulo, self.endereco, self.timestamp, self.assinatura)


    def _dicionario(self):
        return {"tipo": self.tipo, "aleatorio": self.aleatorio, "nome": self.nome, "titulo": self.titulo, "endereco": self.endereco, 
                "timestamp": self.timestamp, "hashTransAnterior": self.hashTransAnterior, 
                "assinatura": self.assinatura}
    
    def gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self._dados()).decode()