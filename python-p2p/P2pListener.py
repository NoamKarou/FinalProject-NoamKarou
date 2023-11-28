import socket
import time
import atexit
import public_ip
import P2pNode
import threading
from protocol import protocol_read, protocol_write, Operations

HANDSHAKE_PHRASE = "rock and stone"


def verify_id(id):
    return True


class P2pListener:
    my_id: str
    addr: str
    server_socket: socket
    thread_handle: threading.Thread

    connected_nodes: dict[str, P2pNode.P2pNode]

    def __init__(self, port_num):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', port_num))
        self.server_socket = server_socket
        self.client_socket = client_socket

        my_ip = server_socket.getsockname()[0]
        self.my_id = f'{my_ip}:{port_num}'
        secondary_thread = threading.Thread(target=self.server_loop)
        secondary_thread.start()
        self.thread_handle = secondary_thread
        self.connected_nodes = dict()


    def connect(self, addr: (str, int)):
        print("trying to connect")
        self.client_socket.connect(addr)
        server = self.client_socket
        if self.client_handshake_protocol(server):
            print('client connected sucessfuly')
        else:
            print("connection failed")

    def server_loop(self):
        print("running the server loop")
        self.server_socket.listen()
        while True:
            client_socket, addr = self.server_socket.accept()
            print('accepted client')
            status, username = self.server_handshake_protocol(client_socket)
            if status:
                print("clients username: " + username)

                new_node = P2pNode.P2pNode(username, client_socket)
                self.connected_nodes[username] = new_node
                print('accepted client')
            else:
                print('did not accept client')



    '''
    ===================================
    --------HANDSHAKE PROTOCOL---------
    ===================================
     validates the user is the deliberately trying to connect to the network

    c2s - HANDSHAKE_PHRASE
    s2c - ok
    c2s  - MY_ID
    cs2 = ok
    '''

    def server_handshake_protocol(self, target_socket) -> (bool, str):
        '''
        the server side of the handshake between the server and the client
        func is called instantly after the socket is created
        :param target_socket: the socket with the client
        :return: true if the connection is valid, according to the protocol
                 and the user id is valid and was sent by the user
        '''

        try:
            #stage 1
            operation, data = protocol_read(target_socket)
            if operation != Operations.CONNECTION_ESTABLISHMENT or data['phrase'] != HANDSHAKE_PHRASE:
                return False, ""
            protocol_write(target_socket, {'status': "ok"}, Operations.CONNECTION_ESTABLISHMENT)
            # stage 2
            operation, data = protocol_read(target_socket)
            if operation != Operations.CONNECTION_ESTABLISHMENT or 'id' not in data:
                return False, ""

            client_id = data['id']

            if not verify_id(data['id']):
                return False, ""
            protocol_write(target_socket, {'status': "ok"}, Operations.CONNECTION_ESTABLISHMENT)
            print("server handshake success")
            print(client_id)
            return True, client_id

        except Exception as ex:
            print("Exception: ", end='')
            raise ex
            return False
    
    def client_handshake_protocol(self, target_socket):
        '''
        the client side of the handshake between the server and the client
        func is called instantly after the socket is created
        :param target_socket: the socket with the client
        :return: true if the connection is valid, according to the protocol
                 and the user id is valid and was sent by the user
        '''
        try:
            #stage 1
            protocol_write(target_socket, {'phrase': HANDSHAKE_PHRASE}, Operations.CONNECTION_ESTABLISHMENT)
            operation, data = protocol_read(target_socket)
            if operation != Operations.CONNECTION_ESTABLISHMENT or data['status'] != "ok":
                return False
            # stage 2
            protocol_write(target_socket, {'id': self.my_id}, Operations.CONNECTION_ESTABLISHMENT)
            operation, data = protocol_read(target_socket)
            if operation != Operations.CONNECTION_ESTABLISHMENT or data['status'] != "ok":
                return False
            print("client handshake success")
            return True

        except Exception as ex:
            print("Exception: ", end='')
            raise ex
            return False

    '''
    ===================================================
    -----------------BROADCASTING----------------------
    ===================================================
    '''
    '''The broadcast method used is flooding'''
    broadcasts = dict[str, time]

    def broadcast_to_all(self, dict_to_broadcast):
        try:
            for node in self.connected_nodes.values():
                protocol_write(node.socket, dict_to_broadcast, Operations.BROADCASTING)

        except Exception as ex:
            raise ex
            return False

    def broadcasting_callback(self, broadcasting_dict):
        try:
            broadcast_id = broadcasting_dict['id']
            if broadcast_id in broadcasting_dict:
                return False

            broadcasting_dict[broadcast_id] = broadcasting_dict

            for node in self.connected_nodes.values():
                protocol_write(node.socket, broadcasting_dict, Operations.BROADCASTING)

            broadcasted_operation = Operations(broadcasting_dict['operation'])

            match broadcasted_operation:
                case Operations.SEND_TEST_MESSAGE:
                    pass
                case _:
                    return

        except Exception as ex:
            print(ex)
            return False



