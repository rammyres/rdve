from Erros import tipoDeOperadorInvalido

class Mesario:
    nome = ''
    titulo = ''
    def __init__(self, nome, titulo):
        self.nome = nome
        self.titulo = titulo

class Presidente(Mesario):
    pass

class Operadores(list):
    def __init__(self, *operadores):
        for x in operadores:
            self.inserir(x)

    def inserir(self, operador):
        if isinstance(operador, Mesario):
            self.append(operador)
        else:
            raise tipoDeOperadorInvalido("Operador deve ser do tipo Mesario ou Presidente")