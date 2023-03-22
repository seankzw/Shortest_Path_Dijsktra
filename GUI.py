
from functools import partial
import re
import pandas as pd
import tkinter as tk
from geopy.geocoders import Nominatim
from geopy import distance
from tkinter import BOTH, END, YES, Listbox, Text, messagebox
import tkintermapview as tkmv

from Coordinates import Coordinates
from brain import distanceBetween, findNearest5Stop, findNearestStop
from main import dijkstra, getOverviewData, getShortestPathFromList

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
    userLoc = userInputLocation.get()
    # global start_lat, start_long
    if userLoc == '':
        messagebox.showinfo("showinfo", "Please enter Start Location")
    else:
        startLocation = geolocator.geocode(userLoc + " JB MY")
        #startLocLatLng = [startLocation.latitude, startLocation.longitude]

        if(startLocation == None):  # When user enters in an non-existent place
            messagebox.showinfo("showinfo", "Unable to find start location, please try another location")
        if(startLocation.latitude == 1.4525798 and startLocation.longitude == 103.769116):  # When user enters in Singapore
            messagebox.showinfo("showinfo", "Please enter a location in Johor Bahru")
        # if(float(startLocation.latitude) > 1.6800) or (float(startLocation.longitude) > 104.0687) or (float(startLocation.latitude) < 1.3272) or (float(startLocation.longitude) < 103.4301):
        #     messagebox.showinfo("showinfo", "Please enter a location within Johor Bahru")
        else:
            #label_lat = tk.Label(windows, text=startLocation.latitude)
            #label_lat.pack()
            #label_long = tk.Label(windows, text=startLocation.longitude)
            #label_long.pack()
            #messagebox.showinfo('LWHwqeewqewqewqeqewewqewq', startLocation.address)
            print(str(startLocation.latitude) + ", " + str(startLocation.longitude))

            # create marker with custom colors and font
            mapview.set_marker(startLocation.latitude, startLocation.longitude)
    return (startLocation.latitude, startLocation.longitude)
        # store latitude and longitude in global variables
        # start_lat, start_long = startLocation.latitude, startLocation.longitude


def getEndLatLong():
    userLoc2 = userInputLocation.get()
    # global end_lat, end_long
    if userLoc2 == '':
        messagebox.showinfo("showinfo", "Enter End Location")

    else:
        endLocation = geolocator.geocode(userLoc2 + " JB MY")
        print(userLoc2 + " JB MY")
        
        if(endLocation == None):
            messagebox.showinfo("showinfo", "Unable to find end location, please try another location")
        if(endLocation.latitude == 1.4525798 and endLocation.longitude == 103.769116):  # When user enters in Singapore
            messagebox.showinfo("showinfo", "Please enter a location in Johor Bahru")
        else:
            #label_lat = tk.Label(windows, text=location.latitude)
            #label_lat.pack()
            #label_long = tk.Label(windows, text=location.longitude)
            #label_long.pack()
            #messagebox.showinfo('Location', location.address)
            #print(str(location.latitude) + ", " + str(location.longitude))

            # create marker with custom colors and font
            mapview.set_marker(endLocation.latitude, endLocation.longitude, text_color="green",
                                 marker_color_circle="white", marker_color_outside="green", font=("Helvetica Bold", 10))

    return (endLocation.latitude, endLocation.longitude)
         # store latitude and longitude in global variables
        # end_lat, end_long = location.latitude, location.longitude




def createPath(left_frame):
    # delete all markers and points whenever createPath is invoked
    mapview.delete_all_marker()
    mapview.delete_all_polygon()
    
    location = getStartLatLong()
    location2 = getEndLatLong()
    overviewData = getOverviewData()
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

    routes = tk.Text(left_frame)
    routes.place(x=10, y=115)
    routes.rowconfigure(2, weight=1)
    routes.columnconfigure(1, weight=1)
    for i in path_to_destination:
        busToTake = i["bus_stop_name"] + "\n"
        routes.insert(END, busToTake)

    distanceFromLocToStop = distanceBetween(Coordinates(location[0], location[1]), Coordinates(overviewData[start_bus_stop]["lat"], overviewData[start_bus_stop]["lng"]))
    routes.insert(END, "Walk {:.2f}km to {} \n\n".format(distanceFromLocToStop, start_bus_stop))

    #eachKeys = path_to_destination.keys()
    print(len(path_to_destination))

    #for i in path_to_destination:
    #    buses=i["bus"]
    #    for eachBusOfStop in range(len(i["bus"])):
    #        if eachBusOfStop not in buses:
    #            del eachBusOfStop

    #    busToTake = i["bus_stop_name"] + str(buses) + "\n\n"
    #    routes.insert(END, busToTake)


        #listbox.insert(counter, i["bus_stop_name"])
    #print(listbox)
    #listbox.pack()

    print(len(path_to_destination))
    path_list.append(location)
    for eachStop in path_to_destination:
        buses = eachStop["bus"]
        for eachBusOfStop in range(len(buses)):
            if eachBusOfStop not in buses:
                del eachBusOfStop

        res, test = re.subn("[\[\]\']","",str(buses))
        busToTake = eachStop["bus_stop_name"] + " via \n " + res + "\n\n"
        routes.insert(END, busToTake)
        #print(eachStop["coordinates"])
        path_list.append((float(eachStop["coordinates"][0]),float(eachStop["coordinates"][1])))
    #  create marker with custom colors and font for this stop
        #mapview.set_marker(eachStop["coordinates"][0],eachStop["coordinates"][1], text_color="red",
        #                         marker_color_circle="white", marker_color_outside="red", font=("Helvetica Bold", 10))
        mapview.set_polygon([(eachStop["coordinates"][0], eachStop["coordinates"][1]), (eachStop["coordinates"][0], eachStop["coordinates"][1])],
            outline_color="red")


    routes["state"] = tk.DISABLED
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