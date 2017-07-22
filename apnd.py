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
#fita vai ser um list com um quadrupla
#cada posicao sera do tipo [estado, fita, Pilha, (int) transicao aplicada]
listaTransicoes = []
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
        for c in linha:
            fita.append(c)

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
        #remove os chaves das transicoes
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
            transicoes[indice] = transicaoTemp
            transicaoTemp[1] = empilha
            #adicionar essas informacoes no vetor temporario de transicoes
            transicoesTemp.append([transicaoTemp[0], transicaoTemp[1]])
        #aqui ja pode adicionar a regra e suas transicoes
        regras.append(Regra(estado, removeDaFita, removeDaPilha, transicoesTemp))
    #fim do for pra cada regra (cada linha do arquivo)

# busca regra pelo que ta no topo da pilha
def buscaRegra(topoPilha): #estado atual tem uma tripla Ex. (0,&,E)
    for indice in range(0, len(regras)):
        if regras[indice]._removePilha == topoPilha:
            return indice
    return -1

def aplicaTransicao(nomeRegra, indiceTr):
    indice = buscaRegra(nomeRegra)

    if indice < 0:
        print "regra nao existe indice < 0"
        sys.exit()

    # nomeRegra é nao terminal
    if nomeRegra not in string.lowercase:
        #aplica substituicao
        # nao mexe na fita
        # altera a pilha
        #faz substituicao
        pilhaTemp = pilhaTemp[1:]
        empilha = regras[indice]._transicoes[indiceTr][1]
        #print "empilha ", empilha
        listaTransicoes.append([fitaTemp,empilha,indiceTr])
        pilhaTemp = empilha + pilhaTemp
        #print "[", pilhaTemp, "]"
        return True
    else: # nomeRegra é terminal
        if nomeRegra == fita[0]:
            # terminais iguais
            # remove inicio fita
            #remove topo pilha
            pilhaTemp = pilhaTemp[1:]
            fitaTemp = fitaTemp[1:]
            listaTransicoes.append([fitaTemp,pilhaTemp,indiceTr])
            return True
        else:
            #terminais diferentes
            return False
            #print "remove transicao, terminais diferentes"


def explosaoDeEstados(pilha, fita):
    #input("explosa jajabum")

    if len(pilha) < 1 or len(fita) < 1:
        if len(pilha) ==0 and len(fita) == 0:
            print "sentença valida"
            sys.exit()
        else:
            print "sentença invalida"
            sys.exit()


    #print "p ",pilha, "\n"
    #print "f ",fita, "\n"
    pilhaTemp = pilha
    fitaTemp = fita

    #print "pT ",pilhaTemp, "\n"
    #print "fT ",fitaTemp, "\n"

    #topoPilha = pilha[len(pilha)-1]
    #indice = buscaRegra(topoPilha)

    print listaTransicoes

    #while len(fita) > 0 or len(pilha) > 0:
    #pilhaTemp = pilha
    #fitaTemp = fita
    lastTrans  = listaTransicoes[len(listaTransicoes)-1]
    #print lastTrans
    nomeRegra = lastTrans[1][0]
    print "nRegra ", nomeRegra
    #print "pt ",pilhaTemp
    #print "fl ",fitaTemp
    indRegra = buscaRegra(nomeRegra)
    if indRegra < 0:
        print "regra nao existe sys out"
        sys.exit()
    for indice in range(0, len(regras[indRegra]._transicoes)):
        #input("k ")
        # nomeRegra é nao terminal
        if nomeRegra not in string.lowercase:
            #aplica substituicao
            # nao mexe na fita
            # altera a pilha
            #faz substituicao
            #print "pp e nenem ", pilhaTemp
            pilhaTemp = pilhaTemp[1:]
            #print "pp e nenem ", pilhaTemp
            empilha = regras[indRegra]._transicoes[indice][1]
            if empilha != '&':
                empilha = empilha[::-1]
                #print "empilha ", empilha
                #print "PTT ", pilhaTemp
                #input("PPT")
                for ind in range(0, len(empilha)):
                    #print "indice ", ind
                    pilhaTemp.insert(0,empilha[ind])
                #print "empilha ", empilha
                #print "PTT ", pilhaTemp
            listaTransicoes.append([fitaTemp,pilhaTemp,indice])


            #pilhaTemp = empilha + pilhaTemp
            #print "xxx[", pilhaTemp, "]"
            transValida = True
        else: # nomeRegra é terminal
            if nomeRegra == fita[0]:
                # terminais iguais
                # remove inicio fita
                #remove topo pilha
                pilhaTemp = pilhaTemp[1:]
                fitaTemp = fitaTemp[1:]
                listaTransicoes.append([fitaTemp,pilhaTemp,indice])
                transValida = True
            else:
                #terminais diferentes
                transValida = False
                #print "remove transicao, terminais diferentes"

        if transValida == False:
            if indice < (len(regras[indRegra]._transicoes)-1) :
                listaTransicoes.pop()
                fitaTemp = listaTransicoes[len(listaTransicoes)-1][0]
                pilhaTemp = listaTransicoes[len(listaTransicoes)-1][1]
                continue
            else:
                #desfaz a ultima transicao
                listaTransicoes.pop()
                fitaTemp = listaTransicoes[len(listaTransicoes)-1][0]
                pilhaTemp = listaTransicoes[len(listaTransicoes)-1][1]
                continue
                #explosaoDeEstados(pilhaTemp, fitaTemp)
                #return
        else:
            explosaoDeEstados(pilhaTemp, fitaTemp)
            continue



try:
    arquivoFita = sys.argv[1]
    arquivoRegras = sys.argv[2]
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

        regraInicial = []
        regraInicial.append(regras[0]._estado)
        regraInicial.append(regras[0]._removeFita)
        regraInicial.append(regras[0]._removePilha)
        #assumindo que a primeira regra é sempre o estado inicial
        pilha.append(regras[0]._removePilha)

        saida.append(regraInicial)
        listaTransicoes.append([fita, regraInicial[2],-1])
        explosaoDeEstados(pilha, fita)
        print listaTransicoes

    else:
        print ("arquivo com as regras nao existe")
        sys.exit()
else:
    print ("arquivo de entrada nao existe")
    sys.exit()
