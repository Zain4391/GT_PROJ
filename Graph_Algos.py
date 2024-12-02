import heapq
import matplotlib.pyplot as plt
import networkx as nx

class Location:
    def __init__(self, lon, lat, name):
        self.longitude = lon
        self.latitude = lat
        self.name = name

    def get_longitude(self):
        return self.longitude

    def get_latitude(self):
        return self.latitude

    def get_name(self):
        return self.name


class Graph:
    def __init__(self, n):
        self.num = n
        self.locations = [None] * n
        self.adj_list = [[] for _ in range(n)]
        self.mst_edges = []  # Store the edges in the MST

    def add_location(self, index, location):
        self.locations[index] = location

    def link_location(self, src, dest, cost):
        self.adj_list[src].append((self.locations[dest].get_name(), cost))
        self.adj_list[dest].append((self.locations[src].get_name(), cost))

    def prim_mst(self):
        pq = []
        start_index = -1
        for i, location in enumerate(self.locations):
            if location.get_name() == "Delivery Station (Karachi)":
                start_index = i
                break

        if start_index == -1:
            print("Start location not found in the graph.")
            return

        key = [float('inf')] * self.num
        parent = [None] * self.num
        in_mst = [False] * self.num

        heapq.heappush(pq, (0, start_index))
        key[start_index] = 0

        while pq:
            u_key, u_index = heapq.heappop(pq)
            in_mst[u_index] = True

            for neighbor_name, weight in self.adj_list[u_index]:
                neighbor_index = -1
                for i, location in enumerate(self.locations):
                    if location.get_name() == neighbor_name:
                        neighbor_index = i
                        break

                if neighbor_index != -1 and not in_mst[neighbor_index] and weight < key[neighbor_index]:
                    key[neighbor_index] = weight
                    parent[neighbor_index] = u_index
                    heapq.heappush(pq, (key[neighbor_index], neighbor_index))

        total_cost = 0
        for i in range(1, self.num):
            if parent[i] is not None:
                # Collect the MST edges
                self.mst_edges.append((self.locations[parent[i]].get_name(), self.locations[i].get_name(), key[i]))
                total_cost += key[i]

        print(f"Total Cost of MST: {total_cost}")


# Create the graph and add locations and connections
graph = Graph(10)

# Adding existing locations
graph.add_location(0, Location(24.8507, 67.0011, "Delivery Station (Karachi)"))
graph.add_location(1, Location(24.8918, 67.0241, "Clifton"))
graph.add_location(2, Location(24.9223, 67.0625, "Saddar"))
graph.add_location(3, Location(24.9700, 67.0274, "DHA"))
graph.add_location(4, Location(24.9872, 67.0408, "Gulshan-e-Iqbal"))
graph.add_location(5, Location(25.0307, 67.0811, "Karachi University"))
graph.add_location(6, Location(24.8286, 67.0334, "Korangi"))
graph.add_location(7, Location(24.9223, 67.0597, "Nazimabad"))
graph.add_location(8, Location(24.9028, 67.0094, "Lyari"))
graph.add_location(9, Location(24.9298, 67.0847, "North Karachi"))

# Linking locations with costs
edges = [
    (0, 1, 5), (0, 2, 8), (0, 3, 6), (0, 4, 3), (0, 5, 7),
    (1, 2, 2), (1, 3, 9), (1, 4, 4), (1, 5, 1),
    (2, 3, 8), (2, 4, 6), (2, 5, 9), (3, 4, 11), (3, 5, 13),
    (4, 5, 3), (5, 6, 7), (6, 7, 5), (7, 8, 6), (8, 9, 3), (9, 0, 4)
]

for src, dest, cost in edges:
    graph.link_location(src, dest, cost)

# Run Prim's MST algorithm
graph.prim_mst()

# Visualization using networkx
G = nx.Graph()

# Adding nodes with positions for visualization
locations = {
    "Delivery Station (Karachi)": (0, 0),
    "Clifton": (1, 4),
    "Saddar": (3, 2),
    "DHA": (4, 5),
    "Gulshan-e-Iqbal": (6, 2),
    "Karachi University": (8, 0),
    "Korangi": (2, -2),
    "Nazimabad": (5, 1),
    "Lyari": (4, -3),
    "North Karachi": (7, -2),
}

for location, pos in locations.items():
    G.add_node(location, pos=pos)

# Adding original edges with weights
for src, dest, weight in edges:
    G.add_edge(graph.locations[src].get_name(), graph.locations[dest].get_name(), weight=weight)

# Define positions for the graph nodes
pos = nx.spring_layout(G, seed=42)

# Draw the original graph with all edges
plt.figure(figsize=(12, 12))
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold", edge_color="gray")
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red", font_size=8)
plt.title("Graph of Locations in Karachi with Connection Costs")
plt.show()

# Draw the MST based on Prim's output
MST = nx.Graph()
for src, dest, weight in graph.mst_edges:
    MST.add_edge(src, dest, weight=weight)

plt.figure(figsize=(12, 12))
nx.draw(MST, pos, with_labels=True, node_size=2000, node_color="lightgreen", font_size=10, font_weight="bold", edge_color="blue")
mst_edge_labels = nx.get_edge_attributes(MST, 'weight')
nx.draw_networkx_edge_labels(MST, pos, edge_labels=mst_edge_labels, font_color="red", font_size=8)
plt.title("Minimum Spanning Tree (MST) of Locations in Karachi")
plt.show()
