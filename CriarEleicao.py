#!/usr/bin/env python3
from rdve.BlocoGenesis import BlocoGenesis
from rdve.Erros import dataInferiorAoLimite
from colorama import init, Fore
import colorama, locale

locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')

init(autoreset=True)

if __name__ == "__main__":
    print(f"{Fore.BLUE}Bem vindo ao controle inicial do RDVE\n\n")
    eleicao = input("Por favor, informe um nome para esta eleição: ")
    
    while True:
        try:            
            data = input("Informe a data da eleicao (formato AAAA-MM-DD): ")
            bGenesis = BlocoGenesis(eleicao, data) 
            break
        except ValueError:
            print("Você deve incluir uma data válida para a eleição")
        except dataInferiorAoLimite:
            print(dataInferiorAoLimite.message)
   
    print("Carregando as abrangencias territoriais")
    bGenesis.carregarAbrangencia()
    bGenesis.criarHash()
    print("Persistindo a blockchain")
    bGenesis.criarBlocoGenesis()
