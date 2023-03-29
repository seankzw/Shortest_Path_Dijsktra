import json

def getOverviewData():
    f = open("excel_overview.json")
    data = json.loads(f.read())
    return data

def dfs(start, end, path, routes):
    data = getOverviewData()
    print(data)
    path.append(start)
    
    if start == end:
        routes.append(path[:])
    else:
        for neighbor in data[start]:
            if any(neighbor == node for node in path):
                continue
            
            if len(path) > 1 and path[-2] in data and neighbor not in data[path[-2]]['edgeTo']:
                path[-1] = (path[-1], neighbor)
            
            dfs(neighbor, end, path, routes)
    
    path.pop()
    print(path)
    
routes = []
dfs('Larkin Terminal', 'Pejabat Daerah Tanah Johor Bahru', [], routes)
print(routes)

# if dfs works can implement function in getShortestPathFromList

def getShortestPathFromList(previous_nodes, start, end_stops, toReach):
    data = getOverviewData()
    collated_data = getCollatedData()
    shortest_path = None
    shortest_length = float('inf')
    distance_to_end = float('inf')

    # Perform DFS traversal to find all routes from start to end
    routes = []
    dfs(start, end_stops, [], routes)

    # Iterate through all routes to find the one with the least amount of transfers
    for route in routes:
        path = []
        num_transfers = 0
        for i in range(len(route)-1):
            curr_stop = route[i]
            next_stop = route[i+1]
            buses_at_curr_stop = data[curr_stop]["operating_buses"]
            buses_at_next_stop = data[next_stop]["operating_buses"]
            common_buses = set(buses_at_curr_stop).intersection(set(buses_at_next_stop))
            if not common_buses:
                num_transfers += 1
            path.append({
                "bus_stop_name": curr_stop,
                "coordinates" : (data[curr_stop]["lat"], data[curr_stop]["lng"]),
                "bus": common_buses
            })
        path.append({
            "bus_stop_name": end_stops,
            "coordinates" : (data[end_stops]["lat"], data[end_stops]["lng"]),
            "bus": data[end_stops]["operating_buses"],
        })

        # Update shortest path if this route has less transfers than previous ones
        if num_transfers < shortest_length or (num_transfers == shortest_length and distanceBetween(eachDestCoord, toReach) < distance_to_end):
            shortest_length = num_transfers
            distance_to_end = distanceBetween(eachDestCoord, toReach)
            shortest_path = path

    shortest_path.reverse