# main.py -- put your code here!from machine import ADC, Pin
from machine import ADC, Pin
import time

# Configura os pinos D14 e D2 como entradas analógicas

adc_d2 = ADC(Pin(2))
adc_d15 = ADC(Pin(15))

while True:
    # Lê os valores dos ADCs

    valor_d15 = adc_d15.read()

    # Imprime o valor do pino D2 na saída serial
    # print("Valor no pino D2:", valor_d2)
    # print("Valor no pino D15:", valor_d15)

    if valor_d15 < 700:
        print("Esta chovendo!!:", valor_d15)
        
    # Delay para não sobrecarregar a saída serial
    time.sleep(1)