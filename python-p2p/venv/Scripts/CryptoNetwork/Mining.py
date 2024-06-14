import threading
import multiprocessing
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
    active_block_mutex: threading.Lock
    def __init__(self, name, database, block_publishing_callback):
        self.name = name
        self.transaction_pool = list()
        self.database = database
        self.miner_thread_kill = False
        self.block_publishing_callback = block_publishing_callback
        latest_block = self.database.get_latest_block_id()
        if latest_block == None:
            latest_block = -1
        self.active_block = Block(self.name, latest_block)
        self.active_block_mutex = threading.RLock()
        self.mining_thread = threading.Thread(target=self.mining_thread)
        self.mining_thread.start()



    def mining_thread(self):
        salt_start_point = 0
        jump_size = 1000
        while True:
            self.miner_thread_kill = False
            if self.active_block is not None:
                with self.active_block_mutex:
                    self.transaction_pool = self.database.check_for_transactions_in_database(self.transaction_pool)
                    self.active_block.transactions = self.transaction_pool
                    salt_calculator = threading.Thread(target=self._salt_generator, args=(z_count, jump_size, salt_start_point))
                    salt_calculator.start()
                    salt_calculator.join()
                    self._salt_generator(z_count, jump_size, salt_start_point)
                    salt = self.salt
                    if salt is not None or self.miner_thread_kill:
                        self.miner_thread_kill = False
                        if self.transaction_pool.__str__() != self.active_block.transactions.__str__():
                            print("fail condition was called")
                            continue
                        self.block_publishing_callback(self.active_block)
                        self.active_block = None
                        salt_start_point = 0
                    salt_start_point += jump_size
                    time.sleep(0.1) # lower the frequency at which the thread runs in order to keep the ui running somthly
            else:
                time.sleep(0.2) # lower the frequency at which the thread runs in order to keep the ui running somthly


    def start_new_block(self, last_block: Block):
        with self.active_block_mutex:
            new_block = Block(self.name, last_block.block_id)
            self.active_block = new_block
            for transaction in self.transaction_pool:
                if last_block.check_for_transaction_in_block(transaction):
                    self.transaction_pool.remove(transaction)
                new_block.transactions = self.transaction_pool
            if len(self.transaction_pool) == 0:
                self.active_block = None


    def _salt_generator(self, zcount = 5, max_itter = 10000, start_index=0):
        #with self.active_block_mutex:
        '''
        ONLY MEANT FOR INTERNAL USE WITHIN THE OBJECT
        DO NOT CREATE INSTANCES OUTSIDE
        a threading helper function for generating salt
        '''
        i = start_index
        while i < max_itter + start_index:
            self.active_block.salt = i
            block_hash = self.active_block.hash_block()
            # hash_bits = string_to_bit_array(block_hash, zcount)
            digest_bytes = bytes.fromhex(block_hash[0: math.ceil(zcount / 8) * 2])
            hash_bits = ''.join(format(byte, '08b') for byte in digest_bytes)
            if (compare_bits_to_zero(hash_bits)):
                print(i)
                self.salt_function_temp = True
                self.salt = self.active_block.salt
                return
            i += 1
        if self.miner_thread_kill:
            self.miner_thread_kill = False
        self.salt_function_temp = False
        self.salt = None
        return
#
    def add_transaction_to_transaction_pool(self, transaction: Transaction):
        with self.active_block_mutex:
            self.transaction_pool.append(transaction)
            block = self.database.get_block(
                    int(self.database.get_latest_block_id()))
            print(block)
            if self.active_block is None:
                self.start_new_block(block)
            try:
                self.active_block.transactions = self.transaction_pool
            except:
                None

    def on_block_added_outside(self, previous_block):
        self.transaction_pool = self.database.check_for_transactions_in_database(self.transaction_pool)
        self.miner_thread_kill = True
        if len(self.transaction_pool) > 0:
            self.start_new_block(previous_block)
        else:
            self.active_block = None

    def update_callback(self):
        final_str = ''
        if self.active_block is not None:
            final_str += f'active_block: {self.active_block.__str__()}\n==========\n'
        else:
            final_str += 'no block is being mined at the moment\n======================\n'
        if len(self.transaction_pool) == 0:
            final_str += "there are no active transactions at the moment\n======================\n"
        final_str += "transaction pool:\n======================\n"
        for transaction in self.transaction_pool:
            final_str += transaction.generate_transaction_text() + '\n'
        final_str += '\n=========\n'
        final_str +=  f'{time.strftime("%H:%M:%S")}'
        return final_str

if __name__ == '__main__':
    active_block = generate_random_block(last_block=1)
    miner = Mining('fatoush')
    miner.active_block = active_block
    print(miner.create_salt(max_itter=50000000, zcount=z_count))
    print(miner.active_block)

#miner architecture:
#   -the miner spawns a thread
#   -the mining thread is always on
#   -controling the mining operation is by controlling which block is being mined
#   -when the mined block is none the mining pauses
#   -controling what is mined is only done by adding transactions/blocks