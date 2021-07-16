import socket
import sys
import os

# Number of seconds socket will wait for connections:
# STANDBY_TIME = 20

# Buffer size for sending and receiving files
BUFFER_SIZE = 4096

def print_intro():
    print("""
 Send4Me - A simple tool to transfer files in a LAN network.
 ----------------------------------------------------------------------
    Example usage:

    For receiver:
        send4me -listen

    For sender:
        send4me -t 192.168.X.X file-to-send.jpg
 ----------------------------------------------------------------------

    """)

def get_local_ip_address():
# Function to find the local IP address
# Show the IP address of the server, 
# Client need this IP address to connect

    address = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
    return address

def get_target_ip_address():
# Read saved IP address from configuration file "send4me.ini"
# This will be the default IP address to connect if user does not specify one in argv

    try: 
        with open("send4me.ini", "r") as conf:
            return conf.readline().strip()
    except FileNotFoundError:
        return None

def receive_content():
# Function for the receiver side

    ip_address = get_local_ip_address()
    print(f" Info:   This computer's IP address is {ip_address}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('', 9587))                        
        except Exception as e:
            print(" Error:  Cannot create a socket")
            print(e)
            print(" Please check your network setting.")
            exit(1)

        try:
            s.listen()
            print(" Info:   Ready to receive files.")
            print(" Info:   Waiting for connection...")
            print(f" Info:   To connect and send files, on the other computer, use: send4me -t {ip_address}")
            print(" Info:   Press Ctrl+C if you want to quit immediately\n\n")
            conn, addr = s.accept()
        except KeyboardInterrupt:
            print(" \nInfo:   Socket has been closed.")
            print(" Info:   Thanks for using Send4Me. See you next time\n\n")
            exit(1)

        try:
            with conn:
                print(" Info:   Connected by", addr)

                #Receive 8-byte header: the amount of files
                buffer = conn.recv(8)
                l = buffer.decode().split()
                rcv_file_amount = int(l[0])

                for i in range(rcv_file_amount):
                    #print("Now receiving file header")
                    buffer = conn.recv(64)
                    
                    l = buffer.decode().split()

                    file_name = l[0]
                    file_size = int(l[1])

                    #print(file_name, file_size)
                    print(f" Info:   Receiving file {file_name}")
                    with open(file_name, "wb") as rf:
                        remain_byte = file_size
                        while remain_byte > BUFFER_SIZE:
                            byte_read = conn.recv(BUFFER_SIZE)
                            rf.write(byte_read)
                            #print("Writing to file")
                            remain_byte -= BUFFER_SIZE

                        #Receive the last packet
                        byte_read = conn.recv(remain_byte)
                        rf.write(byte_read)
                    print(f" Info:   {file_name} received succcessfully")
                print(f" Info:   Successfully received {rcv_file_amount} files")
        except: 
            print(" Error:  Error in receiving file content.")
            print("         Please try sending the files again.\n\n")
            exit(1)
    #print("Info:   Closing the socket")
    print("""
 Info:   Thanks for using Send4Me. See you next time.


    """)
    

def send_files(target_ip, file_list):
# Function to send all files in {file_list} to {target_ip}

    print(f" Info:   Connecting to host at {target_ip} ...")

    file_amount = len(file_list)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((target_ip, 9587))
            print(" Info:   Connect successful")
        except Exception as e:
            print("-"*76)
            print(f" Error:  Cannot connect to host: {target_ip}")
            print("         Please check if send4me is running at the remote host. ")
            print(f"         And the target IP address {target_ip} is correct.\n\n")

            exit(1)
        
        print(f" Info:   There are {file_amount} files to be sent")
        #pack thr file_amount into an 8-byte header
        head_buffer = str(file_amount).encode() + b'\n'
        head_size = len(head_buffer)
        head_buffer += b'0' * ( 8 - head_size )
        s.sendall(head_buffer)

        
        for filename in file_list:
            print(f" Info:   Open file {filename} ")
            
            try:
                #Get the size of the file, 
                #Server need this number to know when to finish receiving one file
                file_len = os.path.getsize(filename)

                # send out file_to_send
                with open(filename, "rb") as f:
                    head_buffer = filename.encode() + b'\n'
                    head_buffer += str(file_len).encode() + b'\n'
                    head_size = len(head_buffer)
                    if head_size > 64:
                        print("-"*76)
                        print(" Error:  File name is too long, or the size is too big, please use other tools to send this file")
                        exit(1)
                    else:
                        # Fill the header and make it 64-byte long
                        head_buffer += b'0' * ( 64-head_size )
                    #Send the file name and its size, this header is 64 byte long:
                
                    s.sendall(head_buffer)

                    #print(f"Info:   Sending {filename}")
                    remain_size = file_len
                    while remain_size > BUFFER_SIZE:
                        bytes_read = f.read(BUFFER_SIZE) 
                        s.sendall(bytes_read)
                        remain_size -= BUFFER_SIZE
                    bytes_read = f.read(remain_size) 
                    s.sendall(bytes_read)
                    print(f" Info:   Finished sending {filename}")
            except FileNotFoundError:
                print("-"*76)
                print(f" Error:  File {filename} is not available")
                print("         Please check the path and the filename.")
                exit(1)
        print(f" Info:   {file_amount} files have been sent successfully.")
        print(" Info:   Thanks for using Send4Me. See you again.\n\n")

def get_file_list(path):
# Function to scan and find all files in current directory
# Hidden files need to be excluded
# send4me.py and send4me.ini also need to be excluded.

    file_list = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        file_list.extend(filenames)
        break
    #Remove two files: send4me.py and send4me.ini
    if 'send4me.ini' in file_list:
        file_list.remove('send4me.ini')
    if 'send4me.py' in file_list:
        file_list.remove('send4me.py')
    if 'send4me.sh' in file_list:
        file_list.remove('send4me.sh')
    #Remove hidden files:
    file_list = [x for x in file_list if x[0]!='.']
    return file_list
    
def check_empty_file_list(fl):
# Print the error message if the there is no files to be sent

    if fl == []:
        print("-"*76)
        print(" Error:  No files to be sent.")
        print("-"*76)
        print("           Please specify the files you want to send.")
        print("           Or copy them here and rerun send4me\n\n")
        exit(1)

def update_conf(addr):
    try:
        with open("send4me.ini", 'w') as conf:
            conf.write(addr)
    except Exception as e:
        print(" Error:  Cannot update send4me.ini")
        print(e)
        exit(1)


# Main function
if __name__ == '__main__':
    # Print help message:
    print_intro()

    if len(sys.argv)==1: #There is no input argument
        #Get target IP address from configuration file

        print(" Info:   Running in client mode.\n")
        target_ip = get_target_ip_address()
        if not target_ip: #Failed in getting saved IP address
            print("-"*76)
            print(" Error:  Cannot decide the target IP address")
            print("           Please specify the target IP address, for example:")
            print("           send4me -t 192.168.1.105\n\n")
        else:        
            #scan and get a list of files in current directory
            file_list = get_file_list('.')
            check_empty_file_list(file_list)
            
            #send files
            send_files(target_ip, file_list)

    elif sys.argv[1] == "-listen": 
        receive_content()

    elif sys.argv[1] == '-t': # Specifying the target ip address
        target_ip = sys.argv[2]

        length_argv = len(sys.argv)
        if length_argv > 3: # User specified one or more files to be sent
            file_list = []
            for i in range(3, length_argv):
                file_list.append(sys.argv[i])

            send_files(target_ip, file_list)
            
        else: # User did not specify the file to be sent, which mean all files in current folder should be sent
            # Scan and get a list of files in current directory
            file_list = get_file_list('.')

            check_empty_file_list
            #send files
            send_files(target_ip, file_list)

        # Save this IP address into the send4me.ini file
        update_conf(target_ip)

    else: #user just specified the files to be sent
        target_ip = get_target_ip_address()
        length_argv = len(sys.argv)
        #print(sys.argv)
        file_list = []
        for i in range(1, length_argv):
            file_list.append(sys.argv[i])
        #print(file_list)
        send_files(target_ip, file_list)