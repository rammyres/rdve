import os, math, hashlib, copy
from erros import alturaDoNoMenorQueZero, quantidadeMenorQueUm, arvoreNaoConstruida
'''
Implementação de uma árvore de Merkle
'''
class arvoreDeMerkle:

    # O nó é a unidade basica de armazenamento dentro da árvore de merkle, ele pode ser um "Nó" ou uma folha
    # Folhas não possuem 
    class No:

        def __init__(self, mae, pai, Hash):
            self.noMae = mae
            self.noPai = pai
            
            if mae == None:
                self._altura = 0
            else:
                self._altura = self.noMae._altura = 0 

            self.Hash = Hash
            self.noFilho = None


        @property
        def altura(self):
            return self._altura
        
        @altura.setter
        def altura(self, h):
            if h < 0:
                raise alturaDoNoMenorQueZero
            self._altura = h
            

        def retorna_umConjuge_peloOutro(self, hashDoOutro):
            if hashDoOutro == self.noMae.Hash:
                return self.noPai
            return self.noMae
    
    def __init__(self, itens):
        if len(itens) <= 0:
            raise quantidadeMenorQueUm

        self.construida = False
        self.hash_raiz = None
        self.tabelaDeNos = {}
        self.alturaMaxima = math.ceil(math.log(len(itens), 2))
        self.folhas = [*map(self._criarFolha, [*map(self._sha256, itens)])]

        if itens and len(itens) > 0:
            self.construirArvore()

    def _criarFolha(self, dados):
        folha = self.No(None, None, dados)
        folha.altura = 0
        return folha

    def _retornaRamoPeloHash(self, hash_):

        caminho = []

        while hash_ != self.hash_raiz:
            no = self.tabelaDeNos[hash_]
            noFilho = no.noFilho
            noConjuge = noFilho.retorna_umConjuge_peloOutro(hash_)
            caminho.append(noConjuge.Hash)
            hash_ = noFilho.Hash
        
        caminho.append(hash_)
        caminho.reverse()
        return caminho

    def _sha256(self, dado):
        dado = str(dado)

        m = hashlib.sha256(dado.encode()).hexdigest()

        return m

    def _auditar(self, hashDeTeste, hashesDeProva):
        """ 
            Testa se o hashDeTeste é membro da árvore de merkle, criando hashes 
            dele junto com o nó "irmão" e verificando se o valor coincide com o nó
            superior, até chegar a raiz da árvore
        """
        hashDeProva = hashesDeProva.pop()

        if not hashDeProva in self.tabelaDeNos.keys():
            return False

        noIrmao = self.tabelaDeNos[hashDeProva]
        noFilho = noIrmao.noFilho

        # O teste verifica qual "pai" é o hashDeTeste, já que a ordem da 
        # concatenação é relevante para a formação da árvore
        if noFilho.noMae.Hash == hashDeTeste:
            hashAtual = self._sha256(hashAtual + noIrmao.Hash)
        elif noFilho.noPai.Hash == hashDeTeste:
            hashAtual = self._sha256(noIrmao.Hash + hashDeTeste)
        else:
            return False

        if hashAtual != noFilho.Hash:
            return False
        if hashAtual == self.hash_raiz:
            return True

        return self._auditar(hashAtual, hashesDeProva)

    def _gerirArvoreComUmaFolha(self,):
        # Caso a árvore possua uma só folha a criação da árvore poderá falhar, 
        # por isso é preciso gerir essa possbilidade
        if len(list(self.folhas)) == 1:
            no_unico = self.folhas.pop()
            self.hash_raiz = no_unico.Hash
            self.tabelaDeNos[no_unico.Hash] = no_unico

    def _retorna_hashes_dasFolhas(self):
        return [no.Hash for no in self.tabelaDeNos.values() if no.noMae == None]

    def construirArvore(self):
        """
        A construção dad árvore funciona da seguinte forma:
        As folhas são adicionadas, uma a uma, a uma pilha e 
        combinando as mesmas quando elas tem a mesma altura 
        (na árvore).
        É esperado que os itens estejam em um array do tipo 
        No. A tabelaDeNos também é construida, como um di-
        cionario, que mantém os hashes que mapeam os nós 
        para auditoria. 
        """
        pilha = []
        
        while self.hash_raiz == None:
            self._gerirArvoreComUmaFolha()

            if len(pilha) >= 2 and pilha[-1].altura == pilha[-2].altura:
                noMae = pilha.pop()
                noPai = pilha.pop()
                hash_noFilho = self._sha256(noMae.Hash+noPai.Hash)
                noFilho = self.No(noMae, noPai, hash_noFilho)
                self.tabelaDeNos[hash_noFilho] = noFilho
                noMae.noFilho = noFilho
                noPai.noFilho = noFilho

                if noFilho.altura == self.alturaMaxima:
                    self.hash_raiz = noFilho.Hash

            elif len(self.folhas) > 0:
                folha = self.folhas.pop()
                self.tabelaDeNos[folha.Hash] = folha
                pilha.append(folha)
            # Handle case where last 2 nodes do not match in height by "graduating"
            # last node
            else:
                pilha[-1].altura += 1
        
        self.construida = True

    def auditar(self, dado, hashesDeProva):

        """ 
            Rertorna falso ou verdadeiro se o dado apresentado
            está na árvore. 
            Os hashesDeProva são nós que deve-se criar hashes
            com o hash do dado apresentado, em ordem, do topo 
            até o penultimo nível da árvore. O comprimento da 
            prova deve ser igual a altura da árvore (log2(n)),
            já que um nó é necessário como prova por nível.
            Se a árvore não estiver consturida o retorno será
            sempre falso.
        """
        if self.hash_raiz == None:
            return False

        hash_ = self._sha256(dado)

        # A one element tree does not make much sense, but if one exists
        # we simply need to check if the files hash is the correct root
        if self.alturaMaxima == 0 and hash_ == self.hash_raiz:
            return True
        if self.alturaMaxima == 0 and hash_ != self.hash_raiz:
            return False

        cp_hashesDeProva = copy.copy(hashesDeProva)
        return self._auditar(hash_, cp_hashesDeProva)

    def retornaRamo(self, item):
        """ Returna o ramo de nós do item na árvore de merkle, como uma lista 
            do topo a raiz.
        """
        if not self.construida:
            raise arvoreNaoConstruida

        hash_ = self._sha256(item)

        if not hash_ in self._retorna_hashes_dasFolhas():
            raise arvoreNaoConstruida

        return self._retornaRamoPeloHash(hash_) 

    def travessia(self, no_):
        print("{}:{}".format(no_.Hash, no_.altura))
        if no_.noMae:
            self.travessia(no_.noMae)
        if no_.noPai:
            self.travessia(no_.noPai)

