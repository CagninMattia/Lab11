import copy

from database.DAO import DAO
import networkx as nx
from collections import Counter
class Model:
    def __init__(self):
        self.colori = DAO.get_color()
        self.grafo = nx.Graph()
        self.diz_nodi = {}
        self.longest_path = []

    def crea_grafo(self, colore, anno):
        self.grafo.clear()
        vertici = DAO.get_vertici(colore)
        for v in vertici:
            self.grafo.add_node(v)
            self.diz_nodi[v.Product_number] = v
        archi = DAO.get_archi(colore, anno)
        for arco in archi:
            if arco["Product1"] in self.diz_nodi.keys() and arco["Product2"] in self.diz_nodi.keys():
                self.grafo.add_edge(self.diz_nodi[arco["Product1"]], self.diz_nodi[arco["Product2"]], weight=arco["weight"])


    def get_colori(self):
        return self.colori

    def get_num_nodi(self):
        return len(self.grafo.nodes)

    def get_num_archi(self):
        return len(self.grafo.edges)

    def get_nodi_da_stampare(self):
        # Get all edges with weights
        all_edges = list(self.grafo.edges(data=True))
        # Sort edges by weight in descending order
        all_edges_sorted = sorted(all_edges, key=lambda x: x[2]['weight'], reverse=True)
        # Get the top 3 edges
        top_edges = all_edges_sorted[:3]

        # Print top 3 edges to txtArchi
        archi = []
        for edge in top_edges:
            prod1 = edge[0].Product_number
            prod2 = edge[1].Product_number
            weight = edge[2]['weight']
            archi.append([prod1, prod2, weight])

        # Find common products
        products = []
        for edge in top_edges:
            products.extend([edge[0].Product_number, edge[1].Product_number])

        product_counts = Counter(products)
        common_products = [product for product, count in product_counts.items() if count > 1]

        # Print common products
        print("Common products in top 3 edges:", common_products)

        # Assume txtArchi is an area of text widget where the results need to be displayed
        # Here, just returning the value for demonstration
        return archi, common_products

    def get_prodotti(self):
        return self.diz_nodi.keys()

    def find_longest_increasing_path(self, start_vertex):
        self.longest_path.clear()

        def ricorsione(node, path, weight):
            # Initialize the longest path with the current path
            if (path is not None) and (len(path) > len(self.longest_path)):
                self.longest_path = copy.deepcopy(path)

            # Explore neighbors of the current node
            for neighbor in self.grafo.neighbors(node):
                edge_weight = self.grafo[node][neighbor]['weight']
                # Check if the neighbor is not in the current path and if the edge weight is increasing
                if neighbor not in path and edge_weight >= weight:
                    print(neighbor)
                    # Recursively search from the neighbor
                    new_path = copy.deepcopy(path + [neighbor])
                    ricorsione(neighbor, new_path, edge_weight)
                    new_path.pop()

        # Start the DFS from the given start vertex
        ricorsione(self.diz_nodi[start_vertex], [self.diz_nodi[start_vertex]], -float('inf'))
        for p in self.longest_path:
            print(p)
        return len(self.longest_path)

