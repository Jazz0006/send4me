#!/bin/bash
tput clear

if [[ ! "$(python3 -V)" =~ "Python" ]]
then
    echo 'It seems you do not have Python installed on your computer.'
    #tput bold
    echo 'Please install Python to use this app.'
fi

python3 send4me.py $@