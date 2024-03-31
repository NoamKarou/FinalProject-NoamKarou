import sqlite3
import os

class PeerToPeerDatabase:
    def __init__(self, port, db_folder='  '):
        self.port = port
        #{db_folder}/
        self.db_file = f'databases_{port}/user_database.db'

        folder_path = os.path.dirname(self.db_file)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        self._create_tables()

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
                        tx_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sender_id INTEGER,
                        receiver_id INTEGER,
                        amount REAL,
                        timestamp DATETIME,
                        FOREIGN KEY (sender_id) REFERENCES users(user_id),
                        FOREIGN KEY (receiver_id) REFERENCES users(user_id)
                    )
                ''')
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS blocks (
                        block_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        previous_block_id INTEGER,
                        timestamp DATETIME,
                        nonce INTEGER,
                        FOREIGN KEY (previous_block_id) REFERENCES blocks(block_id)
                    )
                ''')
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS block_transactions (
                        block_id INTEGER,
                        tx_id INTEGER,
                        FOREIGN KEY (block_id) REFERENCES blocks(block_id),
                        FOREIGN KEY (tx_id) REFERENCES transactions(tx_id)
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

# Example usage:
# database = PeerToPeerDatabase(port=8080)
# print(database.user_exists('user1'))  # False
# database.insert_user('user1', 'password1', 'key1')
# print(database.user_exists('user1'))  # True
# ...
