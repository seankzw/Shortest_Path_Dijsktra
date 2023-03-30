
from functools import partial
import re
import tkinter as tk
import customtkinter as ctk
from geopy.geocoders import Nominatim
from tkinter import END, messagebox
import tkintermapview as tkmv
from Coordinates import Coordinates
from brain import *


#? ===== Windows =====
windows = ctk.CTk() # Main Windows

#? ===== Frames =====
left_frame = ctk.CTkFrame(windows) # Create the left column for the input/label field
buttonFrame=ctk.CTkFrame(windows) # Buttom frame for Toggle and Create Path

right_frame = tk.Frame(windows) # Create the right column for the map

# Create mapview with right click options
mapview = tkmv.TkinterMapView(right_frame, width=800, height=900, corner_radius=0)

#? ===== Labels =====
userStartInputField = ctk.CTkEntry(left_frame, placeholder_text="Johor Zoo", width=250)
userEndInputField = ctk.CTkEntry(left_frame, placeholder_text="Paradigm Mall", width=250)

#? ===== Utilities =====
geolocator = Nominatim(user_agent="myApp") # For map

#? ===== Global variables =====
switch_var = ctk.StringVar(value="dark") # For switching appearance mode
chosenFromMap = False
counter = 1

#? ===== Helper method for the buttons =====
# This method is a helper for the toggle button
def change_appearance_mode():
    ctk.set_appearance_mode(switch_var.get())

#This method is a helper for polygon clicked on the map
def polygonClicked(polygon):
    messagebox.showinfo("showinfo", polygon.name)

# This method is a helper for the right click add start location
def add_start_loc(coord):
    clearMap()
    mapview.set_marker(coord[0],coord[1], text_color="red",
                                 marker_color_circle="white", marker_color_outside="green", font=("Helvetica Bold", 10))
    userStartInputField.delete(0,END)
    userStartInputField.insert(0,(str(coord[0]) + "," + str(coord[1])))
    return

# This method is a helper for the right click add end location
def add_end_loc(coord):
    clearMap()
    mapview.set_marker(coord[0],coord[1], text_color="red",
                                 marker_color_circle="white", marker_color_outside="blue", font=("Helvetica Bold", 10))
    userEndInputField.delete(0,END)
    userEndInputField.insert(0,(str(coord[0]) + "," + str(coord[1])))
    return

def getLatLngFromUserInput(textField, isStartLocation):
    inputField = textField.get()

    if inputField == '':
        # Show error message if empty
        if isStartLocation :
            messagebox.showinfo("Error", "Enter Start Location")
        else:
            messagebox.showinfo("Error", "Enter End Location")
    elif re.match("^-?[0-9].+$",inputField):
        return tuple(float(x) for x in inputField.split(","))
    else:
        inputLocation = geolocator.geocode(inputField, country_codes="MY")

        print(inputField + " JB MY")

        #Unable to find location
        if(inputLocation == None):
            messagebox.showinfo("Error", "Unable to find location, please try another location")

        # Location is out of boundary (Johor Bahru)
        if((inputLocation.latitude>=1.6800 or inputLocation.latitude<=1.3272)or(inputLocation.longitude>=104.0687 or inputLocation.longitude<=103.4301)):
            raise Exception(messagebox.showinfo("Error", "Location is not in Johor Bahru"))
        else:
            # create marker with custom colors and font
            color = "green"
            if not isStartLocation :
                color = "red"
            mapview.set_marker(inputLocation.latitude, inputLocation.longitude, text_color="red",
                                 marker_color_circle="white", marker_color_outside=color, font=("Helvetica Bold", 10))

    return (inputLocation.latitude, inputLocation.longitude)


def clearMap():
    mapview.delete_all_marker()
    mapview.delete_all_polygon()


def createPath(left_frame):
    #Clear markers and polygons on map
    clearMap()

    routesHeight = 280
    routesWidth = 550
    startLocation = getLatLngFromUserInput(userStartInputField, True) # get start location from input field
    endLocation = getLatLngFromUserInput(userEndInputField, False) # Get end location from input field

    overviewData = getOverviewData() # To gather all the data for retrieval
    path_list = [] # Contains the path to show in the routes display

    # Create three tabviews to switch between different routes
    routes_tabview = ctk.CTkTabview(left_frame)
    routes_tabview.grid(column=0, row=9, padx=10, pady=10, sticky="nsew")

    # Tab 1 - Route 1
    tab1 = routes_tabview.add("Least Walk")
    label1 = ctk.CTkLabel(tab1, justify="left", text="Directions for Least Walk:")
    label1.grid(column=0, row=8, sticky="w", padx=10)
    routes = ctk.CTkTextbox(tab1, width=routesHeight, height=routesWidth, scrollbar_button_color="white")
    routes.grid(column=0, row=10, sticky="nsew")


    # Tab 2 - Route 2
    tab2 = routes_tabview.add("Least Transfer")
    label2 = ctk.CTkLabel(tab2, justify="left", text="Directions for Least Transfer:")
    label2.grid(column=0, row=8, sticky="w", padx=10)
    routes2 = ctk.CTkTextbox(tab2, width=routesHeight, height=routesWidth, scrollbar_button_color="white")
    routes2.grid(column=0, row=10)


    # Tab 3 - Route 3
    tab3 = routes_tabview.add("Fastest")
    label3 = ctk.CTkLabel(tab3, justify="left", text="Directions for Fastest:")
    label3.grid(column=0, row=8, sticky="w", padx=10)
    routes3 = ctk.CTkTextbox(tab3, width=routesHeight, height=routesWidth, scrollbar_button_color="white")
    routes3.grid(column=0, row=10)



    # # To display the paths
    # label = ctk.CTkLabel(left_frame, justify="left", text="Directions:")
    # label.grid(column=0, row=8, sticky="w", padx=10)

    # # Show routes
    # routes = ctk.CTkTextbox(left_frame, width=250, height=350, scrollbar_button_color="white", )
    # routes.grid(column=0, row=9)

    print("location = {}".format(startLocation))
    print("location2 = {}".format(endLocation))
    print("location coord= {}".format(startLocation[0]))

    start_bus_stop = findNearestStop(Coordinates(startLocation[0], startLocation[1])) # Get nearest bus stop from start location
    end_bus_stops = findNearest5Stop(Coordinates(endLocation[0],endLocation[1])) # Get nearest bus stop from end location
    # get the address of end location based on geopy api
    endDestinationAddress = (geolocator.geocode(userEndInputField.get()).address).split(",")

    # Get distance between start and end
    distBetweenLoc = distanceBetween(Coordinates(startLocation[0], startLocation[1]), Coordinates(endLocation[0], endLocation[1]))

    #Get distance between start location and start bus stop
    distBetweenStartAndStop = distanceBetween(Coordinates(startLocation[0],startLocation[1]), getCoordFromBusStopName(start_bus_stop))
    print("Distance between locations = {} \nDistance between start and bus stop = {}".format(distBetweenLoc, distBetweenStartAndStop))

    print("============ Running Dijkstra ! ============")
    previous_node, shortest_path = dijkstra(start_bus_stop) # Run dijkstra to get all routes from start bus stop

    # path_to_destination contains shortest path to end bus stop
    # length contains the total distance travelled
    path_to_destination, length = getShortestPathFromList(previous_node,start_bus_stop, end_bus_stops, Coordinates(endLocation[0],endLocation[1]))
    print("LENGTH IS = {}".format(length))

    boundingBox = getBoundingBox(startLocation, endLocation)
    mapview.fit_bounding_box(boundingBox[0],boundingBox[1])

    # if distance between the start and end is more then 2, then consider taking bus
    if distBetweenLoc > 2:
        print("=============== Retrieving shortest bus route ===============")

        # Distance from start location to bus stop
        distanceFromLocToStop = distanceBetween(Coordinates(startLocation[0], startLocation[1]), Coordinates(overviewData[start_bus_stop]["lat"], overviewData[start_bus_stop]["lng"]))
        routes.insert(END, "Walk {:.2f}km to {} \n\n".format(distanceFromLocToStop, start_bus_stop))

        # Push the start location in the path list first
        path_list.append(startLocation)

        #Get all bus stops and append to path_list
        for eachStop in path_to_destination:
            buses = eachStop["bus"]
            #for eachBusOfStop in range(len(buses)):
            #    if eachBusOfStop not in buses:
            #        del eachBusOfStop

            #res, test = re.subn("[\[\]\']","",str(buses))
            #print("EAch stop is : {}".format(eachStop))
            busToTake = eachStop["bus_stop_name"] + " via \n" + " , ".join(buses)+ "\n\n"
            routes.insert(END, busToTake)
            path_list.append((float(eachStop["coordinates"][0]),float(eachStop["coordinates"][1])))

            # create marker with custom colors and font for this stop
            polygon_name = eachStop["bus_stop_name"] + "\n" + ",".join(buses)

            # Set polygon markers for all bus stops
            mapview.set_polygon([(eachStop["coordinates"][0], eachStop["coordinates"][1]), (eachStop["coordinates"][0], eachStop["coordinates"][1])], outline_color="red", border_width=12, command=polygonClicked, name=polygon_name)



            # Set marker from start and end location to start and end bus stop
            mapview.set_marker(path_to_destination[0]["coordinates"][0], path_to_destination[0]["coordinates"][1], "Walk to " + path_to_destination[0]["bus_stop_name"], marker_color_circle="white", marker_color_outside="blue" )
            mapview.set_marker(path_to_destination[-1]["coordinates"][0], path_to_destination[-1]["coordinates"][1], "Walk to " + endDestinationAddress[0], marker_color_circle="white", marker_color_outside="blue")

        # Distance between bus stop and end location
        distanceFromStopToDest = distanceBetween(Coordinates(path_to_destination[-1]['coordinates'][0], path_to_destination[-1]['coordinates'][1]), Coordinates(endLocation[0], endLocation[1]))
        routes.insert(END, "Walk {:.2f}km from {} to {}".format(distanceFromStopToDest, path_to_destination[-1]["bus_stop_name"], endDestinationAddress[0]))

        # calculate the time taken for the route
        totalTimeTaken = getTimeTaken(distanceFromLocToStop, 5.0) + getTimeTaken(length, 20.5) + getTimeTaken(distanceFromStopToDest, 5.0)
        timeTakenFormat = TimeFormatter(totalTimeTaken)
        labelTimeTaken = ctk.CTkLabel(tab1, justify="left", text="Time taken: " + timeTakenFormat)
        labelTimeTaken.grid(column=0, row=9, sticky="w", padx=10)

        path_list.append(endLocation)
    else:
        print("=============== Walk is nearer ===============")
        # WALK TO DESTINATION
        endstop = geolocator.geocode(endLocation, country_codes="MY")
        walkTo = ""
        if endstop == None:
            walkTo = "({:.4f},{:.4f})".format(endLocation[0], endLocation[1])
        else:
            walkTo = endstop

        # Set marker from start and end location to start and end bus stop
        routes.insert(END, "Walk {:.2f}km to {} \n\n".format(distBetweenStartAndStop, walkTo))

    # set routes to be disabled state so text field cannot be edited
    routes.configure(state=tk.DISABLED)

def button_event():
    global counter
    if counter < 5:
        busTiming = getBusTiming()
        displayTime = "Bus timing of the first bus stop of every bus number\n\n"
        for i in busTiming:
            displayTime += i + " : " + ", ".join(busTiming[i]) + "\n\n"
        top = ctk.CTkToplevel()
        top.title('Bus Timings')
        label = ctk.CTkLabel(top, text=displayTime)
        label.grid(column=0, row=0, padx=10, sticky="w")

        counter += 1
    else:
        messagebox.showinfo("Error", "You have opened too many windows")

#Initialising Windows Configuration
def initWindows():
    #windows = ctk.CTk()
    windows.geometry("900x900") # Size of window
    windows.title("CSC1108 Johor Bahru Maps") # Title of the window
    windows.resizable(0,0) # prevent the resize of window
    windows.iconphoto(False, tk.PhotoImage(file="compass.png")) # Custom image icon for the project
    ctk.CTkFont("Helvetica") # Font of the window

    ctk.set_default_color_theme("green") # Green apperance accent colour
    ctk.set_appearance_mode("dark") # Apperance mode of the program

    left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10) # Place left_frame position

    # Right frame configuration
    right_frame.pack(side="left", fill="both", expand=True)
    right_frame.columnconfigure(0, weight=1)
    right_frame.rowconfigure(0, weight=1)

    # Create the label Start Location
    label = ctk.CTkLabel(left_frame,justify="left", text="Enter your start location:")
    label.grid(column=0, row=0, padx=10, sticky="w")

    userStartInputField.grid(column=0, row=1, padx=10, pady=10, sticky="w") # Pack and position userInputField (Start Location)

    # Create the label End Location
    label2 = ctk.CTkLabel(left_frame, justify="left",text="Enter your end location:")
    label2.grid(column=0, row=2, padx=10, sticky="w")

    # Create the input field for End Location
    userEndInputField.grid(column=0, row=3, padx=10, pady=10, sticky="w")

    # Toggle button for apperance mode
    toggleAndPath= ctk.CTkSwitch(left_frame, text="Dark Mode",command=change_appearance_mode, variable=switch_var, onvalue="dark",offvalue="light")
    toggleAndPath.grid(row=5, column=0, sticky="w", padx=10, pady=10)

    #Create path button
    action_with_arg= partial(createPath, left_frame)
    button3 = ctk.CTkButton(left_frame, text="Create Path", command=action_with_arg)
    button3.grid(column=0, row=5, columnspan=10,sticky="e")

    # Button for bus timings
    button = ctk.CTkButton(master=windows, text="Bus Timings", command=button_event, width=120, height=32, border_width=0, corner_radius=8)
    button.place(relx=0.9, rely=0.05, anchor=tk.CENTER)

    # Map view configurations
    mapview.add_right_click_menu_command(label="Add start location", command=add_start_loc, pass_coords=True)
    mapview.add_right_click_menu_command(label="Add end location", command=add_end_loc, pass_coords=True)
    mapview.set_address("JB, MY")
    mapview.set_zoom(12)
    mapview.grid(row=0, column=0, sticky="nsew")

    windows.mainloop()


initWindows()