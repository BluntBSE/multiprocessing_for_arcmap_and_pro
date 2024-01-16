import time
import arcpy
import sys
from time import sleep
import multiprocessing

# The daemon is where all of your actual geoprocessing logic should go.
# It must go in a separate file from the script tool that calls it (if you are attempting to run from a toolbox)
# The logic must go under the "if __name__ == "__main__":" line or it will not work.
# If you don't need your script to be run from a toolbox, you can just run this daemon from the command line, which might make your programming easier.


def demo_logic(number):
    sleep(2)
    return int(number)*2


def long_logic(number):
    print("Hello from long logic!")
    sleep(60)
    return int(number)*2


if __name__ == "__main__":
    # If you passsed arguments to the daemon, they will be in this array.
    all_args = sys.argv
    # The first few arguments are the python executable and the daemon script, so this makes an array of arguments that excludes those.
    operation_args = all_args[1:]
    pool = multiprocessing.Pool()
    # Switch the callback from demo_Logic to long_logic to see the speed gains on an operation that should take 30 minutes.
    # The more time the operation takes, the more speed gains you will see.
    results = pool.map(demo_logic, operation_args)
    pool.close()
    pool.join()
    print(results)
