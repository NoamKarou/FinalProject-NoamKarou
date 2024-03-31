from Scripts.CryptoNetwork.BlockGenerator import Block, z_count, miner_money_multiplier
from Scripts.CryptoNetwork.Transaction import Transaction
from Scripts.CryptoNetwork.tests.BlockGeneratorTests import generate_random_block
from Scripts.CryptoNetwork.Mining import Mining


class Blockchain:
    blocks: list[Block]

    def __init__(self):
        self.blocks = list()
        genesis_block = Block(miner='sys', last_block=-1)
        self.blocks.append(genesis_block)

    def add_block(self, block: Block):
        if block.last_block_hash != self.blocks[-1].hash_block():
            #raise RuntimeError("the added block does not come after the latest block")
            print('failed validating hash')
            return False

        if block.validate_block_signature() == False:
            print('failed validating signature')
            return False

        self.blocks.append(block)
        return True

    def __str__(self):
        ret = ""
        for i, block in enumerate(self.blocks):
            ret += f'==========={i}=============\n'
            ret += block.__str__() + '\n'
        return ret

    def sum_blockchain(self):
        user_balance = {}
        for block in self.blocks:
            user_balance[block.miner] = user_balance.get(block.miner, 0) + len(block.transactions) * miner_money_multiplier
            for transaction in block.transactions:
                user_balance[transaction.sender] = user_balance.get(transaction.sender, 0) - transaction.amount

                user_balance[transaction.receiver] = user_balance.get(transaction.receiver, 0) + transaction.amount
        print(sum(user_balance.values()))
        print(user_balance)


if __name__ == '__main__':
    blockchain = Blockchain()

    print(blockchain.blocks[0].hash_block())


    for i in range(10):

        rand_block = generate_random_block(len(blockchain.blocks)-1)
        rand_block.last_block_hash = blockchain.blocks[-1].hash_block()

        miner = Mining(rand_block.miner)
        miner.active_block = rand_block
        miner.create_salt(max_itter=50000000, zcount=z_count)
        miner.active_block

        print(blockchain.add_block(rand_block))

    print(blockchain)
    blockchain.sum_blockchain()

