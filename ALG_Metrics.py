#coding=utf-8

import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
import math
import sklearn.linear_model as linear_model
import operator

def draw(network,pos=None,show=1,methods="eccen",name="untitle",save=0,redges=None,rnodes=None):
    # nodes_isolated = []
    # for node in network.nodes():  # find the nodes without edges
    #     if network.degree(node) == 0:
    #         nodes_isolated.append(node)
    # network.remove_nodes_from(nodes_isolated)  # remove the nodes without edges


    # if pos is None:
    # pos = nx.spring_layout(network)
    print(pos)
    centra={}
    sequencecentra = []
    color={}
    for net in nx.connected_component_subgraphs(network):
        subNetwork=nx.subgraph(network,net.nodes())
        if methods=="eccen":
            curcolor={}
            centrality = nx.eccentricity(subNetwork)
            for i in centrality.keys():
                centra[i]=(1/float(centrality[i])*10000)
                # centra.append(1/float(i)*1000)
            for i in centrality.keys():
                sequencecentra.append(i)
                curcolor[i]=centra[i]*100
            curcolor=MaxMinNormalization(curcolor,1,50)
            color.update(curcolor)
            # for i in centra:
            #     color.append(i*10)
        elif methods=="close":
            centrality = nx.closeness_centrality(subNetwork)
            for i in centrality.keys():
                # centra.append(pow(1000.0/i,2.4)/largesize)
                centra[i]=(1/float(centrality[i])*10000)
            color=centrality
    # centra = MaxMinNormalization(centra, 1, 50)

    if not rnodes==None:
        nx.draw_networkx_nodes(network,pos,nodelist=rnodes,node_color='red',node_size=5000,alpha=0.3,with_labels=False)
        nx.draw_networkx_edges(network, pos,
                           edgelist=redges,
                           width=1, alpha=0.2, edge_color='red')

    nx.draw(network, with_labels=True, pos=pos, node_color=[color[x] for x in network.nodes()], alpha=0.6,
            node_size=3500, font_size=40, width=1)

    if show==1:
        plt.show()
    if save==1:
        plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)

        plt.savefig(str(name) + ".jpg", dpi=1000, bbox_inches='tight')
    return True
def generate_random_graph(network):
    """
    :param network: 一个图
    :return: 一个随机图
    """
    import copy
    G=copy.deepcopy(network)
    data=dict(nx.degree(G)).values()
    tries=sum(data)

    for curtry in range(tries/2):
        # print(curtry)
        #randomly select one edge
        edge1=random.choice(list(G.edges()))
        edge2=random.choice(list(G.edges()))
        differelements=len(set([edge1[0], edge1[1], edge2[0], edge2[1]]))
        while differelements < 3:
            edge2 = random.choice(list(G.edges()))
            differelements = len(set([edge1[0], edge1[1], edge2[0], edge2[1]]))
        if differelements==4:
            a1 = (edge1[0], edge2[1])
            a2 = (edge2[1], edge1[0])
            b1 = (edge1[1], edge2[0])
            b2 = (edge2[0], edge1[1])
            if not ((a1 in list(G.edges())) or (a2 in list(G.edges())) or (b1 in list(G.edges())) or (b2 in list(G.edges()))):
                G.remove_edges_from([edge1])
                G.add_edges_from([a1,b1])
            else:
                a1 = (edge1[0], edge2[0])
                a2 = (edge2[0], edge1[0])
                b1 = (edge1[1], edge2[1])
                b2 = (edge2[1], edge1[1])
                if not ((a1 in list(G.edges()))) or (a2 in list(G.edges())) or (b1 in list(G.edges())) or (b2 in list(G.edges())):
                    G.remove_edges_from([edge1])
                    G.add_edges_from([a1, b1])
                # else:
                #     print("existing) edges"
        if differelements==3:
            if edge1[0]==edge2[0]:
                a1=(edge1[0], edge2[1])
                a2=(edge2[1],edge1[0])
                b1=(edge2[0],edge1[1])
                b2 = (edge1[1], edge2[0])
            elif edge1[0]==edge2[1] or edge1[1]==edge2[0]:
                a1 = (edge1[0], edge2[0])
                a2 = ( edge2[0],edge1[0])
                b1 = (edge2[1], edge1[1])
                b2 = ( edge1[1],edge2[1])
            elif edge1[1]==edge2[1]:
                a1 = (edge1[1], edge2[0])
                a2 = (edge2[0], edge1[1])
                b1 = (edge2[1], edge1[0])
                b2 = (edge1[0], edge2[1])

            if not ((a1 in list(G.edges())) or (a2 in list(G.edges())) or (b1 in list(G.edges())) or (b2 in list(G.edges()))):
                G.remove_edges_from([edge1])
                G.add_edges_from([a1, b1])
            # else:
                # print("existing) edges"
    return G


def generate_random_graph_Withk(network):
    """
    :param network: 一个图
    :return: 一个随机图
    """
    import copy
    G = copy.deepcopy(network)
    # data = dict(nx.degree(G)).values()
    tries = nx.number_of_edges(G)
    adjG = nx.adjacency_matrix(G);
    # print(adjG)
    # print(list(G.edges()))
    for curtry in range(tries*2):

        edge1 = random.choice(list(G.edges()))
        edge2 = random.choice(list(G.edges()))
        # edge1=(edge1[0]-1,edge1[1]-1)
        # edge2 = (edge2[0] - 1, edge2[1] - 1)
        differelements = len(set([edge1[0], edge1[1], edge2[0], edge2[1]]))
        while differelements < 3:
            edge2 = random.choice(list(G.edges()))
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
        if differelements == 3:
            if edge1[0] == edge2[0]:
                a1 = (edge1[0], edge2[1])
                b1 = (edge2[0], edge1[1])
            elif edge1[0] == edge2[1] or edge1[1] == edge2[0]:
                a1 = (edge1[0], edge2[0])
                b1 = (edge2[1], edge1[1])
            elif edge1[1] == edge2[1]:
                a1 = (edge1[1], edge2[0])
                b1 = (edge2[1], edge1[0])

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
def networkProperty(G):
    print("size: ",len(G.nodes()))

    print("Volume: ",nx.number_of_edges(G))

    print("average_degree: ",2*nx.number_of_edges(G)/ float(nx.number_of_nodes(G)))

    print("transitivity: ",nx.transitivity(G))

    print("trianglesNum: ",np.sum(nx.triangles(G).values()))

    print("average_clustering: ", nx.average_clustering(G))

    print("maxdegree: ", max(list(nx.degree(G)),key=lambda x:x[1]))

    # print("core size: ",len(nx.center(max(nx.connected_component_subgraphs(G),key=len))))


    try:
        diameter = nx.diameter(G)
        print("diameter: " + str(diameter))
        print("radius: " + str(nx.radius(G)))
        # average_shortest_path_length = nx.average_shortest_path_length(G)
        # print("average_shortest_path_length: " + str(average_shortest_path_length))
    except:
        Gc = max(nx.connected_component_subgraphs(G), key=len)
        print("sub diameter: " + str(nx.diameter(Gc)))
        print("sub radius: " + str(nx.radius(Gc)))
        average_shortest_path_length = nx.average_shortest_path_length(Gc)
        print("sub average_shortest_path_length: " + str(average_shortest_path_length))
def cc(U,seq):
    return float(len(U)) / sum([1.0 / item[1] for item in seq if item[0] in U])

def Ccp(G,kcore):
    seq = nx.closeness_centrality(G)
    seq=seq.items()
    CcV=cc(G.nodes(),seq)
    CcVcore=cc(kcore,seq)
    Ccp = CcVcore / CcV
    return Ccp
def test_cp(GO):
    import GenerateRG
    G=GenerateRG.dataProcessing(GO)
    # kcore = nx.k_core(G).nodes()
    # Gccp=Ccp(G,kcore)
    Gccp=1.4353750984925144
    sumRCcp=0
    print( Gccp)
    import time
    for i in range(5):
        # time_start=time.time()
        G0=generate_random_graph_Withk(G)
        # G0=nx.havel_hakimi_graph(nx.degree(G).values())
        print('generate ends')
        G0=max(nx.connected_component_subgraphs(G0),key=len)
        kcore0=nx.k_core(G0).nodes()
        temp=Ccp(G0,kcore0)
        print("temp ",temp)
        sumRCcp+=temp
        # time_span = time.time()-time_start
    aveRCcp =sumRCcp/5.0
    print(Gccp-aveRCcp)
    return Gccp-aveRCcp
def draw_regression(X,Y,X1=None,Y1=None,name=None):
    # 设置图表字体为华文细黑，字号15
    fig = plt.figure(figsize=(12, 6))
    plt.rc('font', family='STXihei', size=15)
    # 绘制散点图，广告成本X，点击量Y，设置颜色，标记点样式和透明度等参数
    plt.scatter(X, Y, 60, color='blue', marker='o', linewidth=3, alpha=0.8)
    if not (X1 is None or Y1 is None):
        plt.plot(X1,Y1)
    # 添加x轴标题
    plt.xlabel('log10(d)')
    # 添加y轴标题
    plt.ylabel('log10(f(d))')
    # 添加图表标题
    plt.title('degree distribution')
    # 设置背景网格线颜色，样式，尺寸和透明度
    plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='both', alpha=0.4)
    # 显示图表
    plt.show()
    # plt.savefig(name)
def log_log_regression(RG,r0=0.5,name = None):
    degreeHistogram=nx.degree_histogram(RG)
    del degreeHistogram[0]

    Ldegree=len(degreeHistogram)
    print(Ldegree)
    score=0
    r1=float(1)
    logdegree = []
    # 度数为0不考虑
    for i in range(1, Ldegree):
        j = math.log10(i)
        logdegree.append(j)

    logdegreeHistogram = []
    total = sum(degreeHistogram)
    numiszero=[]
    for i in range(1, Ldegree):
        if degreeHistogram[i] > 0:
            F = math.log10(degreeHistogram[i])
        else:
            F=0
            numiszero.append(i)
        logdegreeHistogram.append(F)
    #print("前")
    #print(len(logdegreeHistogram))
    #print(numiszero)
    numiszero.sort(reverse = True)
    for i in numiszero:
        del logdegreeHistogram[i]
        del logdegree[i]
    #print("后")
    #print(logdegreeHistogram)
    #print(logdegree)
    #print(len(logdegreeHistogram))
    """控制度数为1的点"""
    del logdegreeHistogram[0]
    del logdegree[0]

    Y = np.array(logdegreeHistogram)
    X = np.array(logdegree)

    X = X.reshape((len(X), 1))
    Y = Y.reshape((len(Y), 1))
    score0=1
    while score<0.8:
        if abs(score-score0)<=0.00001:
            break
        # r0=r1
        #"指定分类器"
        clf=linear_model.LinearRegression()
        clf.fit(X,Y)
        #返回斜率
        coef= clf.coef_
        print("coef="+str(coef))
        #截距
        # r1=float(r0)
        intercept=clf.intercept_
        #判定系数
        score0=score
        score=clf.score(X,Y)
        print("score: "+str(score))
    # draw_regression(X,Y,X,clf.predict(X),name = name)
    draw_regression(X, Y)
    return r1

def MaxMinNormalization(x,nr_min,nr_max):

    # out = np.zeros(len(x))
    out={}
    _min = min(x.values())
    _max = max(x.values())
    for i in x.keys():
        tmp = (x[i] - _min) / (_max - _min) if _max>_min else 0
        out[i] = nr_min + tmp*(nr_max - nr_min)

    # print(np.argmax(out))
    return out
def drawNetwork(network):
    nodes_isolated = []
    centrality = nx.eccentricity(network)  # show the network colored according the the centrality of nodes
    centra = []
    for i in centrality.values():
        centra.append(1 / float(i) * 1000)
    # print(centra)
    # print(centrality)

    nx.draw(network, with_labels=True, pos=nx.spring_layout(network), node_color=centrality.values(), alpha=0.2,
            node_size=centra, font_size=7)
    plt.show()
    return True
def drawNewEdge(G,newEdge=[],show=0,save=1,title="untitled",nodeset = [],kCore = [],edges=[],epoch = 0):
    plt.close()
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.layout

    centrality = nx.eccentricity(G)  # show the network colored according the the centrality of nodes
    centra = []
    sequencecentra=[]
    centraNew = []
    centraKCore = []
    for i in centrality.keys():
        sequencecentra.append(i)
    for i in centrality.values():
        centra.append(1 / float(i))
    centra = MaxMinNormalization(centra,1,50)
    for i in nodeset:
        centraNew.append(centra[i])
    for i in kCore:
        centraKCore.append(centra[sequencecentra.index(i)])
    # nodes
    nx.draw_networkx_nodes(G, pos,
                           node_size=centra,
                           alpha=0.4,node_color='black',with_labels=True)

    nx.draw_networkx_nodes(G, pos,
                           nodelist=list(kCore),
                           node_color='red',
                           node_size=centraKCore,
                           alpha=0.9, with_labels=True)
    nx.draw_networkx_nodes(G, pos,
                           nodelist=list(nodeset),
                           node_color='blue',
                           node_size=centraNew,
                           alpha=0.9,with_labels=True)
    nx.draw_networkx_edges(G, pos, alpha=0.1,edge_color='green')
    # edges
    nx.draw_networkx_edges(G, pos,
                           edgelist=newEdge,
                           width=1, alpha=0.4, edge_color='red')

    nx.draw_networkx_edges(G, pos,
                           edgelist=edges,
                           width=1, alpha=0.4, edge_color='blue')


    plt.axis('off')
    if save == 1:
        plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)


        plt.savefig(title+".jpg",dpi = 1000,bbox_inches='tight')
        #plt.savefig(title+".jpg",dpi = 1000,bbox_inches='tight')
    if show==1:
        plt.show()  # display
def drawNewEdgeandNode(G,newEdge=[],show=0,save=1,title="untitled",nodeset = [],kCore = [],edges=[],epoch = 0):
    plt.close()
    pos = nx.spring_layout(G)  # positions for all nodes

    centrality = nx.eccentricity(G)  # show the network colored according the the centrality of nodes
    centra = []
    centraNew = []
    centraKCore = []
    sequencecentra=[]
    for i in centrality.keys():
        sequencecentra.append(i)
    for i in centrality.values():
        centra.append(1 / float(i))
    centra = MaxMinNormalization(centra,8,50)
    for i in nodeset:
        centraNew.append(centra[i])
    for i in kCore:
        centraKCore.append(centra[sequencecentra.index(i)])
    print(centraKCore)
    # nodes
    nx.draw_networkx_nodes(G, pos,
                           node_size=centra,
                           alpha=0.7,node_color='black',with_labels=False)

    nx.draw_networkx_nodes(G, pos,
                           nodelist=list(kCore),
                           node_color='red',
                           node_size=centraKCore,
                           alpha=1, with_labels=False)

    nx.draw_networkx_edges(G, pos, alpha=0.2,edge_color='green')
    # edges
    nx.draw_networkx_edges(G, pos,
                           edgelist=newEdge,
                           width=2, alpha=1, edge_color='red')

    nx.draw_networkx_edges(G, pos,
                           edgelist=edges,
                           width=1, alpha=0.5, edge_color='blue')


    plt.axis('off')
    if save == 1:
        plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)


        plt.savefig(title+".jpg",dpi = 1000,bbox_inches='tight')
        #plt.savefig(title+".jpg",dpi = 1000,bbox_inches='tight')
    if show==1:
        plt.show()  # display
def prob_select(target_list, probability, num=1):
    selected = []
    i = 0
    while i < num:
        x = random.uniform(0,1)
        cumulative_probability = 0.0
        for item, item_probability in zip(target_list,probability):
            cumulative_probability += item_probability
            if x < cumulative_probability:
                selected.append(item)
                break
        i += 1

    selected_list = list(set(selected))  # remove repeated items
    # print(target_list)
    # print(selected_list)
    return selected_list
if __name__ == '__main__':
    import networks as ns
    # import linecache
    # G=ns.fig5b()
    #["BA", "Rich club", "onion", "SFOF1", "SFOF5", "SFOF25"]
    # temp = linecache.getline("dataEpoch//" + "SBM" + "_" + "50000" + ".txt",
    #                          1)
    # edge = eval(temp)
    # G=nx.Graph()
    # G.add_edges_from(edge)
    # networkProperty(G)
    # G=
    # log_log_regression(G)

    target=[1,2]
    print(prob_select(target,[0.3,0.7]))
    # draw(G,show=1)
    # draw(G)
    # plt.show()