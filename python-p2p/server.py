import time
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
    return
    interface = crypto_network_interface.interface()
    interface.connect(20000, None, None)
    time.sleep(1)
    interface.create_account("fatoush", "yuthyjgh")
    print("tried creating user")

    interface.listener.thread_handle.join()


def p2():
    interface = crypto_network_interface.interface()
    interface.connect(20001, '127.0.0.1', 20000)
    interface.listener.thread_handle.join()

if __name__ == '__main__':
    main()