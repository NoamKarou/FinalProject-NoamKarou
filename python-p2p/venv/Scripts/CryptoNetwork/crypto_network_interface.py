import random
import threading
import time

import operations
from Scripts.P2P.P2pListener import P2pListener
from Scripts.P2P.P2pNode import P2pNode

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
        self.listener = P2pListener(my_port)
        print("listener created")

        self.listener.broadcast_callback = self.route_callback

        self.database = database.PeerToPeerDatabase(port=my_port)
        self.my_user = None

        if start_ip is not None:
            self.listener.connect((start_ip, target_port))


        #self.listener.thread_handle.join()

    def create_account(self, username: str, password: str):
        try:
            if self.user_exists(username):
                print("The duplicate account was located the right way")
                return False
            new_user = User(username=username, password=password)
            self.database.insert_user(new_user.username, new_user.encrypted_password, new_user.public_key)
            broadcasting_dict = {
                "id": generate_broadcast_id(),
                "username" : new_user.username,
                "encrypted_password": new_user.encrypted_password,
                "public_key": new_user.public_key,
                "operation": Operations.ACCOUNT_CREATION.value
            }
            self.listener.broadcast_to_all(broadcasting_dict)
            return True
        except Exception as ex:
            raise (ex)
            return False

    def set_self_details(self, username):
        self.username = username
        my_user = self.database.get_user(username)
        self.encryption_key = encryption_key

    def is_logged_in(self):
        return self.my_user is not None

    def try_login(self, username, password) -> bool:
        try:
            username, encrypted_password, public_key = self.database.get_user(username)
            return UserGenerator.check_login(public_key, encrypted_password, password)
        except:
            return False
    def account_creation_callback(self, data: dict):
        try:
            if self.database.user_exists(data["username"]):
                print("username already exists")
                return False

            self.database.insert_user(data["username"], data["encrypted_password"], data["public_key"])
            return True
        except Exception as ex:
            print(f"{ex}: data was not fromatted correctly")
            return False

    def user_exists(self, username: str):
        return self.database.user_exists(username)

    def route_callback(self, data: dict, operation: operations.Operations):
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


    miner_update_message = "miner update"
    def update_miner_status(self, status: bool):
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
        try:
            user, enc, pub = self.database.get_user(username)
            print(decrypt_message(signiture, pub))
            print(status)
            return True
        except Exception as ex:
            print(f'ex from miner_update_callback {ex}')
            return False

    #def generate_id(self):
        #self.listener.

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
        self.mining.on_block_added_outside()

    def block_receive_callback(self, data):
        print("received block")
        try:
            received_block = Block.from_json(json_string=data['block'])
            print(received_block)
            last_id = self.database.get_latest_block_id()
            if last_id is None:
                last_id = -1
            print(1)
            if received_block.block_id != int(last_id) + 1:
                print('the block is not the latest in the chain')
                return False
            print(2)
            for received_transaction in received_block.transactions:
                if not self.validate_transaction(received_transaction):
                    print("block addition failed due to transaction validation error")
                    return False
                print(2.5)
                if None in self.database.get_transaction(received_transaction.id):
                    print("transaction failed due to database error")
                    return False
                print(3)
            self.database.add_block(received_block)

        except Exception as ex:
            raise ex
            return


    def create_transaction(self, recevier: str, amount: int):
        try:
            transaction = Transaction(self.username, recevier, amount, key=self.encryption_key, id=generate_broadcast_id())
            broadcasting_dict = {
                "id": generate_broadcast_id(),
                "operation": Operations.TRANSACTION_CREATION.value,
                "transaction": transaction.to_json()
            }
            self.listener.broadcast_to_all(broadcasting_dict)
            self.mining.add_transaction_to_transaction_pool(transaction)
            return True
        except Exception as ex:
            raise ex
            return False

    def transaction_receive_callback(self, data: dict):
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
            self.mining.add_transaction_to_transaction_pool(received_transaction)
            
        except Exception as ex:
            raise ex
            return

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
