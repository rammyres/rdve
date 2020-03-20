#!/usr/bin/env python3
from Transacoes import Candidato, Voto
from blocoDeTransacoes import blocosDeTransacoesFinal, blocosDeTransacoesIntermediario
from BoletimDeUrna import registroDeVotacao
import colorama, pymerkle, math, random

colorama.init(autoreset=True)

if __name__ == "__main__":
    nEleitores = 10000
    blocosIntermediarios = []
    blocoFinal = blocosDeTransacoesFinal()
    nBlocos = math.ceil(math.log2(nEleitores))
    print("{} - {}".format(nEleitores, math.ceil(math.log2(nEleitores))))

    for x in range(0, nBlocos):
        b = blocosDeTransacoesIntermediario()
        blocosIntermediarios.append(b)

    for x in range(nEleitores):
        v = Voto(1, random.randint(10,20))
        random.shuffle(blocosIntermediarios)
        blocosIntermediarios[0].append(v)

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