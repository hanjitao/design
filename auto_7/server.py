import socket
from compose_poem import generate_poetry
server = socket.socket()
server.bind(('localhost', 8081))
server.listen(100)

while True:
    conn, addr = server.accept()
    print('start........')
    while True:
        data = conn.recv(1024)
        if not data:
            print('the client is lost')
            break
        print('>>>', data.decode())
        describe = data.decode()
        if len(describe)>1 :
            describe = describe[0]
        poetry = generate_poetry(describe)
        conn.send(poetry.encode('utf-8'))

server.close()
