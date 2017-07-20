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
fita = []
pilha = []

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
        transicoes = transicoes.replace("<","")
        transicoes = transicoes.replace(">","")
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

            # fim for de cada transicao

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
    print "ch-->[", caractere, "]"
    print "fita[0][", fitaTemp[0], "]"
    #print "fita[1][", fitaTemp[1], "]"
    print "fita-->[", fitaTemp, "]"

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
            sys.exit()
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
            #print "topo da pilha nao bate"
            #print caractere, " ", pilhaTemp[len(pilhaTemp)-1]
            sys.exit()
    return pilhaTemp


def explosaoDeEstados(estadoInicial, pilhaTemp, fitaTemp):
    print "\n\n"
    print "fitaTemp-->[", fitaTemp, "]"
    print "pilhaTemp-->[", pilhaTemp, "]"
    #pilhaTemporaria = pilhaTemp
    #print pilhaTemp
    #print pilhaTemporaria
    #fitaTemporaria = fitaTemp
    if len(pilhaTemp) == 0:
        if len(fitaTemp) == 0:
            print "reconhece cadeia"
            sys.exit()
        else:
            return PILHA_VAZIA_FITA_NAO
    else:
        if len(fitaTemp) == 0:
            return FITA_VAZIA_PILHA_NAO

    
    topoPilha = pilhaTemp[len(pilhaTemp)-1]
    print 'tp p-->', topoPilha
    #indice atual possui qual regra tem alguma transicao q remove o q tem no topo da pilha
    indiceRegraAtual = buscaRegra(topoPilha)
    if(indiceRegraAtual == -1):
        print ("transicao impossivel")
        sys.exit()

        regraAtual = regras[indiceRegraAtual]

        if regraAtual._removePilha == pilhaTemp[len(pilhaTemp)-1]:
            for transicao in regra._transicoes:
                #pilha vazia
                if len(pilhaTemp) == 0:
                    #fita vazia
                    if len(fitaTemp) == 0:
                        print "reconhece a cadeia"
                        sys.exit()
                    #fita nao vazia
                    else:
                        print "ainda ha coisas na fita"
                        ESTADO_PILHA_FITA = PILHA_VAZIA_FITA_NAO
                #pilha nao vazia
                else:
                    #fita vazia
                    if len(fitaTemp) == 0:
                        print "acabou fita e ainda ha coisas na pilha"
                        ESTADO_PILHA_FITA = FITA_VAZIA_PILHA_NAO
                    #fita nao vazia
                    else:
                        ESTADO_PILHA_FITA = CONTINUA

                if ESTADO_PILHA_FITA == CONTINUA:
                    print "removerFita--> [", regraAtual._removeFita, "]"
                    print "removerPilha--> [", regraAtual._removePilha, "]"
                    print "fita[0]-->[", fita[0],"]"
                    print "tpPP-->[", pilhaTemp[len(pilhaTemp)-1], "]"
                    if fitaTemp[0] == pilhaTemp[len(pilhaTemp)-1]:
                        fitaTemp = removeDaFita(regraAtual._removeFita, fitaTemp)
                        pilhaTemp = removeDaPilha(regraAtual._removePilha, pilhaTemp)
                    else:
                        pilhaTemp = removeDaPilha(regraAtual._removePilha, pilhaTemp)

                    #cu = input("kk")
                    #print cu
                    #print "f --> ", fitaTemporaria
                    #print "P --> ", pilhaTemporaria
                    empilhar = transicao[1] #transicao[1] é o que vai ser empilhado
                    print "empilhar--> [", empilhar, "]"
                    empilhar = empilhar[::-1]
                    for c in empilhar:
                        if c != '&':
                            pilhaTemp.append(c)

                    retorno = explosaoDeEstados(estadoInicial, pilhaTemp, fitaTemp)
                    if retorno == FITA_VAZIA_PILHA_NAO or retorno == PILHA_VAZIA_FITA_NAO:
                        #lembrar de reconstruir a pilha e fita
                        continue
                    else:
                        return CONTINUA
                else:
                    continue

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
        #for regra in regras:
        #    print "estado -->", regra._estado
        #    print "remFita -->", regra._removeFita
        #    print "remPilha -->", regra._removePilha
        #    print "transicoes -->", regra._transicoes
        readFita(arquivoFita)
        #print str(fita)
        estadoInicial = []
        estadoInicial.append(regras[0]._estado)
        estadoInicial.append(regras[0]._removeFita)
        estadoInicial.append(regras[0]._removePilha)
        pilha.append(regras[0]._removePilha)
        #print ('pilha --> ', pilha)
        #print ('fita --> ', fita)
        #print "est in ", estadoInicial
        explosaoDeEstados(estadoInicial, pilha, fita)
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
