import random
import sqlite3
import os
from Scripts.CryptoNetwork.tests.BlockGeneratorTests import generate_random_block, add_people_to_database
from Scripts.CryptoNetwork.BlockGenerator import Block, miner_money_multiplier
from Scripts.CryptoNetwork.Transaction import Transaction


class PeerToPeerDatabase:
    def __init__(self, port, db_folder='  '):
        self.port = port
        #{db_folder}/
        module_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_file = module_dir + f'/databases/databases_{port}/user_database.db'

        folder_path = os.path.dirname(self.db_file)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        self._create_tables()
        self.user_balance_cache = 0, {}

    def _create_tables(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                encrypted_password TEXT,
                public_key TEXT
            )
        ''')
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS transactions (
                        tx_id INTEGER PRIMARY KEY,
                        block_id INTEGER,
                        sender_id INTEGER,
                        receiver_id INTEGER,
                        amount REAL,
                        FOREIGN KEY (sender_id) REFERENCES users(user_id),
                        FOREIGN KEY (receiver_id) REFERENCES users(user_id),
                        FOREIGN KEY (block_id) REFERENCES blocks(block_id)
                    )
                ''')
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS blocks (
                        block_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        previous_block_id INTEGER,
                        previous_block_hash TEXT,
                        miner TEXT,
                        FOREIGN KEY (previous_block_id) REFERENCES blocks(block_id)
                    )
                ''')

        conn.commit()
        conn.close()


    def user_exists(self, username):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT EXISTS(SELECT 1 FROM users WHERE username = ?)', (username,))
        result = cursor.fetchone()[0]
        print(f'{result}: {username}')
        conn.close()
        return result == 1

    def insert_user(self, username, encrypted_password, public_key):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users VALUES (?, ?, ?)', (username, encrypted_password, public_key))
        conn.commit()
        conn.close()

    def get_user(self, username) -> tuple[str, str, str]:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        return user

    def update_user(self, username, encrypted_password, public_key):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET encrypted_password = ?, public_key = ? WHERE username = ?',
                       (encrypted_password, public_key, username))
        conn.commit()
        conn.close()

    def delete_user(self, username):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.commit()
        conn.close()

    def user_details(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT username, public_key FROM users;')
        users = cursor.fetchone()
        conn.close()

    '''
    ================== TRANSACTIONS ==================
    '''

    def add_transaction(self, transaction: Transaction, block_id):
        transaction_id = transaction.id
        sender_id = transaction.sender
        receiver_id = transaction.receiver
        amount = transaction.amount

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        try:
            # Insert transaction into the transactions table
            cursor.execute('''
                INSERT INTO transactions (tx_id, block_id, sender_id, receiver_id, amount)
                VALUES (?, ?, ?, ?, ?)
            ''', (transaction_id, block_id, sender_id, receiver_id, amount))

            conn.commit()
            #print("Transaction added successfully.")
        except sqlite3.Error as e:
            print("Error occurred:", e)

        conn.close()

    # Function to retrieve all transactions for a given user
    def get_transaction(self, transaction_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT tx_id, block_id, sender_id, receiver_id, amount
            FROM transactions
            WHERE tx_id = ?
        ''', (transaction_id,))

        transactions = cursor.fetchall()
        conn.close()

        return transactions

    '''
    ================== blocks ==================
    '''

    def add_block(self, block: Block, add_transactions = True):
        block_id = block.block_id
        previous_block_id = block.block_id - 1
        previous_block_hash = block.last_block_hash
        miner = block.miner
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        try:
            # Insert transaction into the transactions table
            cursor.execute('''
                INSERT INTO blocks (block_id, previous_block_id, previous_block_hash, miner)
                VALUES (?, ?, ?, ?)
            ''', (block_id, previous_block_id, previous_block_hash, miner))
            conn.commit()
            #print("Transaction added successfully.")
        except sqlite3.Error as e:
            print("Error occurred while adding transaction to database:", e)

        conn.close()

        try:
            if add_transactions:
                for transaction in block.transactions:
                    self.add_transaction(transaction, block_id)
        except sqlite3.Error as e:
            print("Error occurred:", e)

    # Function to retrieve all transactions for a given user
    def get_block(self, block_id):
        '''
        CREATE TABLE IF NOT EXISTS blocks (
                        block_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        previous_block_id INTEGER,
                        previous_block_hash TEXT,
                        miner TEXT,
                        FOREIGN KEY (previous_block_id) REFERENCES blocks(block_id)
        '''
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT block_id, previous_block_id, previous_block_hash, miner
            FROM blocks
            WHERE block_id = ?
        ''', (block_id,))

        transactions = cursor.fetchall()
        conn.close()

        return transactions


    def get_users(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users;')
        users = [user[0] for user in cursor.fetchall()]
        conn.close()
        return users

    def sum_blockchain(self, use_cache = True):

        if not use_cache:
            starting_block = 0
            user_balance = {}
        else:
            starting_block, user_balance = self.user_balance_cache


        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM blocks;')
        block_count = cursor.fetchone()[0]



        for block in range(starting_block, block_count):
            block += 1
            #print(f'block: {block}')
            cursor.execute("SELECT * FROM transactions WHERE block_id = ?", (block,))
            transactions = cursor.fetchall()

            print(block)

            cursor.execute("SELECT miner FROM blocks WHERE block_id = ?", (block,))
            miner = cursor.fetchone()[0]

            #print(transactions)
            for transaction in transactions:
                user_balance[transaction[2]] = user_balance.get(transaction[2], 0) - transaction[4]
                user_balance[transaction[3]] = user_balance.get(transaction[3], 0) + transaction[4]
                user_balance[miner] = user_balance.get(miner, 0) + miner_money_multiplier

        conn.close()
        return user_balance

# Example usage:

if __name__ == '__main__':
    database = PeerToPeerDatabase(port=random.randint(1, 65000))
    add_people_to_database(database)
    block = generate_random_block(last_block=0)
    #database.add_transaction(block.transactions[0], block.block_id)
    database.add_block(block)
    block = generate_random_block(last_block=1)
    database.add_block(block)

    print(database.sum_blockchain())

    block = generate_random_block(last_block=2)
    database.add_block(block)

    print(database.sum_blockchain())

    print(database.get_users())

