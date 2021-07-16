#!/bin/bash

# Delete all files except for send4me app
for FILE in *
do
    #echo $FILE
    if [[ ! $FILE =~ ^send4m ]] && [ $FILE != test_receiver.sh ]
    then
        echo Deleted $FILE
        rm $FILE
    fi
done

# Confirm file testfile1.txt does not exist
if [[ -s testfile1.txt ]] 
then
    echo 'Please make sure testfile1.txt does not exist before the test'
    exit 1
fi

./send4me.sh -listen

if [[ $? == 0 ]]
then
    echo Test failed. Please check the error message above.
fi

if [[ -s testfile1.txt ]] 
then
    echo Successfully received testfile1.txt
fi