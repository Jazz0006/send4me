import socket
import sys
#from test_client import BUFFER_SIZE
import time

# Number of seconds socket will wait for connections:
STANDBY_TIME = 20

# Buffer size for sending and receiving files
BUFFER_SIZE = 4096


def get_local_ip_address():
    host_name = socket.gethostname()
    address = socket.gethostbyname(host_name)
    return address

def get_target_ip_address():
    with open("send4me.ini", "r") as conf:
        if not conf:
            return None
        else:
            return conf.readline()

if len(sys.argv)==1: #There is no input argument
    #Get target IP address from configuration file
    target_ip = get_target_ip_address()
    if not target_ip: #Failed in getting saved IP address
        print("Please specify the target IP address")
    else:
        #scan and get a list of files in current directory

        #send files
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

elif sys.argv[1] == "-listen":
    ip_address = get_local_ip_address()
    print(f"This computer's IP address is {ip_address}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('', 9587))                        
        except Exception as e:
            print("Error in creating socket")
            print(e)
            exit(1)

        try:
            s.listen()
            print("Ready to receive files.")
            print("Waiting for connection...")
            print(f"To connect and send files, on the other computer, use: \n   send4me -t {ip_address}")
            #print("After 5 minutes, this app will automatically exit")
            print("Press Ctrl+C if you want to quit immediately\n\n")
            #time.sleep(STANDBY_TIME)
            #return False
        except KeyboardInterrupt:
            print("\n\n")
            print("Socket has been closed.")
            print("Thanks for using Send4Me. See you next time\n\n")
            exit(1)

        conn, addr = s.accept()
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

elif sys.argv[1] == '-t': #specifying the target ip address
    pass
