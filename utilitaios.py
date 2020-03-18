import os

class utilitarios:

    def remover_seguramente(self, caminho, passagens):
        with open(caminho, "ba+", buffering=0) as arquivo:
            tamanho = arquivo.tell()
        arquivo.close()
        
        with open(caminho, "br+", buffering=0) as arquivo:
    
            for i in range(passagens):
                arquivo.seek(0,0)
                arquivo.write(os.urandom(tamanho))
        arquivo.seek(0)
        for x in range(tamanho):
            arquivo.write(b'\x00')
    
        os.remove(caminho) 
