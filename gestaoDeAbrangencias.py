#!/usr/bin/env python3
from colorama import init, Fore, Back, Style
from collections import OrderedDict
from rdve.Abrangencias import RegistroAbrangencias
import json, colorama, copy

Reg = RegistroAbrangencias()
        
def menu():
    print(f"{Fore.BLUE}Escolha uma opção")
    print("1- Cadastrar nova abrangência ")
    print("2- Listar abrangencias estaduais ")
    print("3- Listar abrangencias municipais de um estado ")
    print("Deb - imprimir o arquivo bruto ")
    print("9- Encerrar")
    _escolha = str(input("Escolha sua opção: "))
    if _escolha == "1" or _escolha == "2" or _escolha == "3" or _escolha == "Deb" or _escolha == "9":
        return _escolha
    else:
        print(f"{Fore.RED}{Style.BRIGHT}Escolha uma opção válida")

def listarAbrangencias(tipo, UF = None):
    lista = Reg.listarAbrangencias(tipo, UF)
    if not lista: 
        return -1
    if UF:
        for i in lista:
            if tipo == 2:
                print("{} - {}".format(i["ID Municipio"], i["Nome"]))
            if tipo == 3:
                print("{} - {}".format(i["ID Zona"], i["Numero"]))
    elif tipo == 1:
        print("UF - Estado")
        for i in lista:
            print("{} - {}".format(i["UF"], i["nome"]))
    return 1
    

if __name__ == "__main__":
    init(autoreset=True)
    
    print(f"{Fore.BLUE}Bem vindo ao gestão de abrangencias")
    try:
        Reg.importarAbrangencias("abrangencias.json")
    except IOError:
        print(f"{Fore.RED}{Back.CYAN}{Style.BRIGHT}Abrangencias não localizadas")

    while True:
        op = menu()
        
        if op == "1":
            while True:
                _e = str.upper(input("Digite uma das opções abaixo:\nE para lista abrangências estaduais\nM para municipios\nZ para zonas\nS para seções\ndigite sua opção: "))
                if _e == "E" or _e == "M" or _e == "Z" or _e == "S":
                    if _e == "E":
                        _nE = input("Digite o nome do estado (sem acentos): ")
                        _uf = input("Digite oa sigla do estado: ")
                        Reg.abrNacional.incluirAbrEstadual(_nE, _uf)
                        Reg.exportarAbrangencias("abrangencias.json")
                    if _e == "M" or _e == "S" or _e == "Z":
                        _t = listarAbrangencias(1)
                        if _t == -1:
                            print(f"{Fore.RED}Sua lista não possui abragências estaduais\nVocê precisa de estados para incluir zonas ou municípios")
                    
                        elif _e == "M":                      
                            _uf = str.upper(input("Digite a sigla do estado: "))
                            _nM = input("Digite o nome do município (sem acentos): ")
                            _abrM = Reg.abrNacional.abrEstaduais[Reg.abrNacional.indexEstadoPorUF(_uf)].incluirAbrMunicipal(_nM)
                            Reg.exportarAbrangencias("abrangencias.json")
                    break                
        elif op == "2":
            listarAbrangencias(1)
        elif op == "3":
            listarAbrangencias(1)
            _abrE = str.upper(input("Digite a sigla do estado para listar as abrangências municipais: "))
            listarAbrangencias(2, _abrE)

        elif op == "Deb":
            print(Reg.abrNacional.serializar())
        elif op == "9":
            break
