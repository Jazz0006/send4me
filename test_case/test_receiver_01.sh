#!/bin/bash


current_dir=$(pwd)
if [[ ! $current_dir =~ "test_case" ]] 
then
    echo It seems like you are not in the "test_case" folder.
    echo This script is designed to be run in the "test_case" folder
    exit 1
fi

if [[ -d receiver ]]
then
    rm -r receiver
fi

mkdir receiver
cd receiver
cp ../../send4me.sh .
cp ../../send4me.py .

# Confirm file testfile1.txt does not exist
if [[ -s testfile1.txt ]] 
then
    echo 'Please make sure testfile1.txt does not exist before the test'
    exit 1
fi

echo " Running test case 01 for receiver."
echo " Ready to receive file from the client."
echo " Please go to the sender computer to run test_sender_01.sh"
./send4me.sh -listen > test01-receiver-log.txt

if [[ $? != 0 ]]
then
    echo "!!!Test failed!!!"
    echo "You can find the output log in test01-receiver-log.txt"
    exit 1
fi

if [[ -s testfile1.txt ]] 
then
    echo "Test 01 Passed"
    echo "Successfully received testfile1.txt"
fi