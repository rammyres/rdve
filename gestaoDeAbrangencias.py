#!/usr/bin/env python3
from colorama import init, Fore, Back, Style
from collections import OrderedDict
import json, colorama, copy

class abrangencias(OrderedDict):
    def __init__(self):
        self.update({"1":"BRASIL"})
        self.ultMun = 0
        self.ultEst = 0

    def ordenarPorChave(self):
        _tmp = OrderedDict(sorted(self.items()))
        self.clear()
        self.update(_tmp)

    def listarEstados(self):
        est = OrderedDict({"Estado":"Nome"})
        if len(est) == 0:
            return None
        for k in self.keys():
            if k.startswith("3"):
                _d = {k[-2:]: self[k]}
                est.update(_d)
        return est

    def listarMunicipios(self):
        mun = OrderedDict()
        for k in self.keys():
            if k.startswith("5"):
                mun.update(str(k), self[k])
        return mun

    def inserir(self, tipo, nome, estado = None):
        nome = str.upper(nome)
        if tipo == "3":
            self.ultEst += 1
            self.update({"3{:0>2d}".format(self.ultEst):nome})
        if tipo == "5" and estado != None:
            self.ultMun += 1
            self.update({"5{:0>2d}{:0>3d}".format(estado, self.ultMun):nome})
        elif tipo == "5" and estado != None:
            return False
        self.ordenarPorChave()
        self.exportarJson()
        return True

    def importarJson(self):
        try:
            _arq = open("abrangencias.json", "r")
            _dict = json.load(_arq)

            for k in _dict.keys():
                if k.startswith("3"):
                    self.ultEst += 1
                elif k.startswith("5"):
                    self.ultMun += 1
                self.update({k:str.upper(_dict[k])})

            _arq.close()
            return True
        
        except IOError:
            return False
        
    def exportarJson(self):
        _arq = open("abrangencias.json", "w")
        json.dump(self, _arq, indent=4)
        _arq.close()

    def listarAbrangencias(self):
        if len(self) == 0:
            print("Não existem abrangências cadastradas ")
        else:
            for k in self.keys():
                print("{} - {}".format(k, self[k]))

        
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

abrNacional = abrangencias()

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
