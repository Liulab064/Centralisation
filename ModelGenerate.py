#coding=utf-8
import networkx as nx
import evolution_models
import multiprocessing
def Regular(n):
    G = nx.path_graph(n)
    G.add_edge(n - 1, 0)
    return G

def generateNetwork(evolutionmodel,size,avedeg):
    gama = {6: 4, 8: 2.9, 10: 2.52, 12: 2.3, 14: 2.1}
    SFOF = {4: [(4.0, 4.0, 0.25, 0.25), (2.0, 2.0, 0.5, 0.5), (2, 1, 0.75, 0.75), (1.0, 1.0, 1, 1)],
            6: [(6.0, 6.0, 0.25, 0.25), (3.0, 3.0, 0.5, 0.5), (2.0, 2.0, 0.75, 0.75), (2, 1, 1, 1)],
            8: [(8.0, 8.0, 0.25, 0.25), (4.0, 4.0, 0.5, 0.5), (3, 2, 0.75, 0.75), (2.0, 2.0, 1, 1)],
            10: [(10.0, 10.0, 0.25, 0.25), (5.0, 5.0, 0.5, 0.5), (4, 3, 0.75, 0.75), (3, 2, 1, 1)],
            12: [(12.0, 12.0, 0.25, 0.25), (6.0, 6.0, 0.5, 0.5), (4.0, 4.0, 0.75, 0.75), (3.0, 3.0, 1, 1)],
            14: [(14.0, 14.0, 0.25, 0.25), (7.0, 7.0, 0.5, 0.5), (5, 4, 0.75, 0.75), (4, 3, 1, 1)]}
    RG = Regular(10)

    while len(RG) < size:
        if evolutionmodel== 'BA':
            print("start======")
            evolution_models.BA_evolution(RG, 1, int(avedeg/2))
        elif evolutionmodel == 'SFOF5':
            evolution_models.Friends_FoF(RG, len(RG.nodes()) + 1, SFOF[avedeg][1][0], SFOF[avedeg][1][1], SFOF[avedeg][1][2], SFOF[avedeg][1][3])
        elif evolutionmodel == 'SFOF25':
            evolution_models.Friends_FoF(RG, len(RG.nodes()) + 1, SFOF[avedeg][0][0], SFOF[avedeg][0][1], SFOF[avedeg][0][2],SFOF[avedeg][0][3])
        elif evolutionmodel == 'SFOF1':
            evolution_models.Friends_FoF(RG, len(RG.nodes()) + 1, SFOF[avedeg][3][0], SFOF[avedeg][3][1], SFOF[avedeg][3][2], SFOF[avedeg][3][3])
        elif evolutionmodel == 'Rich club':
            RG = evolution_models.rich_club(RG, 2.0/(avedeg), len(RG.nodes()) + 1)
        elif evolutionmodel == 'onion':
            if avedeg in gama.keys():
                RG = evolution_models.onionEvolution(RG, gama[avedeg])
    print(len(RG))
    print("network generating ends")
    with multiprocessing.Lock():
        f = open("dataEpoch//" +str(evolutionmodel)+"_"+str(size)+"_deg"+ str(avedeg)+".txt", 'a+')
        f.write( str(RG.edges()) + "\n")
        f.close()
if __name__ == '__main__':
    # generateNetwork("SFOF5",5000,4)
    poolist = []
    p = multiprocessing.Pool(3)
    for k in ['SFOF5',"SFOF1",'SFOF25']:     #,"Rich club""onion"'BA',
        for j in range(4,16,2):
            if j==6:continue
            for i in range(2):
                poolist.append(p.apply_async(generateNetwork, args=(k,5000,j,)))
    p.close()
    p.join()