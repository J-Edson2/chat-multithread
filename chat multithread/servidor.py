import threading
import socket
from datetime import datetime

class Servidor:
    def __init__(self, host = '127.0.0.1', port = 55555):
        self.host = host  # O endereço IP do servidor
        self.port = port  # A porta que o servidor irá escutar
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um novo socket
        self.server.bind((self.host, self.port))  # Vincula o socket ao endereço e porta especificados
        self.server.listen()  # Coloca o servidor em modo de escuta para aceitar conexões de clientes
        self.clients = []  # Uma lista para armazenar todos os clientes conectados
        self.nicknames = []  # Uma lista para armazenar os nicks dos clientes

    def broadcast(self, message):
        for client in self.clients:  # Para cada cliente conectado
            client.send(message)  # Envia a mensagem para o cliente

    def handle(self, client):
        while True:  # Loop infinito para receber mensagens do cliente
            try:
                message = client.recv(1024).decode('utf-8')  # Recebe a mensagem do cliente
                if message == '/sair':  # Se a mensagem for '/sair'
                    index = self.clients.index(client)  # Obtém o índice do cliente na lista de clientes
                    self.clients.remove(client)  # Remove o cliente da lista de clientes
                    client.close()  # Fecha a conexão com o cliente
                    nickname = self.nicknames[index]  # Obtém o nick do cliente
                    self.nicknames.remove(nickname)  # Remove o nick da lista de apelidos
                    self.broadcast(f'{nickname} saiu do chat!'.encode('utf-8'))  # Informa aos outros clientes que este cliente saiu do chat
                    break
                print(f'{datetime.now()} - {message}')  # Imprime a mensagem no terminal do servidor com a data e hora atuais
                with open('registro.txt', 'a') as f:  # Abre o arquivo de registro em modo de anexação
                    f.write(f'{datetime.now()} - {message}\n')  # Escreve a mensagem no arquivo de registro com a data e hora atuais
                timestamped_message = f'{datetime.now()} - {message}'.encode('utf-8')  # Adiciona a data e hora à mensagem antes de enviá-la aos clientes
                self.broadcast(timestamped_message)  # Envia a mensagem para todos os clientes conectados
            except:  # Se ocorrer um erro (por exemplo, se o cliente desconectar)
                index = self.clients.index(client)  # Obtém o índice do cliente na lista de clientes
                self.clients.remove(client)  # Remove o cliente da lista de clientes
                client.close()  # Fecha a conexão com o cliente
                nickname = self.nicknames[index]  # Obtém o nick do cliente
                self.nicknames.remove(nickname)  # Remove o nick da lista de nicks
                self.broadcast(f'{nickname} saiu do chat!'.encode('utf-8'))  # Informa aos outros clientes que este cliente saiu do chat
                break

    def receive(self):
        while True:  # Loop infinito para aceitar conexões de novos clientes
            client, address = self.server.accept()  # Aceita uma nova conexão de um cliente
            print(f'Conectado com {str(address)}')  # Imprime o endereço IP do novo cliente

            client.send('NICK'.encode('ascii'))  # Solicita ao novo cliente que envie seu nickname
            nickname = client.recv(1024).decode('ascii')  # Recebe o nick do novo cliente
            self.nicknames.append(nickname)  # Adiciona o nick à lista de apelidos
            self.clients.append(client)  # Adiciona o novo cliente à lista de clientes

            print(f'Nickname do cliente é {nickname}!')  # Imprime o nickname do novo cliente no terminal do servidor
            self.broadcast(f'{nickname} entrou no chat!'.encode('ascii')) # Informa aos outros clientes que um novo cliente entrou no chat 
            client.send('Conectado ao servidor!'.encode('ascii'))  # Informa ao novo cliente que ele está conectado ao servidor

            thread = threading.Thread(target=self.handle, args=(client,))  # Cria um novo thread para lidar com a comunicação com este cliente
            thread.start()  # Inicia o novo thread

if __name__ == "__main__":
    servidor = Servidor()  # Cria um novo objeto Servidor
    servidor.receive()  # Começa a aceitar conexões de novos clientes
