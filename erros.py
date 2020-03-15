class alturaDoNoMenorQueZero(Exception):
    def __init__(self):
        self.message = "A altura do nó/folha nao pode ser inferior a 0"

class quantidadeMenorQueUm(Exception):
    def __init__(self):
        self.message = "Pelo menos um item deve estar presente \
                        para formar uma árvore válida"

class arvoreNaoConstruida(Exception):
    def __init__(self):
        self.message = "A árvore não está construida"

class tipoDeTransacaoDesconhecido(Exception):
    def __init__(self):
        self.message = "A transação a ser inserida deve ser de um tipo especifico"
