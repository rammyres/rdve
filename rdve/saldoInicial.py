from Erros import incrementoDeSaldoInvalido

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