import os
import time
import ujson
import machine
import network
from umqtt.simple import MQTTClient

import dht 



import random



sensor = dht.DHT22(machine.Pin(14))

def gerar_float_aleatorio(minimo, maximo):
    return random.uniform(minimo, maximo)

# Exemplo de uso

# Digite seu SSID wifi e senha abaixo.
wifi_ssid = "--"
wifi_password = "--"

# Insira seu endpoint do AWS IoT. Você pode encontrá-lo na página Configurações do
# seu console do AWS IoT Core.
# https://docs.aws.amazon.com/iot/latest/developerguide/iot-connect-devices.html
aws_endpoint = b'----.iot.us-east-1.amazonaws.com'
                 
# nomes que vamos definir para o nosso dispositivo e cliente.
thing_name = "ccThing"
client_id = "ccThing01"
private_key = "cert/--.private.key"
private_cert = "cert/--.cert.pem"

# ler a chave privada e o certificado do arquivo para autenticação na AWS IoT.
with open(private_key, 'r') as f:
    key = f.read()
with open(private_cert, 'r') as f:
    cert = f.read()

topic_pub = "sensor/climao"
# topic_sub = "topic/sub"

ssl_params = {"key":key, "cert":cert, "server_side":False}

# Define pins for LED and light sensor. In this example we are using a FeatherS2.
#The sensor and LED are built into the board, and no external connections are required.
light_sensor = machine.ADC(machine.Pin(2))
led = machine.Pin(13, machine.Pin.OUT)
info = os.uname()

#Connect to the wireless network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to network...')
    wlan.connect(wifi_ssid, wifi_password)
    while not wlan.isconnected():
        pass

    print('Connection successful')
    print('Network config:', wlan.ifconfig())

def mqtt_connect(client=client_id, endpoint=aws_endpoint, sslp=ssl_params):
    mqtt = MQTTClient(client_id=client, server=endpoint, port=8883, keepalive=1200, ssl=True, ssl_params=sslp)
    print("Connecting to AWS IoT...")
    mqtt.connect()
    print("Done")
    return mqtt

def mqtt_publish(client, topic=topic_pub, message=''):
    print("Publishing message...")
    client.publish(topic, message)
    print(message)

def mqtt_subscribe(topic, msg):
    print("Message received...")
    message = ujson.loads(msg)
    print(topic, message)
    if message['state']['led']:
        led_state(message)
    print("Done")

def led_state(message):
    led.value(message['state']['led']['onboard'])

#We use our helper function to connect to AWS IoT Core.
#The callback function mqtt_subscribe is what will be called if we 
#get a new message on topic_sub.
try:
    mqtt = mqtt_connect()
    mqtt.set_callback(mqtt_subscribe)
    # mqtt.subscribe(topic_sub)
except:
    print("Unable to connect to MQTT.")


while True:
#Check for messages.
    try:
        mqtt.check_msg()
    except:
        print("Unable to check for messages.")

    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    
    numero_aleatorio1 = gerar_float_aleatorio(1.1, 50.5)
    numero_aleatorio2 = gerar_float_aleatorio(1.1, 30.5)

    mesg = ujson.dumps({
        "temperatura": temp,
        "umidade": hum,
    })

    # Using the message above, the device shadow is updated.
    try:
        mqtt_publish(client=mqtt, message=mesg)
    except:
        print("Erro ao publica rmensagem.")

#Wait for 10 seconds before checking for messages and publishing a new update.
    print("Aguarde 5 segundos")
    time.sleep(5)