#!/usr/bin/env python3
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


class registroSemTransacoes(Exception):
    def __init__(self):
        self.message = "O registro de votação deve conter transações antes do calculo da árvore de assinaturas"

class processoDeAssinaturaInvalido(Exception):
    def __init__(self):
        self.message = "Para assinatura o metódo deve receber os dados e a chave privada como parametros"

class urnaSemEndereco(Exception):
    def __init__(self):
        self.message = "A urna deve ter um endereço válido para gerar uma transação válida"

class dataInferiorAoLimite(Exception):
    message = "A data apresentada é inferior ao limite de criação da votação"

class listaDeTransacoesVazia(Exception):
    message = "Lista de transações vazia"

class saldoInconsistente(Exception):
    message = "O saldo de cédulas e o comprimento da lista deve ser igual"

class enderecoDaUrnaNulo(Exception):
    message = "O endereço da urna não pode ser nulo"

class hashDoBlocoDeCedulasInvalido(Exception):
    message = "Há uma divergência entre algum dos hashes computados e persistidos"

class abragenciaDuplicada(Exception):
    message = "Não pode haver inclusão de abrangências com o mesmo número ou nome"

class abrangenciaInvalida(Exception):
    message = "Houve tentativa de insersão de uma abrangência não existe na lista de abrangências válidas"

class requisicaoVotoInvalida(ValueError):
    pass

class tipoDeEscolhaInvalida(TypeError):
    pass

class excedeMaxVotos(ValueError):
    pass

class incrementoDeSaldoInvalido(ValueError):
    pass

class tipoDeEleicaoInvalida(ValueError):
    pass

class cedulaNaoAssinada(ValueError):
    pass

class cedulaSemVotos(ValueError):
    pass

class votoNulo(ValueError):
    pass

class candidatoInvalido(ValueError):
    pass

class votosNaoPreparadosParaApuracao(Exception):
    pass

class tipoDeOperadorInvalido(TypeError):
    pass

class naoEhCedula(TypeError):
    pass
        