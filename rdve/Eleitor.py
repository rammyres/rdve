#!/usr/bin/env python3
from Transacoes import Transacoes
from AES import CifrarComAES
from datetime import datetime, date
from Cryptodome.Protocol.KDF import scrypt
from Utilitarios import hashSenha, gerarChavePrivada, exportarChavePrivada, gerarChavePublica, gerarEndereco, importarChavePublica, importarChavePrivada
import codecs, os, qrcode

class Eleitor:
    chavePrivada = None

    def __init__(self, nome = None, titulo = None, endereco = None, chavePublica = None, aleatorio = None, timestamp = None):
        self.nome = nome
        self.titulo = titulo
        self.endereco = endereco
        self.chavePublica = chavePublica
        self.aleatorio = aleatorio
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.timestamp(datetime.now().timestamp())
        
    def importarEleitor(self, nome, titulo, endereco, chavePublica, aleatorio, timestamp):
        self.timestamp = timestamp
        self.nome = nome
        self.titulo = titulo
        self.endereco = endereco

    def importarDicionario(self, dicionario):
        self.importarEleitor(dicionario["nome"], 
                            dicionario["titulo"], 
                            dicionario["endereco"],
                            dicionario['chavePublica'],
                            dicionario['aleatorio'],
                            dicionario["timestamp"])

    def gerarChavePrivada(self, modo, senha = None):
        _sk = gerarChavePrivada()

        # O modo 1 indica que o arquivo será persistido como um arquivo pem
        # sem criptografia
        if modo == 1:
            exportarChavePrivada(_sk, 'Eleitor{}.pem'.format(self.titulo))
        elif modo == 2:
            # O modo 2 indica que o arquivo será exportado como um arquivo qrcode
            # protegido por senha 
            self.exportarChavePrivada_QR(_sk, senha)

    def exportarChavePrivada_QR(self, chave, senha):
        encriptador = CifrarComAES(hashSenha(senha, self.aleatorio))
        qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=24,
                border=4,
            )

        _chave_encriptada = encriptador.criptografar(chave.to_pem().encode('utf-8'))

        qr.add_data(_chave_encriptada)
        qr.make(fit=True)
        _img = qr.make_image()
        _img.save("Eleitor{}.png".format(self.titulo))
    
    def importarChavePrivada(self, modo, chave = None):
        # O modo indica a forma de geração da chave publica, se partir de um arquivo 
        # pem pesistido no disco, o modo 2 indica que a chave vai ser importada a partir
        # da chave já existente na memória
        if modo == 1: 
            self.chavePrivada = importarChavePrivada("Eleitor{}.pem".format)
        elif modo == 2 and chave:
            self.chavePrivada = importarChavePrivada(chave)


    def dados(self):
        return (self.nome, self.titulo, self.endereco, self.chavePublica, self.aleatorio, self.timestamp)

    def criarTransacao(self):
        self.tEleitor = tEleitor(self.nome, self.titulo, self.endereco,  self.chavePublica, self.aleatorio, self.timestamp)

class tEleitor(Transacoes):
    assinatura = None

    def __init__(self, nome, titulo, endereco, chavePublica, aleatorio, timestamp, assinatura = None):
        self.tipo = "Eleitor"
        self.nome = nome 
        self.titulo = titulo
        self.endereco = endereco
        self.chavePublica = chavePublica
        self.aleatorio = aleatorio
        self.timestamp = timestamp
        self.assinatura = assinatura
        self.gerarHash()

    def dados(self):
        return "{}:{}:{}:{}:{}:{}:{}:{}:{}:{}".format(self.tipo, 
                                                self.nome, 
                                                self.titulo, 
                                                self.endereco, 
                                                self.chavePublica,
                                                self.aleatorio,
                                                self.timestamp, 
                                                self.assinatura,
                                                self.hashTransAnterior, 
                                                self.Hash)

    def __key(self):
        return (self.timestamp, self.nome, self.titulo, self.endereco, self.Hash, self.hashTransAnterior, self.assinatura)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self):
            return self.__key() == other.__key()
        return NotImplemented

    def gerarObjeto(self):
        _eleitor = Eleitor(self.nome, self.titulo, self.endereco, self.timestamp)
        return _eleitor

    def serializar(self):
        return {"tipo": self.tipo, 
                "nome": self.nome, 
                "titulo": self.titulo,                 
                "endereco": self.endereco, 
                "chavePublica": self.chavePublica,
                "aleatorio": self.aleatorio,
                "timestamp": self.timestamp, 
                "assinatura": self.assinatura, 
                "hash": self.Hash, 
                "hashTransAnterior": self.hashTransAnterior}

    def importarDicionario(self, dicionario):
        self.tipo = dicionario["Eleitor"]
        self.nome = dicionario["nome"]
        self.titulo = dicionario["titulo"]
        self.endereco = dicionario["endereco"]
        self.timestamp = dicionario["timestamp"]
        self.assinatura = dicionario["assinatura"]
        self.hashTransAnterior = dicionario["hashTransAnterior"]
        self.Hash = dicionario["hash"]

        return self
    
    def gerarHash(self):        
        if not self.Hash:
            self.Hash = self.gerador.hash(self.dados()).decode()