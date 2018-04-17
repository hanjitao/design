import socket

client = socket.socket()
client.connect(('localhost',8080))

data = '春天'
client.send(data.encode('utf-8'))
data = client.recv(1024).decode()
print('>>>',data)

client.close()
