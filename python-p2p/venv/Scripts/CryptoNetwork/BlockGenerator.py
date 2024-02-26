import hashlib
from Scripts.CryptoNetwork.Transaction import Transaction
from Scripts.CryptoNetwork.UserGenerator import generate_key_pair

class Block:
    block_id: int
    last_block: int
    transactions: list[Transaction]
    last_hash: str

    def __init__(self, last_block=None, last_hash=None):
        if last_block is None:
            self.last_block = 0
            self.block_id = 1
        else:
            self.last_block = last_block
            self.block_id = last_block + 1
            self.last_hash = last_hash
        self.transactions = list()

    def hash_block(self):
        to_hash = ''
        to_hash += f'{self.block_id}{self.last_block}'
        for transaction in self.transactions:
            to_hash += transaction.generate_signature()
        return hash_string_sha256(to_hash)


def hash_string_sha256(input_string):
    encoded_string = input_string.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(encoded_string)
    hashed_string = sha256_hash.hexdigest()

    return hashed_string


if __name__ == '__main__':
    pub, priv = generate_key_pair()
    block = Block(last_block=0, last_hash="hkjdgfkjlhfdgkjhdfgkjhdgfk")
    transactions = list()

    transactions.append(Transaction("noam", "itamar", 200, key=priv))
    transactions.append(Transaction("moti", "tsvika", 300, key=priv))
    transactions.append(Transaction("alphasa", "alphasa", 700, key=priv))

    block.transactions = transactions

    print(block.hash_block())
