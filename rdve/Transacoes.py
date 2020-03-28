#!/usr/bin/env python3
import codecs 
from Erros import processoDeAssinaturaInvalido
from datetime import time, date, datetime
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