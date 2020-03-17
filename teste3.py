from pymerkle import MerkleTree
from Transacoes import Voto
from blocoDeTransacoes import blocosDeTransacoesFinal
from random import randint
import json

if __name__ == "__main__":
    x = blocosDeTransacoesFinal()

    for i in range(1, 100):
        v = Voto(str(randint(1,10)))
        x.inserir(v)
    y = MerkleTree(*x.dados())

    y.export("tree.json")

    in_f = open("tree.json", "r")
    z = json.load(in_f)
    
    d = {"cabecalho": z, "blocos":x.dicionarios()}

    o_f = open("bloco.json", "w")

    json.dump(d, o_f, indent=4)
