from Erros import tipoDeOperadorInvalido
from Criptografia import Criptografia

class Operador:
    criptUtil = Criptografia()
    nome = ''
    titulo = ''
    chavePublica = ''
    def __init__(self, tipo, nome, titulo, chavePublica):
        if tipo == "Mesario" or tipo == "Presidente":
            self.tipo = tipo
        else:
            raise tipoDeOperadorInvalido("O operador deve ser Mesario ou Presidente")
        self.nome = nome
        self.titulo = titulo

class Operadores(list):
    def __init__(self, *operadores):
        for x in operadores:
            self.inserir(x)

    def inserir(self, operador):
        if isinstance(operador, Operador):
            self.append(operador)
        else:
            raise tipoDeOperadorInvalido("Operador deve ser do tipo Mesario ou Presidente")
    
    def importar(self, dicionarios):
        for dicionario in dicionarios:
            _operador = Operador(dicionario["tipo"],
                                 dicionario["nome"],
                                 dicionario["titulo"],
                                 dicionario["chavePublica"])
            self.inserir(_operador)
    
    def serializar(self):
        lista = [{"tipo": x.tipo, "nome":x.nome, "titulo":x.titulo, "chavePublica":x.chavePublica} for x in self]
        return lista

