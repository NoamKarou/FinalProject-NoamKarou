import threading

from Scripts.CryptoNetwork.BlockGenerator import Block, z_count
from Scripts.CryptoNetwork.Transaction import Transaction
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
    name: str
    def __init__(self, name):
        self.name = name

    def start_new_block(self, last_block, last_hash):
        new_block = Block(last_block, last_hash)
        self.active_block = new_block

    def create_salt(self, zcount = 5, max_itter = 10000):
        '''

        :param zcount: the desired amount of zeros
        :param max_itter: the max itterations for finding the value (0=∞)
        :return: True if the salt has been created, False if it haden't
        '''
        self.miner_thread = threading.Thread(target=self._salt_generator, args=(zcount, max_itter))
        self.salt_function_temp = False
        self.miner_thread.daemon = True
        self.miner_thread.start()
        self.miner_thread.join()
        temp = self.salt_function_temp
        self.salt_function_temp = None
        return temp
    def _salt_generator(self, zcount = 5, max_itter = 10000):
        '''
        ONLY MEANT FOR INTERNAL USE WITHIN THE OBJECT
        DO NOT CREATE INSTANCES OUTSIDE
        a threading helper function for generating salt
        '''
        i = 0
        while i < max_itter:
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

        self.salt_function_temp = False
        return

    def get_latest_block(self):
        return self.active_block

    def monitor_block_relevance(self):
        while True:
            if self.active_block != self.get_latest_block():
                self.miner_thread
                self.active_block = None


if __name__ == '__main__':
    active_block = generate_random_block(last_block=1)
    miner = Mining('fatoush')
    miner.active_block = active_block
    print(miner.create_salt(max_itter=50000000, zcount=z_count))
    print(miner.active_block)