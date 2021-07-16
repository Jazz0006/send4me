# Test Plan

## Test Case 01

- Test Target

    The client specifies the target IP address, sends a single file.

    The server receives that single file 

- Test Procedure

1. On the receiver computer, run ./test_case/test_receiver_01.sh
2. On the sender computer, Update the TARGET_IP in line 3 of ./test_case/test_sender_01.sh
3. Run ./test_case/test_sender_01.sh"

- Expected Result

    Both two scripts show that test passed.

    The test_receiver_01.sh checks 
    1. The exit code of send4me.sh;
    2. Testfile1.txt is successfully received 
    
    <br>

    The test_sender_01.sh checks:
    1. Target computer is accessible (ping)
    2. The exit code of send4me.sh"

## Test Case 02

- Test Target

    The client reads IP address from the configuration file; scan current directory; send all files in the current directory to the receiver.

    The server receiles multiple files

- Test Procedure

1. On the receiver computer, run ./test_case/test_receiver_02.sh
2. On the sender computer, Update the TARGET_IP in line 3 of ./test_case/test_sender_02.sh
3. Run ./test_case/test_sender_02.sh"

- Expected Result

    Both two scripts show that test passed.

    The test_receiver_02.sh checks 
    1. The exit code of send4me.sh;
    2. Four test files are successfully received 
    
    <br>

    The test_sender_02.sh checks:
    1. Target computer is accessible (ping)
    2. The exit code of send4me.sh"
