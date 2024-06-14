import socket

ports = range(20000, 20100)

used_ports = []

def generate_port():
    for port in ports:
        if check_port_available(port):
            return port

def check_port_available(port, host='0.0.0.0'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False