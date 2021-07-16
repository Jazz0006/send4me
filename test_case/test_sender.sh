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

if [[ ! -d sender ]]
then
    mkdir sender
fi

# First test the testing target is accessible
echo " Step 1:   Try to ping the target computer @ $TARGET_IP ..."
echo
ping $TARGET_IP -c 4 
if [[ $? != 0 ]]
then
    echo "Cannot reach the computer at $TARGET_IP."
    echo "Please confirm the IP address is correct. You can open this script and edit it in the 4th line"
    exit 1
else
    echo " Step 1 Passed"
    echo 
fi

cd sender
cp ../../send4me.sh .
cp ../../send4me.py .
# Create a txt file for transmistion
env>testfile1.txt

# Check the txt file exists and its size is bigger than 0
if [[ -s testfile1.txt ]] 
then
    echo
    echo " Step 2: Sending file: testfile1.txt"
else
    echo "Cannot create testfile1.txt for this test case"
    exit 1
fi

./send4me.sh -t $TARGET_IP testfile1.txt > test01-sender-log.txt

if [[ $? == 0 ]]
then
    echo " Step 2 Passed."
    echo " Please check the result on the receiver side to make sure the test case is successful."
else
    echo "!!!Test failed!!!"
    echo "You can find the output log in test01-sender-log.txt"
    exit 1
fi