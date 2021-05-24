# Adjacency List Graph implementation for WGUPS Delivery Locations
class LocationDistanceGraph:

    def __init__(self):
        self.graph = {}
        self.location_names = {}

    def __getitem__(self):
        return self.graph

    # Adds a location
    # O(1)
    def add_location(self, location_name):
        self.graph[location_name] = []

    # Add an edge between location1 and location2 with given edge length
    # O(1)
    def add_edge(self, location1, location2, edge):
        temp = [location2, edge]
        self.graph[location1].append(temp)

    # Returns all edge lengths for a given location1
    # O(1)
    def get_edge_length(self, location1):
        return self.graph[location1]


