import random
import sqlite3
import os
from Scripts.CryptoNetwork.tests.BlockGeneratorTests import generate_random_block, add_people_to_database
from Scripts.CryptoNetwork.BlockGenerator import Block, miner_money_multiplier
from Scripts.CryptoNetwork.Transaction import Transaction
from datetime import datetime

class PeerToPeerDatabase:
    def __init__(self, port, db_folder='  '):
        self.port = port
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
                        timestamp TIME,
                        signature TEXT,
                        FOREIGN KEY (sender_id) REFERENCES users(username),
                        FOREIGN KEY (receiver_id) REFERENCES users(username),
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

    def database_to_bytes(self):
        database_handle = open(self.db_file, 'rb')
        database_bytes = database_handle.read()
        database_handle.close()
        return database_bytes

    def write_database(self, data: bytes):
        database_handle = open(self.db_file, 'wb')
        database_handle.write(data)
        database_handle.close()
        print('database transfered successfully')

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
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            conn.close()
            return user
        except:
            return None

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
        timestamp = transaction.timestamp
        signature = transaction.signature

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        try:
            # Insert transaction into the transactions table
            cursor.execute('''
                INSERT INTO transactions (tx_id, block_id, sender_id, receiver_id, amount, timestamp, signature)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (transaction_id, block_id, sender_id, receiver_id, amount, timestamp, signature))

            conn.commit()
            #print("Transaction added successfully.")
        except sqlite3.Error as e:
            print("Error occurred:", e)

        conn.close()

    # Function to retrieve all transactions for a given user
    def get_transaction(self, transaction_id):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT tx_id, block_id, sender_id, receiver_id, amount, timestamp, signature
                FROM transactions
                WHERE tx_id = ?
            ''', (transaction_id,))

            transactions = cursor.fetchall()
            conn.close()
            return transactions
        except:
            return [None]

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

        block_details = cursor.fetchall()[0]

        cursor.execute('''
                    SELECT tx_id, block_id, sender_id, receiver_id, amount, timestamp, signature
                    FROM transactions
                    WHERE block_id = ?
                ''', (block_id,))

        transactions_db_format = cursor.fetchall()
        transaction_objects = []
        for transaction in transactions_db_format:
            new_transaction = Transaction(transaction[2],
                                          transaction[3],
                                          transaction[4],
                                          transaction[6],
                                          None,
                                          transaction[0],
                                          transaction[5])


        conn.close()


        block_object = Block(block_details[3], block_details[1])
        block_object.last_block_hash = block_details[2]
        block_object.block_id = block_details[0]
        return block_object


    def get_users(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users;')
        users = [user[0] for user in cursor.fetchall()]
        conn.close()
        return users


    def get_latest_block_id(self):
        try:
            conn =  sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
            SELECT block_id
                FROM blocks b1
                WHERE b1.block_id = (
                SELECT MAX(block_id)
                FROM blocks b2
                );
            ''')
            index = cursor.fetchone()
            conn.close()
            return index[0]
        except:
            return None

    def check_for_transactions_in_database(self, transactions: list[Transaction]):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        for transaction in transactions:
            try:
                cursor.execute("SELECT 1 FROM transactions WHERE tx_id = ?", (transaction.id,))
                result = cursor.fetchone()
                if result is not None:
                    transactions.remove(transaction)
            except Exception as ex:
                raise ex
                None
        conn.close()
        return transactions

    def check_for_transaction_in_database(self, transactions: list[Transaction]):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        for transaction in transactions:
            cursor.execute("SELECT 1 FROM transactions_table WHERE id = ?", (transaction.id,))
            if cursor.fetchone() is not None:
                transactions.remove(transaction)
        conn.close()
        return transactions

    def generate_transactions_text(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions_table", ())
        transactions_db_format = cursor.fetchall()
        transaction_objects = []
        for transaction in transactions_db_format:
            new_transaction = Transaction(transaction[2],
                                          transaction[3],
                                          transaction[4],
                                          transaction[6],
                                          None,
                                          transaction[0],
                                          transaction[5])
            transaction_objects.append(new_transaction)

        conn.close()


    def get_transactions_with_user(self, user: str):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE sender_id = ? OR receiver_id = ?", (user, user))
        transactions_db_format = cursor.fetchall()
        transaction_objects = []

        for transaction in transactions_db_format:
            print(f'timestamp: {transaction[5]}')
            new_transaction = Transaction(transaction[2],
                                          transaction[3],
                                          transaction[4],
                                          transaction[6],
                                          None,
                                          transaction[0],
                                          datetime.strptime(transaction[5], '%Y-%m-%d %H:%M:%S.%f')
            )
            transaction_objects.append(new_transaction.to_json())

        conn.close()
        return transaction_objects

    def get_user_balance(self, user):
        try:
            return self.user_balance_cache[1][user]
        except Exception as ex:
            return '-'



    def sum_blockchain(self, use_cache=True):
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
            # print(f'block: {block}')
            cursor.execute("SELECT * FROM transactions WHERE block_id = ?", (block,))
            transactions = cursor.fetchall()

            print(f'current caching block: {block}')

            cursor.execute("SELECT miner FROM blocks WHERE block_id = ?", (block,))
            miner = cursor.fetchone()[0]

            # print(transactions)

            for transaction in transactions:
                sender = str(transaction[2])
                receiver = str(transaction[3])
                amount = transaction[4]
                user_balance[sender] = user_balance.get(sender, 0) - amount
                user_balance[receiver] = user_balance.get(receiver, 0) + amount
            miner_bonus = miner_money_multiplier * (len(transactions) + 1)

            user_balance[miner] = user_balance.get(miner, 0) + miner_bonus
            print('==============')
            print(user_balance.get(miner, 0))
            print(miner_bonus)
            print(sum(user_balance.values()))
            print(len(transactions))
            print('=================')

        self.user_balance_cache = (block_count, user_balance)
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

    blocksum = database.sum_blockchain()
    print(blocksum)


    print(database.get_users())
    print(database.get_latest_block_id())

