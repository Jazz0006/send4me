import socket
import sys
#from test_client import BUFFER_SIZE
import os

# Number of seconds socket will wait for connections:
STANDBY_TIME = 20

# Buffer size for sending and receiving files
BUFFER_SIZE = 4096


def get_local_ip_address():
    address = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
    return address

def get_target_ip_address():
    with open("send4me.ini", "r") as conf:
        if not conf:
            return None
        else:
            return conf.readline().strip()

def receive_content():
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

            print("Now receiving the number of files:")
            buffer = conn.recv(8)
            l = buffer.decode().split()
            rcv_file_amount = int(l[0])

            for i in range(rcv_file_amount):
                print("Now receiving file header")
                buffer = conn.recv(64)
                
                l = buffer.decode().split()

                file_name = l[0]
                file_size = int(l[1])

                print(file_name, file_size)

                with open(file_name, "wb") as rf:
                    remain_byte = file_size
                    while remain_byte > BUFFER_SIZE:
                        byte_read = conn.recv(BUFFER_SIZE)
                        rf.write(byte_read)
                        print("Writing to file")
                        remain_byte -= BUFFER_SIZE

                    #Receive the last packet
                    byte_read = conn.recv(remain_byte)
                    rf.write(byte_read)
                print(f"Finished receiving {file_name}")
    print("Successfully received one file")
    print("close the socket")

def send_files(target_ip, file_list):
    file_amount = len(file_list)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((target_ip, 9587))
            print("Connect successfle")
        except Exception as e:
            print(f"Cannot connect to host: {target_ip}")
            print("Please check the if the IP address specified is correct.")
            exit(1)
        
        
        print(f"There are {file_amount} files to be sent")
        #pack thr file_amount into an 8-byte header
        head_buffer = str(file_amount).encode() + b'\n'
        head_size = len(head_buffer)
        head_buffer += b'0' * ( 8 - head_size )
        s.sendall(head_buffer)

        print("Now opening file to be sent")
        for filename in file_list:
            #Get the size of the file, 
            #Server need this number to know when to finish receiving one file
            file_len = os.path.getsize(filename)
            # send out file_to_send
            with open(filename, "rb") as f:
                if not f:
                    print(f"Cannot open file: {filename}")
                    exit(1)
                head_buffer = filename.encode() + b'\n'
                head_buffer += str(file_len).encode() + b'\n'
                head_size = len(head_buffer)
                if head_size > 64:
                    print("File name is too long, or the size is too big, please use other tools to send this file")
                    exit(1)
                else:
                    #Fill the header size to 64 byte
                    head_buffer += b'0' * ( 64-head_size )
                #Send the file name and its size, this header is 64 byte long:
                
                s.sendall(head_buffer)

                print(f"Sending {filename}")
                remain_size = file_len
                while remain_size > BUFFER_SIZE:
                    bytes_read = f.read(BUFFER_SIZE) 
                    s.sendall(bytes_read)
                    remain_size -= BUFFER_SIZE
                bytes_read = f.read(remain_size) 
                s.sendall(bytes_read)
                print(f"Finished sending {filename}")

def get_file_list(path):
    file_list = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        file_list.extend(filenames)
        break
    #Remove two files: send4me.py and send4me.ini
    if 'send4me.ini' in file_list:
        file_list.remove('send4me.ini')
    if 'send4me.py' in file_list:
        file_list.remove('send4me.py')
    #Remove hidden files:
    file_list = [x for x in file_list if x[0]!='.']
    return file_list
    

if len(sys.argv)==1: #There is no input argument
    #Get target IP address from configuration file
    target_ip = get_target_ip_address()
    if not target_ip: #Failed in getting saved IP address
        print("Please specify the target IP address")
    else:
        #scan and get a list of files in current directory
        file_list = get_file_list('.')
        #send files
        send_files(target_ip, file_list)

elif sys.argv[1] == "-listen": 
    receive_content()

elif sys.argv[1] == '-t': #specifying the target ip address
    target_ip = sys.argv[2]
    length_argv = len(sys.argv)
    if length_argv > 3: # User specified one or more files to be sent
        file_list = []
        for i in range(3, length_argv):
            file_list.append(sys.argv[i])
        
        send_files(target_ip, file_list)
        
    else: #User did not specify the file to be sent, which mean all files in current folder should be sent
        #scan and get a list of files in current directory
        file_list = get_file_list('.')
        #send files
        send_files(target_ip, file_list)

else: #user just specified the files to be sent
    target_ip = get_target_ip_address()
    length_argv = len(sys.argv)
    #print(sys.argv)
    file_list = []
    for i in range(1, length_argv):
        file_list.append(sys.argv[i])
    #print(file_list)
    send_files(target_ip, file_list)