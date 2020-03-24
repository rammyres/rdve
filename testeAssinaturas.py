#!/usr/bin/env python3
import json, os, sys, codecs, random 
from ecdsa import SigningKey, curves, SECP256k1

if __name__ == "__main__":
    
    urnas = []
    
    for x in range (int(sys.argv[1])):
        chavePrivada = SigningKey.generate(curve=SECP256k1)
        chavePu = chavePrivada.verifying_key
        chavePublica = chavePu.to_string().hex()
        saldo = random.randint(1, 300000)
        assinatura = codecs.encode(chavePrivada.sign(str(saldo).encode()), 'hex').decode()
        urnaID = codecs.encode(os.urandom(16), 'hex').decode()
        
        assinaturas.append({"urnaID": urnaID, "saldo": saldo, "chavePrivada": chavePrivada.to_string().hex(), "chavePublica": chavePublica, "assinatura": assinatura})
    
    print("Concluida a geração das chaves, exportando...")

    arquivo = open("testeAssinaturas.json", "w")

    urna = {"urnas": assinaturas}

    json.dump(urna, arquivo, indent=4)
    arquivo.close()
    print("Dados exportados, encerrando")

    arquivo = open("testeAssinaturas.json", "r")

    urna2 = json.load(arquivo)

    for u in urna2["urnas"]:


        

