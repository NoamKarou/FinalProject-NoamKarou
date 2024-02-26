import time

from operations import Operations
from Scripts.P2P.P2pListener import P2pListener
from Scripts.P2P.P2pNode import P2pNode
from Scripts.CryptoNetwork import crypto_network_interface
import threading


def main():
    t1 = threading.Thread(target=p1)
    t2 = threading.Thread(target=p2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

def p1():
    listener = P2pListener(20000)
    listener.broadcast_callback = lambda x, y: print(x)


def p2():
    listener = P2pListener(20001)
    listener.connect(("127.0.0.1", 20000))
    broadcast_dict = {
        "id": "1",
        "operation": Operations.TEST.value,
        "content": "hi"
    }
    listener.broadcast_callback = lambda x, y: print(x)
    listener.broadcast_to_all(broadcast_dict)

if __name__ == '__main__':
    main()