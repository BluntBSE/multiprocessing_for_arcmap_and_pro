This simple repository shows how multiprocessing can be leveraged in ArcMap and ArcGIS Pro to reduce the processing times of geoprocessing tools.
I hope to write more material on the topic in the future, but hope what I have assembled here can be of use.
Interested users are encouraged to write to ram.news1@gmail.com. If you are an Arcadis user, you can reach me at robert.meyer@arcadis.com.

HOW TO USE THIS DEMO:
1. Open ArcMap
2. Create a new toolbox
3. Create a new script tool
4. Set the script tool to point to "demo.py"
5. Choose whether to run "demo" or "mp_demo" in the main body of the script.
6. Run the script tool with no parameters. Compare the different processing times of "demo" vs "mp_demo"
7. Inspect "advanced.py" and "advanced_daemon.py" to see how to do real geoprocessing tasks.

The included powerpoint shows diagrams and a brief explanation of how multiprocessing works in the context of ArcMap.
