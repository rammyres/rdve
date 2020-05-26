from Cedulas import Cedula
from hashlib import sha256
from Erros import excedeMaxVotos, cedulaSemVotos, cedulaNaoAssinada

class CedulaPreenchida(Cedula):
    votos = []
    assinatura = None
    Hash = None

    def __init__(self, dicionario_cedula):
        self.idCedula = dicionario_cedula["idCedula"]
        self.tipoEleicao = dicionario_cedula["tipoEleicao"]
        self.maxVotos = int(dicionario_cedula["maxVotos"])

    def inserirVotos(self, votos):
        if isinstance(votos, list):
            for v in votos:
                self._inserirVoto(v)

    def _inserirVoto(self, voto):
        # A classe vai verificar se o voto segue os votos contidos 
        # contém as chaves certas
        if len(self.votos) <= self.maxVotos:
            if len(voto.keys)>2:
                if voto.keys()[0] == "enderecoDestino" and voto.keys()[1] == "quantidade":
                    self.votos.append(voto)
        else:
            raise excedeMaxVotos("Numero de votos superior ao máximo permitido para a cédula")   

    def importarVotos(self, dicionario):
        self.votos = [v for v in dicionario["votos"]]

    def dadosCedula(self):
        if not self.votos:
            raise cedulaSemVotos
        else:
            for x in range(len(self.votos)):
                _vs = "{}:{}:".format(_vs, self.votos(x))

        return "{}{}{}{}".format(self.idCedula, self.tipoEleicao, self.maxVotos, _vs[:-1])

    def gerarHash(self):
        if self.assinatura:
            _hash = sha256(self.dadosCedula().encode())
        else:
            raise cedulaNaoAssinada

    def dicionario_votos(self):
        if self.votos:
            _d = [v for v in self.votos]
            return _d
        else:
            raise cedulaSemVotos

    def serializar(self):
        if len(self.votos) == self.maxVotos and self.assinatura and self.Hash:
            return {"idCedula": self.idCedula, 
                    "tipoEleicao": self.tipoEleicao, 
                    "maxVotos": self.maxVotos,
                    "votos": self.dicionario_votos(),
                    "assinatura": self.assinatura,
                    "hash": self.Hash}