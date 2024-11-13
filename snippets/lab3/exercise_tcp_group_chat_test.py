from time import sleep
from snippets.lab2 import address
from snippets.lab3.exercise_tcp_group_chat import TcpPeer


listenings = 0
connections = 0
messages = 0

def on_new_connection(event, connection, address, error):
    global listenings, connections
    match event:
        case 'listen':
            assert address[1] == 8080
            listenings += 1
        case 'connect':
            connection.callback = on_message_received
            connections += 1
        case 'error':
            raise error

def on_message_received(event, payload, connection, error):
    global messages
    match event:
        case 'message':
            assert payload == "hello"
            messages += 1
        case 'error':
            raise error

p1 = TcpPeer(8080, [], on_new_connection, on_peer_death=lambda *_: None)
p2 = TcpPeer(8081, [address(port=8080)], lambda *_: None, lambda *_: None)
p2.send_all("hello")
sleep(1)
assert listenings == 1
assert connections == 1
assert messages == 1
