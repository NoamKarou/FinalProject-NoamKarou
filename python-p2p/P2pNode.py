import socket

class P2pNode:
    node_id: str
    socket: socket.socket

    def __init__(self, addr, socket):
        self.node_id = addr
        self.socket = socket

