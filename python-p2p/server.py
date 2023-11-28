import socket
import time

from P2pListener import P2pListener
from enum import Enum
import protocol
import threading

from operations import Operations

def main():
    t2 = threading.Thread(target=main1)
    t2.start()
    t2.join()
def main1():
    listener = P2pListener(20001)
    listener.thread_handle.join()

def main2():
    time.sleep(1)
    print("creating listener")
    listener = P2pListener(20000)
    print("listener created")

    listener.connect(('127.0.0.1', 20001))
    listener.thread_handle.join()

if __name__ == '__main__':
    main()