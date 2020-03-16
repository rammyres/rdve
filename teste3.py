from pymerkle import MerkleTree
from Transacoes import Voto
from blocoDeTransacoes import blocosDeTransacoes
from random import randint

if __name__ == "__main__":
    x = blocosDeTransacoes()

    for i in range(1, 100):
        v = Voto(str(randint(1,10)))
        x.inserir(v)
    y = MerkleTree(*x.dados())
    y.export("tree.json")
    z = MerkleTree(*x.dados())
    z.export("tree1.json")

    if y == z:
        print("Arvore validada")
    yy = MerkleTree.loadFromFile("tree1.json")
    print(yy)
    if y == yy:
        print("Avore carregada validada")