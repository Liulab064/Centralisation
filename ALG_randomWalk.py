#import networkx as nx
#import matplotlib.pyplot as plt
import ALG_LinkingMethods2 as cm
#import time
import multiprocessing
#import sys
#import random
import linecache
# import soc_sign_bitcoinotc
# import network_colledgeMsg
# import network_cit_new
# import network_haggle
import copy
import math


def test2(evolutionmodel, initsize, methods):
    """

    :param evolutionmodel:
    :param initsize:
    :return:
    """
    """
    initialize network:   nodeAttribute:[{nodeindex:deg+color},{}]
                        nodeNeighbors:[{nodeindex:[neighbors]}]
    """
    nodeAttribute = {}
    nodeNeighbors = {}
    init = 1
    for i in range(init, initsize + 1, 1):
        if evolutionmodel == "cit":
            temp = linecache.getline("dataEpoch//cit.txt", i)
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel == "colledge":
            temp = linecache.getline("dataEpoch//CollegeMsg.txt", i)
            temp1 = temp.split(" ")
            edge = [(eval(temp[0]), eval(temp1[1]))]
        elif evolutionmodel == "bitcoin":
            temp = linecache.getline("dataEpoch//soc-sign-bitcoinotc.txt", i)
            temp1 = temp.split(" ")
            edge = [(eval(temp[0]), eval(temp1[1]))]
        elif evolutionmodel == "election_Data":
            temp = linecache.getline("dataEpoch//election_Data.txt", i)
            edge = eval(temp)
        elif evolutionmodel == "infectious":
            temp = linecache.getline("dataEpoch//infectious_data.txt", i)
            edge = eval(temp)
        elif evolutionmodel == 'netScience':
            temp = linecache.getline("dataEpoch//netScienceNew.txt", 1)
            temp = temp.strip()
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel == 'coDblp':
            temp = linecache.getline("dataEpoch//coDblp.txt", 1)
            temp = temp.strip()
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel == 'ca':
            temp = linecache.getline("dataEpoch//ca.txt", 1)
            edge = eval(temp)
        else:
            edge = []

        for e in edge:
            if e[0] not in nodeAttribute.keys():
                nodeAttribute[e[0]] = [0, 0]
                nodeNeighbors[e[0]] = set()
            if e[1] not in nodeAttribute.keys():
                nodeAttribute[e[1]] = [0, 0]
                nodeNeighbors[e[1]] = set()
            nodeNeighbors[e[0]].add(e[1])
            nodeAttribute[e[0]][0] = len(nodeNeighbors[e[0]])
            nodeNeighbors[e[1]].add(e[0])
            nodeAttribute[e[1]][0] = len(nodeNeighbors[e[1]])

        # print(i)
    print("network building end")
    N = len(nodeAttribute.keys())



    print("num of nodes:%d" % N)

    for r in range(3, 2, -1):
        Opinion = cm.opinion(nodeAttribute, ValueFlag=True)
        poolist1 = []
        p1 = multiprocessing.Pool(5)
        coverS = cm.coverSet(r)
        coverS.opinion = Opinion
        for i in range(5):
            poolist1.append(p1.apply_async(dynamicMethods, args=(
            copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), initsize, evolutionmodel, methods, r, coverS,
            None, None, Opinion, False,)))
        p1.close()
        p1.join()

        # tmp,cost,op=dynamicMethods(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), initsize, evolutionmodel, methods, r, coverS,opinion=Opinion)

        sizelist = []
        opinionList = []
        bsSize=[]
        regionSize=[]
        for i in range(5):
            tmp, cost, op = poolist1[i].get()
            sizelist.append(len(tmp.bs))
            # opinionList.append(op.ComputeOpinion(nodeAttribute)/float(len(coverS.bs)))
            # opinionList.append(op.ComputeRounds(nodeAttribute))
            opinionList.append(op.OpValue)
            bsSize.append(op.CSsize)
            regionSize.append(op.Region)
        Length = len(max(opinionList, key=len))
        tt=[0]*Length
        count=[0]*Length
        for j in range(Length):
            for k in opinionList:
                if len(k)>j:
                    tt[j]+=k[j]

                    count[j]+=1
            tt[j]=tt[j]/float(count[j])
        Length = len(max(bsSize, key=len))
        ss = [0] * Length
        count = [0] * Length
        for j in range(Length):
            for k in bsSize:
                if len(k) > j:
                    ss[j] += k[j]
                    count[j] += 1
            ss[j] = ss[j] / float(count[j])
        Length = len(max(regionSize, key=len))
        kk=[0]*Length
        count = [0] * Length
        for j in range(Length):
            for k in regionSize:
                if len(k) > j:
                    kk[j] += k[j]
                    count[j] += 1
            kk[j] = kk[j] / float(count[j])
        print("=====================")
        print(len(ss)==len(tt))
        with multiprocessing.Lock():
            f = open("experiment//value_" + str(evolutionmodel) + "control_" + str(methods) + ".txt", 'a+',
                     encoding='utf8')
            f.write("模型interval_1:" + str(evolutionmodel) + "\n")
            f.write("initsize:" + str(initsize) + "\n")
            f.write("radius:" + str(r) + "\n")
            f.write("方法:" + str(methods) + "\n")
            f.write("size:" + str(sizelist) + "\n")
            f.write("size:" + str(sum(sizelist) / 5.0) + "\n")
            f.write("TemporalSize:"+str(ss)+"\n")
            f.write("RegionSIze:" + str(kk) + "\n")
            f.write("OpinionValues:" + str(tt) + "\n")
            # f.write("AveOpinionValue:" + str(sum(tt) / 10.0) + "\n")
            f.close()
def dynamicMethods(nodeAttribute,nodeNeighbors,initsize,evolutionmodel,methods,r,coverS,edges=None,avedeg=None,opinion=None,static=False):
    count=0
    Cost=[0,0]   #jump, walk
    a = 0
    interval = 1
    while len(coverS.CS)<len(nodeAttribute.keys()):
        """
        网络演化
        """
        if not static:
            if avedeg:
                nodesInvolved = cm.networkEvolution(nodeAttribute, nodeNeighbors, initsize, a, interval, coverS,
                                                    evolutionmodel, edges,avedeg=avedeg)
            else:
                nodesInvolved=cm.networkEvolution(nodeAttribute,nodeNeighbors,initsize,a,interval,coverS,evolutionmodel,edges)
            coverS.updateCS(nodesInvolved, nodeNeighbors)
            if opinion:
                opinion.updateOpinion(nodeAttribute)
        if len(coverS.CS)==len(nodeAttribute.keys()):
            break
        a+=1
        count+=1
        print("第%d次演化" % count)
        """
        策略
        """

        if methods == "Smax":
            res,Cost = cm.US_localAlg(nodeAttribute,nodeNeighbors,r,Cost,coverS=coverS,opinion=opinion)
            if res is None: break

            coverS.updateBS(nodeNeighbors, [res])
        elif methods == "Rmax":
            res,Cost = cm.RS_localAlg(nodeAttribute,nodeNeighbors,r,Cost, coverS=coverS,opinion=opinion)
            if res is None:break
            coverS.updateBS(nodeNeighbors,[res])
        elif methods=="RdmWalk1":
            res, Cost = cm.RandomWalktest1(nodeAttribute, nodeNeighbors, r, Cost, coverS=coverS, opinion=opinion)
            if res is None: break
            coverS.updateBS(nodeNeighbors, [res])
        elif methods=="RdmWalk2":
            res, Cost = cm.RandomWalktest2(nodeAttribute, nodeNeighbors, r, Cost, coverS=coverS, opinion=opinion)
            if res is None: break
            coverS.updateBS(nodeNeighbors, [res])
        if coverS.opinion.rounds and len(coverS.bs) > 5:
            tt = opinion.ComputeRounds(nodeNeighbors, coverS)
            if tt:
                coverS.RoundsList.append(tt)
    print("count:%d"%count)
    return coverS,Cost,opinion
if __name__ == '__main__':
    test2("cit",275,"RdmWalk1")
    test2("cit", 275, "RdmWalk2")
    test2("cit", 275, "Rmax")