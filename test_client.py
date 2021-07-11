import socket
import sys
import os
#import cowsay

#cowsay.stegosaurus("YOU are outstanding!")
#print(cowsay.get_output_string('trex', "I like a hug, but my arms are too short"))

BUFFER_SIZE = 4096

filename = "send4me.svg"
file_len = os.path.getsize(filename)
print(file_len)
print("send4me".encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 9587))
    print("Connect successfle")

    print("Now opening the file to be sent")
    with open("send4me.svg", "rb") as f:
        head_buffer = filename.encode() + b'\n'
        head_buffer += str(file_len).encode() + b'\n'
        head_size = len(head_buffer)
        if head_size > 64:
            print("File name is too long, or the size is too big, please use other tools to send this file")
            exit(1)
        else:
            #Fill the head size to 64 byte
            head_buffer += b'0' * ( 64-head_size )
        #Send the file name and its size, this header is 64 byte long:
        s.sendall(head_buffer)
        
        # while True:
        #     bytes_read = f.read(BUFFER_SIZE) 
        #     if not bytes_read:
        #         break

        #     s.sendall(bytes_read)

    print("Finished sending send4me.svg")
    #s.sendall(b'Hello World')
    #data = s.recv(1024)
print("Close the socket")
exit(0)
