# Purpose: Demonstrate how to use multiprocessing in ArcMap.
import os
import arcpy
import sys
from time import sleep
import subprocess

# HOW TO USE THIS DEMO:
# 1. Open ArcMap
# 2. Create a new toolbox
# 3. Create a new script tool
# 4. Set the script tool to point to this script
# 5. Choose whether to run "demo" or "mp_demo" in the main body of the script.
# 6. Run the script tool with no parameters.

def mp_demo(args):
    arcpy.AddMessage("Multiprocessing demo started")
    # Make sure that whatever python executable called this script is used to call child processes.
    py_prefix = sys.exec_prefix
    py_path = os.path.join(py_prefix, "python.exe")
    arcpy.AddMessage(py_path)
    # current_dir = path of the directory that this script is in
    current_dir = os.path.dirname(os.path.realpath(__file__))
    daemon_path = os.path.join(current_dir, "demo_daemon.py")

    args_array = [py_path, daemon_path] 
    #The first two arguments in args_array are the python executable and the daemon script.
    #You can add additional arguments to args_array here. They will be passed to the daemon script.
    #Access those arguments with sys.argv in the daemon script.

    for arg in args:
        args_array.append(str(arg)) #When calling subprocess, all arguments will be stringified. That's why we don't just pass an entire array here, but append each item.
        #You can avoid having to call subprocess if you are willing to run your script from the command line.


        # We use "subprocess" to open a new python process that then manages the daemons.
        # We do this because multiprocessing is not possible out of a mark
        # Check_output is friendly to Python 2.7. There are more options in Python 3.
        # Children of the subprocess can only report their output via print(), not ArcPy.AddMessage.
        # Recommend writing a function that logs to both.
    try:
        result = subprocess.check_output(args_array, stderr=subprocess.STDOUT)
        return result
    except subprocess.CalledProcessError as e:
        arcpy.AddMessage(e.output)
        raise e

def demo_logic(number):
    return int(number)*2

def demo(number_list):
    results = []
    # Print the numbers from the list
    for number in number_list:
        # Wait two seconds
        sleep(2)
        times_two = demo_logic(number)
        results.append(times_two)
    return results

# An array of numbers 1 through 3:
# Multiplying these all by two in serial should take 6 seconds
numbers = [1, 2, 3]

# An array of numbers 1 through 30:
# NMultiplying all of these by two in serial should take 60 seconds
numbers2 = [i for i in range(1, 30)]

if __name__ == "__main__":
    arcpy.AddMessage(demo(numbers)) #Expected output: [2, 4, 6]
    # Comment above and uncomment the below when ready to try mulitprocessing.

    # results = mp_demo(numbers2)
    # arcpy.AddMessage(results)
    #Expected output: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58]
