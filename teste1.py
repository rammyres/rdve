#!/usr/bin/env python3
from arvore import arvoreDeMerkle
from Transacoes import Voto
from blocoDeTransacoes import blocosDeTransacoes
from random import randint

if __name__ == "__main__":
    x = blocosDeTransacoes()

    for i in range(1, 10):
        v = Voto(str(randint(1,20)))
        x.inserir(v)
    y = arvoreDeMerkle(x.dados())
    print(y.hash_raiz)
    y.travessia(y.tabelaDeNos[y.hash_raiz])
    print(y.tabelaDeNos[y.hash_raiz])