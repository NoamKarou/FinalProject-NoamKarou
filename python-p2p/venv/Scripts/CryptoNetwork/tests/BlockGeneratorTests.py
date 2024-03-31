import random
import string
from Scripts.CryptoNetwork.BlockGenerator import Block, generate_key_pair
from Scripts.CryptoNetwork.Transaction import Transaction
from faker import Faker

fake = Faker()

# Assuming you have Block, Transaction, and generate_key_pair defined somewhere

# Define a function to generate random names
names = ["Alice", "Bob", "Ryan", "Sophia", "Thomas", "Ursula", "Victor", "Wendy", "Xavier", "Yvonne", "Zach"]
def generate_random_name():
    #return fake.first_name()
    return random.choice(names)

# Define a function to generate random amounts
def generate_random_amount():
    return random.randint(50, 250)  # Random amount between 100 to 1000

# Define a function to generate a random block
def generate_random_block(last_block):
    pub, priv = generate_key_pair()
    block = Block(last_block=last_block, miner=generate_random_name())
    transactions = []

    num_transactions = random.randint(6, 13)  # Random number of transactions per block

    for _ in range(num_transactions):
        sender = generate_random_name()
        receiver = generate_random_name()
        amount = generate_random_amount()
        transaction = Transaction(sender, receiver, amount, key=priv)
        transactions.append(transaction)

    block.transactions = transactions

    return block
if __name__ == '__main__':

    # Example usage
    last_hash = "hkjdgfkjlhfdgkjhdfgkjhdgfk"  # Assuming you have a valid last hash

    transactions = list()
    for i in range(13):
        random_block = generate_random_block(i,  last_hash)
        last_hash = random_block.hash_block()
        print(random_block)
