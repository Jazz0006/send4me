#!/bin/bash
current_dir=$( pwd )
echo $current_dir

if [[  $current_dir =~ "sender" ]] 
then
    echo It seems like you are not in the "sender" folder.
    echo This script is designed to be run under the "sender" folder
fi

if [[ -s testfile1.txt ]] 
then
    echo OKOK
else
    echo We are going to send testfile1.txt
    echo Please make sure testfile1.txt exists in the current directory
fi

./send4me.sh -t 127.0.0.1 testfile1.txt

if [[ $? == 0 ]]
then
    echo File has been sent successfully
    echo Please check the result on the receiver side.
fi