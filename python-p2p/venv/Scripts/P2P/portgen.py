ports = range(20000, 20100)

used_ports = []

def generate_port():
    new_port = ports[len(used_ports)]
    print(new_port)
    used_ports.append(new_port)
    return ports[len(used_ports)]
