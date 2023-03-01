import json
import pandas as pd

xl = pd.ExcelFile("./datas/bus_stops.xlsx")

dict = {}

for eachSheetIdx in range(len(xl.sheet_names)):
    sheetName = xl.sheet_names[eachSheetIdx]
    eachSheetData = xl.parse(sheetName)
    df = pd.DataFrame(eachSheetData)
    for index, row in df.iterrows():
        location = row["GPS Location"]
        coordinatesVal = (0,0)
        if location != "NIL":
            coordinatesVal = (float(location.split(",")[0]), float(location.split(",")[1]))

        if row["Bus stop"] not in dict:
            dict[row["Bus stop"]] = {
                "buses" : [sheetName],
                "coordinates": coordinatesVal

            }
        else:
            dict[row["Bus stop"]]["buses"] += [sheetName]

with open("data.json", "w") as outfile:
    json.dump(dict, outfile)

