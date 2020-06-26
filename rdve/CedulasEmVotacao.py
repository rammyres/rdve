from Cedulas import Cedula
from hashlib import sha256
from Erros import excedeMaxVotos, cedulaSemVotos, cedulaNaoAssinada, naoEhCedula

class CedulaEmVotacao(Cedula):
    votos = []
    
    def __init__(self, dicionario_cedula):
        try: 
            self.idCedula = dicionario_cedula["idCedula"]
            self.tipoEleicao = dicionario_cedula["tipoEleicao"]
            self.maxVotos = int(dicionario_cedula["maxVotos"])
            self.assinatura = dicionario_cedula["assinatura"]
            self.Hash = dicionario_cedula["hash"]
            self._importarVotos(dicionario_cedula)
        except KeyError:
            self.Hash == None
            self.assinatura = None        

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

    def _importarVotos(self, dicionario):
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

    def _serializar_votos(self):
        if self.votos:
            _d = [v for v in self.votos]
            return _d
        else:
            raise cedulaSemVotos


    def serializar(self):
        if len(self.votos) == self.maxVotos and self.assinatura and self.Hash:
            return {"tipo": "cedulaPreenchida",
                    "idCedula": self.idCedula, 
                    "tipoEleicao": self.tipoEleicao, 
                    "maxVotos": self.maxVotos,
                    "votos": self._serializar_votos(),
                    "assinatura": self.assinatura,
                    "hash": self.Hash}

class CedulasEmVotacao(list):

    def __init__(self, dicionariosCedulas):
        if dicionariosCedulas:
            self.importarCedulasEmBranco(dicionariosCedulas)
        

    def inserirCedula(self, cedula):
        if isinstance(cedula, Cedula):
            self.append(cedula)
        else:
            raise naoEhCedula

    def importarCedulasEmBranco(self, dicionariosCedulas):
        for _dictCedula in dicionariosCedulas:
            _cedula = CedulaEmVotacao(_dictCedula)
            self.inserirCedula(_cedula)
    
    def serializar(self):
        _cedulas = []
        for _c in self:
            self.idCedula = dicionario_cedula["idCedula"]
            self.tipoEleicao = dicionario_cedula["tipoEleicao"]
            self.maxVotos = int(dicionario_cedula["maxVotos"])
            self.assinatura = dicionario_cedula["assinatura"]
            self.Hash = dicionario_cedula["hash"]
            _cc = {"idCedula":self.idCedula, "tipoEleicao"}
