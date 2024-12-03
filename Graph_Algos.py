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

    def add_location(self, index, location):
        self.locations[index] = location

    def link_location(self, src, dest, cost):
        self.adj_list[src].append((self.locations[dest].get_name(), cost))
        self.adj_list[dest].append((self.locations[src].get_name(), cost))

    def prim_mst(self):
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

        key[start_index] = 0

        for _ in range(self.num - 1):
            # Find the vertex with the minimum key value which is not yet included in MST
            u = -1
            for i in range(self.num):
                if not in_mst[i] and (u == -1 or key[i] < key[u]):
                    u = i

            in_mst[u] = True

            # Update key values and parent of adjacent vertices
            for neighbor_name, weight in self.adj_list[u]:
                neighbor_index = -1
                for i, location in enumerate(self.locations):
                    if location.get_name() == neighbor_name:
                        neighbor_index = i
                        break

                if not in_mst[neighbor_index] and weight < key[neighbor_index]:
                    key[neighbor_index] = weight
                    parent[neighbor_index] = u

        total_cost = 0
        print(f"Prim's MST starting from delivery station:")
        mst_edges = []
        for i in range(1, self.num):
            if parent[i] is not None:
                weight = key[i]
                print(f"Edge: {self.locations[parent[i]].get_name()} - {self.locations[i].get_name()} Weight: {weight}")
                total_cost += weight
                mst_edges.append((self.locations[parent[i]].get_name(), self.locations[i].get_name(), weight))

        print(f"Total Cost of MST: {total_cost}")
        return mst_edges


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
mst_edges = graph.prim_mst()

# Visualization of the graph (initial graph and MST)

# Create the initial graph (networkx)
G = nx.Graph()

# Adding nodes and edges for the initial graph
for src, dest, weight in edges:
    G.add_edge(graph.locations[src].get_name(), graph.locations[dest].get_name(), weight=weight)

# Draw the initial graph with all edges
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, seed=42, k=0.5)  # Adjust 'k' for spreading the nodes further apart
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold", edge_color="gray")
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red", font_size=8)
plt.title("Initial Graph with Connection Costs")
plt.show()

# Create the MST graph based on Prim's MST output
mst_graph = nx.Graph()

# Adding edges for the MST
for edge in mst_edges:
    mst_graph.add_edge(edge[0], edge[1], weight=edge[2])

# Draw the MST
plt.figure(figsize=(12, 12))
nx.draw(mst_graph, pos, with_labels=True, node_size=2000, node_color="lightgreen", font_size=10, font_weight="bold", edge_color="blue")
mst_edge_labels = nx.get_edge_attributes(mst_graph, 'weight')
nx.draw_networkx_edge_labels(mst_graph, pos, edge_labels=mst_edge_labels, font_color="red", font_size=8)
plt.title("Minimum Spanning Tree (MST) of Locations")
plt.show()
