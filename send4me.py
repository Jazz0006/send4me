import socket
import time

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind(('', 4587))
    print("Socket binded")

    print("Now listening")
    serversocket.listen()

#print("Socket listening for 5 seconds")
#time.sleep(5)
    conn, addr = serversocket.accept()
    with conn:
        print("Connected by", addr)

        print("Now receiving files")
        with open("received.svg", "wb") as rf:
            while True:
                byte_read = conn.recv(4096)
                if not byte_read:
                    break
                rf.write(byte_read)

                #data = conn.recv(4096)
                #if not data:
                #    break
            #conn.sendall(data)
    print("Successfully received one file")
print("close the socket")





