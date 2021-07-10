import socket
#import cowsay

#cowsay.stegosaurus("YOU are outstanding!")
#print(cowsay.get_output_string('trex', "I like a hug, but my arms are too short"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('192.168.1.106', 5555))
    s.sendall(b'Hello World')
    data = s.recv(1024)

print('Received', repr(data))