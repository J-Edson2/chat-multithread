import socket 
import threading
from datetime import datetime

server_host = input("Escolha a rede: ")  # Solicita ao usuário que insira um nick
nickname = input("Escolha um nickname: ")  # Solicita ao usuário que insira um nick

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um novo socket
client.connect((server_host, 55555))  # Conecta-se ao servidor

def receive():
    while True:  # Loop infinito para receber mensagens do servidor
        try:
            message = client.recv(1024).decode('utf-8') # Recebe a mensagem do servidor
            if message == 'NICK':  # Se a mensagem for 'NICK'
                client.send(nickname.encode('utf-8'))  # Envia o apelido para o servidor
            else:
                print(message)  # Imprime a mensagem no terminal do cliente
        except:  # Se ocorrer um erro (por exemplo, se o servidor desconectar)
            print("Conexão encerrada!")  # Imprime uma mensagem informando que a conexão foi encerrada
            break

def write():
    while True:  # Loop infinito para enviar mensagens para o servidor
        message = f'{input("")}'  # Solicita ao usuário que insira uma mensagem
        if message.lower() == '/sair':  # Se a mensagem for '/sair'
            client.send(message.encode('utf-8'))  # Envia a mensagem para o servidor
            client.close()  # Fecha a conexão com o servidor
            break
        client.send(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - {nickname}:  {message}'.encode('utf-8'))  # Envia a mensagem para o servidor com o nick do cliente

receive_thread = threading.Thread(target=receive)  # Cria um novo thread para receber mensagens do servidor
receive_thread.start()  # Inicia o thread de recebimento

write_thread = threading.Thread(target=write)  # Cria um novo thread para enviar mensagens para o servidor
write_thread.start()  # Inicia o thread de escrita
