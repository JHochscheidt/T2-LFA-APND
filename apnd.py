# coding: utf-8
import sys
import os
import string





class Regra(object):
    def __init__(self, estado, fita, pilha, transicoes):
        self._estado = estado
        self._removeFita = fita
        self._removePilha = pilha
        self._transicoes = transicoes


class Transicao(object):
    def __init__(self, estado, empilha):
        self._estado = estado
        self._empilha = empilha


regras = [] #vetor com as regras
fita = []
pilha = []
saida = []
terminals = []
noTerminals = []
PILHA_VAZIA_FITA_NAO = -1
FITA_VAZIA_PILHA_NAO = -2
CONTINUA = -3
ESTADO_PILHA_FITA = 0
def readFita(arquivoFita):
    file = open(arquivoFita, 'r')
    fitaTemp = file.readlines()
    file.close()
    for linha in fitaTemp:
        linha = linha.replace("\n", "")
        linha = linha.replace(" ", "")
        #print type(linha)
        #print linha
        for c in linha:
            #print c
            fita.append(c)
    #print fita


def readRegras(arquivoRegras):
    file = open(arquivoRegras, 'r')
    arq_regras = file.readlines()
    file.close()
    for linha in arq_regras:
        #print linha
        linha = linha.replace(" ","")

        ## quebra a linha em 2 partes
        ## primeira parte é a readRegras
        ## segunda parte sao as transicoes
        linha = linha.split('=')
        #print linha

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
        #print "estado -->", estado
        removeDaFita = regra[1]
        removeDaPilha = regra[2]
        removeDaPilha = removeDaPilha[0:-1] # remove ")" do do final da regra
        #print "remove Pilha -->", removeDaPilha
        #print ("regra --> " + str(regra))

        transicoes = linha[1]
        #print ("transicoes --> " + str(transicoes))

        #primeiro remove \n
        transicoes = transicoes.replace("\n", "")
        #print transicoes
        #remove os chaves das transicoes
        transicoes = transicoes.replace("{","")
        transicoes = transicoes.replace("}","")
        transicoes = transicoes.replace(">","")
        transicoes = transicoes.replace("<","")
        ## regra possui campos separados por virgula e parentes "),(", entao faz split
        transicoes = transicoes.split("),(")
        ## remover "(" da primeira transicao

        #print ("transicoes --> " + str(transicoes))
        #print ("Len " + str(len(transicoes)))
        #print transicoes
        transicoesTemp = []
        for indice in range(0, len(transicoes)):
            # se for a primeira transicao, remover os parenteses sobrando
            transicaoTemp = transicoes[indice]
            #print "TTT ", transicaoTemp
            if indice == 0:
                #print "before ", transicoes[indice]
                transicaoTemp = transicoes[indice]
                #so tem 1 transicao
                if len(transicoes) == 1:
                    transicaoTemp = transicaoTemp[1:-1]
                else:
                    transicaoTemp = transicaoTemp[1:]
                #print "after ", transicaoTemp
                #transicoes[indice] = transicaoTemp
            #se for a ultima transicao remover os parenteses sobrando
            elif indice == len(transicoes)-1:
                #print "before ", transicoes[indice]
                transicaoTemp = transicoes[indice]
                transicaoTemp = transicaoTemp[0:-1]
                #print "after ", transicaoTemp
                #transicoes[indice] = transicaoTemp

            # fim for de cada transicao


            #split pra pegar o estado e o que vai ser empilhado
            transicaoTemp = transicaoTemp.split(',')
            #print "temporaria cacete ", transicaoTemp

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

            #print "t ", terminalsprint "nt ", noTerminals
            transicoes[indice] = transicaoTemp
            transicaoTemp[1] = empilha
            #print "kkk ", transicoes[indice]
            #adicionar essas informacoes no vetor temporario de transicoes
            transicoesTemp.append([transicaoTemp[0], transicaoTemp[1]])
        #aqui ja pode adicionar a regra e suas transicoes
        regras.append(Regra(estado, removeDaFita, removeDaPilha, transicoesTemp))
        #print "after () --> ", transicoes
        #print "temp trans --> ", transicoesTemp

    #fim do for pra cada regra (cada linha do arquivo)
    #for regra in regras:
    #    print "estado -->", regra._estado
    #    print "remFita -->", regra._removeFita
    #    print "remPilha -->", regra._removePilha
    #    print "transicoes -->", regra._transicoes

# busca regra pelo que ta no topo da pilha
def buscaRegra(topoPilha): #estado atual tem uma tripla Ex. (0,&,E)
    for indice in range(0, len(regras)):
        if regras[indice]._removePilha == topoPilha:
            return indice
    return -1

def removeDaFita(caractere, fitaTemp):
    #print "ch-->[", caractere, "]"
    #print "fita[0][", fitaTemp[0], "]"
    #print "fita[1][", fitaTemp[1], "]"
    #print "fita-->[", fitaTemp, "]"

    #cu = input("kkk")
    if caractere != '&':
        if caractere == fitaTemp[0]:
            print "beforeF[", fitaTemp, "]"
            fitaTemp = fitaTemp[1:]
            print "afterF[", fitaTemp, "]"
            return fitaTemp
        else:
            #print "caracteres nao batem"
            print "sentenca invalida"
            return False
            #sys.exit()
            #print caractere, " ", fitaTemp[0][0]
    #print "teste ", fitaTemp
    return fitaTemp

def removeDaPilha(caractere, pilhaTemp):
    #print "char ", caractere
    #print "cmp ", pilhaTemp[len(pilhaTemp)-1]
    if caractere != '&':
        if caractere == pilhaTemp[len(pilhaTemp)-1]:
            print "beforeP[", pilhaTemp, "]"
            pilhaTemp = pilhaTemp[0:-1]
            print "afterP[", pilhaTemp, "]"
            return pilhaTemp
        else:
            print "topo da pilha nao bate"
            #print caractere, " ", pilhaTemp[len(pilhaTemp)-1]
            #sys.exit()
            return False

    return pilhaTemp


def explosaoDeEstados(regraInicial, pilhaTemp, fitaTemp):

    print regraInicial

    while len(fitaTemp) > 0 or len(pilhaTemp) > 0:




try:
    arquivoFita = sys.argv[1]
    arquivoRegras = sys.argv[2]
    #print arquivoFita
    #print arquivoRegras

except:
    print ("Erro nos parametros")
    sys.exit()



if(os.path.exists(arquivoFita)):
    if(os.path.exists(arquivoRegras)):
        readRegras(arquivoRegras)
        for regra in regras:
            print "estado -->", regra._estado
            print "remFita -->", regra._removeFita
            print "remPilha -->", regra._removePilha
            print "transicoes -->", regra._transicoes
        readFita(arquivoFita)
        #print str(fita)
        regraInicial = []
        regraInicial.append(regras[0]._estado)
        regraInicial.append(regras[0]._removeFita)
        regraInicial.append(regras[0]._removePilha)
        #pilha.append(regras[0]._removePilha)
        #print ('pilha --> ', pilha)
        #print ('fita --> ', fita)
        #print "est in ", estadoInicial
        #saida.append(regraInicial)
        #explosaoDeEstados(regraInicial, pilha, fita)
        #print "cu de rola"
        #print "after"
        #print ('pilha --> ', pilha)
        #print ('fita --> ', fita)
    else:
        print ("arquivo com as regras nao existe")
        sys.exit()
else:
    print ("arquivo de entrada nao existe")
    sys.exit()
