# Test Plan

## Test Case 1

script on server:
- enter the receiver folder
- clear current directory
- run "send4me.sh -listen"
- check the exit code
- check if testfile1.txt exists

script on client:
- enter the sender folder
- check if testfile1.txt exists
- ping the target computer, check the return code
- run "send4me.sh -t [target_ip] testfile1.txt"
- check the exit code

