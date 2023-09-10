import linecache
import networkx as nx

if __name__ == '__main__':
    edges=[]
    for i in range(1,2):
        temp = linecache.getline("ca.txt", i)
        # temp1 = temp.split("--")
        # print(temp1)
        # edge = eval(temp1[1])
        edge=eval(temp)
        edges.extend(edge)
    G=nx.Graph()
    print(len(edges))
    G.add_edges_from(edges)
    print([len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)])
    # largest_cc = max(nx.connected_components(G), key=len)
    # subg=nx.subgraph(G,largest_cc)
    # print(subg.edges())