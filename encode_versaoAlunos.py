
#importe as bibliotecas
from suaBibSignal import *
import sys
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

#funções a serem utilizadas
def generateSin(freq, time, fs):
    n = time*fs #numero de pontos
    x = np.linspace(0.0, time, n)  # eixo do tempo
    s = np.sin(freq*x*2*np.pi)
    plt.figure()
    plt.plot(x,s)
    return (x, s)
    
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando encoder")
    print("Aguardando usuário")

    signal = signalMeu()
    fs = freqDeAmostragem = 44100

    sd.default.samplerate = freqDeAmostragem #taxa de amostragem
    sd.default.channels = 2

    duration = 5  #tempo em segundos que ira emitir o sinal acustico 
      
    #relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3
    amplitude = 1.5

    print("Gerando Tons base")

    digits = {
    "1":[1209,697], "2":[1336,697], "3":[1477,697], "4":[1209,770], 
    "5":[1336,770], "6":[1477,770], "7":[1209,852], "8":[1336,852],
    "9":[1477,852], "0":[1336,941]
    }
    T = duration

    #deixe tudo como array
    t   = np.linspace(0,T/2,T*fs)
    y = t
    #printe a mensagem para o usuario teclar um numero de 0 a 9.
    digit = int(input("Escolha um número de 0 a 9:"))
    #nao aceite outro valor de entrada.
    while not 0 <= digit <= 9:
        print("Entrada inválida")
        digit = int(input("Escolha um número de 0 a 9:"))

    print("Gerando Tom referente ao símbolo : {}".format(digit))
    #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides
    valors = digits[str(digit)]
    y1 = np.sin(2*np.pi*valors[0]*t)
    y2 = np.sin(2*np.pi*valors[1]*t)    
    x = y1 + y2

    #printe o grafico no tempo do sinal a ser reproduzido
    plt.axis([0, 1e-2, -2.1, 2.1])
    plt.plot(y,x)
    # reproduz o som
    print("Reproduzindo Tom referente ao símbolo : {}".format(digit))
    tone = x*gainX
    print("Aguardando fim do audio")
    sd.play(tone, fs)
    sd.wait()
    print("Fim da reprodução")
    # Exibe gráficos
    plt.title("Sinal no tempo")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.show()

    # aguarda fim do audio
    sd.wait()
    
if __name__ == "__main__":
    main()