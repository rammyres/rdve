#!/usr/bin/env python3
from rdve.Criptografia import Criptografia
from rdve.AES import CifrarComAES
from ecdsa import SigningKey, SECP256k1
import qrcode, os

aux = Criptografia()

sk = SigningKey.generate(curve=SECP256k1)
pem = sk.to_pem().decode()
print(pem)

senha = input("Digite uma senha para encriptar o certificado: ")
sal = os.urandom(32).hex()
encriptador = CifrarComAES(aux.hashSenha(senha, sal))
encriptado = encriptador.criptografar(pem.encode('utf-8'))

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=24,
    border=4,
)

qr.add_data(encriptado)
qr.make_image(fit=True)
img = qr.make_image()
img.save("teste.png")

senha = input("Digite uma senha para decriptar o certificado: ")
decriptador = CifrarComAES(aux.hashSenha(senha, sal))
decriptado = decriptador.decriptar(encriptado)
print(len(encriptado))

print(encriptado)
print(decriptado)