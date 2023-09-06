#coding=utf-8

import networkx as nx
import random
import copy
import multiprocessing
from scipy import sparse

def dataProcessing(network):
    G=nx.Graph()
    nodesNum=nx.number_of_nodes(network)
    nodesDict={}
    count=0
    for edge in network.edges():
        if nodesDict.get(edge[0])==None:
            nodesDict[edge[0]]=count
            count+=1
        if nodesDict.get(edge[1])==None:
            nodesDict[edge[1]]=count
            count += 1
        G.add_edge(nodesDict[edge[0]],nodesDict[edge[1]])
    return G
def ForceMethod(network0):
    """
    :param network: 一个图
    :return: 一个随机图
    """
    network = dataProcessing(network0)
    G=copy.deepcopy(network)
    data=nx.degree(G).values()
    tries=nx.number_of_edges(G)
    nodesNum=nx.number_of_nodes(G)
    adjG = sparse.lil_matrix((nodesNum, nodesNum))

    for i in G.edges():
        adjG[i[0], i[1]] = 1
        adjG[i[1], i[0]] = 1

    for curtry in range(tries):
        edge1=random.choice(G.edges())
        edge2=random.choice(G.edges())
        differelements=len(set([edge1[0], edge1[1], edge2[0], edge2[1]]))
        while differelements < 4:
            edge2 = random.choice(G.edges())
            differelements = len(set([edge1[0], edge1[1], edge2[0], edge2[1]]))
        if differelements==4:
            a1 = (edge1[0], edge2[1])
            b1 = (edge1[1], edge2[0])
            if (adjG[a1[0], a1[1]] == 0) and (adjG[b1[0], b1[1]] == 0):
                G.remove_edges_from([edge1,edge2])
                G.add_edges_from([a1, b1])

                adjG[edge1[0], edge1[1]] = 0
                adjG[edge1[1], edge1[0]] = 0
                adjG[edge2[0], edge2[1]] = 0
                adjG[edge2[1], edge2[0]] = 0

                adjG[a1[0], a1[1]] = 1
                adjG[a1[1], a1[0]] = 1
                adjG[b1[0], b1[1]] = 1
                adjG[b1[1], b1[0]] = 1
            else:
                a1 = (edge1[0], edge2[0])
                b1 = (edge1[1], edge2[1])
                if (adjG[a1[0], a1[1]] == 0) and (adjG[b1[0], b1[1]] == 0):
                    G.remove_edges_from([edge1,edge2])
                    G.add_edges_from([a1, b1])

                    adjG[edge1[0], edge1[1]] = 0
                    adjG[edge1[1], edge1[0]] = 0
                    adjG[edge2[0], edge2[1]] = 0
                    adjG[edge2[1], edge2[0]] = 0

                    adjG[a1[0], a1[1]] = 1
                    adjG[a1[1], a1[0]] = 1
                    adjG[b1[0], b1[1]] = 1
                    adjG[b1[1], b1[0]] = 1

    return G
def rewiremethods(network0):
    print("begin new process")
    network = dataProcessing(network0)

    G = copy.deepcopy(network)
    nodesNum=nx.number_of_nodes(G)

    edgesNum = nx.number_of_edges(G)
    adjG = sparse.lil_matrix((nodesNum,nodesNum))

    for i in G.edges():
        adjG[i[0],i[1]]=1
        adjG[i[1], i[0]] = 1
    """选m/2条边，配对进行重连，重复k次"""
    for tries in range(edgesNum):
        edgePool=G.edges()
        edgeHalf=random.sample(edgePool,edgesNum/2)
        edgePool=list(set(edgePool)-set(edgeHalf))
        for edge1 in edgeHalf:
            edge2=random.choice(edgePool)
            edgePool.remove(edge2)
            differelements = len(set([edge1[0], edge1[1], edge2[0], edge2[1]]))
            if differelements == 4:
                a1 = (edge1[0], edge2[1])
                b1 = (edge1[1], edge2[0])
                if (adjG[a1[0], a1[1]] == 0) and (adjG[b1[0], b1[1]] == 0):
                    G.remove_edges_from([edge1, edge2])
                    G.add_edges_from([a1, b1])

                    adjG[edge1[0], edge1[1]] = 0
                    adjG[edge1[1], edge1[0]] = 0
                    adjG[edge2[0], edge2[1]] = 0
                    adjG[edge2[1], edge2[0]] = 0

                    adjG[a1[0], a1[1]] = 1
                    adjG[a1[1], a1[0]] = 1
                    adjG[b1[0], b1[1]] = 1
                    adjG[b1[1], b1[0]] = 1
                else:
                    a1 = (edge1[0], edge2[0])
                    b1 = (edge1[1], edge2[1])
                    if (adjG[a1[0], a1[1]] == 0) and (adjG[b1[0], b1[1]] == 0):
                        G.remove_edges_from([edge1, edge2])
                        G.add_edges_from([a1, b1])

                        adjG[edge1[0], edge1[1]] = 0
                        adjG[edge1[1], edge1[0]] = 0
                        adjG[edge2[0], edge2[1]] = 0
                        adjG[edge2[1], edge2[0]] = 0

                        adjG[a1[0], a1[1]] = 1
                        adjG[a1[1], a1[0]] = 1
                        adjG[b1[0], b1[1]] = 1
                        adjG[b1[1], b1[0]] = 1
    return G
def generativeMethods(network0):
    print("begin new process")
    network=dataProcessing(network0)
    """
    :param network: 一个图
    :return: 一个随机图
    """

    nodesNum=nx.number_of_nodes(network)
    degreeDist=dict(nx.degree(network))
    sortedDegreeTuple=sorted(list(degreeDist.items()), key=lambda x: x[1], reverse=True)
    sortedDegree=[]
    for i in sortedDegreeTuple:
        sortedDegree.append([i[0],i[1]])
    # print(sortedDegree(node,deg))
    edges=sparse.lil_matrix((nodesNum,nodesNum))  #adjacent matrix
    rest=[] #rest stubs
    edgespool=[]  #edges pool
    for t in range(len(sortedDegree)):
        if(len(sortedDegree)==0):break
        source=sortedDegree[0]

        sortedDegree.remove(source)
        if(source[1]<len(sortedDegree)):
            targetSet=random.sample(range(len(sortedDegree)),source[1])

        else:
            targetSet = [j for j in range(len(sortedDegree))]
            rest.extend([source[0]]*(source[1]-len(sortedDegree)))
        removeEdges = set()
        for x in targetSet:
            tmp=sortedDegree[x]
            if tmp[1]>0:
                edges[source,tmp[0]]=1
                edges[tmp[0],source] = 1
                edgespool.append((source[0],tmp[0]))
                tmp[1]-=1
                if(tmp[1]==0):removeEdges.add((tmp[0],tmp[1]))
                else:sortedDegree[x][1]=tmp[1]
            else:
                removeEdges.add(tmp)
        for x in removeEdges:

            sortedDegree.remove(list(x))
    if(len(rest)>0):
        print("rewire begin")
        pool=RewireRest(rest,edges,edgespool)
        print("rewire end")
    else:
        pool=edgespool
    G=nx.Graph()
    G.add_edges_from(pool)
    return G

def RewireRest(rest,edges,pool):
    """

    :param rest: (nodes,degree)
    :param edges: sparse.lil_matrix perform existing edges
    :return:
    """
    candidatePool = copy.deepcopy(pool)
    while(len(rest)>0):
        edge1 = random.sample(rest, 2)
        edge2 = random.choice(candidatePool)
        differelements = len(set([edge1[0], edge1[1], edge2[0], edge2[1]]))

        while differelements < 3:
            candidatePool.remove(edge2)
            try:
                edge2 = random.choice(candidatePool)
            except:
                raise TypeError("candidatePool error")
            differelements = len(set([edge1[0], edge1[1], edge2[0], edge2[1]]))
        # print("rest",rest)
        # print("edge2",edge2)
        # print(pool)
        if differelements == 3:
            a1 = (edge1[0], edge2[1])
            b1 = (edge1[1], edge2[0])
            if (edges[a1[0], a1[1]] == 0) and (edges[b1[0], b1[1]] == 0):
                pool.remove(edge2)
                pool.extend([a1, b1])
                candidatePool.extend([a1, b1])
                edges[edge1[0], edge1[1]] = 0
                edges[edge1[1], edge1[0]] = 0
                edges[edge2[0], edge2[1]] = 0
                edges[edge2[1], edge2[0]] = 0

                edges[a1[0], a1[1]] = 1
                edges[a1[1], a1[0]] = 1
                edges[b1[0], b1[1]] = 1
                edges[b1[1], b1[0]] = 1
                rest.remove(edge1[0])
                rest.remove(edge1[1])
            # elif edges[a1[0], a1[1]] == 0:
            #
            #     pool.remove(edge2)
            #     pool.extend([a1])
            #     rest.extend([b1[0],b1[1]])
            #     candidatePool.extend([a1])
            #     edges[edge2[0], edge2[1]] = 0
            #     edges[edge2[1], edge2[0]] = 0
            #
            #     edges[a1[0], a1[1]] = 1
            #     edges[a1[1], a1[0]] = 1
            #     rest.remove(edge1[0])
            # elif edges[b1[0], b1[1]] == 0:
            #     pool.remove(edge2)
            #     pool.extend([b1])
            #     candidatePool.extend([ b1])
            #     edges[edge2[0], edge2[1]] = 0
            #     edges[edge2[1], edge2[0]] = 0
            #
            #     edges[b1[0], b1[1]] = 1
            #     edges[b1[1], b1[0]] = 1
            #     rest.remove(edge1[1])

        if differelements==4:
            a1 = (edge1[0], edge2[1])
            b1 = (edge1[1], edge2[0])
            if (edges[a1[0], a1[1]] == 0) and (edges[b1[0], b1[1]] == 0):
                pool.remove(edge2)
                pool.extend([a1, b1])
                candidatePool.extend([a1, b1])

                edges[edge1[0], edge1[1]] = 0
                edges[edge1[1], edge1[0]] = 0
                edges[edge2[0], edge2[1]] = 0
                edges[edge2[1], edge2[0]] = 0

                edges[a1[0], a1[1]] = 1
                edges[a1[1], a1[0]] = 1
                edges[b1[0], b1[1]] = 1
                edges[b1[1], b1[0]] = 1
                rest.remove(edge1[0])
                rest.remove(edge1[1])
            else:
                a1 = (edge1[0], edge2[0])
                b1 = (edge1[1], edge2[1])
                if (edges[a1[0], a1[1]] == 0) and (edges[b1[0], b1[1]] == 0):
                    pool.remove(edge2)
                    pool.extend([a1, b1])
                    candidatePool.extend([a1, b1])

                    edges[edge1[0], edge1[1]] = 0
                    edges[edge1[1], edge1[0]] = 0
                    edges[edge2[0], edge2[1]] = 0
                    edges[edge2[1], edge2[0]] = 0

                    edges[a1[0], a1[1]] = 1
                    edges[a1[1], a1[0]] = 1
                    edges[b1[0], b1[1]] = 1
                    edges[b1[1], b1[0]] = 1
                    rest.remove(edge1[0])
                    rest.remove(edge1[1])
        candidatePool.remove(edge2)
    return pool
def cc(U,seq):
    return float(len(U)) / sum([1.0 / item[1] for item in seq if item[0] in U])

def Ccp(G,kcore):
    seq = nx.closeness_centrality(G)
    seq=seq.items()
    CcV=cc(G.nodes(),seq)
    CcVcore=cc(kcore,seq)
    Ccp = CcVcore / CcV
    return Ccp
def test_cp(G):
    kcore = nx.k_core(G).nodes()
    Gccp=Ccp(G,kcore)
    sumRlist=[]
    sumRCcp=0.0
    print(Gccp)

    p=multiprocessing.Pool(8)
    for i in [0]*8:

        sumRlist.append(p.apply_async(calCCp,args=(G,)))

    p.close()
    p.join()
    print(sumRlist)
    for i in sumRlist:
        print(i.get())
        sumRCcp+=float(i.get())
    aveRCcp =sumRCcp/8.0
    print(Gccp-aveRCcp)
    return Gccp-aveRCcp
def calCCp(G):
    G0 = generativeMethods(G)
    # G0=rewiremethods(G)
    # G0=ForceMethod(G)
    G0 = max(nx.connected_component_subgraphs(G0), key=len)
    kcore0 = nx.k_core(G0).nodes()
    temp = Ccp(G0, kcore0)
    return temp

if __name__ == '__main__':
    import networks as ns
    # G=ns.fof_500_4_4_0d3_0d3() #0.01
    # G=ns.B_A_500() #-0.0908364800241

    # G=ns.richClub500() #0.13
    # G=ns.onionNetwork_500() #0.27
    import socfb_trinity100
    # G=socfb_trinity100.socfb_Trinity100(1,111996) #0.072260687574
    # G=socfb_trinity100.socfb_Haverford76(1,59589) #0.0902903014734
    # G=socfb_trinity100.soc_anybeat(1,67053) #0.176343543475
    # G=socfb_trinity100.American75(1,217662) #0.0731664655508
    # G=socfb_trinity100.BC17(1,486967) #0.0874967123593
    # G = socfb_trinity100.soc_gplus(1, 39242)  #0.149134123186
    # G = socfb_trinity100.ego_facebook(1, 2981) #0.0702003292496
    # G = socfb_trinity100.facebook(1, 88234)   #-0.0996722411775
    import network_trade
    # G=socfb_trinity100.soc_sign_bitcoinotc(1,35200) #0.115613850914
    # G=socfb_trinity100.CollegeMsgNetwork(1,59000) #0.08790548731
    # G=socfb_trinity100.citNetwork(1,2000) #0.148864521541
    # G=network_trade.trade(2009)  #0.11677630026

    import evolution_models as em
    G = ns.Regular(10)
    # avedeg=3
    # gama = {6: 4, 8: 2.9, 10: 2.52, 12: 2.3, 14: 2.1}
    # while len(G) < 500:
    #     G = em.rich_club(G, float(2*avedeg)/(2*avedeg-2)+1, len(G.nodes()) + 1) #0.133618043968
    while(len(G.nodes())<500):
        em.BA_evolution(G, 1, 3)  #-0.096325184624
        # em.Friends_FoF(G,len(G.nodes())+1,3, 3, 0.5, 0.5) #0.00225019396291  0.025
        # em.Friends_FoF(G, len(G.nodes()) + 1, 6,6 , 0.25, 0.25) #0.0186918577854 0.04
        # em.Friends_FoF(RG, len(RG.nodes()) + 1, 2, 2, 0.75, 0.75)
        # em.Friends_FoF(G, len(G.nodes()) + 1, 2, 1, 1, 1)  #-0.0574009283917  -0.03
        # G=em.onionEvolution1(G,gama[6])   #0.35  0.26

    # G=ns.B_A_500()
    # G.remove_edges_from(G.selfloop_edges())
    # G = max(nx.connected_component_subgraphs(G), key=len)

    test_cp(G)
    # G=ns.symetric()
    # G1=generativeMethods(G)
    # import calculate_param

    # calculate_param.drawNetwork(G1)
    # print("前:",nx.number_of_edges(G))
    # G1=generate_random_graph_with_m(G)
    # print("后:",nx.number_of_edges(G1))
