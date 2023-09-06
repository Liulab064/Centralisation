# -*- coding: utf-8 -*-

# import networkx as nx
# import matplotlib.pyplot as plt
import ALG_LinkingMethods2 as cm
# import time
import multiprocessing
# import sys
# import random
import linecache
# import soc_sign_bitcoinotc
# import network_colledgeMsg
# import network_cit_new
# import network_haggle
import copy
import math


# def MaxConnectedComponent(nodeAttribute,nodeNeighbors):
#     seen = set()
#     for v in nodeAttribute.keys():
#         if v not in seen:
#             c = set(_plain_bfs(G, v))
#             yield c
#             seen.update(c)
# nx.is_connected() 是否联通需要做一次bfs遍历
def test1(evolutionmodel, initsize, methods, duration=None):
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
        elif evolutionmodel == "EuCore":
            temp = linecache.getline("dataEpoch//email-Eu-core.txt", i)
            temp1 = temp.split(" ")
            edge = [(eval(temp[0]), eval(temp1[1]))]
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
    for r in range(2, 0, -1):
        poolist1 = []
        p1 = multiprocessing.Pool(3)
        coverS = cm.coverSet(r)
        for i in range(10):
            poolist1.append(p1.apply_async(dynamicMethods, args=(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), initsize, evolutionmodel, methods, r,coverS,None,None,None,duration,)))
        p1.close()
        p1.join()

        # tmp, cost = dynamicMethods(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), initsize, evolutionmodel,
        #                            methods, r, coverS, duration=duration)
        sumlist=[]
        for i in range(10):
            tmp=poolist1[i].get()
            sumlist.append(len(tmp[0].bs))
            # Jumplist.append(tmp[1][0])
            # walklist.append(tmp[1][1])
        print("=====================")
        with multiprocessing.Lock():
            f = open("experiment//" + str(evolutionmodel) + "radius_" + str(methods) + "_cost" + ".txt", 'a+',
                     encoding='utf8')
            f.write("模型interval_1:" + str(evolutionmodel) + "\n")
            f.write("initsize:" + str(initsize) + "\n")
            f.write("radius:" + str(r) + "\n")
            f.write("方法:" + str(methods) + "\n")
            f.write("steps:" + str(duration) + "\n")
            f.write("size:" + str(sum(sumlist)/len(sumlist)) + "\n")
            f.write("max_size:"+str(max(sumlist))+"\n")
            f.write("min_size:"+str(min(sumlist))+"\n")
            f.write("===================================="+"\n")
            # f.write("AVECost:"+str(math.log(N)*cost[0]+cost[1])+"\n")
            f.close()


def ModelTest(evolutionmodel, initsize, methods):
    """

        :param evolutionmodel:
        :param initsize:
        :return:
        """
    """
    initialize network:   nodeAttribute:[{nodeindex:deg+color},{}]
                        nodeNeighbors:[{nodeindex:[neighbors]}]
    """

    for r in range(5, 1, -1):
        sumlist = []
        Jumplist = []
        walklist = []
        edge = []
        for i in range(1, 2, 1):
            nodeAttribute = {}
            nodeNeighbors = {}
            if evolutionmodel in ["BA", "Rich club", "onion", "SFOF1", "SFOF5", "SFOF25", "SBM"]:
                try:
                    temp = linecache.getline("dataEpoch//" + str(evolutionmodel) + "_" + str(initsize) + ".txt", i)
                    edge = eval(temp)
                except:
                    print("=====wrong size========")
            else:
                print("=======Wrong Input========")
                break
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
            if evolutionmodel == "SBM":
                for node in nodeAttribute.keys():
                    if node < len(nodeAttribute) // 3:
                        nodeAttribute[node][1] = 1
                    elif node < 2 * len(nodeAttribute) // 3:
                        nodeAttribute[node][1] = 3
                    else:
                        nodeAttribute[node][1] = 3
            print("network building end")

            N = len(nodeAttribute.keys())
            print("num of nodes:%d" % N)

            poolist1 = []
            p1 = multiprocessing.Pool(1)
            coverS = cm.coverSet(r)
            for i in range(1):
                if methods == "random":
                    poolist1.append(p1.apply_async(cm.Random, args=(
                        copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), coverS, evolutionmodel, initsize,)))
                else:
                    poolist1.append(p1.apply_async(dynamicMethods, args=(
                        copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), initsize, evolutionmodel, methods,
                        r, coverS, copy.deepcopy(edge),)))
            p1.close()
            p1.join()

            for i in range(1):
                if methods == "random":
                    tmp = poolist1[i].get()
                    sumlist.append(len(tmp.bs))
                else:
                    tmp = poolist1[i].get()
                    sumlist.append(len(tmp[0].bs))
                    Jumplist.append(tmp[1][0])
                    walklist.append(tmp[1][1])
            print("=====================")

        if methods == "random":
            with multiprocessing.Lock():
                f = open("experiment//" + str(evolutionmodel) + "_" + str(initsize) + "Test_Random" + ".txt", 'a+',
                         encoding='utf8')
                f.write("模型interval_0:" + str(evolutionmodel) + "\n")
                f.write("initsize:" + str(initsize) + "\n")
                f.write("radius:" + str(r) + "\n")
                f.write("Random:" + str(sumlist) + "\n")
                f.write("ave:" + str(sum(sumlist) / 2.0) + "\n")
                f.write("AVECost:" + str(math.log(initsize) * sum(sumlist) / 4.0) + "\n")
                f.close()
        else:
            with multiprocessing.Lock():
                f = open("experiment//" + str(evolutionmodel) + "_" + str(initsize) + "Test_" + str(
                    methods) + "_cost" + ".txt", 'a+',
                         encoding='utf8')
                f.write("模型interval_1:" + str(evolutionmodel) + "\n")
                f.write("initsize:" + str(initsize) + "\n")
                f.write("radius:" + str(r) + "\n")
                f.write("方法:" + str(methods) + "\n")
                f.write("size:" + str(sumlist) + "\n")
                f.write("AVEsize:" + str(sum(sumlist) / 2.0) + "\n")
                f.write("JumpCost:" + str(Jumplist) + "\n")
                # f.write("AveJump:"+str(sum(Jumplist)/3.0)+"\n")
                f.write("WalkCost:" + str(walklist) + "\n")
                f.write("AVECost:" + str(math.log(initsize) * sum(Jumplist) / 4.0 + sum(walklist) / 4.0) + "\n")
                f.close()


def ModelTestAR(evolutionmodel, initsize, r=3):
    """

        :param evolutionmodel:
        :param initsize:
        :return:
        """
    """
    initialize network:   nodeAttribute:[{nodeindex:deg+color},{}]
                        nodeNeighbors:[{nodeindex:[neighbors]}]
    """

    edge = []
    nodeAttribute = {}
    nodeNeighbors = {}
    if evolutionmodel in ["BA", "Rich club", "onion", "SFOF1", "SFOF5", "SFOF25", "SBM"]:
        try:
            temp = linecache.getline("dataEpoch//" + str(evolutionmodel) + "_" + str(initsize) + ".txt", 1)
            edge = eval(temp)
        except:
            print("=====wrong size========")
    else:
        print("=======Wrong Input========")
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
    if evolutionmodel == "SBM":
        for node in nodeAttribute.keys():
            if node < len(nodeAttribute) // 3:
                nodeAttribute[node][1] = 1
            elif node < 2 * len(nodeAttribute) // 3:
                nodeAttribute[node][1] = 3
            else:
                nodeAttribute[node][1] = 3
    print("network building end")

    N = len(nodeAttribute.keys())
    print("num of nodes:%d" % N)

    print("=====================")
    coverS = cm.coverSet(r)
    tmp, cost = cm.AlternateRandom2(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), copy.deepcopy(coverS))
    with multiprocessing.Lock():
        f = open("experiment//" + str(evolutionmodel) + "Test_AR" + ".txt", 'a+')
        f.write("模型interval_0:" + str(evolutionmodel) + "\n")
        f.write("initsize:" + str(initsize) + "\n")
        f.write("radius:" + str(coverS.r) + "\n")
        # f.write("cost:" + str(cost[0] * math.log(len(nodeAttribute)) + cost[1]) + "\n")
        f.write("AlternateRandom:" + str(len(tmp.bs)) + "\n")
        f.close()


def ModelTestAR2(evolutionmodel, initsize, r=3, avedeg=None):
    """

        :param evolutionmodel:
        :param initsize:
        :return:
        """
    """
    initialize network:   nodeAttribute:[{nodeindex:deg+color},{}]
                        nodeNeighbors:[{nodeindex:[neighbors]}]
    """

    edge = []
    nodeAttribute = {}
    nodeNeighbors = {}

    if evolutionmodel in ["BA", "Rich club", "onion", "SFOF1", "SFOF5", "SFOF25", "SBM"]:
        try:
            if avedeg:
                temp = linecache.getline(
                    "dataEpoch//" + str(evolutionmodel) + "_" + str(initsize) + "_deg" + str(avedeg) + ".txt", 1)
            else:
                temp = linecache.getline("dataEpoch//" + str(evolutionmodel) + "_" + str(initsize) + ".txt", 1)
            edge = eval(temp)
        except:
            print("=====wrong size========")
    else:
        print("=======Wrong Input========")
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
    if evolutionmodel == "SBM":
        for node in nodeAttribute.keys():
            if node < len(nodeAttribute) // 3:
                nodeAttribute[node][1] = 1
            elif node < 2 * len(nodeAttribute) // 3:
                nodeAttribute[node][1] = 3
            else:
                nodeAttribute[node][1] = 3
    print("network building end")

    N = len(nodeAttribute.keys())
    print("num of nodes:%d" % N)
    cost = [0, 0]

    print("=====================")
    coverS = cm.coverSet(r)
    tmp, cost = cm.AlternateRandom2(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), copy.deepcopy(coverS),
                                    cost)
    with multiprocessing.Lock():
        f = open("experiment//" + str(evolutionmodel) + "Test_AR_DorR" + ".txt", 'a+')
        f.write("模型interval_0:" + str(evolutionmodel) + "\n")
        f.write("initsize:" + str(initsize) + "\n")
        f.write("radius:" + str(coverS.r) + "\n")
        f.write("cost:" + str(cost[0] * math.log(len(nodeAttribute)) + cost[1]) + "\n")
        f.write("AlternateRandom:" + str(len(tmp.bs)) + "\n")
        f.close()


def ModelTest2(evolutionmodel, methods, avedeg=None, initsize=5000):
    """

        :param evolutionmodel:
        :param initsize:
        :return:
        """
    """
    initialize network:   nodeAttribute:[{nodeindex:deg+color},{}]
                        nodeNeighbors:[{nodeindex:[neighbors]}]
    """

    for r in range(5, 1, -1):
        sumlist = []
        Jumplist = []
        walklist = []
        edge = []
        for i in range(1, 2, 1):
            nodeAttribute = {}
            nodeNeighbors = {}
            if evolutionmodel in ["BA", "Rich club", "onion", "SFOF1", "SFOF5", "SFOF25", "SBM"]:
                try:
                    temp = linecache.getline(
                        "dataEpoch//" + str(evolutionmodel) + "_" + str(initsize) + "_deg" + str(avedeg) + ".txt", i)
                    edge = eval(temp)
                except:
                    print("=====wrong size========")
                    return
            else:
                print("=======Wrong Input========")
                return
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
            if evolutionmodel == "SBM":
                for node in nodeAttribute.keys():
                    if node < len(nodeAttribute) // 3:
                        nodeAttribute[node][1] = 1
                    elif node < 2 * len(nodeAttribute) // 3:
                        nodeAttribute[node][1] = 3
                    else:
                        nodeAttribute[node][1] = 3
            print("network building end")
            N = len(nodeAttribute.keys())
            print("num of nodes:%d" % N)

            poolist1 = []
            p1 = multiprocessing.Pool(2)
            coverS = cm.coverSet(r)
            for i in range(2):
                if methods == "random":
                    if avedeg:
                        poolist1.append(p1.apply_async(cm.Random, args=(
                            copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), coverS, evolutionmodel,
                            initsize, copy.deepcopy(edge), avedeg,)))
                    else:
                        poolist1.append(p1.apply_async(cm.Random, args=(
                            copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), coverS, evolutionmodel,
                            initsize, copy.deepcopy(edge),)))
                else:
                    if avedeg:
                        poolist1.append(p1.apply_async(dynamicMethods, args=(
                            copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), initsize, evolutionmodel,
                            methods,
                            r, coverS, copy.deepcopy(edge), avedeg,)))
                    else:
                        poolist1.append(p1.apply_async(dynamicMethods, args=(
                            copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), initsize, evolutionmodel,
                            methods,
                            r, coverS, copy.deepcopy(edge),)))
            p1.close()
            p1.join()

            for i in range(2):
                if methods == "random":
                    tmp = poolist1[i].get()
                    sumlist.append(len(tmp.bs))
                else:
                    tmp = poolist1[i].get()
                    sumlist.append(len(tmp[0].bs))
                    Jumplist.append(tmp[1][0])
                    walklist.append(tmp[1][1])
            print("=====================")

        if methods == "random":
            with multiprocessing.Lock():
                f = open("experiment//" + str(evolutionmodel) + "_" + str(initsize) + "_deg" + str(
                    avedeg) + "Test_Random" + ".txt", 'a+',
                         encoding='utf8')
                f.write("模型interval_0:" + str(evolutionmodel) + "\n")
                f.write("initsize:" + str(initsize) + "\n")
                f.write("radius:" + str(r) + "\n")
                f.write("Random:" + str(sumlist) + "\n")
                f.write("ave:" + str(sum(sumlist) / 4.0) + "\n")
                f.write("AVECost:" + str(math.log(initsize) * sum(sumlist) / 4.0) + "\n")
                f.close()
        else:
            with multiprocessing.Lock():
                f = open("experiment//" + str(evolutionmodel) + "_" + str(initsize) + "Test_" + str(
                    methods) + "_cost" + "_deg" + str(avedeg) + ".txt", 'a+',
                         encoding='utf8')
                f.write("模型interval_1:" + str(evolutionmodel) + "\n")
                f.write("initsize:" + str(initsize) + "\n")
                f.write("radius:" + str(r) + "\n")
                f.write("方法:" + str(methods) + "\n")
                f.write("size:" + str(sumlist) + "\n")
                f.write("AVEsize:" + str(sum(sumlist) / 4.0) + "\n")
                f.write("JumpCost:" + str(Jumplist) + "\n")
                # f.write("AveJump:"+str(sum(Jumplist)/3.0)+"\n")
                f.write("WalkCost:" + str(walklist) + "\n")
                f.write("AVECost:" + str(math.log(initsize) * sum(Jumplist) / 4.0 + sum(walklist) / 4.0) + "\n")
                f.close()


def dynamicMethods(nodeAttribute, nodeNeighbors, initsize, evolutionmodel, methods, r, coverS, edges=None, avedeg=None,
                   opinion=None, duration=3):
    count = 0
    Cost = [0, 0]  # jump, walk
    a = 0
    interval = 1
    while len(coverS.CS) < len(nodeAttribute.keys()):
        """
        网络演化
        """
        # nodesInvolved=set()
        # if evolutionmodel == 'colledge':
        #     """1899 nodes  20296 edges   59835 timestamp"""
        #     nodesInvolved = cm.networkEvolution(nodeAttribute, nodeNeighbors, initsize, a, interval, coverS,evolutionmodel)
        # elif evolutionmodel == 'bitcoin':
        #     """35592 edges  5881 nodes"""
        #     nodesInvolved = cm.networkEvolution(nodeAttribute, nodeNeighbors, initsize, a, interval, coverS,evolutionmodel)
        # elif evolutionmodel == 'cit':
        #     nodesInvolved = cm.networkEvolution(nodeAttribute, nodeNeighbors, initsize, a, interval, coverS,evolutionmodel)
        # elif evolutionmodel == 'election_Data':
        #     nodesInvolved = cm.networkEvolution(nodeAttribute, nodeNeighbors, initsize, a, interval, coverS,evolutionmodel)
        # elif evolutionmodel == 'infectious':
        #     nodesInvolved = cm.networkEvolution(nodeAttribute, nodeNeighbors, initsize, a, interval, coverS,evolutionmodel)
        # elif evolutionmodel=='BA':
        if avedeg:
            nodesInvolved = cm.networkEvolution(nodeAttribute, nodeNeighbors, initsize, a, interval, coverS,
                                                evolutionmodel, edges=edges, avedeg=avedeg)
        else:
            nodesInvolved = cm.networkEvolution(nodeAttribute, nodeNeighbors, initsize, a, interval, coverS,
                                                evolutionmodel, edges=edges)
        coverS.updateCS(nodesInvolved, nodeNeighbors)

        if len(coverS.CS) == len(nodeAttribute.keys()):
            break
        # # print(coverS.bs)
        # print("covered/total:%d/%d"%(len(coverS.CS),len(nodeAttribute.keys())))
        a += 1
        count += 1
        print("第%d次演化" % count)
        """
        策略
        """

        if methods == "Smax":

            res, Cost = cm.US_localAlg(nodeAttribute, nodeNeighbors, r, Cost, coverS, duration=duration)
            coverS.updateBS(nodeNeighbors, [res])
        elif methods == "USrdm":
            res, Cost = cm.US_rdm(nodeAttribute, nodeNeighbors, r, Cost, coverS, duration=duration)
            coverS.updateBS(nodeNeighbors, [res])
        elif methods=="localrdm":
            res, Cost = cm.local_rdm(nodeAttribute, nodeNeighbors, r, Cost, coverS, duration=duration)
            coverS.updateBS(nodeNeighbors, [res])
        elif methods=="local":
            res, Cost = cm.local_deg_new(nodeAttribute, nodeNeighbors, r, Cost, coverS, duration=duration)
            coverS.updateBS(nodeNeighbors, [res])
        elif methods == "RSrdm":
            res, Cost = cm.RS_rdm(nodeAttribute, nodeNeighbors, r, Cost, coverS, duration=duration)
            coverS.updateBS(nodeNeighbors, [res])
        elif methods == "RSup":
            res, Cost = cm.RS_up(nodeAttribute, nodeNeighbors, r, Cost, coverS, duration=duration)
            coverS.updateBS(nodeNeighbors, [res])
        elif methods == "RSupnew":
            res, Cost = cm.RS_up_new(nodeAttribute, nodeNeighbors, r, Cost, coverS, duration=duration)
            coverS.updateBS(nodeNeighbors, [res])
        elif methods == "Rmaxnew":
            res, Cost = cm.RS_localAlg_new(nodeAttribute, nodeNeighbors, r, Cost, coverS, duration=duration)
            coverS.updateBS(nodeNeighbors, [res])
        elif methods == "RSupS":
            res, Cost = cm.RS_upStochastic(nodeAttribute, nodeNeighbors, r, Cost, coverS, duration=duration)
            coverS.updateBS(nodeNeighbors, [res])
        elif methods == "Rmax":
            res, Cost = cm.RS_localAlg(nodeAttribute, nodeNeighbors, r, Cost, coverS, duration=duration)
            coverS.updateBS(nodeNeighbors, [res])
        elif methods == "RmaxS":
            res, Cost = cm.RS_Stochastic(nodeAttribute, nodeNeighbors, r, Cost, coverS, duration=duration)
            coverS.updateBS(nodeNeighbors, [res])
        elif methods == "Overlapping":
            res, Cost = cm.NumofNewEdge(nodeAttribute, nodeNeighbors, r, Cost, coverS, duration=duration)
            coverS.updateBS(nodeNeighbors, [res])
        # elif methods== "OverlappingPercentage":
        #     res, Cost = cm.NumofNewEdgePercentage(nodeAttribute, nodeNeighbors, r, Cost, coverS,duration)
        #     coverS.updateBS(nodeNeighbors, [res])
        # elif methods== "Overlapping2":
        #     res, Cost = cm.NumofNewEdgeUp(nodeAttribute, nodeNeighbors, r, Cost, coverS)
        #     coverS.updateBS(nodeNeighbors, [res])
        # if cm.subgraphiscovered(coverS,nodeNeighbors):

    print("Cost:%s" % Cost)
    print("count:%d" % count)
    # print(coverS.bs)

    return coverS, Cost


def statiCases(evolutionmodel, endsize, r=100):
    nodeAttribute = {}
    nodeNeighbors = {}
    init = 1
    for i in range(init, endsize + 1, 1):
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
            # 7
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
    print("network building end")
    cost = [0, 0]
    print(len(nodeAttribute.keys()))
    # Citsize=[i for i in range(200+75, 3300, 100)]
    # bitcoinSize=[i for i in range(200, 36200, 1000)]
    # colledgeSize=[i for i in range(2000, 58000, 2000)]
    CitRadius = [10, 9, 9, 8, 9, 9, 8, 8, 9, 9, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 7, 7]
    bitcoinRadius = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                     2, 2, 2]
    colledgeRadius = [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    for r in range(4, 1, -1):
        # if evolutionmodel=="cit":
        #     r=round(sum(CitRadius)/len(CitRadius))+1
        #     print(r)
        # elif evolutionmodel=='bitcoin':
        #     r = round(sum(bitcoinRadius)/len(bitcoinRadius))+1
        # elif evolutionmodel=='colledge':
        #     r=colledgeRadiius[colledgeSize.index(endsize)]+1
        # r=round(sum(colledgeRadius)/len(colledgeRadius))+1
        # poolist1 = []
        # p1 = multiprocessing.Pool(2)
        coverS = cm.coverSet(r)
        tmp, cost, opinion = cm.AlternateRandom2(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors),
                                                 copy.deepcopy(coverS), evolutionmodel=evolutionmodel, initsize=endsize)

        print(len(tmp.bs))
        # for i in range(2):
        #     poolist1.append(p1.apply_async(cm.AlternateRandom2, args=(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors),copy.deepcopy(coverS),)))
        # p1.close()
        # p1.join()
        # sumlist=[]
        # for i in range(2):
        # tmp=poolist1[i].get()
        # sumlist.append(len(tmp.bs))
        print("=====================")
        with multiprocessing.Lock():
            f = open("experiment//" + str(evolutionmodel) + "radius_AR" + ".txt", 'a+')
            f.write("模型interval_0:" + str(evolutionmodel) + "\n")
            f.write("initsize:" + str(endsize) + "\n")
            f.write("radius:" + str(coverS.r) + "\n")
            # f.write("cost:" + str(cost[0]*math.log(len(nodeAttribute))+cost[1]) + "\n")
            f.write("AlternateRandom:" + str(len(tmp.bs)) + "\n")
            f.close()
    # print("step:%d"%coverS.bs)


def Random(evolutionmodel, startsize):
    nodeAttribute = {}
    nodeNeighbors = {}
    init = 1
    for i in range(init, startsize + 1, 1):
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
    print("network building end")
    N = len(nodeAttribute.keys())
    for r in range(2, 1, -1):
        poolist1 = []
        # p1 = multiprocessing.Pool(2)
        coverS = cm.coverSet(r)
        tmp, opinion = cm.Random(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), coverS, evolutionmodel,
                                 startsize, None,
                                 None, 6, None, None, None)
        # for i in range(2):
        # poolist1.append(p1.apply_async(cm.Random, args=(copy.deepcopy(nodeAttribute),copy.deepcopy(nodeNeighbors),coverS,evolutionmodel,startsize,)))
        # poolist1.append(cm.Random(copy.deepcopy(nodeAttribute),copy.deepcopy(nodeNeighbors),coverS,evolutionmodel,startsize,None,None,6,None,None,None,))
        # p1.close()
        # p1.join()
        print(len(tmp.bs))
        sumlist = [len(tmp.bs)]
        # for i in range(1):
        # tmp=poolist1[i].get()
        # tmp = poolist1[i]
        # sumlist.append(len(tmp.bs))

        print("=====================")
        print(N)
        print(len(nodeAttribute.keys()))
        with multiprocessing.Lock():
            f = open("experiment//" + str(evolutionmodel) + "radius_Random" + ".txt", 'a+', encoding='utf8')
            f.write("模型interval_0:" + str(evolutionmodel) + "\n")
            f.write("initsize:" + str(startsize) + "\n")
            f.write("radius:" + str(r) + "\n")
            f.write("Random:" + str(sumlist) + "\n")
            f.write("ave:" + str(sum(sumlist) / 2.0) + "\n")
            f.write("AVECost:" + str(math.log(N) * sum(sumlist) / 2.0) + "\n")
            f.close()


if __name__ == '__main__':
    x = "cit"

    initsize = [1]
    if x == "colledge":
        initsize = [i for i in range(2000, 58000, 2000)]
        """r=4   JumpCost==1"""
    elif x == "bitcoin":
        initsize = [i for i in range(200, 36200, 1000)]
    elif x == "cit":
        initsize = [i for i in range(200 + 75, 3300, 100)]
    elif x == "election_Data":
        initsize = [i for i in range(2000, 98000, 4000)]
    elif x == "infectious":
        initsize = [i for i in range(100, 1500, 200)]
    elif x == "NAroad":
        initsize = [1]
    elif x == "coDblp":
        initsize = [1]
    elif x == "VariableRadius":
        initsize = [1]

    """For Dynamic networks test1(network name, initial timestamp, cover radius, method name)"""
    # poolist = []
    # p = multiprocessing.Pool(3)
    # for i in initsize:
    #     # if i < 1775: continue
    #     poolist.append(p.apply_async(test1, args=(x,i,"Overlapping2",)))
    # p.close()
    # p.join()
    # Random(x, 1)
    # x = "ca"
    # i = 1
    # for duration in [3, 6, 9]:  # 3，
    #     test1(x, i, "RmaxS", duration=duration)
        # test1(x,i,"Rmax",duration=duration)
        # test1(x,i,"RSrdm",duration=duration)
        # test1(x,i,"USrdm",duration=duration)
        # test1(x, i, "RSup", duration=duration)
        # test1(x, i, "Smax", duration=duration)
    x = "cit"
    i = 375

    # test1(x, i, "local")
    # test1(x, i, "localrdm")
    for duration in [3, 6, 9]:  # 3，3,
        # test1(x, i, "USrdm", duration=duration)

        # test1(x, i, "Smax", duration=duration)
        # test1(x, i, "RSup", duration=duration)
        test1(x, i, "RSupnew", duration=duration)
        # test1(x, i, "RSupS", duration=duration)


        # test1(x, i, "Rmax", duration=duration)
        # test1(x, i, "Rmaxnew", duration=duration)
        # test1(x, i, "Overlapping", duration=duration)
        # test1(x, i, "RSrdm", duration=duration)

        # test1(x,i,"Overlapping",duration=duration)
    # for i in initsize:
    #     if i==375:
    # Random(x,i)
    # test1(x, i, "Smax", duration=6)
    # test1(x, i, "Overlapping", duration=3)
    # test1(x,i,"Rmax",duration=3)
    # statiCases(x,i)

    # for m in ["BA", "Rich club",  "SFOF1", "SFOF5", "SFOF25","onion"]:
    #     # for i in initsize[10:]:
    #     #     test1(x,i,"Rmax")
    #     # m="SFOF25"
    #     ModelTest2(m,"OverlappingPercentage",4)
    #     ModelTest2(m, "OverlappingPercentage", 8)
    #     ModelTest2(m, "OverlappingPercentage", 10)
    #     ModelTest2(m, "OverlappingPercentage", 12)
    #     ModelTest2(m, "OverlappingPercentage", 14)

    # m="SBM"
    # for deg in [4,8,10,12,14]:
    #     # ModelTest2(m, "Rmax", deg)
    #     # ModelTest2(m, "Smax", deg)
    #     # ModelTest2(m, "Overlapping", deg)
    #     ModelTest2(m, "random", deg)
    # deg=6
    # i=5000
    # ModelTest(m,i, "Rmax")
    # ModelTest(m,i, "Smax")
    # ModelTest(m,i, "Overlapping")
    # ModelTest(m,i, "random")
    # ModelTest(m,5000, "Rmax")
    # ModelTest(m,5000, "Smax")
    # ModelTest(m,5000, "Overlapping")
    # ModelTestAR(m,5000, 2)
    # ModelTestAR(m, 5000, 3)
    # ModelTestAR(m, 5000, 4)
    # ModelTestAR(m, 5000, 5)

    # for i in [2000, 5000, 10000, 20000, 50000, 100000]:
    # ModelTestAR(m, i, 3)
    # ModelTest("Rich club", 100000, "Overlapping")
    # for j in ["BA", "Rich club", "SFOF1", "SFOF5", "SFOF25", "onion"]:
    #     ModelTest(j, 5000, "OverlappingPercentage")
    # for i in [2000, 5000, 10000, 20000, 50000, 100000]:

    #     for j in ["BA",  "Rich club","SFOF1", "SFOF5", "SFOF25", "onion"]: #"BA",
    #         ModelTest(j, i, "OverlappingPercentage")
    # for i in [20000,50000,100000]:
    #     ModelTest("SFOF1", i, "random")

    """For Static networks  test1(network name, 1, cover radius, method name)"""
    # test1(x,1,"Smax")

    """For AlternateRandom algorithm, for dynamic networks: statiCases(network name,ending timestamp,cover radius)"""
    # poolist = []
    # p = multiprocessing.Pool(3)
    # for i in initsize[17:]:

    # for i in [2000,5000,10000,20000,50000,100000]:
    # for j in [ "Rich club", "onion", "SFOF1", "SFOF5", "SFOF25"]:   #"BA",
    # j="SBM"
    # ModelTest(j, i, "Overlapping")
    # ModelTest(j, i, "Rmax")
    # ModelTest(j, i, "Smax")
    # ModelTest(j, i, "random")
    # ModelTest(j, i, "Overlapping")
    # poolist.append(p.apply_async(ModelTest, args=(j, i, "Overlapping",)))
    # for i in range(10,3,-1):
    #
    # poolist.append(p.apply_async(statiCases, args=(x,i,)))
    #     poolist.append(p.apply_async(ModelTestAR, args=(m, i,)))
    # p.close()
    # p.join()

    # for i in initsize[-2:-1]:
    #     statiCases(x, i)
    #     print(i.get())
    # for i in range(10, 1, -1):
    # for m in ["BA", "Rich club", "onion", "SFOF1", "SFOF5", "SFOF25"]:
    # for ave in [4,8,10,12,14]:
    # for r in range(2,6):
    # ModelTestAR2(m,5000,3)

    """For Random algorithm"""
    # for i in initsize[10:]:
    #     Random(x,i)
    # poolist = []
    # p = multiprocessing.Pool(2)
    # for i in initsize[-1:]:
    #     poolist.append(p.apply_async(Random, args=(x, i,)))
    # p.close()
    # p.join()