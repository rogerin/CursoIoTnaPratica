import network
import time

def conectar_wifi(ssid, senha):
    estacao = network.WLAN(network.STA_IF)  # Cria uma interface de estação

    if not estacao.isconnected():  # Verifica se já está conectado
        estacao.active(True)  # Ativa a interface de estação
        estacao.connect(ssid, senha)  # Tenta conectar à rede
        print('Conectando à rede', ssid)

        # Espera até que a conexão seja estabelecida
        while not estacao.isconnected():
            time.sleep(1)

    # Imprime o endereço IP se conectado
    print('Conexão estabelecida:', estacao.ifconfig())

# Substitua 'nome_da_rede' e 'senha_da_rede' pelos seus dados de Wi-Fi
conectar_wifi('nome_da_rede', 'senha_da_rede')


