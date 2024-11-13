import sys
from typing import List, Tuple
from snippets.lab2 import address, local_ips, message
from snippets.lab3 import Client, Connection, Server


class TcpPeer:
    def __init__(self, port: int, peers: List[Tuple[str, int]], on_new_connection, on_peer_death):
        self.__clients = [Client(peer) for peer in peers]
        self.__server = Server(port, on_new_connection)
        self.__on_peer_death = on_peer_death

    def send_all(self, message):
        died_peers = []
        for client in self.__clients:
            try:
                client.send(message)
            except BrokenPipeError:
                died_peers.append(client)
        for died_peer in died_peers:
            self.__on_peer_death(died_peer)
            self.__clients.remove(died_peer)
        

    def close(self):
        for client in self.__clients:
            client.close()
        self.__server.close()
        

if __name__ == "__main__":
    port = int(sys.argv[1])
    peers_addresses = [address(peer) for peer in sys.argv[2:]]

    def on_message_received(event, payload, connection: Connection, error):
        match event:
            case 'message':
                print(payload)
            case 'error':
                print(error)

    def on_new_connection(event, connection, address, error):
        match event:
            case 'listen':
                print(f"Server listening on port {address[0]} at {', '.join(local_ips())}")
            case 'connect':
                print(f"Open ingoing connection from: {address}")
                connection.callback = on_message_received
            case 'stop':
                print(f"Stop listening for new connections")
            case 'error':
                print(error)

    def on_peer_death(client: Client):
        print(f"Connection with peer {client.remote_address} closed")

    username = input('Enter your username to start the chat:\n')
    print('Type your message and press Enter to send it. Messages from other peers will be displayed below.')
    peer = TcpPeer(port, peers_addresses, on_new_connection, on_peer_death)

    while True:
        try:
            content = input()
            peer.send_all(message(content, username))
        except (EOFError, KeyboardInterrupt):
            peer.close()
            break
