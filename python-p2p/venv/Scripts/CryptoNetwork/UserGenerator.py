import json

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
from base64 import b64encode, b64decode

def hash_key(key):
    hasher = hashes.Hash(hashes.SHA256(), backend=default_backend())
    hasher.update(key.encode('utf-8'))
    return hasher.finalize()

def encrypt_message_aes(message, key):
    key_bytes = hash_key(key)
    iv = b'\0' * 16  # Initialization vector (IV) for CBC mode
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padded_message = _pad(message)
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()

    return b64encode(iv + ciphertext).decode("utf-8")


def decrypt_message_aes(ciphertext, key):
    key_bytes = hash_key(key)
    data = b64decode(ciphertext)
    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()

    return _unpad(decrypted_message).decode("utf-8")


def _pad(message):
    block_size = 16
    padding_length = block_size - (len(message) % block_size)
    padding = bytes([padding_length]) * padding_length
    return message.encode("utf-8") + padding


def _unpad(message):
    padding_length = message[-1]
    return message[:-padding_length]

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    return private_pem, public_pem

def encrypt_message(message, public_key):
    public_key = serialization.load_pem_public_key(public_key.encode(), backend=default_backend())
    ciphertext = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext.hex()

def decrypt_message(ciphertext, private_key):
    private_key = serialization.load_pem_private_key(private_key.encode(), password=None, backend=default_backend())
    plaintext = private_key.decrypt(
        bytes.fromhex(ciphertext),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()

class User:
    username: str
    encrypted_password: str
    public_key: str

    def __init__(self, username, password):
        self.username = username
        private_key, public_key = generate_key_pair()
        self.public_key = str(private_key)
        encrypted_key = str(encrypt_message_aes(public_key, password))
        self.encrypted_password =str(encrypted_key)

    def to_json(self):
        json_dict = {"username": self.username, "encrypted_password": self.encrypted_password, "public_key": self.public_key}
        return json.dumps(json_dict)

    def from_json(json_string):
        json_dict = json.loads(json_string)
        u = User("e", "e")
        u.username = json_dict["username"]
        u.encrypted_password = json_dict["encrypted_password"]
        u.public_key = json_dict["public_key"]
        return u

def check_login(public_key: str, private_key: str, password: str):
    try:
        TEST_MESSAGE = "Hello. This Is a test"
        #create a test message
        encryption_key = decrypt_message_aes(private_key, password)
        #encrypt it using the private key
        encrypted_message = encrypt_message(TEST_MESSAGE, encryption_key)
        #decrypt it using the public key
        if decrypt_message(encrypted_message, public_key) == TEST_MESSAGE:
            #check if the result matches
            return encryption_key
        return False
    except:
        # If this errors it means that invalid data was entered
        # which means login failure
        return False

def user_from_data(username, encrypted_password, public_key):
    #json_dict = json.loads(json_string)
    u = User("e", "e")
    u.username = username
    u.encrypted_password = encrypted_password
    u.public_key = public_key
    return u

if __name__ == '__main__':
    new_user = User("fatoush", "password")

    encryption_key = decrypt_message_aes(new_user.encrypted_password, "password")
    print(new_user.encrypted_password)
    print(type(new_user.encrypted_password))
    encrypted_message = encrypt_message("hello", encryption_key)

    user_str = new_user.to_json()

    re_user = User.from_json(user_str)

    encrypted_message = encrypt_message("hello", encryption_key)

    print(type(new_user.public_key))
    print(type(new_user.encrypted_password))

    print(check_login(new_user.public_key, new_user.encrypted_password, "password"))
