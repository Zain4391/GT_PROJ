#include <iostream>
#include <string>
#include <vector>
#include <list>
#include <climits>
using namespace std;

typedef pair<string, int> psi;

class Location
{
    float longitude;
    float latitude;
    string name;

public:
    Location(float lon, float lat, string n)
    {
        longitude = lon;
        latitude = lat;
        name = n;
    }

    Location()
    {
        longitude = 0.0f;
        latitude = 0.0f;
        name = "NULL";
    }

    float getLongitude() const
    {
        return longitude;
    }

    float getLatitude() const
    {
        return latitude;
    }

    string getName() const
    {
        return name;
    }
};

class Graph
{
    vector<Location> locations;
    int num;
    list<psi> *adj_list;

public:
    Graph(int n)
    {
        num = n;
        locations.resize(num);
        adj_list = new list<psi>[n];
    }

    void addLocation(int index, Location l_name)
    {
        locations[index] = l_name;
    }

    void link_location(int src, int dest, int cost)
    {
        adj_list[src].push_back(make_pair(locations[dest].getName(), cost));
        adj_list[dest].push_back(make_pair(locations[src].getName(), cost));
    }

    void primMST()
    {
        int startIndex = -1;
        for (int i = 0; i < locations.size(); ++i)
        {
            if (locations[i].getName() == "Delivery Station (Karachi)")
            {
                startIndex = i;
                break;
            }
        }

        if (startIndex == -1)
        {
            cerr << "Start location not found in the graph." << endl;
            return;
        }

        int src = startIndex;
        vector<int> key(num, INT_MAX);
        vector<int> parent(num, -1); 
        vector<bool> inMST(num, false);

        key[src] = 0;

        for (int count = 0; count < num - 1; ++count)
        {
            // Find the vertex with the minimum key value which is not yet included in MST
            int u = -1;
            for (int i = 0; i < num; ++i)
            {
                if (!inMST[i] && (u == -1 || key[i] < key[u]))
                {
                    u = i;
                }
            }

            inMST[u] = true;

            // Update key values and parent of adjacent vertices
            for (const auto &neighbor : adj_list[u])
            {
                int v = -1;
                for (int i = 0; i < num; ++i)
                {
                    if (locations[i].getName() == neighbor.first)
                    {
                        v = i;
                        break;
                    }
                }

                int weight = neighbor.second;
                if (!inMST[v] && weight < key[v])
                {
                    key[v] = weight;
                    parent[v] = u;
                }
            }
        }

        // Print the MST edges and total cost
        int totalCost = 0;
        cout << "Prim's MST starting from delivery station:" << endl;
        for (int i = 1; i < num; ++i)
        {
            if (parent[i] != -1)
            {
                // Print the edge and its weight
                int weight = key[i];
                cout << "Edge: " << locations[parent[i]].getName() << " - " << locations[i].getName() << " Weight: " << weight << endl;
                totalCost += weight;
            }
        }

        cout << "Total Cost of MST: " << totalCost << endl;
    }
};

int main()
{
    // Creating a graph with 10 locations
    Graph graph(10);

    // Adding locations to the graph
    graph.addLocation(0, Location(24.8507, 67.0011, "Delivery Station (Karachi)"));
    graph.addLocation(1, Location(24.8918, 67.0241, "Clifton"));
    graph.addLocation(2, Location(24.9223, 67.0625, "Saddar"));
    graph.addLocation(3, Location(24.9700, 67.0274, "DHA"));
    graph.addLocation(4, Location(24.9872, 67.0408, "Gulshan-e-Iqbal"));
    graph.addLocation(5, Location(25.0307, 67.0811, "Karachi University"));
    graph.addLocation(6, Location(24.8286, 67.0334, "Korangi"));
    graph.addLocation(7, Location(24.9223, 67.0597, "Nazimabad"));
    graph.addLocation(8, Location(24.9028, 67.0094, "Lyari"));
    graph.addLocation(9, Location(24.9298, 67.0847, "North Karachi"));

    // Adding edges with given costs
    vector<tuple<int, int, int>> edges = {
        {0, 1, 5}, {0, 2, 8}, {0, 3, 6}, {0, 4, 3}, {0, 5, 7},
        {1, 2, 2}, {1, 3, 9}, {1, 4, 4}, {1, 5, 1},
        {2, 3, 8}, {2, 4, 6}, {2, 5, 9}, {3, 4, 11}, {3, 5, 13},
        {4, 5, 3}, {5, 6, 7}, {6, 7, 5}, {7, 8, 6}, {8, 9, 3}, {9, 0, 4}
    };

    // Linking the locations with the given costs
    for (const auto& edge : edges) {
        int src, dest, cost;
        tie(src, dest, cost) = edge;
        graph.link_location(src, dest, cost);
    }

    cout << "-----------------------------" << endl;

    graph.primMST();

    return 0;
}
