import threading

# Create a mutex object
mutex = threading.RLock()

def a():
    # Acquire the lock
    with mutex:
        # Critical section
        print("Function a is running")
        # Perform necessary operations
        # Release the lock automatically at the end of the with statement

def b():
    # Acquire the lock
    with mutex:
        # Call function a within the critical section
        a()
        # Critical section for b
        print("Function b is running")
        # Release the lock automatically at the end of the with statement

# Test the functions
b()
