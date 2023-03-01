import pandas as pd
import tkinter
from geopy.geocoders import Nominatim
from geopy import distance
from tkinter import messagebox
window = tkinter.Tk()

#to rename the title of the window
window.title("GUI")

# Size of windows
window.geometry('450x350')

geolocator = Nominatim(user_agent="myApp")

# df2 = pd.DataFrame({'Location':
#             ['Jalan Abu Bakar, JB, MY',
#              'Larkin Terminal, JB, MY']})

# df2[['location_lat', 'location_long']] = df2['Location'].apply(
#     geolocator.geocode).apply(lambda x: pd.Series(
#         [x.latitude, x.longitude], index=['location_lat', 'location_long']))
# Getting distance between 2 location
location1 = (1.4964559999542668, 103.74374661113058)
location2 = (1.491850778809332, 103.740872550932728)
print(distance.distance(location1, location2).km)

label1 = tkinter.Label (window, text="Route Finder")
label1.grid(column=0, row=0)

def getLatLong():
    location = geolocator.geocode(userInputLocation.get() + " JB MY")
    print(userInputLocation.get() + " JB MY")
    label3 = tkinter.Label (window, text=location.latitude)
    label3.grid(column=0, row=3)
    label4 = tkinter.Label (window, text=location.longitude)
    label4.grid(column=1, row=3)
    tkinter.messagebox.showinfo('Location',location.address)
    print(str(location.latitude) + ", " + str(location.longitude))

label2 = tkinter.Label (window, text="Enter your start location")
label2.grid(column=0, row=1)
userInputLocation = tkinter.Entry(window,width = 20)
userInputLocation.grid(column=1, row=1)

bt1 = tkinter.Button(window, text="Enter", command=getLatLong)
bt1.grid(column=2, row=1)

window.mainloop()