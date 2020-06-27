from Erros import incrementoDeSaldoInvalido, tipoDeEleicaoInvalida

class saldoInicial:
    
    def __init__(self, idCargo):
        self.idCargo = idCargo
        self.saldo = 0

    def incrementarSaldo(self, incremento):
        if incremento == 1:
            self.saldo += 1
        elif self.saldo == 0:
            self.saldo = incremento
        else:
            raise incrementoDeSaldoInvalido("Só é possível incrementar o saldo em unidades ou setar o valor total quando o saldo estiver 0")

    def serializar(self):
        return {"idCargo": self.idCargo, "saldo": self.saldo}

class saldosIniciais(list):

    def __init__(self, tipoEleicao):
        if tipoEleicao == "1":
            self.maxSaldos = 5
        elif tipoEleicao == "2":
            self.maxSaldos = 2
        elif tipoEleicao == "3" or tipoEleicao == "4" or tipoEleicao == "5":
            self.maxSaldos == 1
        else:
            raise tipoDeEleicaoInvalida("Tipo de eleição não previsto")

    def serializar(self):
        _dictSaldos = [{x.serializar() for x in self}]

        return _dictSaldos

    def inserir(self, saldo):
        if isinstance(saldo, saldoInicial):
            self.append(saldo)
        else:
            raise TypeError("Tipo de saldo inválido")

    def dados(self):
        _dados = ':'
        return _dados.join(self)

