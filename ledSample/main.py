# codigo 1
# import machine
# import time

# led_pin = machine.Pin(2, machine.Pin.OUT)

# while True:
#     led_pin.on()
#     time.sleep(1)
#     led_pin.off()
#     time.sleep(1)


#codigo 2
# from machine import Pin
# from time import sleep

# led = Pin(4, Pin.OUT)
# button = Pin(5, Pin.IN)

# while True:
#     valorBtn = button.value()
#     led.value(valorBtn)
   


# # codigo 3
# from machine import Pin
# from time import sleep
# import dht

# sensor = dht.DHT22(Pin(2))

# while True:
#     try:
#         sleep(2)
#         sensor.measure()
#         temp = sensor.temperature()
#         hum = sensor.humidity()
#         print('Temperatura: {}C'.format(temp))
#         print('Humidade: {}%'.format(hum))
        
#     except OSError as e:
#         print('Erro no leitor do sensor')


import network 
import time

def conectar_wifi(ssid, senha):
    estacao = network.WLAN(network.STA_IF)

    if not estacao.isconnected():
        print('Conectando na rede...')
        estacao.active(True)
        estacao.connect(ssid, senha)

        while not estacao.isconnected():
            print('tentando... 1s de espera')
            time.sleep(1)

    print('Conectado com sucesso')


conectar_wifi('---', '----')