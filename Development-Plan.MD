### T1A3 - Terminal Application - Send For Me

# Software Development Plan

## **Purpose**

This App provides a simple way for computers in a LAN network to exchange files.

Today it is common to have multiple devices in our home network. We often need to send a file from one device to the other. 

Although we have online software such as Dropbox and OneDrive, we sometimes just need to quickly send files without login or other additional settings. This `send4me` app provides one solution. You can use it to share files between your devices in a vey simple way.

## **Target Audience**

Household and small businesses who have multiple devices, who need to share files between these devices.

## **How to use**

Below is an example of using `send4me` to share files between two computers.

1. On the computer that will receive files, run the app with the command shown below:

   `send4me -listen`

   It will wait for the client to send files.

2. On the computer to send files, run the app with the command shown below:

   `send4me -t 192.168.1.106 IMG001.jpg`

   * The "-t" is followed by the target IP address.
   * You can specify one or more files that need to be sent. If none is given,  `send4me` will send all in the local directory to the target.

   * Alternatively, just run 
   
      `send4me` 
      
      without any parameter. All files in the local directory will be sent the computer that was the target last time.

As a typical usecase, we just copy the files to the folder where `send4me` is located, and run the `send4me`. 

## **Features**

- Receiver-side
1. Create a server socket and listen on port 9587. Display the server's IP address on the screen. Display an error message if the socket cannot be created or binded.
2. If the client-side connect, create a new socket to receive files. Display an error message if the socket cannot be created.
3. When the client-side send files, receive those files and save them in the current directory. Display an error message if there is exception in receiving files.

<br>

- Sender-side

1. If `-t` parameter exists in the input arguments, use the IP address that follows it. Otherwise, use the IP address saved in `send4me.ini`. If that `send4me.ini` does not exist, prompt an error message, asking the user to provide a target IP address.
2. Create a socket and connect to the server, prompt an error message if fail.
3. If one or more file names are given in the input arguments, send those files. Otherwise scan and send all files in the local directory. Prompt the error messages if no files are given and no files can be found in the local directory. Update status of files sending, success or failure. 
3. When all files are sent, update `./send4me.ini` if a new IP address was given.

## **User Interaction**

Each time `send4me` runs, it will display a simple help message:

> Send4Me - A simple tool to send and receive files for local computers.

> Usage:

> `send4me -listen` for receiver side

> `send4me -t 192.168.X.X file-to-send.jpg` for sender side

- If unknown parameters are given, an error message will display, and the app exits.

- If `-listen` parameter is given, the app will display the local IP address, which is for the client to connect to. 

   It will also update its status:
   * Waiting for connection
   * Connected with client
   * Receiving files
   * All files have been received

   User can quit waiting any time by pressing "Ctrl + C", this is also displayed as part of the help message.

- For the sender side, the app will display the list of the files to be sent, and also update the status:
   * Connected to the server
   * Sending a file
   * Finished sending one file
   * Finished sending all files

## **Control Flow Diagram**

![Flow Diagram](./send4me.svg)