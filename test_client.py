import socket
import sys
#import cowsay

#cowsay.stegosaurus("YOU are outstanding!")
#print(cowsay.get_output_string('trex', "I like a hug, but my arms are too short"))

BUFFER_SIZE = 4096

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('192.168.1.105', 9587))
    print("Connect successfle")

    print("Now opening the file to be sent")
    with open("send4me.svg", "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE) 
            if not bytes_read:
                break

            s.sendall(bytes_read)

    print("Finished sending send4me.svg")
    #s.sendall(b'Hello World')
    #data = s.recv(1024)
print("Close the socket")
exit(0)
#print('Received', repr(data))