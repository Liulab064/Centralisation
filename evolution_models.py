#coding=utf-8
import networkx as nx
import math
import random
import ALG_Metrics as cp
import datetime
import time
import numpy as np
def sample(alpha=2.5, size=1000, xmin=1, xmax=None):
    """
    Generates a random sample from a (bounded) power-law distribution.

    Parameters
    ----------
    alpha : scalar, float, greater than 1
        power-law exponent
    size : scalar, integer
        size (i.e. length) of the random sample to be generated
    xmin : scalar, float
        lower bound of the power-law random variable (greater than zero)
    xmax : scalar, float, optional
        upper bound of the power-law random variable

    Returns
    -------
    s : numpy.ndarray with ``shape = (size, )``
        random deviates from a power-law distribution with exponent ``alpha``
        and with upper and lower bounds as specified

    See Also
    --------
    histogram
    pdf

    """
    assert alpha > 1, "Power law exponent should be greater than 1!"
    beta = 1. - alpha
    r = np.random.rand(size)
    if not xmax:
        s = xmin * ((1. - r) ** (1 / beta))
    else:
        a = xmin ** beta
        b = xmax ** beta - a
        s = (a + b * r) ** (1. / beta)
    return s

def powerlawrnd2(gama,xmin,xmax=None):
    alpha=gama-1
    a=random.uniform(0,1)
    if not xmax:
        x=round(pow(1-a,-1.0/alpha)*(xmin-0.5)+0.5)
    else:
        c1=(xmin-0.5) ** alpha
        c2=(xmax+0.5) ** alpha-a
        x = round((c1 + c2 * a) ** (1. / alpha)+0.5)
    return x

def powerLawDistribution(n,gama=2.5,xmin=2.5):
    result=[]
    while len(result)<n:
        temp=powerlawrnd2(gama,xmin,n)
        # if temp>=n/3:
        #     continue
        result.append(temp)
    return result
# def generate_onion(Num, gama=2.5):
#     # data = powerLawDistribution(Num, gama)
#     data=sample(gama,Num,2,Num-1)
#     for i in range(Num): data[i] = int(round(data[i]))
#     hist = {}
#     for i in data:
#         i = int(i)
#         if not i in hist.keys():
#             hist[i] = 0
#         hist[i] += 1
#     """
#     排序分成si个
#     """
#     sortedhist = sorted(hist.keys())
#     result = []
#     for i in data:
#         result.append(sortedhist.index(i))
#     """
#     data是度数表
#     result是层数表
#     nodesRemian 是stubs pool
#
#     """
#     G = nx.Graph()
#     nodes = range(0, Num)
#     nodesRemain = []
#     for i in nodes:
#         nodesRemain.extend([i] * data[i])
#     edges = []
#     alpha = 3
#     tries = 10
#     rewiretries = 100
#     while len(nodesRemain) > 1:
#         if (len(edges) == 0 or tries >= 0) and len(set(nodesRemain)) > 1:
#
#             a, b = random.sample(set(nodesRemain), 2)
#             if a == b or (a, b) in edges or (b, a) in edges:
#                 tries -= 1
#                 continue
#             tries = 10
#             if random.uniform(0, 1) < (1.0 / (1 + alpha * abs(result[a] - result[b]))):
#                 edges.append((a, b))
#                 nodesRemain.remove(a)
#                 nodesRemain.remove(b)
#             rewiretries = 100
#         else:
#             rewiretries -= 1
#             if rewiretries <= 0:
#                 break
#             tries = 10
#             edge1 = random.choice(edges)
#             if (len(nodesRemain) == 1):
#                 break
#             stub1, stub2 = random.sample(nodesRemain, 2)
#             if (edge1[0] == stub1 or edge1[1] == stub1) and (edge1[0] == stub2 or edge1[1] == stub2):
#                 continue
#             if (not edge1[0] == stub1) and (not edge1[1] == stub2):
#                 a1 = (edge1[0], stub1)
#                 a2 = (stub1, edge1[0])
#                 b1 = (edge1[1], stub2)
#                 b2 = (stub2, edge1[1])
#             elif (not edge1[0] == stub2) and (not edge1[1] == stub1):
#                 a1 = (edge1[0], stub2)
#                 a2 = (stub2, edge1[0])
#                 b1 = (edge1[1], stub1)
#                 b2 = (stub1, edge1[1])
#             else:
#                 print("error")
#                 continue
#             if not ((a1 in edges) or (a2 in edges) or (b1 in edges) or (b2 in edges)):
#                 edges.remove(edge1)
#                 edges.append(a1)
#                 edges.append(b1)
#                 nodesRemain.remove(stub1)
#                 nodesRemain.remove(stub2)
#     G.add_nodes_from(nodes)
#     G.add_edges_from(edges)
#     return G

def onionEvolution(network,gama):
    degree = nx.degree(network)
    hist = {}
    for i in network.nodes():
        if not degree[i] in hist.keys():
            hist[degree[i]] = 0
        hist[degree[i]] += 1
    sortedhist = sorted(hist.keys())
    result = []
    for i in network.nodes():
        result.append(sortedhist.index(degree[i]))
    time1=len(network.nodes())
    time2=time1+1
    degreeOfTime1=[int(round(powerlawrnd2(gama,2)))]
    nodesRemain=[]
    nodes=[]
    edges = list(network.edges())
    if degreeOfTime1[0]%2==0:
        nodesRemain.extend([time1]*degreeOfTime1[0])
        nodes.append(time1)
    else:
        nodesRemain.extend([time1]*(degreeOfTime1[0]-1))
        nodes.append(time1)
        nodes.append(time2)
        edges.append((time1,time2))
    alpha = 3
    tries = 10
    rewiretries = 100
    while len(nodesRemain) > 0:
        if (len(edges) == 0 or tries >= 0) and len(set(nodesRemain)) > 1:

            a, b = random.sample(set(nodesRemain), 2)
            if a == b or (a, b) in edges or (b, a) in edges:
                tries -= 1
                continue
            tries = 10
            if random.uniform(0, 1) < (1.0 / (1 + alpha * abs(result[a] - result[b]))):
                edges.append((a, b))
                nodesRemain.remove(a)
                nodesRemain.remove(b)
            rewiretries=100
        else:
            tries = 10
            rewiretries-=1
            if rewiretries<=0:
                break
            edge1 = random.choice(edges)
            if (len(nodesRemain) == 1):
                break
            stub1, stub2 = random.sample(nodesRemain, 2)
            if (edge1[0] == stub1 or edge1[1] == stub1) and (edge1[0] == stub2 or edge1[1] == stub2):
                continue
            if (not edge1[0] == stub1) and (not edge1[1] == stub2):
                a1 = (edge1[0], stub1)
                a2 = (stub1, edge1[0])
                b1 = (edge1[1], stub2)
                b2 = (stub2, edge1[1])
            elif (not edge1[0] == stub2) and (not edge1[1] == stub1):
                a1 = (edge1[0], stub2)
                a2 = (stub2, edge1[0])
                b1 = (edge1[1], stub1)
                b2 = (stub1, edge1[1])
            else:
                print("error")
                continue
            if not ((a1 in edges) or (a2 in edges) or (b1 in edges) or (b2 in edges)):
                edges.remove(edge1)
                edges.append(a1)
                edges.append(b1)
                nodesRemain.remove(stub1)
                nodesRemain.remove(stub2)

    network.add_edges_from(edges)
    return network
def onionEvolution2(nodeAttribute,nodeNeighbors,gama):
    hist = {}
    for i in nodeAttribute.keys():
        if not nodeAttribute[i][0] in hist.keys():
            hist[nodeAttribute[i][0]] = 0
        hist[nodeAttribute[i][0]] += 1
    sortedhist = sorted(hist.keys())
    result = []
    for i in nodeAttribute.keys():
        result.append(sortedhist.index(nodeAttribute[i][0]))
    time1=len(nodeAttribute.keys())
    time2=time1+1
    degreeOfTime1=[int(round(powerlawrnd2(gama,2)))]
    nodesRemain=[]
    nodes=[]
    edges=[]
    for source in nodeNeighbors.keys():
        tmp = zip([source] * nodeAttribute[source][0], nodeNeighbors[source])
        edges.extend(list(tmp))
    if degreeOfTime1[0]%2==0:
        nodesRemain.extend([time1]*degreeOfTime1[0])
        nodes.append(time1)
    else:
        nodesRemain.extend([time1]*(degreeOfTime1[0]-1))
        nodes.append(time1)
        nodes.append(time2)
        edges.append((time1,time2))
    alpha = 3
    tries = 10
    rewiretries = 100
    while len(nodesRemain) > 0:
        if (len(edges) == 0 or tries >= 0) and len(set(nodesRemain)) > 1:

            a, b = random.sample(set(nodesRemain), 2)
            if a == b or (a, b) in edges or (b, a) in edges:
                tries -= 1
                continue
            tries = 10
            if random.uniform(0, 1) < (1.0 / (1 + alpha * abs(result[a] - result[b]))):
                edges.append((a, b))
                nodesRemain.remove(a)
                nodesRemain.remove(b)
            rewiretries=100
        else:
            tries = 10
            rewiretries-=1
            if rewiretries<=0:
                break
            edge1 = random.choice(edges)
            if (len(nodesRemain) == 1):
                break
            stub1, stub2 = random.sample(nodesRemain, 2)
            if (edge1[0] == stub1 or edge1[1] == stub1) and (edge1[0] == stub2 or edge1[1] == stub2):
                continue
            if (not edge1[0] == stub1) and (not edge1[1] == stub2):
                a1 = (edge1[0], stub1)
                a2 = (stub1, edge1[0])
                b1 = (edge1[1], stub2)
                b2 = (stub2, edge1[1])
            elif (not edge1[0] == stub2) and (not edge1[1] == stub1):
                a1 = (edge1[0], stub2)
                a2 = (stub2, edge1[0])
                b1 = (edge1[1], stub1)
                b2 = (stub1, edge1[1])
            else:
                print("error")
                continue
            if not ((a1 in edges) or (a2 in edges) or (b1 in edges) or (b2 in edges)):
                edges.remove(edge1)
                edges.append(a1)
                edges.append(b1)
                nodesRemain.remove(stub1)
                nodesRemain.remove(stub2)
    ansEdges=[]

    for e in edges:
        if e[0] not in nodeAttribute.keys():
            nodeAttribute[e[0]] = [0, 0]
            nodeNeighbors[e[0]] = set()
        if e[1] not in nodeAttribute.keys():
            nodeAttribute[e[1]] = [0, 0]
            nodeNeighbors[e[1]] = set()
        if e[0] not in nodeNeighbors[e[1]]:
            ansEdges.append(e)
        nodeNeighbors[e[0]].add(e[1])
        nodeAttribute[e[0]][0] = len(nodeNeighbors[e[0]])
        nodeNeighbors[e[1]].add(e[0])
        nodeAttribute[e[1]][0] = len(nodeNeighbors[e[1]])
    return ansEdges
# def onionEvolution1(network,gama):
#     degree = nx.degree(network)
#
#     time1=len(network.nodes())
#     time2=time1+1
#     degreeOfTime1=[int(round(powerlawrnd2(gama,2)))]
#     nodesRemain=[]
#     nodes=[]
#     edges = network.edges()
#     if degreeOfTime1[0]%2==0:
#         nodesRemain.extend([time1]*degreeOfTime1[0])
#         nodes.append(time1)
#         degree[time1] =degreeOfTime1[0]
#     else:
#         nodesRemain.extend([time1]*(degreeOfTime1[0]-1))
#         nodes.append(time1)
#         nodes.append(time2)
#         edges.append((time1,time2))
#         degree[time1] = degreeOfTime1[0]-1
#
#     hist = {}
#     for i in degree.keys():
#         if not degree[i] in hist.keys():
#             hist[degree[i]] = 0
#         hist[degree[i]] += 1
#     sortedhist = sorted(hist.keys())
#     result = {}
#     for i in degree.keys():
#         result[i]=sortedhist.index(degree[i])
#     alpha = 3
#     tries = 10
#     rewiretries = 100
#     while len(nodesRemain) > 0:
#         if (len(edges) == 0 or tries >= 0) and len(set(nodesRemain)) > 1:
#
#             a, b = random.sample(set(nodesRemain), 2)
#             if a == b or (a, b) in edges or (b, a) in edges:
#                 tries -= 1
#                 continue
#             tries = 10
#             if random.uniform(0, 1) < (1.0 / (1 + alpha * abs(result[a] - result[b]))):
#                 edges.append((a, b))
#                 nodesRemain.remove(a)
#                 nodesRemain.remove(b)
#             rewiretries=100
#         else:
#             if len(set(nodesRemain))==1:
#                 if len(network.edges())>=len(nodesRemain):
#                     splitedges=random.sample(network.edges(),len(nodesRemain))
#                 else:
#                     splitedges = network.edges()
#                 network.remove_edges_from(splitedges)
#                 for i in splitedges:
#                     nodesRemain.extend((i[0],i[1]))
#                 continue
#             tries = 10
#             rewiretries-=1
#             if rewiretries<=0:
#                 break
#             edge1 = random.choice(edges)
#             if (len(nodesRemain) == 1):
#                 break
#             stub1, stub2 = random.sample(nodesRemain, 2)
#             if (edge1[0] == stub1 or edge1[1] == stub1) and (edge1[0] == stub2 or edge1[1] == stub2):
#                 continue
#             if (not edge1[0] == stub1) and (not edge1[1] == stub2):
#                 a1 = (edge1[0], stub1)
#                 a2 = (stub1, edge1[0])
#                 b1 = (edge1[1], stub2)
#                 b2 = (stub2, edge1[1])
#             elif (not edge1[0] == stub2) and (not edge1[1] == stub1):
#                 a1 = (edge1[0], stub2)
#                 a2 = (stub2, edge1[0])
#                 b1 = (edge1[1], stub1)
#                 b2 = (stub1, edge1[1])
#             else:
#                 print("error")
#                 continue
#             if not ((a1 in edges) or (a2 in edges) or (b1 in edges) or (b2 in edges)):
#                 edges.remove(edge1)
#                 edges.append(a1)
#                 edges.append(b1)
#                 nodesRemain.remove(stub1)
#                 nodesRemain.remove(stub2)
#     G=nx.Graph()
#     G.add_edges_from(edges)
#     return G
def Friends_FoF(network,n,numofFriends,numofFoF,probofFriends,probofFoF):
    """
    新点选择numofFriends个朋友以概率probofFriends建立连接
    选择nmofFoF个朋友的朋友以概率probofFoF建立连接
    若发现新人没有建立任何连接，则删除新人
    :param network:
    :param n: 变化的次数
    :param numofFriends: 每次选中的朋友的数量
    :param numofFoF:    每次选中的朋友的朋友的数量
    :param probofFriends: 连接选中的朋友的概率
    :param probofFoF:    连接选中的朋友的朋友的概率

    :return: network
    """
    times=len(network.nodes())
    while times<n:

        time1 = times

        """连接朋友"""
        if (numofFriends > times):
            selected_Friends = list(network.nodes())
        else:
            selected_Friends=random.sample(list(network.nodes()),int(numofFriends))
        network.add_node(time1)
        for i in selected_Friends:
            if  random.random()<probofFriends:
                if time1==i:
                    continue
                network.add_edge(time1,i)
        """连接朋友的朋友"""
        Neighbour=list(nx.neighbors(network,time1))
        if len(Neighbour)==0:
            continue
        Neighbourwillconnect=set([])

        for i in Neighbour:
            neighborsexcludeself =list(nx.neighbors(network,i))
            Neighbourwillconnect.update(neighborsexcludeself)
        Neighbourwillconnect.remove(time1)
        if(numofFoF>len(Neighbourwillconnect)):
            selected_FoF=Neighbourwillconnect
        else:
            selected_FoF=random.sample(Neighbourwillconnect,int(numofFoF))
        for i in selected_FoF:
            if random.uniform(0,1)<probofFoF:
                if time1==i:
                    continue
                network.add_edge(time1,i)

        # if not nx.is_connected(network):
        #     network.remove_node(time1)
        times = len(network.nodes())
    return network
def Friends_FoF2(nodeAttribute,nodeNeighbors,n,numofFriends,numofFoF,probofFriends,probofFoF):
    """
    新点选择numofFriends个朋友以概率probofFriends建立连接
    选择nmofFoF个朋友的朋友以概率probofFoF建立连接
    若发现新人没有建立任何连接，则删除新人
    :param network:
    :param n: 变化的次数
    :param numofFriends: 每次选中的朋友的数量
    :param numofFoF:    每次选中的朋友的朋友的数量
    :param probofFriends: 连接选中的朋友的概率
    :param probofFoF:    连接选中的朋友的朋友的概率

    :return: network
    """
    ansedge=[]
    times=len(nodeAttribute.keys())
    while times<n:

        time1 = times

        """连接朋友"""
        if (numofFriends > times):
            selected_Friends = list(nodeAttribute.keys())
        else:
            selected_Friends=random.sample(list(nodeAttribute.keys()),numofFriends)
        for i in selected_Friends:
            if  random.random()<probofFriends:
                if time1==i:
                    continue
                if time1 not in nodeAttribute.keys():
                    nodeAttribute[time1] = [0, 0]
                    nodeNeighbors[time1] = set()
                if i not in nodeAttribute.keys():
                    nodeAttribute[i] = [0, 0]
                    nodeNeighbors[i] = set()
                nodeNeighbors[time1].add(i)
                nodeAttribute[time1][0] = len(nodeNeighbors[time1])
                nodeNeighbors[i].add(time1)
                nodeAttribute[i][0] = len(nodeNeighbors[i])
                ansedge.append((time1,i))
        """连接朋友的朋友"""
        if time1 not in nodeAttribute.keys():
            continue
        Neighbour=nodeNeighbors[time1]
        Neighbourwillconnect=set([])

        for i in Neighbour:
            neighborsexcludeself =list(nodeNeighbors[i])
            Neighbourwillconnect.update(neighborsexcludeself)
        Neighbourwillconnect.remove(time1)
        if(numofFoF>len(Neighbourwillconnect)):
            selected_FoF=Neighbourwillconnect
        else:
            selected_FoF=random.sample(Neighbourwillconnect,numofFoF)
        for i in selected_FoF:
            if random.uniform(0,1)<probofFoF:
                if time1==i:
                    continue
                if time1 not in nodeAttribute.keys():
                    nodeAttribute[time1] = [0, 0]
                    nodeNeighbors[time1] = set()
                if i not in nodeAttribute.keys():
                    nodeAttribute[i] = [0, 0]
                    nodeNeighbors[i] = set()
                nodeNeighbors[time1].add(i)
                nodeAttribute[time1][0] = len(nodeNeighbors[time1])
                nodeNeighbors[i].add(time1)
                nodeAttribute[i][0] = len(nodeNeighbors[i])
                ansedge.append((time1, i))
        # if not nx.is_connected(network):
        #     network.remove_node(time1)
        times = len(nodeAttribute.keys())
    return ansedge
def BA_evolution(G,n,m=None,seed=None):
    """
    BA的演化，每次加一个点，m条边，新点偏向于和度数大的节点连接
    :param G: 网络
    :param n: n次变化
    :param m: 新点连接m条边 默认为网络平均度数
    :param seed: random 的参数
    :return:G
    """
    nodes=list(G.nodes())
    degreeG=nx.degree(G)
    lnodes=len(nodes)

    if m is None:
        m=int(round(sum(degreeG.values())/lnodes))
    if m < 1 or m >= lnodes:
        raise nx.NetworkXError("Barabási–Albert network must have m >= 1"
                               " and m < n, m = %d, n = %d" % (m, lnodes))
    if seed is not None:
        random.seed(seed)
    repeated_nodes = []
    for i in nodes:
        repeated_nodes.extend([i]*degreeG[i])

    times=0
    while times<n:
        targets = _random_subset(repeated_nodes, m)
        source = len(nodes)
        nodes.append(source)
        G.add_node(source)
        G.add_edges_from(zip([source] * m, targets))
        repeated_nodes.extend([source]*m)
        repeated_nodes.extend(targets)

        times=times+1
    return G
def SBM(nodeAttribute, nodeNeighbors, n,deg=6):
    n=len(nodeAttribute.keys())+500+1
    n3 = n // 3
    p2 = 3 * deg / (8 * n)
    p1 = 6 * p2
    ansedges=[]
    newNode=n
    assignBlock=random.choice([1,2,3])
    nodeAttribute[newNode]=[0,assignBlock]
    nodeNeighbors[newNode] = set()
    for node in nodeAttribute.keys():
        if nodeAttribute[node][1]==assignBlock:
            if random.uniform(0, 1) <= p1:
                nodeAttribute[node][0]+=1
                nodeNeighbors[newNode].add(node)
                nodeNeighbors[node].add(newNode)
                ansedges.append((newNode,node))
        else:
            if random.uniform(0, 1) <= p2:
                nodeAttribute[node][0]+=1
                nodeNeighbors[newNode].add(node)
                nodeNeighbors[node].add(newNode)
                ansedges.append((newNode, node))
    nodeAttribute[newNode][0]=len(nodeNeighbors[newNode])

    return ansedges




def BA_evolution2(nodeAttribute,nodeNeighbors,n,m=None,seed=None):
    """
    BA的演化，每次加一个点，m条边，新点偏向于和度数大的节点连接
    :param G: 网络
    :param n: n次变化
    :param m: 新点连接m条边 默认为网络平均度数
    :param seed: random 的参数
    :return:G
    """
    # nodes=list(G.nodes())
    # degreeG=nx.degree(G)
    lnodes=len(nodeAttribute.keys())

    if m is None:
        m=int(round(sum([x[0] for x in nodeAttribute.values()])/lnodes))
    if m < 1 or m >= lnodes:
        print("Barabási–Albert network must have m >= 1"
                               " and m < n, m = %d, n = %d" % (m, lnodes))
    repeated_nodes = []
    for i in nodeAttribute.keys():
        repeated_nodes.extend([i]*nodeAttribute[i][0])
    targets = _random_subset(repeated_nodes, m)
    source = len(nodeAttribute.keys())
    # nodes.append(source)
    # G.add_node(source)
    # G.add_edges_from(zip([source] * m, targets))
    nodeAttribute[source]=[m,0]
    nodeNeighbors[source]=set(targets)
    for j in targets:
        nodeNeighbors[j].add(source)
        nodeAttribute[j][0]=len(nodeNeighbors[j])
    repeated_nodes.extend([source]*m)
    repeated_nodes.extend(targets)
    return list(zip([source] * m, targets))
def _random_subset(seq, m):
    """ Return m unique elements from seq.

    This differs from random.sample which can return repeated
    elements if seq holds repeated elements.
    """
    targets = set()
    while len(targets) < m:
        x = random.choice(seq)
        targets.add(x)
    return targets
def rich_club(network,alpha,n,time1=None):

    """
    根据 幂律分布的指数，决定添加一个点的概率为alpha，否则添加一条边

    添边时，随机选出一个源节点，然后以概率选择一目标度数 概率为 度数*该度数的节点数/sum(度数*节点数)
    之后从目标度数下随机选择一点为目标点
    :param network:
    :param gama:  k^(-gama)

    :param time1:新点名字 默认为len(nodes)
    :return:

    onionveils 层数关系 论文中的[k]
    """
    if time1 is None:
        time1=len(network.nodes())
    # alpha=1-1.0/(gama-1)
    # print(time1
    times=len(network.nodes())
    a=0
    while times<n:
        a+=1
        if random.uniform(0,1)<=alpha:
            """add a new node"""
            """随机选择一个点连接之"""
            target=random.choice(list(network.nodes()))
            network.add_edge(time1,target)
            # print("add 1 node"
        else:
            degree=nx.degree(network)
            hist = nx.degree_histogram(network)
            lhist=len(hist)
            denominator=0
            for i in range(lhist):
                denominator+=i*hist[i]
            prob=[]
            for j in range(lhist):
                prob.append(float(j*hist[j])/denominator)
            bool=True
            # print(prob
            for tries in range(10):
                source=random.choice(list(network.nodes()))

                targetveil=cp.prob_select(range(1,lhist),prob[1:],1)
                targetveilS=[]
                for i in network.nodes():
                    if degree[i]==targetveil[0]:
                        targetveilS.append(i)

                target=random.choice(targetveilS)
                if not (source==target or (source,target) in list(network.edges()) or (target,source) in list(network.edges())):
                    network.add_edge(source,target)
                    # print("add 1 edge"
                    bool=False
                    break
            if bool==True:
                print("超过最大尝试加边次数")
        times=len(network.nodes())
        time1 = times
    # print(a
    return network
def rich_club2(nodeAttribute,nodeNeighbors,alpha,n,time1=None):

    """
    根据 幂律分布的指数，决定添加一个点的概率为alpha，否则添加一条边

    添边时，随机选出一个源节点，然后以概率选择一目标度数 概率为 度数*该度数的节点数/sum(度数*节点数)
    之后从目标度数下随机选择一点为目标点
    :param network:
    :param gama:  k^(-gama)

    :param time1:新点名字 默认为len(nodes)
    :return:

    onionveils 层数关系 论文中的[k]
    """
    if time1 is None:
        time1=len(nodeAttribute.keys())
    # alpha=1-1.0/(gama-1)
    # print(time1

    times=len(nodeAttribute.keys())
    a=0
    ansedge=[]
    while times<n:
        a+=1
        if random.uniform(0,1)<=alpha:
            """add a new node"""
            """随机选择一个点连接之"""
            target=random.choice(list(nodeAttribute.keys()))

            if time1 not in nodeAttribute.keys():
                nodeAttribute[time1] = [0, 0]
                nodeNeighbors[time1] = set()
            if target not in nodeAttribute.keys():
                nodeAttribute[target] = [0, 0]
                nodeNeighbors[target] = set()
            nodeNeighbors[time1].add(target)
            nodeAttribute[time1][0] = len(nodeNeighbors[time1])
            nodeNeighbors[target].add(time1)
            nodeAttribute[target][0] = len(nodeNeighbors[target])
            ansedge.append((time1,target))
            # print("add 1 node"
        else:
            # degree=nx.degree(network)
            hist = degree_histogram(nodeAttribute,nodeNeighbors)
            lhist=len(hist)
            denominator=0
            for i in range(lhist):
                denominator+=i*hist[i]
            prob=[]
            for j in range(lhist):
                prob.append(float(j*hist[j])/denominator)
            bool=True
            # print(prob
            for tries in range(10):
                source=random.choice(list(nodeAttribute.keys()))

                targetveil=cp.prob_select(range(1,lhist),prob[1:],1)
                targetveilS=[]
                for i in nodeAttribute.keys():
                    if nodeAttribute[i][0]==targetveil[0]:
                        targetveilS.append(i)

                target=random.choice(targetveilS)
                if not (source==target or source in nodeNeighbors[target] or target in nodeNeighbors[source]):
                    nodeNeighbors[source].add(target)
                    nodeAttribute[source][0] = len(nodeNeighbors[source])
                    nodeNeighbors[target].add(source)
                    nodeAttribute[target][0] = len(nodeNeighbors[target])

                    # network.add_edge(source,target)
                    # print("add 1 edge"
                    ansedge.append((source,target))
                    bool=False
                    break
            if bool==True:
                print("超过最大尝试加边次数")
        times=len(nodeAttribute.keys())
        time1 = times
    # print(a
    return ansedge
def degree_histogram(nodeAttribute,nodeNeighbors):
    """Return a list of the frequency of each degree value.

    Parameters
    ----------
    G : Networkx graph
       A graph

    Returns
    -------
    hist : list
       A list of frequencies of degrees.
       The degree values are the index in the list.

    Notes
    -----
    Note: the bins are width one, hence len(list) can be large
    (Order(number_of_edges))
    """
    degseq=list(x[0] for x in nodeAttribute.values())
    dmax=max(degseq)+1
    freq= [ 0 for d in range(dmax) ]
    for d in degseq:
        freq[d] += 1
    return freq
def B_A(network, internal_link_factor, links_added_per_step, add_percentage, del_percentage, time_step):
    # parameters initialization
    f = internal_link_factor
    m = links_added_per_step
    num_add = int(add_percentage * nx.number_of_nodes(network))
    num_del = int(del_percentage * nx.number_of_nodes(network))
    time = time_step
    probability = []
    probability_temp = []
    total_probability = 0
    nodes_pre_step = []
    nodes_added_this_step = []
    nodes_pair_without_edge = []
    nodes_for_del = []



    # calculate the probability of each node to be linked according to whose degree
    for node in nx.nodes_iter(network):
        #print('degree',network.degree(node)
        nodes_pre_step.append(node)
        probability_temp.append(network.degree(node))
        total_probability += network.degree(node)
    for prob in probability_temp:
        probability.append(float(prob) / total_probability)
    #print('prob_temp',probability
    #print('prob',probability

    # add num_add nodes to the network
    i = 1
    while i <= num_add:
        nodes_added_this_step.append('%d' % time + '_' + '%d' % i)
        i += 1
    network.add_nodes_from(nodes_added_this_step)

    # create m links for each node added in this time dtep according to the probability
    #print('nodes_pre_step',nodes_pre_step
    for node_added in nodes_added_this_step:
        selected_nodes = cp.prob_select(nodes_pre_step,probability,m)
        #print('selected_nodes', selected_nodes
        for node in selected_nodes:
            network.add_edge(node_added,node)

    # add f % internal links according to the production of each pair of nodes' degrees
    probability = []
    probability_temp = []
    total_probability = 0
    for i, elei in enumerate(nx.nodes_iter(network)):
        for j, elej in enumerate(nx.nodes_iter(network)):
            if i >= j:
                continue
            if not network.has_edge(elei, elej):
                nodes_pair_without_edge.append((elei,elej))
                probability_temp.append(network.degree(elei) * network.degree(elej))
                total_probability += network.degree(elei) * network.degree(elej)
    for prob in probability:
        probability.append(float(prob) / total_probability)
    selected_pairs = cp.prob_select(nodes_pair_without_edge,probability,int(f*nx.number_of_nodes(network)))
    for nodei,nodej in selected_pairs:
        network.add_edge(nodei,nodej)

    # delete num_del nodes according to whose degree
    probability = []
    probability_temp = []
    total_probability = 0.0
    for node in nx.nodes_iter(network):
        nodes_for_del.append(node)
        if network.degree(node) == 0:# if the degree is 0, let it to be 0.1, to avoid errors in probability calculation
            node_degree = 0.1
        else:
            node_degree = network.degree(node)
        probability_temp.append(1.0/node_degree)
        total_probability += 1.0/node_degree
    for prob in probability_temp:
        probability.append(prob/total_probability)
    selected_del = cp.prob_select(nodes_for_del,probability,num_del)
    for node in selected_del:
        network.remove_node(node)
        #print('del',node
    return True

if __name__ == '__main__':
    import networks as ns
    # G=ns.sparse(20)
    # G=ns.Regular(10)
    # print(len(G.edges())
    G = generate_onion(200)
    # G=ns.onionNetwork200()
    # G=ns.fof_200_4_4_0d3_0d3()
    # cp.networkProperty(G)
    # while len(G.nodes())<200:
    #     G=onionEvolution(G)
    #
    # G=BA_evolution(G,190,3)
    # G=rich_club(G, 2.5, 200)
    # G=Friends_FoF(G,200,5,5,0.3,0.3)
    cp.networkProperty(G)

    #     # G=Friends_FoF(G,len(G.nodes())+1,4,4,0.3,0.3)
    #     G=BA_evolution(G,1,3)
    # import calculate_param as cm
    # cm.draw(G)
    # import matplotlib.pyplot as plt
    # plt.show()
    cp.draw(G, 1, "close")
    cp.draw(G, 1,"eccen")
    print(G.edges())
