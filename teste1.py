#!/usr/bin/env python3
from Transacoes import Candidato, Voto, Urna
from blocoDeTransacoes import blocosDeTransacoesFinal, blocosDeTransacoesIntermediario
from BoletimDeUrna import registroDeVotacao
from hashlib import sha256
from pymerkle import MerkleTree, validateProof
from pymerkle.hashing import HashMachine
from tqdm import tqdm
import colorama, pymerkle, math, random

colorama.init(autoreset=True)

if __name__ == "__main__":
    maquina = HashMachine()
    nUrnas = 1000
    nEleitores = 10000
    blocosIntermediarios = []
    urnas = []
    blocoFinal = blocosDeTransacoesFinal()
    blocoUrnas = blocosDeTransacoesFinal()
    nBlocos = math.ceil(math.log2(nEleitores))
    nArquivos = []
    arquivos = []

    print("Gerando blocos de urnas e exportando as chaves privadas como PEMs...")
    for x in tqdm(range(nUrnas)):   
        u = Urna(1, str(random.randint(1,6000)), str(random.randint(1,100)), str(random.randint(1, 20000)))
        blocoUrnas.inserir(u)
    print("Urnas geradas, exportando")
    blocoUrnas.exportar("blocoUrnas.json")

    print("Gerando blocos de votos...")
    for x in tqdm(range(nBlocos)):
        nArquivos.append("arquivo{}.json".format(x+1))

    print("{} - {}".format(nEleitores, math.ceil(math.log2(nEleitores))))

    print("Gerando blocos intermediarios...")
    for x in tqdm(range(0, nBlocos)):
        b = blocosDeTransacoesIntermediario()
        blocosIntermediarios.append(b)

    print("Exportando arquivos dos blocos intermediarios")
    for x in tqdm(range(nEleitores)):
        y = random.randint(0, nBlocos-1)
        v = Voto(1, random.randint(10,20))
        blocosIntermediarios[y].append(v)
        blocosIntermediarios[y].exportar(nArquivos[y])

    print("Limpando os blocos antes da importação dos arqquivos")
    for x in tqdm(range(nBlocos)):
        blocosIntermediarios[x].clear()

    print("Importando arquivos de blocos intermediarios a partir da persistência")
    for x in tqdm(range(nBlocos)):
        blocosIntermediarios[x].importar(nArquivos[x])
    
    print("Preparando o bloco final")
    for x in tqdm(range(len(blocosIntermediarios))):
        print("Misturando os blocos através do algoritmo Fisher-Yates")
        random.shuffle(blocosIntermediarios)
        print("Removendo os dados do bloco atual e incluindo no bloco final")
        for y in tqdm(range(len(blocosIntermediarios[x]))):
            if blocosIntermediarios:
                random.shuffle(blocosIntermediarios[x])
                v = blocosIntermediarios[x].pop()
                blocoFinal.inserir(v)

    print("Gerando o bloco final")
    bloco = registroDeVotacao("urna1", blocoFinal)

    print("Exportando bloco final para formado de persistência")
    bloco.exportar("bloco-urna1.json")

    print("Gerando novo bloco de votação a partir da persistência")
    bloco2 = registroDeVotacao()
    bloco2.importar("bloco-urna1.json")
    bloco2.exportar("bloco-urna2.json")
    print("Exportando somente as transações do primeiro bloco")
    bloco.transacoes.exportar("bloco-transações1.json")

    input("Dois blocos contendo os mesmos dados e duas árvores de Merkle válidas foram geradas\n\
           Agora mostraremos as folhas (hashes das transações) registradas\n\
           Pressione [ENTER} para continuar...")
    print(bloco.arvoreDeMerkle.leaves)
    input("O sistema irá escolher uma transação aleatória e verificará se ela consta\n\
           na árvore de Merkle e o caminho percorrido pela validação até o hash-raiz\n\
           Pressione [ENTER] para continuar")
    t = random.randint(0, len(bloco.transacoes)-1)
    teste = bloco.transacoes[t].Hash
    print("{} - {}".format(bloco.transacoes[t]._dados(), teste))
    tt = bloco.arvoreDeMerkle.merkleProof({"checksum": teste}) 
    print(tt)
    input("Verificaremos a validade do caminho (auditoria)\nPressione [ENTER] para continuar")
    validateProof(tt)
    print(tt)