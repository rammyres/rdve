from arvoreMerkle import ArvoreDeMerkle
from Transacoes import Voto
from blocoDeTransacoes import blocosDeTransacoes
import random

if __name__ == "__main__":

    l = blocosDeTransacoes()

    for i in range(0, 999):
        v = Voto(random.randint(1,20))
        l.inserir(v)

    x = ArvoreDeMerkle(l.dados())
    print(x)

