import socket
import threading


class P2pNode:
    node_id: str
    socket: socket.socket
    thread_handle: threading

    def __init__(self, addr, socket_):
        self.node_id = addr
        self.socket = socket_

