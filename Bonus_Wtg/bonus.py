import networkx as nx
import matplotlib.pyplot as plt

def draw_simple_graph(n=12):
    G_simple = nx.erdos_renyi_graph(n, 0.5)

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.canvas.manager.set_window_title("Simple Graph")

    nx.draw(G_simple, with_labels=True, node_color='lightblue', node_size=500, font_size=12, ax=ax)
    plt.title(f"Simple Graph (n = {n})")
    plt.show()

    return G_simple

def generate_complete_graph(n=12):
    G_complete = nx.complete_graph(n)

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.canvas.manager.set_window_title("Complete Graph")

    nx.draw(G_complete, with_labels=True, node_color='lightgreen', node_size=500, font_size=12, ax=ax)
    plt.title(f"Complete Graph (n = {n})")
    plt.show()

def create_bipartite_tripartite_graphs(n=12):
    n1 = n // 2
    n2 = n - n1
    G_bipartite = nx.complete_bipartite_graph(n1, n2)

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.canvas.manager.set_window_title("Bipartite Graph")

    nx.draw(G_bipartite, with_labels=True, node_color='orange', node_size=500, font_size=12, ax=ax)
    plt.title(f"Bipartite Graph (n = {n})")
    plt.show()

    n1, n2, n3 = n // 3, n // 3, n - 2 * (n // 3)
    G_tripartite = nx.complete_bipartite_graph(n1, n2)
    G_tripartite.add_nodes_from(range(n1 + n2, n1 + n2 + n3))

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.canvas.manager.set_window_title("Tripartite Graph")

    nx.draw(G_tripartite, with_labels=True, node_color='lightpink', node_size=500, font_size=12, ax=ax)
    plt.title(f"Tripartite Graph (n = {n})")
    plt.show()

def havel_hakimi_theorem(degree_sequence):
    steps = []
    while degree_sequence:
        degree_sequence.sort(reverse=True)
        steps.append(list(degree_sequence))

        if degree_sequence[0] < 0 or degree_sequence[0] >= len(degree_sequence):
            return False, steps

        for i in range(degree_sequence[0]):
            degree_sequence[i+1] -= 1
        degree_sequence = degree_sequence[1:]

    return True, steps

def check_havel_hakimi():
    degree_sequence = [5, 4, 3, 3, 2, 2, 1, 1, 1, 0]
    valid, steps = havel_hakimi_theorem(degree_sequence)

    print("Can the degree sequence represent a simple graph?", "Yes" if valid else "No")
    print("\nSteps of degree sequence modification:")
    for step in steps:
        print(step)

def main():
    G_simple = draw_simple_graph(n=12)
    print("\nApplying Havel-Hakimi Theorem on the Simple Graph:")
    check_havel_hakimi()
    generate_complete_graph(n=12)
    create_bipartite_tripartite_graphs(n=12)

if __name__ == "__main__":
    main()
