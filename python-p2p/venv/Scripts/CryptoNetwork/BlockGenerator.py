import hashlib
import json
import time

from Scripts.CryptoNetwork.Transaction import Transaction
from Scripts.CryptoNetwork.UserGenerator import generate_key_pair
import math

z_count = 16
miner_money_multiplier = 20

class Block:


    '''
    ======BLOCK RULES=======
    the first block to come wins
    if two blocks come at the same time the one with more transactions wins
    if they both have the same amount of transactions the one with more value in them wins
    if they both have the same value the one with the larger hash wins
    ========================
    '''
    
    block_id: int
    last_block_hash: int
    miner: str
    transactions: list[Transaction]
    salt: str

    def __init__(self, miner, last_block=None):
        if last_block is None:
            self.last_block_hash = 0
            self.block_id = 1
            self.miner = miner
        else:
            self.last_block_hash = last_block
            self.block_id = last_block + 1
            self.miner = miner
        self.salt = "None"
        self.transactions = list()

    def hash_block(self):
        to_hash = ''
        to_hash += f'{self.block_id}{self.last_block_hash}'
        to_hash += f'{self.miner}'
        for transaction in self.transactions:
            to_hash += transaction.generate_transaction_text()
        to_hash += f'{self.salt}'
        return hash_string_sha256(to_hash)

    def validate_block_signature(self):
        block_hash = self.hash_block()
        digest_bytes = bytes.fromhex(block_hash[0: math.ceil(z_count / 8) * 2])
        hash_bits = ''.join(format(byte, '08b') for byte in digest_bytes)
        if not compare_bits_to_zero(hash_bits):
            return False

        return True

    def check_for_transaction_in_block(self, transaction: Transaction):
        transaction_text = transaction.generate_transaction_text()
        for block_transaction in self.transactions:
            if transaction_text == block_transaction.generate_transaction_text():
                return True
        return False

    def to_dict(self):
        return_dict = {
            'block_id': self.block_id,
            'miner': self.miner,
            'last_block': self.last_block_hash,
            'salt': self.salt
        }
        transactions_list = []
        for transaction in self.transactions:
            transactions_list.append(transaction.to_json())
        return_dict['transactions'] = transactions_list
        return return_dict

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_string):
        user_dict = json.loads(json_string)
        return_block = cls(
            user_dict['miner'],
            user_dict['last_block'])
        return_block.block_id = user_dict['block_id']

        for transaction in user_dict['transactions']:
            return_block.transactions.append(Transaction.from_json(transaction))
        return_block.salt = user_dict['salt']
        return return_block

    def __str__(self):
        ret = ''
        ret += f'=====Begin block info for block: {self.block_id}==============\n'
        ret += f'miner: {self.miner}-received {(len(self.transactions)+1) * miner_money_multiplier} for creating the block\n'
        copied_transactions = self.transactions
        copied_transactions = sorted(copied_transactions, key=lambda transaction: transaction.amount)
        for transaction in copied_transactions:
            ret += f'transaction: {transaction.generate_transaction_text()} : {transaction.signature}\n'
        ret += f'the salt of the block is: {self.salt}\n'
        ret += f'{self.hash_block()}\n'
        ret += f'=====End info for block {self.block_id}============='
        return ret

def hash_string_sha256(input_string):
    encoded_string = input_string.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(encoded_string)
    hashed_string = sha256_hash.hexdigest()

    return hashed_string
38810

def compare_bits_to_zero(bit_arr):
    return bit_arr == ''.zfill(len(bit_arr))

if __name__ == '__main__':
    pub, priv = generate_key_pair()
    block = Block(miner="noam" ,last_block=0)
    transactions = list()

    transactions.append(Transaction("noam", "itamar", 200, key=priv))
    transactions.append(Transaction("moti", "tsvika", 300, key=priv))
    transactions.append(Transaction("alphasa", "alphasa", 700, key=priv))

    block.transactions = transactions

    #print(block)

    block = Block(miner="noam", last_block=0)
    transactions = list()

    transactions.append(Transaction("noam", "itamar", 200, key=priv))
    transactions.append(Transaction("moti", "tsvika", 300, key=priv))
    transactions.append(Transaction("alphasa", "alphasa", 700, key=priv))

    block.transactions = transactions

    print(block.check_for_transaction_in_block(block.transactions[0]))
    time.sleep(0.1)
    print(block.check_for_transaction_in_block(Transaction("alphasa", "alphasa", 700, key=priv)))