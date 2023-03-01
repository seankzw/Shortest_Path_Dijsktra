import pandas as pd
import tkinter as tk
from geopy.geocoders import Nominatim
from geopy import distance
from tkinter import messagebox 
import tkintermapview as tkmv


windows = tk.Tk()
windows.geometry("800x600")
windows.title("Maps")

geolocator = Nominatim(user_agent="myApp")

# Create the left column for the input/label field
left_frame = tk.Frame(windows)
left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
left_frame.rowconfigure(1, weight=1)

# Create the label and input field
label = tk.Label(left_frame, text="Enter your start location:")
label.grid(column=0, row=0, pady=10)

# Create the input field
userInputLocation = tk.Entry(left_frame, width=20)
userInputLocation.grid(column=1, row=0, padx=10, pady=10)




def getLatLong():
    location = geolocator.geocode(userInputLocation.get() + " JB MY")
    print(userInputLocation.get() + " JB MY")
    label_lat = tk.Label(windows, text=location.latitude)
    label_lat.pack()
    label_long = tk.Label(windows, text=location.longitude)
    label_long.pack()
    messagebox.showinfo('Location', location.address)
    print(str(location.latitude) + ", " + str(location.longitude))
    

# Create the "Enter" button
button = tk.Button(left_frame, text="Enter", command=getLatLong)
button.grid(column=1, row=1)


# Create the right column for the map
right_frame = tk.Frame(windows)
right_frame.pack(side="left", fill="both", expand=True)
right_frame.columnconfigure(0, weight=1)
right_frame.rowconfigure(0, weight=1)

# Create mapview
mapview = tkmv.TkinterMapView(right_frame, width=800, height=600, corner_radius=0)
mapview.grid(row=0, column=0, sticky="nsew")





    
# Start the main loop
windows.mainloop()
