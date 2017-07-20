# coding: utf-8
import sys
import os

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
        #remove os parenteses da regra
        regra = regra.replace("(","")
        regra = regra.replace(")","")
        ## regra possui campos separados por virgula, entao faz split
        regra = regra.split(',')
        #regra[0] possui o estado
        #regra[1] possui o que sera removido da fita
        #regra[2] possui o que sera tirado do topo da pilha
        estado = regra[0]
        removeDaFita = regra[1]
        removeDaPilha = regra[2]
        #print ("regra --> " + str(regra))

        transicoes = linha[1]
        #print ("transicoes --> " + str(transicoes))

        #primeiro remove \n
        transicoes = transicoes.replace("\n", "")
        #print transicoes
        #remove os chaves das transicoes
        transicoes = transicoes.replace("{","")
        transicoes = transicoes.replace("}","")
        ## regra possui campos separados por virgula e parentes "),(", entao faz split
        transicoes = transicoes.split("),(")
        ## remover "(" da primeira transicao

        #print ("transicoes --> " + str(transicoes))
        #print ("Len " + str(len(transicoes)))

        transicoesTemp = []
        for indice in range(0, len(transicoes)):
            # se for a primeira transicao, remover os parenteses sobrando
            transicaoTemp = transicoes[indice]
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


            #split pra pegar o estado e o que vai ser empilhado
            transicaoTemp = transicaoTemp.split(',')
            #print transicaoTemp
            #transicaoTemp[0] tem o estado
            #transicaoTemp[1] tem o que vai ser empilhado
            transicoes[indice] = transicaoTemp
            #adicionar essas informacoes no vetor temporario de transicoes
            transicoesTemp.append([transicaoTemp[0], transicaoTemp[1]])

        #aqui ja pode adicionar a regra e suas transicoes
        regras.append(Regra(estado, removeDaFita, removeDaPilha, transicoesTemp))
        #print "after () --> ", transicoes
        #print "temp trans --> ", transicoesTemp

    for regra in regras:
        print "estado -->", regra._estado
        print "remFita -->", regra._removeFita
        print "remPilha -->", regra._removePilha
        print "transicoes -->", regra._transicoes













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
    else:
        print ("arquivo com as regras nao existe")
        sys.exit()
else:
    print ("arquivo de entrada nao existe")
    sys.exit()
