import multiprocessing
import os
import sys
import arcpy

#This example shows how to iterate through feature classes and create a simple table from each one using multiprocessing.

def process_feature_class(args):
    [fc_name, output_path, output_workspace, remote_workspace] = args
    fc_name_underscored = fc_name.replace(".", "_")
    gdb_name = fc_name_underscored + ".gdb"
    scratch_name = fc_name_underscored+"_scratch.gdb"
    gdb_path = os.path.join(output_path, gdb_name)
    fc_gdb = arcpy.CreateFileGDB_management(output_path, gdb_name)
    arcpy.env.workspace = gdb_path
    arcpy.env.scratchWorkspace = scratch_name
    arcpy.env.overwriteOutput = True
    arcpy.env.lockingEnabled = False
    print("Created GDB at " + gdb_path)
    fc_classname = fc_name_underscored + "_fc"
    fc_path = os.path.join(gdb_path, fc_classname)

    remote_feature = os.path.join(remote_workspace, fc_name)
    print("Remote feature is:")
    print(remote_feature)

    table_name = fc_name_underscored + "_table"

    event_table = arcpy.TableToTable_conversion(
        in_rows=remote_feature, out_path=fc_gdb, out_name=table_name, where_clause="ToDate IS NULL", config_keyword="")

    arcpy.Copy_management(event_table, os.path.join(
        output_workspace, table_name))

    arcpy.env.workspace = output_workspace
    arcpy.env.scratchWorkspace = os.path.join(output_path, "Scratch.gdb")

    # Compact the gdb at gdb_path to release locks
    arcpy.Compact_management(gdb_path)


if __name__ == '__main__':
    print("The Daemon manager is running")
    # Makes sure that the python executable is the same as the one that is running the script. This uses the ArcMap/Pro python executable without
    # Accessing the ArcMap UI, which does not work with multiprocessing
    print(sys.executable)
    py_prefix = sys.exec_prefix
    print(py_prefix)
    py_path = os.path.join(py_prefix, "python.exe")
    print(py_path)
    multiprocessing.set_executable(py_path)

    # Inherits the arguments from main.py
    args = []
    for arg in sys.argv:
        args.append(arg)

    # This section requires customization per use case.
    output_path = args[1]
    output_workspace = args[2]
    # This is the connection where you are getting event layers , such as 'FunctionalSystem', from. AKA: 'QAEdit'
    remote_workspace = args[3]
    strings = args[4:]
    worker_args = [[string, output_path, output_workspace,
                    remote_workspace] for string in strings]
    # Breaking your computer? Set a max workers here. Try 4-8.
    p = multiprocessing.Pool(maxtasksperchild=1)
    p.map(process_feature_class, worker_args)
    p.close()
    p.join()
    ##You may or may not want to run a "clean up" step either here, or in the process_feature_class() function
