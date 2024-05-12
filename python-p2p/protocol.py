import socket
import json
import time

from operations import Operations
import base64



def int_to_base64(number, size=4):
    if number < 0:
        raise ValueError("Input must be a non-negative integer.")

    result = ""
    while number > 0:
        result = chr(number % 64 + 48) + result
        number //= 64
    return base64.b64encode(result.encode()).decode().rjust(size, 'A')

def base64_to_int(base64_string):
    decoded_str = base64.b64decode(base64_string).decode()
    result = 0
    for char in decoded_str:
        result = result * 64 + ord(char) - 48
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
    '''
    :param socket_:
    :return: (operation, content)
    '''
    data = socket_.recv(4).decode()
    content_length = base64_to_int(data)
    operation = int(socket_.recv(4).decode())
    operation = Operations(operation)
    json_string = socket_.recv(content_length).decode()
    content = json.loads(json_string)

    return operation, content


def protocol_write(socket_: socket.socket, value: dict, operation: Operations) -> None:
    try:
        json_string = json.dumps(value)
        content_len_num = len(json_string)
        content_len = int_to_base64(content_len_num)
        socket_.sendall(f'{f'{content_len}'.zfill(4)}{f'{operation.value}'.zfill(4)}{json_string}'.encode())
    except Exception as ex:
        print(value)
        raise ex