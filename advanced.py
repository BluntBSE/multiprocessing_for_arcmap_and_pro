import sys, os, subprocess, arcpy
#This is an example of how to process feature classes with multiprocessing. This example iterates over many feature classes and runs a simple operation on each one.
#The script tool that calls this script should have two parameters: a remote workspace (where the feature classes are stored) and an output workspace (where the results will be stored).


if __name__ == "__main__":
    
    remote_workspace = arcpy.GetParameterAsText(0)
    output_workspace = arcpy.GetParameterAsText(1)
    arcpy.env.scratchWorkspace = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Scratch.gdb")
    arcpy.env.overwriteOutput = True
    arcpy.env.lockingEnabled = False
   
    
    py_prefix = sys.exec_prefix
    py_path = os.path.join(py_prefix, "python.exe")
    output_path = os.path.dirname(arcpy.env.workspace)
    current_path = os.path.dirname(os.path.abspath(__file__))

    fc_names = [
        "feature_class_1",
        "feature_class_2"
    ]
    print("My output path is:")
    print(output_path)

    
    #Python executable, daemon script, current path (to create child GDBs in), followed by common data (stored in the parent workspace), followed by feature class strings
    args_array = [py_path, current_path+r"\daemon.py", output_path, output_workspace, remote_workspace]
    for fc_name in fc_names:
        args_array.append(fc_name)

    try :
        result = subprocess.check_output(args_array, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        arcpy.AddMessage(e.output)
        raise e
    
    arcpy.AddMessage(result)

    #re-enable locking
    arcpy.env.lockingEnabled = True