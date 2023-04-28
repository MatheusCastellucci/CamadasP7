#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
import numpy as np
from numpy.lib.nanfunctions import nancumprod
import sounddevice as sd
import matplotlib as plt
import peakutils 
from suaBibSignal import *
import time as ZaWarudo
#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    signal= signalMeu()
    freqDeAmostragem = 44100
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = freqDeAmostragem #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = 4 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    print("Começa a gravar em 2 segundos")
    #ZaWarudo.sleep(2)
    #faca um print informando que a gravacao foi inicializada
    print("Começou a gravação")
    #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    duracao = 3
    numAmostras = freqDeAmostragem*duracao
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")
    print(audio)
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    inicio = 0
    fim = duracao
    numPontos = numAmostras
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.linspace(inicio,fim,numPontos)
    # plot do gravico  áudio vs tempo!
    plt.plot(t, audio)
    
    # Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias

    fs = freqDeAmostragem
    xf, yf = signal.calcFFT(audio[:,0], fs)
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.

   
    index = peakutils.indexes(yf,0.3,50)
    digits = {
    "1":[1209,697], "2":[1336,697], "3":[1477,697], "4":[1209,770], 
    "5":[1336,770], "6":[1477,852], "7":[1209,852], "8":[1336,852],
    "9":[1477,852], "0":[1336,941]
    }
    #printe os picos encontrados! 
    #print("index",index)
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    tolerancia = 10
    resposta = []
    for pico in index:
        print("Pico",xf[pico])
        if 1477-tolerancia <= xf[pico] <= 1477+tolerancia:
            resposta.append(1477)
        if 1336-tolerancia <= xf[pico] <= 1336+tolerancia:
            resposta.append(1336)
        if 1209-tolerancia <= xf[pico] <= 1209+tolerancia:
            resposta.append(1209)
        if 941-tolerancia <= xf[pico] <= 941+tolerancia:
            resposta.append(941)
        if 852-tolerancia <= xf[pico] <= 852+tolerancia:
            resposta.append(852)
        if 770-tolerancia <= xf[pico] <= 770+tolerancia:
            resposta.append(770)
        if 697-tolerancia <= xf[pico] <= 697+tolerancia:
            resposta.append(697)      
    for digit in digits:
        valor = digits[str(digit)]
        if valor[0] in resposta and valor[1] in resposta:
            print(digit)
    ## Exibe gráficos
    print(resposta)
    plt.show()

if __name__ == "__main__":
    main()