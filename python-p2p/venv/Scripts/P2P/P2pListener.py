import socket
import time
from Scripts.P2P import P2pNode
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

    broadcast_callback: callable
    direct_operation_callback: callable
    returning_operations_callback: callable
    connected_nodes: dict[str, P2pNode.P2pNode]
    mutex: threading.Lock
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
        self.mutex = threading.Lock()

    def connect(self, addr: (str, int)):
        print("trying to connect")
        self.client_socket.connect(addr)
        server = self.client_socket
        status, name = self.client_handshake_protocol(server)
        if status:
            new_node = P2pNode.P2pNode(name, self.client_socket)
            self.connected_nodes[name] = new_node
            thread_handle = threading.Thread(target=self.listen_to_node, args=(new_node,))
            thread_handle.start()
            new_node.thread_handle = thread_handle
            print('client connected sucessfuly')
        else:
            print("connection failed")

    def server_loop(self):
        print("running the server loop")
        self.server_socket.listen()
        while True:
            client_socket, self.addr = self.server_socket.accept()
            print(f'{self.my_id}: accepted client: {self.addr}')
            status, username = self.server_handshake_protocol(client_socket)
            if status:
                print("clients username: " + username)

                new_node = P2pNode.P2pNode(username, client_socket)
                thread_handle = threading.Thread(target=self.listen_to_node, args=(new_node,))
                thread_handle.start()
                new_node.thread_handle = thread_handle

                self.connected_nodes[username] = new_node
                print('accepted client')
            else:
                print('did not accept client')

    def listen_to_node(self, node: P2pNode.P2pNode):
        print(f"{self.my_id}: listening...")
        while True:
            operation, content = protocol_read(node.socket)
            print(f"{self.my_id}: got a broadcast!")
            match operation:
                case Operations.BROADCASTING:
                    self.broadcasting_callback(content)
                case Operations.DIRECT:
                    result = self.direct_callback(content)
                    protocol_write(node.socket, result, Operations.DIRECT_RETURN)
                case Operations.DIRECT_RETURN:
                    self.direct_callback(content, returning=True)

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
            protocol_write(target_socket, {'status': "ok", 'id': f'{self.my_id}'}, Operations.CONNECTION_ESTABLISHMENT)
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
                return False,
            # stage 2
            protocol_write(target_socket, {'id': self.my_id}, Operations.CONNECTION_ESTABLISHMENT)
            operation, data = protocol_read(target_socket)
            if operation != Operations.CONNECTION_ESTABLISHMENT or data['status'] != "ok":
                return False,
            print("client handshake success")
            return True, data['id']

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
    broadcasts = dict[str, time]()

    def broadcast_to_all(self, dict_to_broadcast):
        '''
        ACCEPTED DICTIONARY MUST CONTAIN
        id-the broadcast id
        operation - the operation that will be done using that broadcast
        :param dict_to_broadcast:
        :return:
        '''
        try:
            print(f'connected nodes: {self.connected_nodes.values()}')
            dict_to_broadcast['__sender'] = self.my_id
            for node in self.connected_nodes.values():
                protocol_write(node.socket, dict_to_broadcast, Operations.BROADCASTING)
                print(f"broadcast was sent to {node.node_id}")

        except Exception as ex:
            raise ex
            return False


    def broadcasting_callback(self, broadcasting_dict: dict):
        try:
            print('========broadcast========')
            for key in broadcasting_dict.keys():
                print(f'{key}: {broadcasting_dict[key]}')
            print('=======end-broadcast========')

            broadcast_id = broadcasting_dict['id']
            if broadcast_id in self.broadcasts.keys():
                print("threw package away")
                return False
            print(f"{self.my_id}: rebroadcasting")
            self.broadcasts[broadcast_id] = broadcasting_dict

            broadcasted_operation = broadcasting_dict['operation']
            if not self.broadcast_callback(broadcasting_dict, broadcasted_operation):
                print('canceling broadcast because it failed')
                return False

            sender_id = broadcasting_dict['__sender']
            for node_id,node in self.connected_nodes.items():
                if (sender_id == node_id):
                    continue
                print(f"{self.my_id}: rebroadcasted")
                print(broadcasting_dict)
                protocol_write(node.socket, broadcasting_dict, Operations.BROADCASTING)

            print(broadcasting_dict['operation'])


            self.broadcasts['id'] = broadcasting_dict['id'], time.time()


        except Exception as ex:
            raise ex
            return False

    '''
    =====================================================
    ------------------direct messages--------------------
    =====================================================
    '''
    def send_direct(self, direct_dict: dict):
        try:
            print('======returning operation proccesing')
            node_id, target_node = next(iter(self.connected_nodes.items()))
            print(f'connected nodes: {self.connected_nodes.values()}')
            direct_dict['__sender'] = self.my_id
            protocol_write(target_node.socket, direct_dict, Operations.DIRECT)
            print('======sent returning operation')

        except Exception as ex:
            print(ex)
            #raise ex
            return False
    def direct_callback(self, direct_dict: dict, returning=False):
        print('entered direct callback')
        try:
            if not returning:
                direct_operation = direct_dict['operation']
                result = self.direct_operation_callback(direct_dict, direct_operation)
                if result == False:
                    print('canceling direct because it failed')
                    return {'result': False, 'operation': Operations.REQUEST_DB_RETURN}

                sender_id = direct_dict['__sender']
                return result
            else:
                direct_operation = direct_dict['operation']
                self.returning_operations_callback(direct_dict, direct_operation)

        except Exception as ex:
            raise ex
            return False