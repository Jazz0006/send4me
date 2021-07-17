### T1A3 - Terminal Application - Send For Me
---
# Help File for Send4Me APP

## Introduction

Send4Me is an app that transfers files in a LAN network. It can act as a server or a client, depending on the input argument.

## Usage

**As a server (receiver):**

`./send4me.sh -listen`

**As a client (sender):**

`./send4me.sh -t {target_ip} <files_to_send.abc>`

- For Target IP Address:

    To send to a specific IP address, use `-t` argument
  
    Example:

    `./send4me.sh -t 192.168.1.101`

    You do not need to specify the target IP address every time. If there is no `-t` input argument, the app will try to find the configuration file send4me.ini in the current directory and read the saved IP address.

    *The send4me.ini file will always keep the IP address you used last time. It updates automatically.*

- For Files to be Sent

    To specify the files to be sent, list them in the arguments.

    Example:

    `./send4me.sh pic1.jpg video2.avi`

    It will send pic1.jpg and video2.avi to the receiving computer.

    If you do not specify any file in the input argument, this app will send all files in the current directory, except for itself.

    Example:

    `./send4me`

    This will send all files in the current directory to the computer specified in send4me.ini configuration file.



