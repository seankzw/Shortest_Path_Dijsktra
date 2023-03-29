from datetime import datetime
import json

def checkBusTime(busNo):
    # Load json with bus timings
    f = open("bus_timings.json")
    data = json.load(f)

    for eachBus in data:
        print("Bus number:" ,eachBus)
        print("Bus timing: ", data[eachBus]["bus_timing"])
        print("First bus:" , data[eachBus]["bus_timing"][0])
        print("Last bus:" , data[eachBus]["bus_timing"][-1])

    # Get current time
    current_date_and_time = datetime.now()
    time_now = datetime.now()
    current_time = time_now.strftime("%H:%M:%S")

    # Compare current time to bus timings to get next bus time
    # First, see if timing is within First and Last bus timing
    # If within, go through the array to find closest timing. Must be greater than current time
    # Store the timing into nextBusTime and return

    return
    #return(nextBusTime)