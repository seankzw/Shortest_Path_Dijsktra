from datetime import datetime
import json

def checkBusTime(busNo):
    # Load json with bus timings
    f = open("bus_timings.json")
    data = json.load(f)

    # Get current time
    current_date_and_time = datetime.now()
    time_now = datetime.now()
    current_time = time_now.strftime("%H:%M:%S")

    # Compare current time to bus timings to get next bus time
    # First, see if timing is within First and Last bus timing
    # If within, go through the array to find closest timing. Must be greater than current time
    # Store the timing into nextBusTime and return

    return(nextBusTime)