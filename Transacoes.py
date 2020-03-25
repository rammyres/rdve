import codecs, os, ecdsa, base58, binascii, hashlib
from erros import processoDeAssinaturaInvalido
from ecdsa import SigningKey, curves, SECP256k1
from datetime import time
from datetime import datetime
from pymerkle.hashing import HashMachine

class Transacoes:

    hashTransAnterior = '0'
    assinatura = None
    Hash = None
    gerador = HashMachine()

    def assinar(self, dados = None, chavePrivada = None):
        if dados == None or chavePrivada == None:
            raise processoDeAssinaturaInvalido 
        
        assinatura = chavePrivada.sign(dados.encode())
        assinaturaStr = codecs.encode(assinatura, 'hex').decode()
        
        return assinaturaStr
    
    def verificarAssinatura(self, assinatura, chavePublica):
        return chavePublica.verify(assinatura, chavePublica)


    def ripemd160(self, x):
        d = hashlib.new('ripemd160')
        d.update(x)
        return d

    def gerarEndereco(self, zona = None, secao = None):
        # generate private key , uncompressed WIF starts with "5"
        chavePrivada = os.urandom(32)
        #chaveCompleta = '80' + binascii.hexlify(chavePrivada).decode()
        #sha256a = hashlib.sha256(binascii.unhexlify(chaveCompleta)).hexdigest()
        #sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
        #WIF = base58.b58encode(binascii.unhexlify(chaveCompleta+sha256b[:8]))
        
        # get public key , uncompressed address starts with "1"
        sk = ecdsa.SigningKey.from_string(chavePrivada, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        chavePublica = '04' + binascii.hexlify(vk.to_string()).decode()
        hash160 = self.ripemd160(hashlib.sha256(binascii.unhexlify(chavePublica)).digest()).digest()
        enderecoPublico_a = b"\x00" + hash160
        checksum = hashlib.sha256(hashlib.sha256(enderecoPublico_a).digest()).digest()[:4]
        enderecoPublico_b = base58.b58encode(enderecoPublico_a + checksum)

        if isinstance(self, Urna):
            arquivo = "tmp/chavePrivadaZ{}S{}.pem".format(zona, secao)

            arq = open(arquivo, "wb")

            arq.write(sk.to_pem())

            arq.close()
        
        return enderecoPublico_b.decode()

class Urna(Transacoes):
    endereco = None

    def __init__(self, modo, zona, secao, saldoInicial, endereco = None, timestamp = None, hashTransAnterior = None, Hash = None):
        
        if modo == 1:
            self.tipo = "Urna"
            self.zona = zona
            self.secao = secao
            self.saldo = saldoInicial
            self.timestamp = datetime.now().timestamp()
            self.endereco = self.gerarEndereco(self.zona, self.secao)   
        
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


class Eleitor(Transacoes):

    def __init__(self, modo, nome, titulo, dataDoAlistamento, endereco = None, timestamp = None, aleatorio = None, Hash = None):
        
        if modo == 1:
            self.tipo = "Eleitor"
            self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
            self.timestamp = datetime.timestamp(datetime.now().timestamp())
            self.nome = nome
            self.titulo = titulo
            self.dataDoAlistamento = dataDoAlistamento
            self.gerarEndereco()
        
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
        return {"tipo": self.tipo, "aleatorio": self.aleatorio, "nome": self.nome, "titulo": self.titulo,
                "endereco": self.endereco, "dataDoAlistamento": self.dataDoAlistamento,
                "timestamp": self.timestamp, "hashTransAnterior": self.hashTransAnterior, 
                "assinatura": self.assinatura}
    
    def _gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self._dados()).decode()

class Candidato(Eleitor):
    def __init__(self, modo, nome, titulo, endereco, numero, processo, aleatorio = None, timestamp = None):
        
        if modo == 1:
            self.tipo = "Candidato"
            self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
            self.timestamp = datetime.timestamp(datetime.now().timestamp())
            self.nome = nome
            self.titulo = titulo
            self.endereco = endereco
            self.numero = numero
            self.processo = processo
        
        elif modo == 9:
            self.tipo = "Candidato"
            self.aleatorio = aleatorio
            self.timestamp = timestamp
            self.nome = nome
            self.titulo = titulo
            self.endereco = endereco
            self.numero = numero
            self.processo = processo

    def __key(self):
        return (self.tipo, self.aleatorio, self.nome, self.titulo, self.endereco, self.numero, 
                self.processo, self.timestamp, self.hashTransAnterior, self.assinatura)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented
    
    def _dados(self):
        return "{}:{}:{}:{}:{}:{}:{}:{}:{}:{}".format(self.tipo, self.aleatorio, self.nome, self.titulo, self.endereco, 
                                                self.numero, self.processo, self.timestamp, self.hashTransAnterior, 
                                                self.assinatura)

    def _dicionario(self):
        if self.Hash:
            return {"tipo": self.tipo, "aleatorio": self.aleatorio, "nome": self.nome, "titulo": self.titulo,
                   "endereco": self.endereco, "numero": self.processo, "timestamp": self.timestamp,
                    "hashTransAnterior": self.hashTransAnterior, "hash": self.Hash, "assinatura": self.assinatura}
        else:
            return {"tipo": self.tipo, "aleatorio": self.aleatorio, "nome": self.nome, "titulo": self.titulo,
                    "endereco": self.endereco, "numero": self.processo, "timestamp": self.timestamp,
                    "hashTransAnterior": self.hashTransAnterior, "assinatura": self.assinatura}

    def _gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self._dados()).decode()
    
class Voto(Transacoes):
    def __init__(self, modo, numero, aletorio = None, assinatura = None):
        if modo == 1:
            self.tipo = "Voto"
            self.numero = numero
            self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode()
                
        elif modo == 9:
            self.tipo = "Voto"
            self.numero = numero
            self.aleatorio = aletorio
            self.assinatura = assinatura
    
    def _dados(self):
        return "{}:{}:{}:{}:{}".format(self.tipo, self.numero, self.aleatorio, self.assinatura, self.hashTransAnterior)

    def _dicionario(self):
        if self.Hash:
            return {"tipo": self.tipo, "numero": self.numero, "aleatorio": self.aleatorio, "hash": self.Hash, 
                    "hashTransAnterior": self.hashTransAnterior, "assinatura": self.assinatura}
        else:
            return {"tipo": self.tipo, "numero": self.numero, "aleatorio": self.aleatorio, 
                    "hashTransAnterior": self.hashTransAnterior, "assinatura": self.assinatura}

    def _gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self._dados()).decode()

    def __key(self):
        return(self.tipo, self.numero, self.aleatorio, self.hashTransAnterior, self.assinatura)
    
    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
            
        return NotImplemented