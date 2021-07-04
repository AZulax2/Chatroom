import socket
import os
import threading

host = ''
port = 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} nous a quitter!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connecter avec {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)

        print(f"Le pseudo est  {nickname}")
        broadcast(f"{nickname} est connecte au serveur !\n".encode("utf-8"))
        client.send('Connecter au serveur !\n'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server running !")
receive()
