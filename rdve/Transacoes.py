#!/usr/bin/env python3
from Erros import processoDeAssinaturaInvalido
from datetime import time, date, datetime
from pymerkle.hashing import HashMachine
from ecdsa import SigningKey
import binascii

class Transacoes:

    hashTransAnterior = '0'
    assinatura = None
    Hash = None
    gerador = HashMachine()

    def assinar(self, dados, chavePrivada):
        if not isinstance(chavePrivada, SigningKey):
            raise processoDeAssinaturaInvalido 
        
        assinatura = chavePrivada.sign(dados.encode())
        assinaturaStr = assinatura.hex()
        
        return assinaturaStr

    def verificarAssinatura(self, assinatura, chavePublica):
        assinaturaBytes = binascii.unhexlify(assinatura)
        return chavePublica.verify(assinaturaBytes, chavePublica)