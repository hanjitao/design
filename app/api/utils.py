from flask import jsonify, request, url_for
import socket
import time


def get_poetry(describe, ptype):

    port = 8080 if ptype == 5 else 8081
    client = socket.socket()
    client.connect(('localhost',port))

    if not describe:
        describe = '春'

    client.send(describe.encode('utf-8'))
    content = client.recv(1024).decode()

    client.close()
    return content



def get_params(name, default_value = None, default_type = None):
    value = request.args.get(name, default_value)
    if default_type:
        value = default_type(value)
    return value

