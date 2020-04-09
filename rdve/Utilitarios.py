import codecs, os, ecdsa, base58, binascii, hashlib
from ecdsa import SigningKey, VerifyingKey, curves, SECP256k1


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

def gerarChavePrivada(arquivo):
    _chavePrivada = os.urandom(32)
    _sk = ecdsa.SigningKey.from_string(_chavePrivada, curve=ecdsa.SECP256k1)
    _arq = open(arquivo, "wb")
    _arq.write(_sk.to_pem())
    _arq.close()

def gerarChavePublica(arquivo):
    try:
        _arq = open(arquivo, "rb")
        chavePrivada = SigningKey.from_pem(_arq.read())
        chavePublica = chavePrivada.verifying_key
        return chavePublica
    except IOError:
        print("Arquivo inexistente")
    finally:
        _arq.close()

def importarChavePrivada(arquivo):
    try:
        _arq = open(arquivo, "rb")
        chavePrivada = SigningKey.from_pem(_arq.read())
        return chavePrivada
    except IOError:
        print("Arquivo inexistente")
    finally:
        _arq.close()

def importarChavePublica(arquivo):
    try:
        _arq = open(arquivo, "rb")
        chavePublica = VerifyingKey.from_pem(_arq.read())
        return chavePublica
    except IOError:
        print("Arquivo inexistente")
    finally:
        _arq.close()

def ripemd160(x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d

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
