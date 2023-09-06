import networkx as nx
import linecache
def citNetwork(init,end,network=None):
    if not network is None:
        G=network
        nodes=set(network.nodes())
        edges=set(network.edges())
    else:
        G = nx.Graph()
        nodes=set()
        edges=set()
    for i in range(init,end+1,1):
        temp=linecache.getline("dataEpoch//citNew.txt", i)
        temp1=temp.split("--")
        node=eval(temp1[0])
        edge=eval(temp1[1])
        nodes.update(node)
        edges.update(edge)
    for e in list(edges):
        if not e[0] in nodes or not e[1] in nodes:
            edges.remove(e)

    # print len(nodes)
    # print len(edges)
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G