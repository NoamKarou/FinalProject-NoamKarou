import threading
import time

from Scripts.CryptoNetwork.BlockGenerator import Block, z_count
from Scripts.CryptoNetwork.Transaction import Transaction
from Scripts.Database.database import PeerToPeerDatabase
from Scripts.CryptoNetwork.tests.BlockGeneratorTests import generate_random_block
import timeit
import hashlib
import math
def string_to_bit_array(s, desired_length):
    bit_array = []
    for char in s:
        # Convert each character to its ASCII value
        ascii_value = ord(char)
        # Convert ASCII value to binary representation and remove the '0b' prefix
        binary_representation = bin(ascii_value)[2:]
        # Make sure each binary representation is 8 bits long by padding with zeros if necessary
        padded_binary = binary_representation.zfill(8)
        # Extend the bit array with the bits of the current character
        bit_array.extend([int(bit) for bit in padded_binary])

    # Pad the bit array with zeros to reach the desired length
    pad_length = desired_length - len(bit_array)
    if pad_length > 0:
        bit_array.extend([0] * pad_length)
    elif pad_length < 0:
        bit_array = bit_array[:desired_length]  # Trim excess bits if the length is greater than desired

    return bit_array


def compare_bits_to_zero(bit_arr):
    return bit_arr == ''.zfill(len(bit_arr))

def test_time(bit_length):
    string = "Hello" * (bit_length // 40 + 1)  # Adjusting string length to generate the required bit length
    desired_length = bit_length
    return timeit.timeit(lambda: string_to_bit_array(string, desired_length), number=10000)

class Mining:
    active_block: Block
    transaction_pool: list[Transaction]
    name: str
    database: PeerToPeerDatabase
    active_mining_thread: threading.Thread
    def __init__(self, name, database):
        self.name = name
        self.transaction_pool = list()
        self.database = database
        self.active_block = None

    def start_new_block(self, last_block: Block):
        new_block = Block(self.name, last_block.block_id)
        self.active_block = new_block
        for transaction in self.transaction_pool:
            if transaction in last_block.transactions:
                self.transaction_pool.remove(transaction)
        try:
            self.create_salt()
        except:
            return

    def create_salt(self, zcount = 5, max_itter = 10000):
        '''

        :param zcount: the desired amount of zeros
        :param max_itter: the max itterations for finding the value (0=∞)
        :return: True if the salt has been created, False if it haden't
        '''
        try:
            self.miner_thread = threading.Thread(target=self._salt_generator, args=(zcount, max_itter))
            self.salt_function_temp = False
            self.miner_thread.daemon = True
            self.miner_thread.start()
            self.miner_thread.join()
            temp = self.salt_function_temp
            self.salt_function_temp = None
            return temp
        except:
            return None
    def _salt_generator(self, zcount = 5, max_itter = 10000):
        '''
        ONLY MEANT FOR INTERNAL USE WITHIN THE OBJECT
        DO NOT CREATE INSTANCES OUTSIDE
        a threading helper function for generating salt
        '''
        i = 0
        while i < max_itter and not self.miner_thread_kill:
            self.active_block.salt = i
            block_hash = self.active_block.hash_block()
            # hash_bits = string_to_bit_array(block_hash, zcount)
            digest_bytes = bytes.fromhex(block_hash[0: math.ceil(zcount / 8) * 2])
            hash_bits = ''.join(format(byte, '08b') for byte in digest_bytes)
            if (compare_bits_to_zero(hash_bits)):
                print(i)
                self.salt_function_temp = True
                return

            i += 1
        if self.miner_thread_kill:
            self.miner_thread_kill = False
        self.salt_function_temp = False
        return

    def get_latest_block(self):
        return self.active_block

    def add_transaction_to_transaction_pool(self, transaction: Transaction):
        self.transaction_pool.append(transaction)
        self.moderate_block_relevance()

    def moderate_block_relevance(self):
        None

    def on_block_added_outside(self):
        self.transaction_pool = self.database.check_for_transactions_in_database(self.transaction_pool)
        if self.miner_thread != None:
            self.miner_thread_kill = True
        if len(self.transaction_pool) > 0:
            previous_block = self.database.get_block(self.database.get_latest_block_id())
            self.start_new_block(previous_block)
            self.create_salt()

    def update_callback(self):
        final_str = ''
        if self.active_block is not None:
            final_str += f'active_block: {self.active_block.__str__()}\n==========\n'
        for transaction in self.transaction_pool:
            final_str += transaction.generate_transaction_text()
        final_str += '\n=========\n'
        final_str +=  f'{time.strftime("%H:%M:%S")}'
        return final_str

if __name__ == '__main__':
    active_block = generate_random_block(last_block=1)
    miner = Mining('fatoush')
    miner.active_block = active_block
    print(miner.create_salt(max_itter=50000000, zcount=z_count))
    print(miner.active_block)
