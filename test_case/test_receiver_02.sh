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

echo " Running test case 02 for receiver."
echo " Ready to receive files from the client."
echo " Please go to the sender computer to run test_sender_02.sh"
./send4me.sh -listen > test02-receiver-log.txt

if [[ $? != 0 ]]
then
    echo "!!!Test failed!!!"
    echo "You can find the output log in test02-receiver-log.txt"
    exit 1
fi

num_file=0
for file in testfile*
do
    num_file=$(( num_file + 1 ))
done

echo $num_file
if [[ $num_file == 4 ]]
then
    echo "Test successful. Received 4 files from client."
else
    echo "!!!Test failed!!!"
    echo "You can find the output log in test02-receiver-log.txt"
    exit 1
fi