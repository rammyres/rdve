import os, codecs

class cedula:
    endUrna = None
    idCedula = None

    def __init__(self, endUrna = None, idCedula = None):
        if endUrna and idCedula:
            self.endUrna = endUrna
            self.idCedula = idCedula

    def criarCedula(self, endUrna):
        self.endUrna = endUrna
        self.idCedula = codecs.encode(os.urandom(32), 'hex').decode()

class cedulas(list):
    endUrna = None
    _saldo = None

    @property
    def saldo(self, saldo):
        return _saldo

    @saldo.setter
    def saldo(self, saldo):
        if not _saldo:
            


    def __init__(self, endUrna, saldo = None):
        if not saldo:
            self.endUrna = endUrna
        elif saldo == 0:

    
    def _criarCedulas(self, saldo):
        for x in range(saldo):
            _Cedula = cedula()
            _Cedula.criarCedula(self.endUrna)
            self.append(_Cedula)
