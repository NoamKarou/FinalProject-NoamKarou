import socket
import json
from operations import Operations




def int_to_base256(number, size=4):
    if number < 0:
        raise ValueError("Input must be a non-negative integer.")

    result = ""
    while number > 0:
        result = chr(number % 256) + result
        number //= 256
    return result.rjust(size, '\x00')


def base256_to_int(base256_string):
    result = 0
    for char in base256_string:
        result = result * 256 + ord(char)
    return result


'''
================
---protocol-----
================
    
    msg_len - 4 bytes - encoded in base 256
    operation type - 2 bytes -a number encoded in base 256 representing the operation
        the number is based on the values created in the Operations enum
    content - N bytes -the conents sent, a dictionary encoded in json containing the info sent
        content is of type dict<str, str>. and will be read and returned as one
'''


def protocol_read(socket_: socket.socket) -> (Operations, dict[str, str]):
    content_length = base256_to_int(socket_.recv(4).decode())
    operation = int(socket_.recv(4).decode())
    operation = Operations(operation)
    json_string = socket_.recv(content_length).decode()
    content = json.loads(json_string)

    return operation, content


def protocol_write(socket_: socket.socket, value: dict, operation: Operations) -> None:
    json_string = json.dumps(value)
    content_len_num = len(json_string)
    content_len = int_to_base256(content_len_num)
    socket_.send(f'{content_len}{f'{operation.value}'.zfill(4)}{json_string}'.encode())
