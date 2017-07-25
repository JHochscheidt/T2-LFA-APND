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

LAST_TR_VALIDA = True
proxima_transicao = 0


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
    global LAST_TR_VALIDA
    global proxima_transicao


    firstTr = listaTransicoes[len(listaTransicoes)-1]
    topoPilha = listaTransicoes[len(listaTransicoes)-1]._pilha
    indR = buscaRegra(topoPilha)


    while len(pilha) > 0 or len(fita) > 0 or len(listaTransicoes) > 0:

        if listaTransicoes == 0:
            print "\n ### ---Sentença inválida --- ###\n"
            printTransicoes()
            return

        if LAST_TR_VALIDA == True:
            #pegar a ultima transicao
            lastTr = listaTransicoes[len(listaTransicoes)-1]
            if len(lastTr._pilha) == 0:
                #pilha vazia
                if len(fita) == 0:
                    print "\n ### ---SENTENÇA VÁLIDA --- ###\n"
                    printTransicoes()
                    return
                else:
                    print "\n ### ---SENTENÇA INVÁLIDA --- ###\n"
                    printTransicoes()
                    return

            topoPilha = lastTr._pilha[0]

            #indice da regra
            indR = buscaRegra(topoPilha)

            #para cada transicao da regra
            for indT in range(proxima_transicao, len(regras[indR]._transicoes)):
                #se topo da pilha é terminal

                #TERMINAL
                if topoPilha in terminals:
                    #verifica se é igual ao inicio da fita
                    #se sim faz REDUCAO
                    #se nao, busca por proximo transicao possivel
                    if len(fita) == 0:
                        if len(pilha) != 0:
                            listaTransicoes.pop()
                            pilha = listaTransicoes[len(listaTransicoes)-1]._pilha
                            fita = listaTransicoes[len(listaTransicoes)-1]._fita
                            proxima_transicao = 0
                            LAST_TR_VALIDA = False
                        else:
                            print "\n ### ---SENTENÇA VÁLIDA --- ###\n"
                            printTransicoes()
                            return
                    elif topoPilha == fita[0]:
                        #topoPilha e inicia fita IGUAISs

                        #fazer reducao
                        fita = fita[1:]
                        pilha = pilha[1:]
                        estado = regras[indR]._transicoes[indT]._estado
                        newTr = Transicao(estado, fita, pilha, indR, indT)
                        listaTransicoes.append(newTr)
                        #printTransicoes()
                        proxima_transicao = 0
                        LAST_TR_VALIDA = True
                        break
                    elif topoPilha != fita[0]:
                        #topo pilha e inicio fita DIFERENTES
                        last_regra = listaTransicoes[len(listaTransicoes)-1]._regra
                        last_transicao = listaTransicoes[len(listaTransicoes)-1]._transicao

                        #se o estado anterior ainda possui transicoes possiveis
                        if last_transicao < (len(regras[int(last_regra)]._transicoes)-1):
                            if len(listaTransicoes) == 0:
                                print "\n ### ---SENTENÇA INVÁLIDA --- ###\n"
                                printTransicoes()
                                return
                            listaTransicoes.pop()
                            pilha = listaTransicoes[len(listaTransicoes)-1]._pilha
                            fita = listaTransicoes[len(listaTransicoes)-1]._fita
                            proxima_transicao = last_transicao + 1
                            LAST_TR_VALIDA = True
                            continue
                        else:
                            listaTransicoes.pop()
                            pilha = listaTransicoes[len(listaTransicoes)-1]._pilha
                            fita = listaTransicoes[len(listaTransicoes)-1]._fita
                            proxima_transicao = 0
                            LAST_TR_VALIDA = False
                            break

                #NAO TERMINAL
                elif topoPilha in noTerminals:
                    #faz SUBSTITUICAO
                    pilha = pilha[1:]
                    estado = regras[indR]._transicoes[indT]._estado
                    empilha = regras[indR]._transicoes[indT]._empilha
                    #print empilha
                    empilha = empilha[::-1]
                    #print empilha
                    for char in empilha:
                        if char != '&':
                            pilha.insert(0,char)
                    newTr = Transicao(estado, fita, pilha, indR, indT)
                    listaTransicoes.append(newTr)
                    #printTransicoes()
                    LAST_TR_VALIDA = True
                    proxima_transicao = 0
                    break
        elif LAST_TR_VALIDA == False:
            # significa que a ultima transicao foi removida
            # porque nao haviam mais transicoes possiveis naquela regra
            last_regra = listaTransicoes[len(listaTransicoes)-1]._regra
            last_transicao = listaTransicoes[len(listaTransicoes)-1]._transicao
            if last_transicao < (len(regras[last_regra]._transicoes)-1):
                listaTransicoes.pop()
                if len(listaTransicoes) == 0:
                    print "\n ### ---SENTENÇA INVÁLIDA --- ###\n"
                    printTransicoes()
                    return
                pilha = listaTransicoes[len(listaTransicoes)-1]._pilha
                fita = listaTransicoes[len(listaTransicoes)-1]._fita
                proxima_transicao = last_transicao + 1
                LAST_TR_VALIDA = True
            else:
                #print "nao sei"
                listaTransicoes.pop()
                pilha = listaTransicoes[len(listaTransicoes)-1]._pilha
                fita = listaTransicoes[len(listaTransicoes)-1]._fita
                proxima_transicao = 0
                LAST_TR_VALIDA = False


try:
    arquivoFita = sys.argv[1]
    arquivoRegras = sys.argv[2]
except:
    print ("Erro nos parametros. Os parametros para execucao são: ")
    print ("python <arquivo_executavel.py> <arquivo_com_sentenca.txt> <arquivo_com_regras.txt>" )
    sys.exit()

if(os.path.exists(arquivoFita)):
    if(os.path.exists(arquivoRegras)):
        readRegras(arquivoRegras)
        readFita(arquivoFita)
        entrada = ''
        for char in fita:
            entrada+=char

        terminals.sort()
        noTerminals.sort()
        regraInicial = Regra(regras[0]._estado, regras[0]._removeFita, regras[0]._removePilha, regras[0]._transicoes)
        #assumindo que a primeira regra é sempre o estado inicial
        pilha.append(regraInicial._removePilha)
        #or regra in regras:
        #    print type(regra._estado),
        #    print type(regra._removeFita),
        #    print type(regra._removePilha),
        #    for transicao in regra._transicoes:
        #        print type(transicao._estado),
        #        print type(transicao._empilha),
        #    print "\n"
        #printRegras()
        #print terminals
        #print noTerminals
        estadoInicial = regraInicial._estado
        primeiraTransicao = Transicao(estadoInicial,fita,pilha,-1,-1)
        listaTransicoes.append(primeiraTransicao)
        explosaoDeEstados(pilha,fita)

        print "Entrada --> [", entrada, "]"

    else:
        print ("arquivo com as regras nao existe")
        sys.exit()
else:
    print ("arquivo de entrada nao existe")
    sys.exit()
