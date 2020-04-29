import codecs, os, ecdsa, base58, binascii, hashlib, io, qrcode
from ecdsa import SigningKey, VerifyingKey, curves, SECP256k1
from Cryptodome.Protocol.KDF import scrypt
from rdve.AES import CifrarComAES

def hashArquivo(arquivo):
    tamanho = 65536
    calculador = hashlib.sha256()
    
    _arq = open(arquivo, "rb")

    tmp = _arq.read(tamanho)
    while len(tmp)>0:
        calculador.update(tmp)
        tmp = _arq.read(tamanho)
    _arq.close()

    return calculador.hexdigest()

def remover_seguramente(caminho, passagens):
    with open(caminho, "ba+", buffering=0) as arquivo:
        tamanho = arquivo.tell()
    arquivo.close()
        
    with open(caminho, "br+", buffering=0) as arquivo:
        for _ in range(passagens):
            arquivo.seek(0,0)
            arquivo.write(os.urandom(tamanho))
        arquivo.seek(0)
    
    for _ in range(tamanho):
        arquivo.write(b'\x00')
    
    os.remove(caminho) 

def gerarChavePrivada():
    _chavePrivada = os.urandom(32)
    _sk = ecdsa.SigningKey.from_string(_chavePrivada, curve=ecdsa.SECP256k1)
    return _sk

def exportarChavePrivada(chave, arquivo):
    _arq = open(arquivo, "wb")
    _arq.write(chave.to_pem())
    _arq.close()

def gerarChavePublica(chavePrivada):
    if isinstance(chavePrivada, io.IOBase):
        _arq = open(chavePrivada, "rb")
        _sk = SigningKey.from_pem(_arq.read())
    elif isinstance(chavePrivada, str):
        _sk = SigningKey.from_pem(bytearray.fromhex(chavePrivada))
    _vk = _sk.verifying_key
    return _vk
    
def exportarChavePublica(chavePublica, arquivo):
    try:
        _arq = open(arquivo, "rb")
    except IOError:
        print("Arquivo inexistente")
    finally:
        _arq.close()

def importarChavePrivada(chave):
    try:
        if isinstance(chave, io.IOBase):
            _arq = open(chave, "rb")
            chavePrivada = SigningKey.from_pem(_arq.read())
        elif isinstance(chave, str):
            chavePrivada = SigningKey.from_string(bytearray.fromhex(chave))
        return chavePrivada
    except IOError:
        print("Arquivo inexistente")
    finally:
        _arq.close()

def importarChavePublica(chave):
    try:
        if isinstance(chave, io.IOBase):
            _arq = open(chave, "rb")
            chavePublica = VerifyingKey.from_pem(_arq.read())
        elif isinstance(chave, str):
            chavePublica = VerifyingKey.from_string(bytearray.fromhex(chave))
        return chavePublica
    except IOError:
        print("Arquivo inexistente")
    finally:
        _arq.close()

def exportarChaveQRCode(chave, arquivo, senha):
    encriptador = CifrarComAES(senha)
    if isinstance(chave, io.IOBase):
        _arq = open(chave)
        cert = _arq.read()
    elif isinstance(chave, SigningKey):
        cert = chave.to_pem().hex()
    encriptado = encriptador.criptografar(cert)
    img = qrcode.make(encriptado)
    img.save(arquivo)
   
def ripemd160(x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d

def hashSenha(senha, sal):
    _s = scrypt(senha.encode(), sal, 32, N=2**16, r=8, p=8)
    return _s


def gerarEndereco(chavePrivada):
    # generate private key , uncompressed WIF starts with "5"
    #chavePrivada = os.urandom(32)
    #chaveCompleta = '80' + binascii.hexlify(chavePrivada).decode()
    #sha256a = hashlib.sha256(binascii.unhexlify(chaveCompleta)).hexdigest()
    #sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
    #WIF = base58.b58encode(binascii.unhexlify(chaveCompleta+sha256b[:8]))
    
    # get public key , uncompressed address starts with "1"
    _sk = open(chavePrivada, "rb")
    sk = ecdsa.SigningKey.from_pem(_sk.read())
    vk = sk.get_verifying_key()
    chavePublica = '04' + binascii.hexlify(vk.to_string()).decode()
    hash160 = ripemd160(hashlib.sha256(binascii.unhexlify(chavePublica)).digest()).digest()
    enderecoPublico_a = b"\x00" + hash160
    checksum = hashlib.sha256(hashlib.sha256(enderecoPublico_a).digest()).digest()[:4]
    enderecoPublico_b = base58.b58encode(enderecoPublico_a + checksum)

    return enderecoPublico_b.decode()
