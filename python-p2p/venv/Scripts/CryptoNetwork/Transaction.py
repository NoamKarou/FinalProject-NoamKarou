import json
from Scripts.CryptoNetwork.UserGenerator import decrypt_message, encrypt_message, generate_key_pair

class Transaction:
    sender: str
    receiver: str
    signature: str
    amount: int

    def __init__(self, sender, receiver, amount, signature=None, key=None):
        self.sender = sender
        self.receiver = receiver
        self.signature = signature
        self.amount = amount
        if key is not None:
            self.generate_signature(key)

    def to_json(self):
        return json.dumps(self.to_dict())

    def signature_text(self):
        return f"{self.sender}-{self.amount}->{self.receiver}"

    def generate_signature(self, key):
        signature_text = self.signature_text()
        encrypted = encrypt_message(signature_text, key)
        self.signature = encrypted
        return encrypted

    def validate(self, key):
        signature_string = decrypt_message(self.signature, key)
        return signature_string == self.signature_text()

    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'signature': self.signature,
            'amount': self.amount
        }

    @classmethod
    def from_json(cls, json_string):
        user_dict = json.loads(json_string)
        return cls(user_dict['sender'], user_dict['receiver'], user_dict['amount'], user_dict['signature'])

if __name__ == '__main__':
    pub, priv = generate_key_pair()
    Transaction = Transaction("noam", "itamar",200,None)
    Transaction.generate_signature(priv)
    json_String = Transaction.to_json()
    print(json_String)

    retransacted = Transaction.from_json(json_String)
    print(retransacted.validate(pub))
