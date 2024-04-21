# main.py -- put your code here!
import machine
import time

# Define o pino GPIO 2 como saída
led = machine.Pin(2, machine.Pin.OUT)

def blink_led(tempo_intervalo):
    while True:
        # Liga o LED (0 para acender devido à lógica invertida em alguns dispositivos como o ESP8266)
        led.value(1)
        # Espera por um certo intervalo de tempo
        time.sleep(tempo_intervalo)
        
        # Desliga o LED
        led.value(0)
        # Espera pelo mesmo intervalo de tempo
        time.sleep(tempo_intervalo)

# Chama a função blink_led com um intervalo de 1 segundo
blink_led(0.5)
