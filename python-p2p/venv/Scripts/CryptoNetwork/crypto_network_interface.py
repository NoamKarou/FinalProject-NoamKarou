import random
import threading
import time
import base64
import os

import operations
from Scripts.P2P.P2pListener import P2pListener
from Scripts.P2P.P2pNode import P2pNode
from Scripts.P2P.portgen import generate_port

from Scripts.CryptoNetwork.UserGenerator import User
from Scripts.CryptoNetwork.Transaction import Transaction
from Scripts.CryptoNetwork.BlockGenerator import Block
from Scripts.CryptoNetwork import UserGenerator
from Scripts.CryptoNetwork.Mining import Mining
from Scripts.CryptoNetwork.UserGenerator import decrypt_message, encrypt_message

from operations import Operations

from Scripts.Database import database


class interface:
    listener: P2pListener
    username: str
    encryption_key: str
    is_miner: bool
    active_miner_thread: threading.Thread
    transaction_pool: list[dict]

    def connect(self, my_port, start_ip, target_port):
        '''
        Establish a connection for peer-to-peer communication.
        :param my_port: The port number for my P2P listener.
        :param start_ip: The starting IP address to connect to (can be None).
        :param target_port: The target port number to connect to.
        '''

        if my_port == target_port:
            raise RuntimeError('target port cant be the same as your port')

        self.listener = P2pListener(my_port)
        print("listener created")

        self.listener.broadcast_callback = self.route_callback
        self.listener.direct_operation_callback = self.route_direct
        self.listener.returning_operations_callback = self.returning_direct
        if start_ip is not None:
            self.listener.connect((start_ip, target_port))
        self.database = database.PeerToPeerDatabase(port=my_port)
        try:
            print('requesting database')
            self.request_database()
        except Exception as ex:
            #print(ex)
            raise ex
        self.my_user = None



        self.mining = None

        #self.listener.thread_handle.join()

    def auto_connect(self):
        module_dir = os.path.dirname(os.path.abspath(__file__))
        nodes_file = module_dir + f'/available_nodes.txt'

        my_port = generate_port()

        with open(nodes_file, 'r') as file:
            available_nodes = file.readlines()
        for node in available_nodes:
            try:
                ip, port = node.split(':')
                try:
                    self.connect(my_port, ip, int(port))
                    return my_port, ip, int(port)
                except Exception as ex:
                    print(ex)
                    None
            except Exception as ex:
                print(ex)
                continue
        return False



    def get_username(self):
        '''
        Retrieve the username of the user.
        :return: The username if available, otherwise 'guest'.
        '''
        try:
            return self.username
        except:
            return 'guest'

    def create_account(self, username: str, password: str):
        '''
        This method attempts to create a new user account with the provided username
        and password.
        :param username: The desired username for the new account.
        :param password: The desired password for the new account.
        :return: True if the account was successfully created, False if the username
        is already taken or an exception occurred.
        '''
        try:
            if self.user_exists(username):                           # -confirm the username is not taken
                print("The duplicate account was located the right way")
                return False
            new_user = User(username=username, password=password)    # -create user object
            self.database.insert_user(new_user.username, new_user.encrypted_password, new_user.public_key)  
            broadcasting_dict = {
                "id": generate_broadcast_id(),
                "username" : new_user.username,                      # -create a dictionary
                "encrypted_password": new_user.encrypted_password,   # containg the user 
                "public_key": new_user.public_key,                   # details
                "operation": Operations.ACCOUNT_CREATION.value       # 
            }                                                        # 
            self.listener.broadcast_to_all(broadcasting_dict)        # -Send the transaction to everyone
            return True
        except Exception as ex:
            raise (ex)
            return False

    def set_self_details(self, username: str):
        '''
        Set the details of the current user.
        :param username: The username of the current user.
        :return:
        '''
        self.username = username
        my_user = self.database.get_user(username)
        self.encryption_key = encryption_key

    def is_logged_in(self):
        '''
        :return: True if the user is logged in
        '''
        return self.my_user is not None

    def try_login(self, username, password) -> bool:
        '''
        Attempt to log in with the provided username and password.
        :param username (str): The username of the user attempting to log in.
        :param password (str): The password of the user attempting to log in.
        :return:
        '''
        try:
            username, encrypted_password, public_key = self.database.get_user(username)
            return UserGenerator.check_login( #check the credetinals match the key
                public_key, encrypted_password, password)
        except:
            return False
    def account_creation_callback(self, data: dict):
        '''
        processes the incoming data for account creation, checks if the
        username already exists, and if not, adds the new user to the database.
        :param data: (dict): A dictionary containing the account details
        :return: True if the account was successfully created, False if the username
        already exists or if an error occurred
        '''
        try:
            if self.database.user_exists(data["username"]):     #check the account doesnt exist
                print("username already exists")
                return False

            self.database.insert_user(
                data["username"], data["encrypted_password"], data["public_key"])     #add the user to the database
            return True
        except Exception as ex:
            print(f"{ex}: data was not fromatted correctly")
            return False

    def request_database(self):
        '''
        Request the database from the network.
        :return: True if the request was sent successfully, False otherwise.
        '''
        try:
            direct_dict = {
                "id": generate_broadcast_id(),
                "operation": Operations.REQUEST_DB.value
            }
            self.listener.send_direct(direct_dict)
            return True
        except Exception as ex:
            raise (ex)
            return False
    def database_requestion_callback(self, data):
        '''
        called back when a database requestion is sent
        :param data (dict): A dictionary containing the request data (unused in this method).
        :return: A dictionary with the base64-encoded database bytes and the operation type.
        '''
        db_bytes = self.database.database_to_bytes()
        return {'result': base64.b64encode(db_bytes).decode('utf-8'),
                'operation': Operations.REQUEST_DB_RETURN.value}


    def user_exists(self, username: str):
        '''
        Check if a user exists in the database.
        :param username (str): The username to check for existence.
        :return: True if the user exists, False otherwise.
        '''
        return self.database.user_exists(username)

    def route_callback(self, data: dict, operation: operations.Operations):
        '''
        Route the incoming data based on the operation type.
        :param data (dict): The incoming data to be routed.
        :param operation (Operations enum): The operation type to determine the callback.
        :return: bool: True if the operation was successfully processed, False otherwise.
        '''
        print(operation)
        match operation:
            case Operations.ACCOUNT_CREATION.value:
                return self.account_creation_callback(data)
            case Operations.MINER_STATUS.value:
                return self.miner_update_callback(data['username'], data['signature'], data["status"])
            case Operations.TRANSACTION_CREATION.value:
                return self.transaction_receive_callback(data)
            case Operations.BLOCK_CREATION.value:
                return self.block_receive_callback(data)
            case _:
                print(data)
                pass
        return False

    def route_direct(self, data: dict, operation: operations.Operations):
        '''
        Route the incoming direct data based on the operation type.
        :param data (dict): The incoming direct data to be routed.
        :param operation (Operations): The operation type to determine the callback.
        :return bool: True if the operation was successfully processed, False otherwise.
        '''
        print(operation)
        match operation:
            case Operations.REQUEST_DB.value:
                return self.database_requestion_callback(data)
            case _:
                print(data)
                pass
        return False

    def returning_direct(self, data: dict, operation: operations.Operations):
        '''
        Handle returning direct data based on the operation type.
        :param data (dict): The incoming returning direct data to be routed.
        :param operation (Operations): The operation type to determine the callback.
        :return bool: True if the operation was successfully processed, False otherwise.
        '''
        print('received returning direct')
        match operation:
            case Operations.REQUEST_DB_RETURN.value:
                return self.database_receive_callback(data)
            case _:
                print(data)
                pass
        return False

    def database_receive_callback(self, data: dict):
        '''
        is called when another user sends their database to you
        updates the database file
        :param data (dict): A dictionary containing the base64-encoded database data with the key 'result'.
        '''
        print(data)
        decoded_data = base64.b64decode(data['result'])
        self.database.write_database(decoded_data)

    miner_update_message = "miner update"
    def update_miner_status(self, status: bool):
        '''
        initiates the users ability to mine blocks
        :param status: bool stating if mining should be active or not
        :return:
        '''
        """
        send_dict = {
            "id": generate_broadcast_id(),
            "signature": encrypt_message(self.miner_update_message, self.encryption_key),
            "username": self.username,
            "status": status,
            "operation": Operations.MINER_STATUS.value
        }
        self.listener.broadcast_to_all(send_dict)
        """
        self.is_miner = status
        if status:
            self.mining = Mining(self.username, self.database, self.create_block)
            #self.active_miner_thread = threading.Thread(target=self.miner_thread)
            #self.active_miner_thread.start()

    #As of now: deprecated
    def miner_update_callback(self, username, signiture, status):
        '''
        Handle the miner status update callback.
        :param username (str): The username of the miner.
        :param  username (str): The username of the miner.
        :param  signature (str): The encrypted signature of the miner.
        :return: True if the miner update was successfully processed, False otherwise.
        '''
        try:
            user, enc, pub = self.database.get_user(username)
            print(decrypt_message(signiture, pub))
            print(status)
            return True
        except Exception as ex:
            print(f'ex from miner_update_callback {ex}')
            return False


    def create_block(self, block: Block):
        '''
        a callback that is sent to the mining srcipt
        is used whenever a new block is mined
        '''
        broadcasting_dict = {
            "id": generate_broadcast_id(),
            "operation": Operations.BLOCK_CREATION.value,
            "block": block.to_json()
        }
        self.listener.broadcast_to_all(broadcasting_dict)
        self.block_receive_callback(broadcasting_dict)

    def block_receive_callback(self, data):
        '''
        is called when a block is received from the outside
        :param (dict): A dictionary containing the block data with the key 'block'.
        :return: bool: True if the block was successfully added to the blockchain, False otherwise.
        '''
        try:
            received_block = Block.from_json(json_string=data['block'])
            print(received_block)
            last_id = self.database.get_latest_block_id()
            if last_id is None:
                last_id = -1
            if received_block.block_id != int(last_id) + 1:
                print('the block is not the latest in the chain')
                return False
            for received_transaction in received_block.transactions:
                if not self.validate_transaction(received_transaction):
                    print("block addition failed due to transaction validation error")
                    return False
                print(f'block transaction id: {received_transaction.id}')
                transaction_info = self.database.get_transaction(received_transaction.id)
                print(f'block transaction info: {transaction_info}')
                if len(transaction_info) != 0:
                    print("transaction failed due to being a duplicate")
                    return False

            print(received_block.transactions)
            if len(received_block.transactions) == 0 and received_block.block_id != 0:
                return False
            self.database.add_block(received_block)
            self.database.sum_blockchain(use_cache=False)
            if self.mining is not None:
                self.mining.on_block_added_outside(received_block)
            return True

        except Exception as ex:
            raise ex
            return


    def create_transaction(self, recevier: str, amount: int):
        '''
        Create and broadcast a new transaction.
        :param receiver (str): The username of the transaction receiver.
        :param amount (int): The amount to be transferred in the transaction.
        :return: bool: True if the transaction was successfully created and processed, False otherwise.
        '''
        try:
            transaction = Transaction(self.username, recevier, amount, key=self.encryption_key, id=generate_broadcast_id())
            broadcasting_dict = {
                "id": generate_broadcast_id(),
                "operation": Operations.TRANSACTION_CREATION.value,
                "transaction": transaction.to_json()
            }
            self.listener.broadcast_to_all(broadcasting_dict)
            self.transaction_receive_callback(broadcasting_dict)
            return True
        except Exception as ex:
            raise ex
            return False

    def transaction_receive_callback(self, data: dict):
        '''
        is called when a transaction is added in the outside
        :param (dict): A dictionary containing the transaction data with the key 'transaction'.
        :return: bool: True if the transaction was successfully processed, False otherwise.
        '''
        print("received transaction")
        try:
            received_transaction = Transaction.from_json(json_string=data['transaction'])
            if not self.validate_transaction(received_transaction):
                print("transaction failed due to validation error")
                return False
            print(self.database.get_transaction(received_transaction.id))
            if None in self.database.get_transaction(received_transaction.id):
                print("transaction failed due to database error")
                return False
            if self.is_logged_in():
                self.mining.add_transaction_to_transaction_pool(received_transaction)
            return True
            
        except Exception as ex:
            raise ex
            return True

    def validate_transaction(self, transaction: Transaction):
        sender_details = self.database.get_user(transaction.sender)
        if not transaction.validate(sender_details[2]):
            return False
        # if not database.validate_transaction_contents():
        #    return False
        return True
    def validate_block(self, block: Block):
        latest_block = self.database.get_latest_block_id()
        if block.block_id != latest_block + 1:
            return False

        if not block.validate_block_signature():
            return False

        for transaction in block.transactions:
            self.validate_transaction(transaction)
        return True

    def miner_thread(self):
        if not self.is_miner:
            return
        try:
            print("im a miner! WOOOOOO")
        except:
            pass
        finally:
            timer = threading.Timer(2, self.miner_thread)
            timer.start()

def generate_broadcast_id():
    return f'{random.randint(1000, 9999)}'
