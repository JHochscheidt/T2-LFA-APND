# coding: utf-8
import sys
import os
import string

regras = [] #vetor com de objetos do tipo regra
fita = [] # entrada do programa
listaTransicoes = [] # lista de objetos Transicao
pilha = []
terminals = []
noTerminals = []

class Regra(object):
    def __init__(self, estado, fita, pilha, transicoes):
        self._estado = estado
        self._removeFita = fita
        self._removePilha = pilha
        self._transicoes = transicoes
class TransicaoRegra(object):
    def __init__(self, estado, empilha):
        self._estado = estado
        self._empilha = empilha
class Transicao(object):
    def __init__(self, estado, fita, pilha, regra, transicao):
        self._estado = estado #qual estado foi
        self._fita = fita #o que tem na fita depois da transicao
        self._pilha = pilha #o que tem na pilha depois da transicao
        self._regra = regra #regra que gerou essa transicao
        self._transicao = transicao #indice da transicao
def readFita(arquivoFita):
    file = open(arquivoFita, 'r')
    fitaTemp = file.readlines()
    file.close()
    for linha in fitaTemp:
        linha = linha.replace("\n", "")
        linha = linha.replace(" ", "")
        #fita.append(linha)
        for c in linha:
            fita.append(c)

    #print fita
    #input("hue")
def readRegras(arquivoRegras):
    file = open(arquivoRegras, 'r')
    arq_regras = file.readlines()
    file.close()
    for linha in arq_regras:
        linha = linha.replace(" ","")
        ## quebra a linha em 2 partes
        ## primeira parte é a readRegras
        ## segunda parte sao as transicoes
        linha = linha.split('=')
        #tratar primeira parte linha[0]
        regra = linha[0]
        if regra[0] != '(' or regra[-1] != ')':
            print ("erro na declaracao da regra" + str(regra))
            sys.exit()
        ## regra possui campos separados por virgula, entao faz split
        regra = regra.split(',')
        #regra[0] possui o estado
        #regra[1] possui o que sera removido da fita
        #regra[2] possui o que sera tirado do topo da pilha
        estado = regra[0]
        estado = estado[1:] # pra tirar o "(" do inicio da regra
        removeDaFita = regra[1]
        removeDaPilha = regra[2]
        removeDaPilha = removeDaPilha[0:-1] # remove ")" do do final da regra
        transicoes = linha[1]
        #primeiro remove \n
        transicoes = transicoes.replace("\n", "")
        #remove as chaves das transicoes
        transicoes = transicoes.replace("{","")
        transicoes = transicoes.replace("}","")
        transicoes = transicoes.replace(">","")
        transicoes = transicoes.replace("<","")
        ## regra possui campos separados por virgula e parentes "),(", entao faz split
        transicoes = transicoes.split("),(")
        ## remover "(" da primeira transicao
        transicoesTemp = []
        for indice in range(0, len(transicoes)):
            # se for a primeira transicao, remover os parenteses sobrando
            transicaoTemp = transicoes[indice]
            if indice == 0:
                transicaoTemp = transicoes[indice]
                #so tem 1 transicao
                if len(transicoes) == 1:
                    transicaoTemp = transicaoTemp[1:-1]
                else:
                    transicaoTemp = transicaoTemp[1:]
            #se for a ultima transicao remover os parenteses sobrando
            elif indice == len(transicoes)-1:
                transicaoTemp = transicoes[indice]
                transicaoTemp = transicaoTemp[0:-1]
            #split pra pegar o estado e o que vai ser empilhado
            transicaoTemp = transicaoTemp.split(',')
            estado = transicaoTemp[0]
            empilha = transicaoTemp[1]
            empilha = empilha.replace("<","")
            empilha = empilha.replace(">","")
            #transicaoTemp[0] tem o estado
            #transicaoTemp[1] -- empilha tem o que vai ser empilhado
            for char in empilha:
                # se for terminal
                if char in string.lowercase:
                    if char not in terminals:
                        terminals.append(char)
                #se for nao terminal
                elif char in string.uppercase:
                    if  char not in noTerminals:
                        noTerminals.append(char)

            newTransicaoRegra = TransicaoRegra(estado,empilha)

            #adicionar essas informacoes no vetor temporario de transicoes
            transicoesTemp.append(newTransicaoRegra)
        #aqui ja pode adicionar a regra e suas transicoes
        newRegra = Regra(estado, removeDaFita, removeDaPilha, transicoesTemp)
        regras.append(newRegra)
    #fim do for pra cada regra (cada linha do arquivo)
def printRegras():
    print "\n\n###REGRAS ###\n\n"
    for regra in regras:
        print "qt transicoes ", len(regra._transicoes)
        print "(",regra._estado,",", regra._removeFita,",",regra._removePilha,") =",
        for transicao in regra._transicoes:
            print "(",transicao._estado,",", transicao._empilha,")",
            #printTransicaoRegra(transicao)
        print "\n"
def printRegra(regra):
    print "\n\n###REGRA ###\n\n"
    #print "qt transicoes ", len(regra._transicoes)
    print "(",regra._estado,",", regra._removeFita,",",regra._removePilha,") =",
    for transicao in regra._transicoes:
        print "(",transicao._estado,",", transicao._empilha,")",
    print "\n"
def printTransicao(transicao):
    print "\n\n ### TRANSIÇÃO ### \n\n"
    print "(",transicao._estado,",",transicao._fita,",",transicao._pilha,",",transicao._regra,",",transicao._transicao,")"
def printTransicoes():
    print "### TRANSIÇÕES ###"
    for transicao in listaTransicoes:
        print "[",transicao._estado,",",transicao._fita,",",transicao._pilha,",",transicao._regra,",",transicao._transicao,"]"
def printTransicaoRegra(TrRegra):
    print "\n\n ### TRANSIÇÃO REGRA ### \n\n"
    print "(",TrRegra._estado,",",TrRegra._empilha,")",
# busca regra pelo que ta no topo da pilha
def buscaRegra(topoPilha): #estado atual tem uma tripla Ex. (0,&,E)
    for indice in range(0, len(regras)):
        if regras[indice]._removePilha == topoPilha:
            return indice
    return -1
def explosaoDeEstados(pilha, fita):
    LAST_TR_VALIDA = True
    PROX_TR = 0
    while len(pilha) > 0 or len(fita) > 0 or len(listaTransicoes) > 0:
        if LAST_TR_VALIDA == True:
            #pega a ultima transicao
            if len(listaTransicoes) < 1:
                print "acabou transicoes"
                sys.exit()
            lastTransicao = listaTransicoes[len(listaTransicoes)-1]

            if len(lastTransicao._pilha) == 0:
                print "pilha vazia"
                printTransicoes()
                sys.exit()
            nomeRegra = lastTransicao._pilha[0]
            indR = buscaRegra(nomeRegra)

            if indR < 0:
                print "regra nao existe"
                sys.exit()

            #para cada transicao de uma regra
            for indT in range(PROX_TR , len(regras[indR]._transicoes)):
                infoTransicao = regras[indR]._transicoes[indT]
                #aplica a transicao
                if nomeRegra not in terminals: #topo da pilha é um nao terminal
                    #faz substituicao do topo da pilha
                    #nao mexe na fita
                    print "\n### SUBSTITUICAO ##",
                    print "p ant -->",pilha,
                    #print "tp pilha bf",type(pilha),
                    pilha = pilha[1:]

                    #print "tp pilha af",type(pilha),
                    estado = infoTransicao._estado
                    empilha = infoTransicao._empilha
                    empilha = empilha[::-1] #inverter o que vai ser empilhado pra ficar melhor a insercao
                    #printTransicaoRegra(infoTransicao),
                    for char in empilha:
                        if char != '&':
                            pilha.insert(0,char)
                    newTr = Transicao(estado, fita, pilha, indR, indT)
                    listaTransicoes.append(newTr)
                    print "p dep -->",pilha
                    printTransicoes()
                    LAST_TR_VALIDA = True
                    PROX_TR = 0
                    input("NTerm")
                    break
                else:
                    #topo da pilha é um terminal
                    #verificar se o inicio da fita é igual ao topo da pilha
                    if nomeRegra == fita[0]: #inicio fita == topoPilha
                        print "\n### REDUCAO ###"
                        #fazer reducao
                        #remover inicio da fita e topo da pilha
                        estado = infoTransicao._estado
                        empilha = infoTransicao._empilha
                        empilha = empilha[::-1] #inverter o que vai ser empilhado pra ficar melhor a insercao
                        print "p ant -->",pilha,
                        pilha = pilha[1:]
                        print "f ant -->", fita,
                        fita = fita[1:]
                        for char in empilha:
                            if char != '&':
                                pilha.insert(0,char)
                        newTr = Transicao(estado,fita,pilha,indR,indT)
                        listaTransicoes.append(newTr)
                        print "p dep -->",pilha,
                        print "f dep -->",fita
                        printTransicoes()
                        LAST_TR_VALIDA = True
                        PROX_TR = 0
                        input("Term")
                        break
                    else: #topo pilha e inicio fita TERMINAIS mas DIFERENTES
                        print "\n\n ### topo pilha inicio fita nao batem ### \n\n"
                        if indT < len(regras[indR]._transicoes)-1:
                            #se tiver ainda transicoes nessa regra --> FAZ
                            continue
                        else:
                            #print "Ramo errado"
                            listaTransicoes.pop()
                            #seta flag e desfaz ultima transicao
                            LAST_TR_VALIDA = False
                            break
        else:
            #ultima transicao é invalida
            #remover a ultima transicao
            #printTransicoes()

            regra = listaTransicoes[len(listaTransicoes)-1]._regra
            transicao = listaTransicoes[len(listaTransicoes)-1]._transicao

            if transicao < len(regras[regra]._transicoes)-1:
                #tem transicao pra fazer ainda
                #seta um valor para PROX_TR e faz de novo
                listaTransicoes.pop()
                #print "kk ", type(listaTransicoes[len(listaTransicoes)-1]._pilha)
                #print "kkk ",type(pilha)
                #input ("tipo pilhas")
                print "\n\n"
                print "tp pilha False --> ", type(pilha)
                print "tp pilha TR False --> ", type(listaTransicoes[len(listaTransicoes)-1]._pilha)
                pilha = listaTransicoes[len(listaTransicoes)-1]._pilha
                fita = listaTransicoes[len(listaTransicoes)-1]._fita
                PROX_TR = transicao+1
                LAST_TR_VALIDA = True
            else:
                # nao tem mais transicoes
                listaTransicoes.pop()
                pilha = listaTransicoes[len(listaTransicoes)-1]._pilha
                fita = listaTransicoes[len(listaTransicoes)-1]._fita
                PROX_TR = 0
                LAST_TR_VALIDA = False

try:
    arquivoFita = sys.argv[1]
    arquivoRegras = sys.argv[2]
except:
    print ("Erro nos parametros")
    sys.exit()

if(os.path.exists(arquivoFita)):
    if(os.path.exists(arquivoRegras)):
        readRegras(arquivoRegras)
        readFita(arquivoFita)
        terminals.sort()
        noTerminals.sort()
        regraInicial = Regra(regras[0]._estado, regras[0]._removeFita, regras[0]._removePilha, regras[0]._transicoes)
        #assumindo que a primeira regra é sempre o estado inicial
        pilha.append(regraInicial._removePilha)
        #for regra in regras:
        #    print type(regra._estado),
        #    print type(regra._removeFita),
        #    print type(regra._removePilha),
        #    for transicao in regra._transicoes:
        #        print type(transicao._estado),
        #        print type(transicao._empilha),
        #    print "\n"

        estadoInicial = regraInicial._estado
        primeiraTransicao = Transicao(estadoInicial,fita,pilha,-1,-1)
        listaTransicoes.append(primeiraTransicao)
        explosaoDeEstados(pilha,fita)

    else:
        print ("arquivo com as regras nao existe")
        sys.exit()
else:
    print ("arquivo de entrada nao existe")
    sys.exit()
