import json
import pandas as pd

xl = pd.ExcelFile("./datas/bus_stops.xlsx")
#print(xl.sheet_names)

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
                #"coordinates": row["GPS Location"],
                "coordinates": coordinatesVal

            }
        else:
            dict[row["Bus stop"]]["buses"] += [sheetName]
    #if eachSheetData["Bus stop"] in dict:
        #dict[eachSheetData["Bus stop"]]["buses"].append(sheetName)

        #else:
        #    bus_df.loc[i,"Bus stop"] = {
        #        "buses" : [sheetName],
        #        "coordinates": bus_df.loc[i,"GPS Location"],
        #    }

with open("data.json", "w") as outfile:
    json.dump(dict, outfile)

#print(dict)
