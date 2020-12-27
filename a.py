import time

def main():
    x = 0
    # Do Stuff
    time1 = int(time.time())
    for i in range(50000000):
        x = x + 1
    time2 = int(time.time())
    print(time2 - time1)
    
main() 
