import networkx as nx
import copy
def degrootRounds(nodeAttribute,nodeNeighbors,Dor,W=None,rounds=None):
    # G = ns.test2()
    if W is None:
        W = {x: 0 for x in nodeAttribute.keys()}
    old=copy.deepcopy(W)
    # Dor=nx.dominating_set(G)
    # Dor=[i for i in range(0,429)]
    # Dor = [0]
    # print("len:%d" % len(Dor))
    for i in Dor:
        W[i] = 1
        old[i]=1
    instable = True
    count = 0
    if rounds is None:
        while instable:
            count += 1
            instable = False
            for i in nodeAttribute.keys():
                if i in Dor: continue
                NEI = list(nodeNeighbors[i])
                Deg = len(NEI)
                W[i] = 0
                for j in NEI:
                    W[i] += old[j] / float(Deg)
                if W[i] - old[i] > 0.000001:
                    instable = True
        return count
def degrootOpinion(nodeAttribute,nodeNeighbors,Dor,W=None):
    if W is None:
        W = {x: 0 for x in nodeAttribute.keys()}
    old=copy.deepcopy(W)
    # Dor=nx.dominating_set(G)
    # Dor=[i for i in range(0,429)]
    # Dor = [0]
    # print("len:%d" % len(Dor))
    for i in Dor:
        W[i] = 1
        old[i]=1
    for i in nodeAttribute.keys():
        if i in Dor: continue
        NEI = list(nodeNeighbors[i])
        Deg = len(NEI)
        W[i] = 0
        for j in NEI:
            W[i] += old[j] / float(Deg)
    opinion=sum(W/float(len(nodeAttribute.keys())))
    return opinion
if __name__ == '__main__':
    pass

    # test1  56
    # test2   20