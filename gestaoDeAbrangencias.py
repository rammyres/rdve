#!/usr/bin/env python3
from colorama import init, Fore, Back, Style
from collections import OrderedDict
from rdve.Abrangencias import RegistroAbrangencias
import json, colorama, copy

abrNacional = RegistroAbrangencias()
        
def menu():
    print(f"{Fore.BLUE}Escolha uma opção")
    print("1- Listar abrangencias existentes ")
    print("2- Cadastrar nova abrangência ")
    print("9- Encerrar")
    _escolha = str(input("Escolha sua opção: "))
    if _escolha == "1" or _escolha == "2" or _escolha == "9":
        return _escolha
    else:
        print(f"{Fore.RED}{Style.BRIGHT}Escolha uma opção válida")

def listarAbrangencias(tipo, UF = None):
    if UF and UF not in abrNacional.listarAbrangencias(tipo, UF).keys():
        print("Estado não localizado")
    for x in abrNacional.listarAbrangencias(tipo, UF):
        print(x)

if __name__ == "__main__":
    init(autoreset=True)
    
    print(f"{Fore.BLUE}Bem vindo ao gestão de abrangencias")
    try:
        abrNacional.importarAbrangencias("abrangencias.json")
    except IOError:
        print(f"{Fore.RED}{Back.YELLOW}Abrangencias não localizadas")

    while True:
        op = menu()
        
        if op == "1":

            while True:
                _e = str.upper(input("Digite uma das opções abaixo:\n\
                                      E para lista abrangências estaduais\n\
                                      M para municipios\n\
                                      Z para zonas\n\
                                      S para seções\n\
                                      digite sua opção: "))
                if _e == "E" or _e == "M":
                    listarAbrangencias(1)
                    if _e == "M":                        
                        _m = str.upper(input("Digite a sigla do estado: "))
                        listarAbrangencias(2, _m)
                    break                

        elif op == "2":
            _ab = input("Informe o tipo de abrangência (M para municipal, E para estadual): ")
            if str.upper(_ab) == "M":
                while True:
                    print("Selecione a qual estado pertence o município: ")
                    if not listarEstados():
                        break
                    e = input("Numero do estado: ")
                    _ab_n = input("Informe o nome da abrangência: ")
                    abrNacional.inserir("5", _ab_n, int(e))
                    break
            elif str.upper(_ab) == "E":
                _ab_n = input("Informe o nome da abrangência: ")
                abrNacional.inserir("3", _ab_n)
            elif str.upper(_ab) != "E" and str.upper(_ab) != "M":
                print("Opção invalida, digite M ou E")
        elif op == "9":
            break
