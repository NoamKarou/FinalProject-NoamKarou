import sqlite3

class PeerToPeerDatabase:
    def __init__(self, port, db_folder='peer_to_peer_databases'):
        self.port = port
        #{db_folder}/
        self.db_file = f'peer_to_peer_{port}.db'
        self._create_table()

    def _create_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                encrypted_password TEXT,
                public_key TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def user_exists(self, username):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT EXISTS(SELECT 1 FROM users WHERE username = ?)', (username,))
        result = cursor.fetchone()[0]
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
