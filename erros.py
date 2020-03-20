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

class deveSerBlocoDeTransacaoFinal(Exception):
    def __init__(self):
        self.message = "O bloco de transação para construção do bloco deve ser \
                        do tipo blocoDeTransacoesFinal"

class sequenciaDeHashesInvalida(Exception):
    def __init__(self):
        self.message = "O bloco de transações final possui um erro na validação da sequência dados"

class arvoreDeMerkleInvalida(Exception):
    def __init__(self):
        self.message = "A árvore de Merkle computada a partir das transações do bloco\
                        diverge da árvore persistida"

class listaDeDicioariosVazia(Exception):
    def __init__(self):
        self.message = "Lista de dicionarios a ser importada está vazia"
