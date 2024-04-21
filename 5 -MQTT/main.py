import os
import time
import ujson
import machine
import network
from umqtt.simple import MQTTClient
import utime

import urandom

# Digite seu SSID wifi e senha abaixo.
wifi_ssid = "Cariri"
wifi_password = "0987654321"

# Insira seu endpoint do AWS IoT. Você pode encontrá-lo na página Configurações do
# seu console do AWS IoT Core.
# https://docs.aws.amazon.com/iot/latest/developerguide/iot-connect-devices.html
aws_endpoint = b'a22wgjycrazooz-ats.iot.us-east-1.amazonaws.com'

# nomes que vamos definir para o nosso dispositivo e cliente.
thing_name = "ccThing"
client_id = "ccThing01"
private_key = "cert/ClimaControl.private.key"
private_cert = "cert/ClimaControl.cert.pem"

# ler a chave privada e o certificado do arquivo para autenticação na AWS IoT.
with open(private_key, 'r') as f:
    key = f.read()
with open(private_cert, 'r') as f:
    cert = f.read()

topic_pub = "climacontrol/device"
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

    mesg = ujson.dumps({
        "datachave": "1",
        "temperatura": urandom.randint(0, 100),
        "umidade": urandom.randint(0, 100),
        "time": utime.time()
        
    })

    # Using the message above, the device shadow is updated.
    try:
        mqtt_publish(client=mqtt, message=mesg)
    except:
        print("Erro ao publica rmensagem.")

#Wait for 10 seconds before checking for messages and publishing a new update.
    print("Aguarde 5 segundos")
    time.sleep(5)