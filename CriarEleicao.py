#!/usr/bin/env python3
from rdve.BlocoGenesis import BlocoGenesis
from colorama import init, Fore
import colorama

init(autoreset=True)

if __name__ == "__main__":
    print(f"{Fore.BLUE}Bem vindo ao controle inicial do RDVE\n\n")
    eleicao = input("Por favor, informe um nome para esta eleição: ")

    bGenesis = BlocoGenesis(eleicao)

    data = input("Informe a data da eleicao (formato AAAA-MM-DD): ")
    bGenesis.definirDataVotacao(data)
    print("Carregando as abrangencias territoriais")
    bGenesis.carregarAbrangencia()
    bGenesis.criarHash()
    print("Persistindo a blockchain")
    bGenesis.criarBlocoGenesis()
