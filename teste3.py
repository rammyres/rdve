from pymerkle import MerkleTree
from Transacoes import Voto
from blocoDeTransacoes import blocosDeTransacoes
from random import randint

if __name__ == "__main__":
    x = blocosDeTransacoes()

    for i in range(1, 1000000):
        v = Voto(str(randint(1,10)))
        x.inserir(v)
    y = MerkleTree()
    for d in x:
        y.update(d._dados())
    print(y)
    