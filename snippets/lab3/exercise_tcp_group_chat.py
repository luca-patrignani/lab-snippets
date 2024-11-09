import sys
from snippets.lab2 import address, local_ips, message
from snippets.lab3 import Client, Connection, Server


clients = [Client(address(peer)) for peer in sys.argv[2:]]

port = int(sys.argv[1])

def on_message_received(event, payload, connection: Connection, error):
    match event:
        case 'message':
            print(payload)
        case 'close':
            print(f"Connection with peer {connection.remote_address} closed")
            global remote_peer; remote_peer = None
        case 'error':
            print(error)

def on_new_connection(event, connection, address, error):
    match event:
        case 'listen':
            print(f"Server listening on port {address[0]} at {', '.join(local_ips())}")
        case 'connect':
            print(f"Open ingoing connection from: {address}")
            connection.callback = on_message_received
            global remote_peer; remote_peer = connection
        case 'stop':
            print(f"Stop listening for new connections")
        case 'error':
            print(error)

server = Server(port, on_new_connection)

username = input('Enter your username to start the chat:\n')
print('Type your message and press Enter to send it. Messages from other peers will be displayed below.')
while True:
    try:
        content = input()
        for client in clients:
            client.send(message(text=content, sender=username))
    except (EOFError, KeyboardInterrupt):
        for client in clients:
            client.close()
        server.close()
        break
