import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('192.168.1.106', 5555))
    s.sendall(b'Hello World')
    data = s.recv(1024)

print('Received', repr(data))