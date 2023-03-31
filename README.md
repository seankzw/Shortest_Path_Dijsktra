CSC1108_Project
Run the project at GUI.py.
If there are several scrbbling lines at the top of the file, download the several python packages needed;

For GUI.py: 
The python packages that are needed are 're', 'geopy', 'PIL', 'tkinter', 'tkintermapview' and 'customtkinter';

GUI.py define the frontend stuffs like generating the map and plotting of bus-stops according to the shortest path;

brain.py define the methods used to perform computation such as the dijkstra shortest path algorithm;

Coordinates.py define a class named 'Coordinates' to store the latiude and longtiude as attributesof a coordinate;

json_generator.py define methods that help to transform the data retrieved from the bus_stops.xlsx into json file;

CollatedDataHelper.py define a class named 'CollatedDataHelper' with methods that read and retrieve the data from the json file we generated at json_generator.py;

collated_datav2.json is a json file that contain data that will be used in the project.