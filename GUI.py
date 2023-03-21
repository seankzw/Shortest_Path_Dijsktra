
from functools import partial
import pandas as pd
import tkinter as tk
from geopy.geocoders import Nominatim
from geopy import distance
from tkinter import BOTH, END, YES, Listbox, Text, messagebox
import tkintermapview as tkmv

from Coordinates import Coordinates
from brain import findNearest5Stop, findNearestStop
from main import dijkstra, getShortestPathFromList

# Create Window
windows = tk.Tk()
windows.geometry("800x600")
windows.title("Maps")

geolocator = Nominatim(user_agent="myApp")


# Create the left column for the input/label field
left_frame = tk.Frame(windows)
left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
left_frame.rowconfigure(3, weight=1)

# Create the label and input field for Start Location
label = tk.Label(left_frame, text="Enter your start location:")
label.grid(column=0, row=0, pady=10)

# Create the input field for Start Location
userInputLocation = tk.Entry(left_frame, width=20)
userInputLocation.grid(column=1, row=0, padx=10, pady=10)

# Create the label and input field for End Location
label2 = tk.Label(left_frame, text="Enter your end location:")
label2.grid(column=0, row=1, pady=10)

# Create the input field for End Location
userInputLocation2 = tk.Entry(left_frame, width=20)
userInputLocation2.grid(column=1, row=1, padx=10, pady=10)

# Create the label and input field for End Location

# # define global variables to store latitude and longitude
# start_lat, start_long = None, None
# end_lat, end_long = None, None

def getStartLatLong():
    # global start_lat, start_long
    if userInputLocation.get() == '':
        messagebox.showinfo("showinfo", "Enter Start Location")
    else:
        startLocation = geolocator.geocode(userInputLocation.get() + " JB MY")
        print(userInputLocation.get() + " JB MY")
        if(startLocation == None):
            messagebox.showinfo("showinfo", "Unable to find start location, please try another location")
        else:
            label_lat = tk.Label(windows, text=startLocation.latitude)
            label_lat.pack()
            label_long = tk.Label(windows, text=startLocation.longitude)
            label_long.pack()
            messagebox.showinfo('LWHwqeewqewqewqeqewewqewq', startLocation.address)
            print(str(startLocation.latitude) +
                ", " + str(startLocation.longitude))

            # create marker with custom colors and font
            mapview.set_marker(startLocation.latitude, startLocation.longitude)
    return (startLocation.latitude, startLocation.longitude)
        # store latitude and longitude in global variables
        # start_lat, start_long = startLocation.latitude, startLocation.longitude


def getEndLatLong():
    # global end_lat, end_long
    if userInputLocation2.get() == '':
        messagebox.showinfo("showinfo", "Enter End Location")

    else:
        location = geolocator.geocode(userInputLocation2.get() + " JB MY")
        print(userInputLocation2.get() + " JB MY")
        if(location == None):
            messagebox.showinfo("showinfo", "Unable to find end location, please try another location")
        else: 
            label_lat = tk.Label(windows, text=location.latitude)
            label_lat.pack()
            label_long = tk.Label(windows, text=location.longitude)
            label_long.pack()
            messagebox.showinfo('Location', location.address)
            print(str(location.latitude) + ", " + str(location.longitude))

            # create marker with custom colors and font
            mapview.set_marker(location.latitude, location.longitude, text_color="green",
                                 marker_color_circle="white", marker_color_outside="green", font=("Helvetica Bold", 10))

    return (location.latitude, location.longitude)
         # store latitude and longitude in global variables
        # end_lat, end_long = location.latitude, location.longitude




def createPath(left_frame):
    location = getStartLatLong()
    location2 = getEndLatLong()
    path_list = []

    #start_loc = Coordinates(1.5423777121603113, 103.62969894227055) #AEON
    #end_loc = Coordinates(1.6349379250179437, 103.66630691168017) # Senai Airport Terminal

    start_bus_stop = findNearestStop(Coordinates(location[0], location[1]))
    #end_bus_stop = findNearestStop(Coordinates(location2[0],location2[1]))
    end_bus_stops = findNearest5Stop(Coordinates(location2[0],location2[1]))

    previous_node, shortest_path = dijkstra(start_bus_stop)

    #Original code :
    #path_to_destination = getShortestPath(previous_node, shortest_path, start_bus_stop, end_bus_stop)

    path_to_destination, length = getShortestPathFromList(previous_node,start_bus_stop, end_bus_stops, Coordinates(location2[0],location2[1]))

<<<<<<< Updated upstream
    routes = Text()
    #routes.grid(column=0, row=2, pady=10)
=======
    routes = tk.Text(left_frame)
    routes.place(x=10, y=115)
    routes.rowconfigure(2, weight=1)
    routes.columnconfigure(1, weight=1)
>>>>>>> Stashed changes
    for i in path_to_destination:
        busToTake = i["bus_stop_name"] + "\n"
        routes.insert(END, busToTake)


        #listbox.insert(counter, i["bus_stop_name"])
    routes["state"] = tk.DISABLED
    #print(listbox)
    #listbox.pack()

    path_list.append(location)
    for eachStop in path_to_destination:
        #print(eachStop["coordinates"])
        path_list.append((float(eachStop["coordinates"][0]),float(eachStop["coordinates"][1])))
    #  create marker with custom colors and font for this stop
        #mapview.set_marker(eachStop["coordinates"][0],eachStop["coordinates"][1], text_color="red",
        #                         marker_color_circle="white", marker_color_outside="red", font=("Helvetica Bold", 10))
        mapview.set_polygon([(eachStop["coordinates"][0], eachStop["coordinates"][1]), (eachStop["coordinates"][0], eachStop["coordinates"][1])],
            outline_color="red")


    path_list.append(location2)
    print("Length is {}".format(length))

    #path = mapview.set_path(path_list)
    #mapview.set_path(path_list)
    #path.set_color("blue")

    #if location and location2:
    #    path = mapview.set_path([location, location2])
    #    path.set_color("blue")

# def createPath():
#     # call getStartLatLong() and getEndLatLong() to set global variables
#     getStartLatLong()
#     getEndLatLong()

#     # access global variables to set the path
#     if start_lat and start_long and end_lat and end_long:
#         path = mapview.set_path([(start_lat, start_long), (end_lat, end_long)])
#         path.set_color("blue")



# Create the "Create Path" button to create the path
action_with_arg = partial(createPath, left_frame)
button3 = tk.Button(left_frame, text="Create Path", command=action_with_arg)
button3.grid(column=0, row=2)

# Create the right column for the map
right_frame = tk.Frame(windows)
right_frame.pack(side="left", fill="both", expand=True)
right_frame.columnconfigure(0, weight=1)
right_frame.rowconfigure(0, weight=1)

# Create mapview
mapview = tkmv.TkinterMapView(right_frame, width=800, height=600, corner_radius=0)
mapview.set_address("JB, MY")
mapview.set_zoom(12)
mapview.grid(row=0, column=0, sticky="nsew")


    # location = geolocator.geocode(userInputLocation.get() + " JB MY")
    # location2 = geolocator.geocode(userInputLocation2.get() + " JB MY")

    # print("Creating path...")
    # start_lat = getStartLatLong.location.latitude
    # start_lon = getStartLatLong.startLocation.longitude
    # end_lat = getEndLatLong.location.latitude
    # end_lon = getEndLatLong.location.longitude

    # # create the path
    # path = mapview.set_path([(start_lat, start_lon), (end_lat, end_lon)])

# set a path

# path_1.add_position(...)
# path_1.remove_position(...)
# path_1.delete()




# Start the main loop
windows.mainloop()