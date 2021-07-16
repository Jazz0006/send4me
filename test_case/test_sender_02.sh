#!/bin/bash

# Please assign the target IP here
TARGET_IP="127.0.0.1"

current_dir=$( pwd )

if [[ ! $current_dir =~ "test_case" ]] 
then
    echo It seems like you are not in the "test_case" folder.
    echo This script is designed to be run in the "test_case" folder
    exit 1
fi

# First test the testing target is accessible
echo " Step 1:   Try to ping the target computer @ $TARGET_IP ..."
echo
ping $TARGET_IP -c 2 
if [[ $? != 0 ]]
then
    echo "Cannot reach the computer at $TARGET_IP."
    echo "Please confirm the IP address is correct. You can open this script and edit it in the 4th line"
    exit 1
else
    echo " Step 1 Passed"
    echo 
fi

if [[ -d sender ]]
then
    rm -r sender
fi

mkdir sender
cd sender
cp ../../send4me.sh .
cp ../../send4me.py .

# Create 4 txt file for transmistion
echo " Step 2:  Preparing 4 files..."
env > testfile1.txt
ls /bin > testfile2.txt
cat testfile1.txt testfile2.txt > testfile3.txt
dmesg > testfile4.txt
echo " Below files will be sent:"
ls *.txt

echo $TARGET_IP > send4me.ini

echo " Step 3: Sending files out ..."
./send4me.sh > test02-sender-log.txt

if [[ $? == 0 ]]
then
    echo " Step 3 Passed."
    echo " Please check the result on the receiver side to make sure the test case is successful."
else
    echo "!!!Test failed!!!"
    echo "You can find the output log in test02-sender-log.txt"
    exit 1
fi