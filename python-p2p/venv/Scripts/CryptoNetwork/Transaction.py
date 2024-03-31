import json
import time
from datetime import datetime
from Scripts.CryptoNetwork.UserGenerator import decrypt_message, encrypt_message, generate_key_pair

class Transaction:
    sender: str
    receiver: str
    signature: str
    amount: int
    id:str
    timestamp: time.time
    def __init__(self, sender, receiver, amount, signature=None, key=None, id=None, timestamp = None):
        self.sender = sender
        self.receiver = receiver
        self.signature = signature
        self.amount = amount
        self.id = id
        self.timestamp = timestamp
        if timestamp is None:
            self.timestamp = datetime.now()
        if key is not None:
            self.generate_signature(key)

    def to_json(self):
        return json.dumps(self.to_dict())

    def signature_text(self):
        return f"{self.sender}-{self.amount}->{self.receiver} t-{self.timestamp}"

    def generate_signature(self, key):
        signature_text = self.signature_text()
        encrypted = encrypt_message(signature_text, key)
        self.signature = encrypted
        return encrypted

    def generate_transaction_text(self):
        return self.signature_text()

    def validate(self, key):
        signature_string = decrypt_message(self.signature, key)
        return signature_string == self.signature_text()

    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'receiver': self.receiver,
            'signature': self.signature,
            'amount': self.amount,
            'timestamp': self.timestamp.timestamp()
        }

    @classmethod
    def from_json(cls, json_string):
        user_dict = json.loads(json_string)
        return cls(
            user_dict['sender'],
            user_dict['receiver'],
            user_dict['amount'],
            user_dict['signature'],
            id=user_dict['id'],
            timestamp=datetime.fromtimestamp(user_dict['timestamp']))



if __name__ == '__main__':
    pub, priv = generate_key_pair()
    Transaction = Transaction("noam", "itamar",200,None)
    Transaction.generate_signature(priv)
    json_String = Transaction.to_json()
    print(json_String)
    print(Transaction.signature_text())

    retransacted = Transaction.from_json(json_String)
    print(retransacted.validate(pub))
