import heapq

def dijkstra(graph, start, end):
    # Initialize distances and visited vertices
    distances = {v: float('inf') for v in graph}
    distances[start] = 0
    visited = set()

    # Initialize the priority queue with the start vertex
    pq = [(0, start)]

    while pq:
        # Get the vertex with the smallest tentative distance
        dist, current = heapq.heappop(pq)

        # Check if we have reached the end vertex
        if current == end:
            return distances[current]

        # Skip visited vertices
        if current in visited:
            continue

        # Mark the current vertex as visited
        visited.add(current)

        # Update the tentative distances of the neighboring vertices
        for neighbor, weight in graph[current].items():
            tentative_distance = distances[current] + weight
            if tentative_distance < distances[neighbor]:
                distances[neighbor] = tentative_distance
                heapq.heappush(pq, (tentative_distance, neighbor))

    # If the end vertex is not reachable from the start vertex, return None
    return None

# graph = {
#     'A': {'B': 2, 'C': 4},
#     'B': {'C': 1, 'D': 3},
#     'C': {'D': 2},
#     'D': {}
# }
graph = {
    'A': {'B': 5, 'C': 1},
    'B': {'A': 5, 'C': 2, 'D': 1},
    'C': {'A': 1, 'B': 2, 'D': 4, 'E': 8},
    'D': {'B': 1, 'C': 4, 'E': 3, 'F': 6},
    'E': {'C': 8, 'D': 3},
    'F': {'D': 6}
}

start = 'A'
end = 'E'

shortest_distance = dijkstra(graph, start, end)
print(shortest_distance)  # Output: 7
