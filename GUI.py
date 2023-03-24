
from functools import partial
import re
import tkinter as tk
import customtkinter as ctk
from geopy.geocoders import Nominatim
from geopy import distance
from tkinter import BOTH, BOTTOM, END, RIGHT, YES, Image, Scrollbar, messagebox
import tkintermapview as tkmv
from Coordinates import Coordinates
from brain import *




windows = ctk.CTk()
windows.geometry("800x600")
windows.title("CSC1108 Johor Bahru Maps")
windows.iconphoto(False, tk.PhotoImage(file="compass.png"))
ctk.CTkFont("Helvetica")
geolocator = Nominatim(user_agent="myApp")

# Create Window
ctk.set_default_color_theme("green")
ctk.set_appearance_mode("dark")


# Create the left column for the input/label field
left_frame = ctk.CTkFrame(windows)
left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# Create the label and input field for Start Location
label = ctk.CTkLabel(left_frame,justify="left", text="Enter your start location:")
label.grid(column=0, row=0, padx=10, sticky="w")

# Create the input field for Start Location
userInputLocation = ctk.CTkEntry(left_frame, placeholder_text="Johor Zoo", width=250)
userInputLocation.grid(column=0, row=1, padx=10, pady=10)

# Create the label and input field for End Location
label2 = ctk.CTkLabel(left_frame, justify="left",text="Enter your end location:")
label2.grid(column=0, row=2, padx=10, sticky="w")

# Create the input field for End Location
userInputLocation2 = ctk.CTkEntry(left_frame, placeholder_text="Paradigm Mall", width=250)
userInputLocation2.grid(column=0, row=3, padx=10, pady=10)

switch_var = ctk.StringVar(value="dark")
def change_appearance_mode():
    ctk.set_appearance_mode(switch_var.get())
# Mode switcher ?
#testMenu = ctk.CTkOptionMenu(left_frame, values=["Dark", "Light", "System"], command=change_appearance_mode)
together=ctk.CTkFrame(windows)
testMenu = ctk.CTkSwitch(left_frame, text="Dark Mode",command=change_appearance_mode, variable=switch_var, onvalue="dark",offvalue="light")
testMenu.grid(row=5, column=0, sticky="w", padx=10, pady=10)
# Create the label and input field for End Location

# # define global variables to store latitude and longitude
# start_lat, start_long = None, None
# end_lat, end_long = None, None

def getStartLatLong():
    userLoc = userInputLocation.get()
    # global start_lat, start_long
    if userLoc == '':
        messagebox.showinfo("showinfo", "Please enter Start Location")
    elif re.match("^-?[0-9].+$",userLoc):
        print("User key in as coordinate")
        return tuple(float(x) for x in userLoc.split(","))
    else:
        startLocation = geolocator.geocode(userLoc, country_codes="MY")

        if(startLocation == None):  # When user enters in an non-existent place
            messagebox.showinfo("showinfo", "Unable to find start location, please try another location")
        if((startLocation.latitude>=1.6800 or startLocation.latitude<=1.3272)or(startLocation.longitude>=104.0687 or startLocation.longitude<=103.4301)):
            raise Exception(messagebox.showinfo("showinfo", "Location is not in Johor Bahru"))
        else:
            print(str(startLocation.latitude) +
                ", " + str(startLocation.longitude))

            # create marker with custom colors and font
            mapview.set_marker(startLocation.latitude, startLocation.longitude)
    return (startLocation.latitude, startLocation.longitude)


def getEndLatLong():
    userLoc2 = userInputLocation2.get()
    # global end_lat, end_long
    if userLoc2 == '':
        messagebox.showinfo("showinfo", "Enter End Location")
    elif re.match("^-?[0-9].+$",userLoc2):
        print("User key in as coordinate")
        return tuple(float(x) for x in userLoc2.split(","))
    else:
        endLocation = geolocator.geocode(userLoc2, country_codes="MY")

        print(userLoc2 + " JB MY")
        if(endLocation == None):
            messagebox.showinfo("showinfo", "Unable to find end location, please try another location")
        if((endLocation.latitude>=1.6800 or endLocation.latitude<=1.3272)or(endLocation.longitude>=104.0687 or endLocation.longitude<=103.4301)):
            raise Exception(messagebox.showinfo("showinfo", "Location is not in Johor Bahru"))
        else:
            # create marker with custom colors and font
            mapview.set_marker(endLocation.latitude, endLocation.longitude, text_color="red",
                                 marker_color_circle="white", marker_color_outside="green", font=("Helvetica Bold", 10))

    return (endLocation.latitude, endLocation.longitude)
         # store latitude and longitude in global variables
        # end_lat, end_long = location.latitude, location.longitude

def polygonClicked(polygon):
    messagebox.showinfo("showinfo", polygon.name)


def createPath(left_frame):
    # remove all existing markers and points whenever createPath() is invoked
    mapview.delete_all_marker()
    mapview.delete_all_polygon()

    location = getStartLatLong()
    location2 = getEndLatLong()
    overviewData = getOverviewData()
    path_list = []

    # To display the paths
    label = ctk.CTkLabel(left_frame, width=250, justify="left", text="Directions:")
    label.grid(column=0, row=8)
    routes = ctk.CTkTextbox(left_frame, width=250, height=350, scrollbar_button_color="white", )
    routes.grid(column=0, row=9)
    #routes.place(x=10, y=200)
    #routes.rowconfigure(5, weight=1)
    #routes.columnconfigure(1, weight=1)

    print("location = {}".format(location))
    print("location2 = {}".format(location2))
    print("location coord= {}".format(location[0]))

    start_bus_stop = findNearestStop(Coordinates(location[0], location[1]))
    end_bus_stops = findNearest5Stop(Coordinates(location2[0],location2[1]))

    distBetweenLoc = distanceBetween(Coordinates(location[0], location[1]), Coordinates(location2[0], location2[1]))
    distBetweenStartAndStop = distanceBetween(Coordinates(location[0],location[1]), getCoordFromBusStopName(start_bus_stop))
    print("Distance between locations = {} \nDistance between start and bus stop = {}".format(distBetweenLoc, distBetweenStartAndStop))

    #if distBetweenLoc > 1:
    print("============ Running Dijkstra ! ============")
#if True:
    previous_node, shortest_path = dijkstra(start_bus_stop)

    #Original code :
    #path_to_destination = getShortestPath(previous_node, shortest_path, start_bus_stop, end_bus_stop)

    print("===== location[0], location[1] = {}, {}".format(location[0],location[1]))
    print("===== location2[0], location2[1] = {}, {}".format(location2[0],location2[1]))

    path_to_destination, length = getShortestPathFromList(previous_node,start_bus_stop, end_bus_stops, Coordinates(location2[0],location2[1]))
    endBusStopCoordinate = getCoordFromBusStopName(path_to_destination[-1]["bus_stop_name"])

    #if distBetweenLoc < distBetweenStartAndStop or distBetweenLoc > distanceBetween(endBusStopCoordinate, Coordinates(location2[0], location2[1])):
    if distBetweenLoc > 2:
        boundingBox = getBoundingBox(location, location2)
        mapview.fit_bounding_box(boundingBox[0],boundingBox[1])
        #mapview.fit_bounding_box(location2, location)

        #routes = ctk.CTkTextbox(left_frame)
        #routes.place(x=10, y=115)
        #routes.rowconfigure(2, weight=1)
        #routes.columnconfigure(1, weight=1)

        distanceFromLocToStop = distanceBetween(Coordinates(location[0], location[1]), Coordinates(overviewData[start_bus_stop]["lat"], overviewData[start_bus_stop]["lng"]))
        routes.insert(END, "Walk {:.2f}km to {} \n\n".format(distanceFromLocToStop, start_bus_stop))

        path_list.append(location)
        for eachStop in path_to_destination:
            buses = eachStop["bus"]
            for eachBusOfStop in range(len(buses)):
                if eachBusOfStop not in buses:
                    del eachBusOfStop

            res, test = re.subn("[\[\]\']","",str(buses))
            busToTake = eachStop["bus_stop_name"] + " via \n" + res + "\n\n"
            routes.insert(END, busToTake)
            path_list.append((float(eachStop["coordinates"][0]),float(eachStop["coordinates"][1])))

            # create marker with custom colors and font for this stop
            polygon_name = eachStop["bus_stop_name"] + "\n" + res
            print(path_to_destination[-1])

            mapview.set_polygon([(eachStop["coordinates"][0], eachStop["coordinates"][1]), (eachStop["coordinates"][0], eachStop["coordinates"][1])], outline_color="red", border_width=12, command=polygonClicked, name=polygon_name)

            mapview.set_marker(path_to_destination[0]["coordinates"][0], path_to_destination[0]["coordinates"][1], "Walk to " + path_to_destination[0]["bus_stop_name"], marker_color_circle="white", marker_color_outside="blue" )
            mapview.set_marker(path_to_destination[-1]["coordinates"][0], path_to_destination[-1]["coordinates"][1], "Walk to " + userInputLocation2.get(), marker_color_circle="white", marker_color_outside="blue")

        path_list.append(location2)
    else:
        print("=========== Walk is nearer ===============")
        # WALK TO DESTINATION
        endstop = geolocator.geocode(location2, country_codes="MY")
        routes.insert(END, "Walk {:.2f}km to {} \n\n".format(distBetweenStartAndStop, location2 if endstop == None else endstop))

    routes.configure(state=tk.DISABLED)


def add_start_loc(coord):
    userInputLocation.delete(0,END)
    userInputLocation.insert(0,(str(coord[0]) + "," + str(coord[1])))
    return

def add_end_loc(coord):
    userInputLocation2.delete(0,END)
    userInputLocation2.insert(0,(str(coord[0]) + "," + str(coord[1])))
    return


# Create the "Create Path" button to create the path
action_with_arg= partial(createPath, left_frame)
button3 = ctk.CTkButton(left_frame, text="Create Path", command=action_with_arg)
button3.grid(column=0, row=5, columnspan=10,sticky="e")

# Create the right column for the map
right_frame = tk.Frame(windows)
right_frame.pack(side="left", fill="both", expand=True)
right_frame.columnconfigure(0, weight=1)
right_frame.rowconfigure(0, weight=1)

# Create mapview with right click options
mapview = tkmv.TkinterMapView(right_frame, width=800, height=600, corner_radius=0)
mapview.add_right_click_menu_command(label="Add start location", command=add_start_loc, pass_coords=True)
mapview.add_right_click_menu_command(label="Add end location", command=add_end_loc, pass_coords=True)
mapview.set_address("JB, MY")
mapview.set_zoom(12)
mapview.grid(row=0, column=0, sticky="nsew")


# prevent the resize of window
windows.resizable(0,0)

# Start the main loop
windows.mainloop()