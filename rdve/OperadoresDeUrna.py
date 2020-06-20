from Erros import tipoDeOperadorInvalido

class Mesario:
    nome = ''
    titulo = ''
    chavePublica = ''
    def __init__(self, nome, titulo, chavePublica):
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
    
    def serializar(self):
        lista = [{"titulo":x.titulo, "nome":x.nome, "chavePublica":x.chavePublica} for x in self]
        return lista

