from pymerkle import MerkleTree
from Transacoes import Voto
from blocoDeTransacoes import blocosDeTransacoesFinal
from random import randint
import json

if __name__ == "__main__":
    x = blocosDeTransacoesFinal()

    for i in range(1, 1000):
        v = Voto(str(randint(1,10)))
        x.inserir(v)
    y = MerkleTree(*x.dados())

    y.export("tree.json")

    x.exportar()

    in_f = open("tree.json", "r")
    z = json.load(in_f)
    
    d = {"cabecalho": z, "blocos":x.dicionarios()}

    o_f = open("bloco.json", "w")

    json.dump(d, o_f, indent=4)

    k = y.serialize()

    oo_ff = open("tree_serializada.json", "w")
    json.dump(k, oo_ff, indent=4)
