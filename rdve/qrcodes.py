import qrcode, json
from ecdsa import SigningKey, VerifyingKey
from Criptografia import criptografia

class exportadorTitulo:
    _chave_privada = None

    @property
    def chave_privada(self, chave_privada):
        return self._chave_privada
    
    @chave_privada.setter
    def chave_privada(self, chave_privada):
        if isinstance(chave_privada, SigningKey):
            self._chave_privada = chave_privada
        else:
            raise TypeError("Deve ser passada uma chave privada instanciada como parâmetro")

    def __init__(self, nr_titulo, aleatorio, chave_privada, senha):
        self.numero = nr_titulo
        self.chave_privada = chave_privada
        self.chave_encriptada = self.encriptarChave(self.chave_privada, senha, aleatorio)

    def encriptarChave(self, chave_privada, senha, aleatorio):
        _encriptador = criptografia()
        _ek = _encriptador.encriptarChaveAES(chave_privada, senha, aleatorio)
        return _ek

    def serializar(self):
        return {"titulo": self.numero, "chave": self.chave_encriptada}

    def gerarQR(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(self.serializar(), indent=4))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        return img

    def exportarQR(self, arquivo):
        img = self.gerarQR()
        img.save(arquivo)



    

