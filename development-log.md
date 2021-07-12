### T1A3 - Terminal Application - Send For Me

# Development Log

## 2021-Jul-11: Successfully set up socket connection

Python socket module is quite simple to use. Following the standard procedure, I quickly learned how to setup up a socket, how a client connects and sends data, and how the server receives them.

A problem I met is that since WSL is using a bridged network from its host Windows, it is not in the same subnet of all other computers in my home network. When testing using local loopback address "127.0.0.1", this would not be an issue, but when I tried to connect from another computer to WSL, it was failed. 

One solution is to set port forwarding on the host Windows. But each time starts, WSL will change its IP address. So a script is needed to solve this issue automatically. 

At the moment, I use "127.0.0.1" for quick testing and copy my app to Windows when running test cases that require a connection between different computers.

## 2021-Jul-12: Handling transmission of multiple files

**Challenge**: When sending multiple files, it is not as simple as sending just one. Because the receiver just keeps receiving a stream of data, it does not know the boundary of different files. 

The way to solve this problem is to define a protocol between the sender and the receiver. For example, the sender first tells the receiver the size of the file that will be sent, so the receiver knows how many bytes it needs to receive before the stream of the next file is coming. The receiver will write the content it received into one file. After that, the receiver can accept the content of the second file.

I designed and implemented below simple protocol for my app:

|Section        | Length |  Description |
|----------     |--------|--------------|
|Package Header | 8      |The number of files that will be sent. It controls how many times below content will loop. |
|First File Header   | 64          | file name + \n + file size + \n |
|First File content  | {file size} | The content of the file         |
|Second file header  | 64          | file name + \n + file size + \n |
|Second File content | {file size} | The content of the file         |
|...
|



