#!/usr/bin/env python3
from Transacoes import Candidato, Voto
from blocoDeTransacoes import blocosDeTransacoesFinal, blocosDeTransacoesIntermediario
from BoletimDeUrna import registroDeVotacao
from hashlib import sha256
from pymerkle import MerkleTree, validateProof
from pymerkle.hashing import HashMachine
import colorama, pymerkle, math, random

colorama.init(autoreset=True)

if __name__ == "__main__":
    maquina = HashMachine()
    nEleitores = 10000
    blocosIntermediarios = []
    blocoFinal = blocosDeTransacoesFinal()
    nBlocos = math.ceil(math.log2(nEleitores))
    nArquivos = []
    arquivos = []

    for x in range(nBlocos):
        nArquivos.append("arquivo{}.json".format(x+1))

    print("{} - {}".format(nEleitores, math.ceil(math.log2(nEleitores))))

    for x in range(0, nBlocos):
        b = blocosDeTransacoesIntermediario()
        blocosIntermediarios.append(b)

    for x in range(nEleitores):
        y = random.randint(0, nBlocos-1)
        v = Voto(1, random.randint(10,20))
        blocosIntermediarios[y].append(v)
        blocosIntermediarios[y].exportar(nArquivos[y])

    for x in range(nBlocos):
        blocosIntermediarios[x].clear()

    for x in range(nBlocos):
        blocosIntermediarios[x].importar(nArquivos[x])
    
    for x in range(len(blocosIntermediarios)):
        random.shuffle(blocosIntermediarios[x])
        for y in range(len(blocosIntermediarios[x])):
            if blocosIntermediarios:
                v = blocosIntermediarios[x].pop()
                blocoFinal.inserir(v)

    bloco = registroDeVotacao("urna1", blocoFinal)

    bloco.exportar("bloco-urna1.json")

    bloco2 = registroDeVotacao()
    bloco2.importar("bloco-urna1.json")
    bloco2.exportar("bloco-urna2.json")
    bloco.transacoes.exportar("bloco-transações1.json")

    print(bloco.arvoreDeMerkle.leaves)
    t = random.randint(0, len(bloco.transacoes)-1)
    teste = bloco.transacoes[t].Hash
    print("{} - {}".format(bloco.transacoes[t]._dados(), teste))
    tt = bloco.arvoreDeMerkle.merkleProof({"checksum": teste}) 
    print(tt)
    validateProof(tt)
    print(tt)
