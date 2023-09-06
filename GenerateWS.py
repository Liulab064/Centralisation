import networkx as nx
import community
if __name__ == '__main__':

    # n1=n2=n3,  n1+n2+n3=5000
    #n1=n2
    # p1=6p2

    # n1p1+n2p2+p2*n3=d
    # n1p2+n2p1+p3n3=6
    # n3p1+n1p2+n2p2=6

    # 6cn3p2+cn3p2+n3p2=6....> n3p2=6/(7c+1)
    # 6n3p2+cn3p2+cn3p2=6  ----> n3p2=6/(8)


    # p1n1+p2n-p2n1=6
    # 6p2n3+5p2n3-2p2n3=6
    # p2n3=3/4

    # p2=9/4n
    # p1=27/2n
    # n=2000
    # n3 = n // 3
    # n1=n2=n3
    # p1=27/(2*n)
    # p2=9/(4*n)
    # G=nx.stochastic_block_model([n1, n2, n3],[[p1, p2,p2], [p2, p1,p2], [p2, p2,p1]])
    # print(nx.number_of_edges(G)/nx.number_of_nodes(G))
    #
    # for n in [500,2000,5000,10000,20000,50000,100000]:
    #     print(n)
    #     n3 = n // 3
    #     n1=n2=n3
    #     p1=27/(2*n)
    #     p2=9/(4*n)
    #     G = nx.stochastic_block_model([n1, n1, n3],
    #                                   [[p1, p2,p2], [p2, p1,p2], [p2, p2,p2]])
    #
    #     # G=nx.watts_strogatz_graph(n,6,0.1)
    #     f=open("dataEpoch\\SBM_"+str(n)+".txt",'w')
    #     f.write(str(list(G.edges())))
    #     f.flush()
    #     f.close()

    # n1=n2=n3,  n1+n2+n3=5000
    # n1=n2
    # p1=6p2

    # n1p1+n2p2+p2*n3=d
    # n1p2+n2p1+p3n3=d
    # n3p1+n1p2+n2p2=d
    # p2n3=d/8
    # p2=3d/(8*5000)
    n = 5000
    for deg in [6]: #, 8, 10, 12, 14 10
        print(deg)
        n3 = n // 3
        n1 = n2 = n3
        p2 = 3 * deg / (8 * n)
        p1 = 6 * p2
        G = nx.stochastic_block_model([n1, n1, n3],
                                      [[p1, p2, p2], [p2, p1, p2], [p2, p2, p2]])
        f=open("dataEpoch\\SBM_"+str(n)+".txt",'w')
        largeC=max(nx.connected_components(G), key=len)
        subG=nx.subgraph(G,list(largeC))
        f.write(str(list(subG.edges())))
        f.flush()
        f.close()

        # f = open("dataEpoch\\SBM_5000_deg" + str(deg) + ".txt", 'w')
        # f.write(str(list(G.edges())))
        # f.close()

        # import matplotlib.pyplot as plt
        # nx.draw_kamada_kawai(G,with_labels=True)
        #
        # plt.show()