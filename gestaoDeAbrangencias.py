#!/usr/bin/env python3
from colorama import init, Fore, Back, Style
from collections import OrderedDict
from rdve.Abrangencias import BlocoAbrangencias
import json, colorama, copy

        
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

bAbrangencias = BlocoAbrangencias("1", "2020-1")

def listarEstados():
       
    if abrNacional.listarEstados() == None:
        print("Não existem estados cadastrados")
        return False
    else:
        for k in abrNacional.listarEstados().keys():
            print("{} - {}".format(k, abrNacional.listarEstados()[k]))
    return True

if __name__ == "__main__":
    init(autoreset=True)
    
    print(f"{Fore.BLUE}Bem vindo ao gestão de abrangencias")
    abrNacional.importarJson()

    while True:
        op = menu()
        
        if op == "1":
            abrNacional.listarAbrangencias()
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
