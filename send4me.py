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
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)





