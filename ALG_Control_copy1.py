# -*- coding: utf-8 -*-

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


def test2(evolutionmodel, initsize, methods,duration=None):
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
    for r in range(2, 1, -1):
        Opinion = cm.opinion(nodeAttribute, ValueFlag=True)
        poolist1 = []
        p1 = multiprocessing.Pool(2)
        coverS = cm.coverSet(r)
        coverS.opinion = Opinion
        for i in range(2):
            poolist1.append(p1.apply_async(dynamicMethods, args=(
            copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), initsize, evolutionmodel, methods, r, coverS,
            None, None, Opinion, True,duration,)))
        p1.close()
        p1.join()

        # tmp,cost,op=dynamicMethods(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), initsize, evolutionmodel, methods, r, coverS,opinion=Opinion)

        sizelist = []
        opinionList = []
        bsSize=[]
        regionSize=[]
        for i in range(2):
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
            f.write("size:" + str(sum(sizelist) / 2.0) + "\n")
            f.write("TemporalSize:"+str(ss)+"\n")
            f.write("RegionSIze:" + str(kk) + "\n")
            f.write("OpinionValues:" + str(tt) + "\n")
            # f.write("AveOpinionValue:" + str(sum(tt) / 10.0) + "\n")
            f.close()
def test1(evolutionmodel,initsize,methods):
    """

    :param evolutionmodel:
    :param initsize:
    :return:
    """
    """
    initialize network:   nodeAttribute:[{nodeindex:deg+color},{}]
                        nodeNeighbors:[{nodeindex:[neighbors]}]
    """
    nodeAttribute={}
    nodeNeighbors={}
    init=1
    for i in range(init,initsize+1,1):
        if evolutionmodel=="cit":
            temp = linecache.getline("dataEpoch//cit.txt", i)
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel=="colledge":
            temp = linecache.getline("dataEpoch//CollegeMsg.txt", i)
            temp1 = temp.split(" ")
            edge = [(eval(temp[0]),eval(temp1[1]))]
        elif evolutionmodel=="bitcoin":
            temp = linecache.getline("dataEpoch//soc-sign-bitcoinotc.txt", i)
            temp1 = temp.split(" ")
            edge = [(eval(temp[0]), eval(temp1[1]))]
        elif evolutionmodel=="election_Data":
            temp = linecache.getline("dataEpoch//election_Data.txt", i)
            edge = eval(temp)
        elif evolutionmodel=="infectious":
            temp = linecache.getline("dataEpoch//infectious_data.txt", i)
            edge = eval(temp)
        elif evolutionmodel=='netScience':
            temp=linecache.getline("dataEpoch//netScienceNew.txt",1)
            temp=temp.strip()
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel=='coDblp':
            temp = linecache.getline("dataEpoch//coDblp.txt", 1)
            temp = temp.strip()
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel=='ca':
            temp = linecache.getline("dataEpoch//ca.txt", 1)
            edge = eval(temp)
        else:
            edge=[]

        for e in edge:
            if e[0] not in nodeAttribute.keys():
                nodeAttribute[e[0]]=[0,0]
                nodeNeighbors[e[0]]=set()
            if e[1] not in nodeAttribute.keys():
                nodeAttribute[e[1]] = [0, 0]
                nodeNeighbors[e[1]] = set()
            nodeNeighbors[e[0]].add(e[1])
            nodeAttribute[e[0]][0]=len(nodeNeighbors[e[0]])
            nodeNeighbors[e[1]].add(e[0])
            nodeAttribute[e[1]][0]=len(nodeNeighbors[e[1]])

        # print(i)
    print("network building end")
    N=len(nodeAttribute.keys())




    print("num of nodes:%d"%N)
    for r in range(3,2,-1):
        poolist1 = []
        p1 = multiprocessing.Pool(2)
        coverS = cm.coverSet(r)
        Opinion = cm.opinion(nodeAttribute)
        Opinion.rounds=10000
        coverS.opinion=Opinion
        for i in range(2):
            poolist1.append(p1.apply_async(dynamicMethods, args=(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), initsize, evolutionmodel, methods, r,coverS,None,None,Opinion,True,None,)))
        p1.close()
        p1.join()

        # tmp,cost,op=dynamicMethods(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), initsize, evolutionmodel, methods, r, coverS,opinion=Opinion)


        sizelist=[]
        opinionList=[]
        bsSize=[]
        for i in range(2):
            tmp,cost,op=poolist1[i].get()
            sizelist.append(len(tmp.bs))
            bsSize.append(op.CSsize)
            # opinionList.append(op.ComputeOpinion(nodeAttribute)/float(len(coverS.bs)))
            opinionList.append(tmp.RoundsList)
        Length = len(max(opinionList, key=len))
        tt = [0] * Length
        count = [0] * Length
        for j in range(Length):
            for k in opinionList:
                if len(k) > j:
                    tt[j] += k[j]
                    count[j] += 1
            tt[j] = tt[j] / float(count[j])
        Length = len(max(bsSize, key=len))
        ss = [0] * Length
        count = [0] * Length
        for j in range(Length):
            for k in bsSize:
                if len(k) > j:
                    ss[j] += k[j]
                    count[j]+=1
            ss[j] = ss[j] / float(count[j])
        print("=====================")
        with multiprocessing.Lock():
            f = open("experiment//static_"+str(evolutionmodel)+"control_"+str(methods) + ".txt", 'a+',encoding='utf8')
            f.write("模型interval_1:" + str(evolutionmodel) + "\n")
            f.write("initsize:" + str(initsize) + "\n")
            f.write("radius:" + str(r) + "\n")
            f.write("方法:" + str(methods) + "\n")
            f.write("size:" + str(sizelist) + "\n")
            f.write("size:"+str(sum(sizelist)/2.0)+"\n")
            # f.write("AVECost:"+str(sum(costList)/10.0)+"\n")
            f.write("Opinion:" + str(tt) + "\n")
            f.write("size:" + str(ss) + "\n")
            f.close()
def ModelTest(evolutionmodel,initsize,methods):
    """

        :param evolutionmodel:
        :param initsize:
        :return:
        """
    """
    initialize network:   nodeAttribute:[{nodeindex:deg+color},{}]
                        nodeNeighbors:[{nodeindex:[neighbors]}]
    """

    for r in range(8, 1, -1):
        sumlist = []
        Jumplist = []
        walklist = []
        edge = []
        for i in range(1,3,1):
            nodeAttribute = {}
            nodeNeighbors = {}
            if evolutionmodel in [ "BA","Rich club", "onion","SFOF1","SFOF5","SFOF25"]:
                try:
                    temp = linecache.getline("dataEpoch//"+str(evolutionmodel)+"_"+str(initsize)+".txt", i)
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
            print("network building end")


            N = len(nodeAttribute.keys())
            print("num of nodes:%d" % N)

            poolist1 = []
            p1 = multiprocessing.Pool(2)
            coverS = cm.coverSet(r)
            for i in range(2):
                if methods=="random":
                    poolist1.append(p1.apply_async(cm.Random, args=(
                    copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), coverS, evolutionmodel, initsize,copy.deepcopy(edge),)))
                else:
                    poolist1.append(p1.apply_async(dynamicMethods, args=(
                    copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), initsize, evolutionmodel, methods, r, coverS,copy.deepcopy(edge),)))
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

        if methods=="random":
            with multiprocessing.Lock():
                f = open("experiment//" + str(evolutionmodel) + "_"+str(initsize)+ "Test_Random" + ".txt", 'a+', encoding='utf8')
                f.write("模型interval_0:" + str(evolutionmodel) + "\n")
                f.write("initsize:" + str(initsize) + "\n")
                f.write("radius:" + str(r) + "\n")
                f.write("Random:" + str(sumlist) + "\n")
                f.write("ave:" + str(sum(sumlist) / 4.0) + "\n")
                f.write("AVECost:" + str(math.log(initsize) * sum(sumlist) / 4.0) + "\n")
                f.close()
        else:
            with multiprocessing.Lock():
                f = open("experiment//" + str(evolutionmodel) + "_"+str(initsize)+"Test_" + str(methods) + "_cost" + ".txt", 'a+',
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


def ModelTestAR(evolutionmodel, initsize,r=3):
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
    if evolutionmodel in ["BA", "Rich club", "onion", "SFOF1", "SFOF5", "SFOF25"]:
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
    print("network building end")

    N = len(nodeAttribute.keys())
    print("num of nodes:%d" % N)


    print("=====================")
    coverS = cm.coverSet(r)
    tmp,cost = cm.AlternateRandom2(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), copy.deepcopy(coverS))
    with multiprocessing.Lock():
        f = open("experiment//" + str(evolutionmodel) + "Test_AR" + ".txt", 'a+')
        f.write("模型interval_0:" + str(evolutionmodel) + "\n")
        f.write("initsize:" + str(initsize) + "\n")
        f.write("radius:" + str(coverS.r) + "\n")
        f.write("cost:" + str(cost[0] * math.log(len(nodeAttribute)) + cost[1]) + "\n")
        f.write("AlternateRandom:" + str(len(tmp.bs)) + "\n")
        f.close()
def ModelTestAR2(evolutionmodel, initsize,r=3,avedeg=None):
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

    if evolutionmodel in ["BA", "Rich club", "onion", "SFOF1", "SFOF5", "SFOF25"]:
        try:
            if avedeg:
                temp = linecache.getline("dataEpoch//" + str(evolutionmodel) + "_" + str(initsize) +"_deg"+str(avedeg)+ ".txt", 1)
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
    print("network building end")

    N = len(nodeAttribute.keys())
    print("num of nodes:%d" % N)
    cost=[0,0]

    print("=====================")
    coverS = cm.coverSet(r)
    tmp,cost = cm.AlternateRandom2(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), copy.deepcopy(coverS),cost)
    with multiprocessing.Lock():
        f = open("experiment//" + str(evolutionmodel) + "Test_AR_DorR"+ ".txt", 'a+')
        f.write("模型interval_0:" + str(evolutionmodel) + "\n")
        f.write("initsize:" + str(initsize) + "\n")
        f.write("radius:" + str(coverS.r) + "\n")
        f.write("cost:" + str(cost[0] * math.log(len(nodeAttribute)) + cost[1]) + "\n")
        f.write("AlternateRandom:" + str(len(tmp.bs)) + "\n")
        f.close()

def ModelTest2(evolutionmodel, methods,avedeg=None,initsize=5000):
    """

        :param evolutionmodel:
        :param initsize:
        :return:
        """
    """
    initialize network:   nodeAttribute:[{nodeindex:deg+color},{}]
                        nodeNeighbors:[{nodeindex:[neighbors]}]
    """

    for r in range(8, 1, -1):
        sumlist = []
        Jumplist = []
        walklist = []
        edge = []
        for i in range(1, 3, 1):
            nodeAttribute = {}
            nodeNeighbors = {}
            if evolutionmodel in ["BA", "Rich club", "onion", "SFOF1", "SFOF5", "SFOF25"]:
                try:
                    temp = linecache.getline("dataEpoch//" + str(evolutionmodel) + "_" + str(initsize) + "_deg"+str(avedeg)+".txt", i)
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
                            initsize,copy.deepcopy(edge),avedeg,)))
                    else:
                        poolist1.append(p1.apply_async(cm.Random, args=(
                        copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), coverS, evolutionmodel, initsize,copy.deepcopy(edge),)))
                else:
                    if avedeg:
                        poolist1.append(p1.apply_async(dynamicMethods, args=(
                        copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), initsize, evolutionmodel, methods,
                        r, coverS, copy.deepcopy(edge),avedeg,)))
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
                f = open("experiment//" + str(evolutionmodel) + "_" + str(initsize) + "_deg"+str(avedeg)+ "Test_Random" + ".txt", 'a+',
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
                    methods) + "_cost" +"_deg"+str(avedeg)+ ".txt", 'a+',
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


def dynamicMethods(nodeAttribute,nodeNeighbors,initsize,evolutionmodel,methods,r,coverS,edges=None,avedeg=None,opinion=None,static=False,duration=None):
    count=0
    Cost=[0,0]   #jump, walk
    a = 0
    interval = 1
    while len(coverS.CS)<len(nodeAttribute.keys()):
        """
        网络演化
        """
        for _ in [0]*1000:
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
            res,Cost = cm.US_localAlg(nodeAttribute,nodeNeighbors,r,Cost,coverS=coverS,duration=duration)
            if res is None: break

            coverS.updateBS(nodeNeighbors, [res])
        elif methods == "Rmax":
            res,Cost = cm.RS_localAlg(nodeAttribute,nodeNeighbors,r,Cost, coverS=coverS,duration=duration)
            if res is None:break
            coverS.updateBS(nodeNeighbors,[res])
        elif methods=="Overlapping":
            res, Cost = cm.NumofNewEdge(nodeAttribute, nodeNeighbors, r, Cost, coverS=coverS,duration=duration)
            if res is None: break
            coverS.updateBS(nodeNeighbors, [res])
        elif methods== "Overlapping2":
            res, Cost = cm.NumofNewEdgeUp(nodeAttribute, nodeNeighbors, r, Cost, coverS=coverS)
            coverS.updateBS(nodeNeighbors, [res])
        elif methods=="OverlappingPercentage":
            res, Cost = cm.NumofNewEdgePercentage(nodeAttribute, nodeNeighbors, r, Cost, coverS=coverS)
            coverS.updateBS(nodeNeighbors, [res])
        if coverS.opinion:
            coverS.opinion.updateOpinion(nodeAttribute)
            coverS.opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
        # if coverS.opinion.ComputeOpinion(nodeAttribute)>0.9:
        #     break
        # if coverS.opinion.rounds and len(coverS.bs) <10:
            if coverS.opinion.rounds and len(coverS.bs) > 40:
                tt = opinion.ComputeRounds(nodeNeighbors, coverS)
                # print(tt)
                if tt:
                    coverS.RoundsList.append(tt)
                if len(coverS.bs)>60: break
        # else: break
    print("count:%d"%count)
    return coverS,Cost,opinion
def statiCases(evolutionmodel,endsize,r=100):
    nodeAttribute = {}
    nodeNeighbors = {}
    init = 1
    for i in range(init, endsize + 1, 1):
        if evolutionmodel=="cit":
            temp = linecache.getline("dataEpoch//cit.txt", i)
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel=="colledge":
            temp = linecache.getline("dataEpoch//CollegeMsg.txt", i)
            temp1 = temp.split(" ")
            edge = [(eval(temp[0]),eval(temp1[1]))]
        elif evolutionmodel=="bitcoin":
            temp = linecache.getline("dataEpoch//soc-sign-bitcoinotc.txt", i)
            temp1 = temp.split(" ")
            edge = [(eval(temp[0]), eval(temp1[1]))]
        elif evolutionmodel=="election_Data":
            temp = linecache.getline("dataEpoch//election_Data.txt", i)
            edge = eval(temp)
        elif evolutionmodel=="infectious":
            temp = linecache.getline("dataEpoch//infectious_data.txt", i)
            edge = eval(temp)
        elif evolutionmodel=='netScience':
            temp=linecache.getline("dataEpoch//netScienceNew.txt",1)
            temp=temp.strip()
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel=='coDblp':
            temp = linecache.getline("dataEpoch//coDblp.txt", 1)
            temp = temp.strip()
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel=='ca':
            temp = linecache.getline("dataEpoch//ca.txt", 1)
            edge = eval(temp)
            #7
        else:
            edge=[]
        for e in edge:
            if e[0] not in nodeAttribute.keys():
                nodeAttribute[e[0]]=[0,0]
                nodeNeighbors[e[0]]=set()
            if e[1] not in nodeAttribute.keys():
                nodeAttribute[e[1]] = [0, 0]
                nodeNeighbors[e[1]] = set()
            nodeNeighbors[e[0]].add(e[1])
            nodeAttribute[e[0]][0]=len(nodeNeighbors[e[0]])
            nodeNeighbors[e[1]].add(e[0])
            nodeAttribute[e[1]][0]=len(nodeNeighbors[e[1]])
    print("network building end")
    cost=[0,0]
    print(len(nodeAttribute.keys()))
    Citsize=[i for i in range(200+75, 3300, 100)]
    bitcoinSize=[i for i in range(200, 36200, 1000)]
    colledgeSize=[i for i in range(2000, 58000, 2000)]
    CitRadius=[10, 9, 9, 8, 9, 9, 8, 8, 9, 9, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 7, 7]
    bitcoinRadius=[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    colledgeRadius=[3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    # for r in range(5,1,-1):

    if evolutionmodel=="cit":
        r=round(sum(CitRadius)/len(CitRadius))+1

    elif evolutionmodel=='bitcoin':
        r = round(sum(bitcoinRadius)/len(bitcoinRadius))
    elif evolutionmodel=='colledge':
        # r=colledgeRadiius[colledgeSize.index(endsize)]+1
        r=round(sum(colledgeRadius)/len(colledgeRadius))
    r=2
    print(r)
    poolist1 = []
    p1 = multiprocessing.Pool(1)

    # tmp,cost=cm.AlternateRandom2(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), copy.deepcopy(coverS),cost)

    for i in range(1):
        op = cm.opinion(nodeAttribute,ValueFlag=True)
        op.rounds=10000
        coverS = cm.coverSet(r)
        coverS.opinion=op
        poolist1.append(p1.apply_async(cm.AlternateRandom2, args=(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors),copy.deepcopy(coverS),None,op,None,None)))
    p1.close()
    p1.join()
    sizelist = []
    opinionList = []
    bsSize = []
    for i in range(1):
        tmp, cost, op = poolist1[i].get()
        sizelist.append(len(tmp.bs))
        bsSize.append(tmp.opinion.CSsize)
        # opinionList.append(op.ComputeOpinion(nodeAttribute)/float(len(coverS.bs)))
        opinionList.append(tmp.RoundsList)
    Length = len(max(opinionList, key=len))
    tt = [0] * Length
    count = [0] * Length
    for j in range(Length):
        for k in opinionList:
            if len(k) > j:
                tt[j] += k[j]
                count[j] += 1
        tt[j] = tt[j] / float(count[j])
    Length = len(max(bsSize, key=len))
    ss = [0] * Length
    count = [0] * Length
    for j in range(Length):
        for k in bsSize:
            if len(k) > j:
                ss[j] += k[j]
                count[j] += 1
        ss[j] = ss[j] / float(count[j])
    print("=====================")
    with multiprocessing.Lock():
        f = open("experiment//static_" + str(evolutionmodel) + "control_AR"+ ".txt", 'a+',
                 encoding='utf8')
        f.write("模型interval_1:" + str(evolutionmodel) + "\n")
        f.write("initsize:" + str(initsize) + "\n")
        f.write("radius:" + str(r) + "\n")
        # f.write("方法:" + str(methods) + "\n")
        f.write("size:" + str(sizelist) + "\n")
        # f.write("size:" + str(sum(sizelist) / 1.0) + "\n")
        # f.write("AVECost:"+str(sum(costList)/10.0)+"\n")
        f.write("Opinion:" + str(tt) + "\n")
        f.write("size:" + str(ss) + "\n")
        f.close()
def statiCases2(evolutionmodel,endsize,r=100):
    nodeAttribute = {}
    nodeNeighbors = {}
    init = 1
    for i in range(init, endsize + 1, 1):
        if evolutionmodel=="cit":
            temp = linecache.getline("dataEpoch//cit.txt", i)
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel=="colledge":
            temp = linecache.getline("dataEpoch//CollegeMsg.txt", i)
            temp1 = temp.split(" ")
            edge = [(eval(temp[0]),eval(temp1[1]))]
        elif evolutionmodel=="bitcoin":
            temp = linecache.getline("dataEpoch//soc-sign-bitcoinotc.txt", i)
            temp1 = temp.split(" ")
            edge = [(eval(temp[0]), eval(temp1[1]))]
        elif evolutionmodel=="election_Data":
            temp = linecache.getline("dataEpoch//election_Data.txt", i)
            edge = eval(temp)
        elif evolutionmodel=="infectious":
            temp = linecache.getline("dataEpoch//infectious_data.txt", i)
            edge = eval(temp)
        elif evolutionmodel=='netScience':
            temp=linecache.getline("dataEpoch//netScienceNew.txt",1)
            temp=temp.strip()
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel=='coDblp':
            temp = linecache.getline("dataEpoch//coDblp.txt", 1)
            temp = temp.strip()
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel=='ca':
            temp = linecache.getline("dataEpoch//ca.txt", 1)
            edge = eval(temp)
            #7
        else:
            edge=[]
        for e in edge:
            if e[0] not in nodeAttribute.keys():
                nodeAttribute[e[0]]=[0,0]
                nodeNeighbors[e[0]]=set()
            if e[1] not in nodeAttribute.keys():
                nodeAttribute[e[1]] = [0, 0]
                nodeNeighbors[e[1]] = set()
            nodeNeighbors[e[0]].add(e[1])
            nodeAttribute[e[0]][0]=len(nodeNeighbors[e[0]])
            nodeNeighbors[e[1]].add(e[0])
            nodeAttribute[e[1]][0]=len(nodeNeighbors[e[1]])
    print("network building end")
    cost=[0,0]
    print(len(nodeAttribute.keys()))
    Citsize=[i for i in range(200+75, 3300, 100)]
    bitcoinSize=[i for i in range(200, 36200, 1000)]
    colledgeSize=[i for i in range(2000, 58000, 2000)]
    CitRadius=[10, 9, 9, 8, 9, 9, 8, 8, 9, 9, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 7, 7]
    bitcoinRadius=[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    colledgeRadius=[3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    # for r in range(5,1,-1):
    if evolutionmodel=="cit":
        r=round(sum(CitRadius)/len(CitRadius))+1

    elif evolutionmodel=='bitcoin':
        r = round(sum(bitcoinRadius)/len(bitcoinRadius))
    elif evolutionmodel=='colledge':
        # r=colledgeRadiius[colledgeSize.index(endsize)]+1
        r=round(sum(colledgeRadius)/len(colledgeRadius))
    r=2
    print(r)
    poolist1 = []
    p1 = multiprocessing.Pool(2)

    # tmp,cost=cm.AlternateRandom2(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors), copy.deepcopy(coverS),cost)

    for i in range(2):
        op = cm.opinion(nodeAttribute,ValueFlag=True)
        # op.rounds=100
        coverS = cm.coverSet(r)
        coverS.opinion=op
        poolist1.append(p1.apply_async(cm.AlternateRandom2, args=(copy.deepcopy(nodeAttribute), copy.deepcopy(nodeNeighbors),copy.deepcopy(coverS),None,op,None,None, )))
    p1.close()
    p1.join()
    sizelist = []
    opinionList = []
    bsSize = []
    regionSize = []
    for i in range(2):
        tmp, cost, op = poolist1[i].get()
        sizelist.append(len(tmp.bs))
        # opinionList.append(op.ComputeOpinion(nodeAttribute)/float(len(coverS.bs)))
        # opinionList.append(op.ComputeRounds(nodeAttribute))
        opinionList.append(tmp.opinion.OpValue)
        bsSize.append(tmp.opinion.CSsize)
        regionSize.append(tmp.opinion.Region)
    Length = len(max(opinionList, key=len))
    tt = [0] * Length
    count = [0] * Length
    for j in range(Length):
        for k in opinionList:
            if len(k) > j:
                tt[j] += k[j]

                count[j] += 1
        tt[j] = tt[j] / float(count[j])
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
    kk = [0] * Length
    count = [0] * Length
    for j in range(Length):
        for k in regionSize:
            if len(k) > j:
                kk[j] += k[j]
                count[j] += 1
        kk[j] = kk[j] / float(count[j])
    print("=====================")
    print(len(ss) == len(tt))
    with multiprocessing.Lock():
        f = open("experiment//value_" + str(evolutionmodel) + "control_AR" + ".txt", 'a+',
                 encoding='utf8')
        f.write("模型interval_1:" + str(evolutionmodel) + "\n")
        f.write("initsize:" + str(initsize) + "\n")
        f.write("radius:" + str(r) + "\n")
        # f.write("方法:" + str(AR) + "\n")
        f.write("size:" + str(sizelist) + "\n")
        f.write("size:" + str(sum(sizelist) / 2.0) + "\n")
        f.write("TemporalSize:" + str(ss) + "\n")
        f.write("RegionSIze:" + str(kk) + "\n")
        f.write("OpinionValues:" + str(tt) + "\n")
        # f.write("AveOpinionValue:" + str(sum(tt) / 10.0) + "\n")
        f.close()




def Random(evolutionmodel,startsize):
    nodeAttribute = {}
    nodeNeighbors = {}
    init = 1
    for i in range(init, startsize + 1, 1):
        if evolutionmodel=="cit":
            temp = linecache.getline("dataEpoch//cit.txt", i)
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel=="colledge":
            temp = linecache.getline("dataEpoch//CollegeMsg.txt", i)
            temp1 = temp.split(" ")
            edge = [(eval(temp[0]),eval(temp1[1]))]
        elif evolutionmodel=="bitcoin":
            temp = linecache.getline("dataEpoch//soc-sign-bitcoinotc.txt", i)
            temp1 = temp.split(" ")
            edge = [(eval(temp[0]), eval(temp1[1]))]
        elif evolutionmodel=="election_Data":
            temp = linecache.getline("dataEpoch//election_Data.txt", i)
            edge = eval(temp)
        elif evolutionmodel=="infectious":
            temp = linecache.getline("dataEpoch//infectious_data.txt", i)
            edge = eval(temp)
        elif evolutionmodel=='netScience':
            temp=linecache.getline("dataEpoch//netScienceNew.txt",1)
            temp=temp.strip()
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel=='coDblp':
            temp = linecache.getline("dataEpoch//coDblp.txt", 1)
            temp = temp.strip()
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel=='ca':
            temp = linecache.getline("dataEpoch//ca.txt", 1)
            edge = eval(temp)
        else:
            edge=[]
        for e in edge:
            if e[0] not in nodeAttribute.keys():
                nodeAttribute[e[0]]=[0,0]
                nodeNeighbors[e[0]]=set()
            if e[1] not in nodeAttribute.keys():
                nodeAttribute[e[1]] = [0, 0]
                nodeNeighbors[e[1]] = set()
            nodeNeighbors[e[0]].add(e[1])
            nodeAttribute[e[0]][0]=len(nodeNeighbors[e[0]])
            nodeNeighbors[e[1]].add(e[0])
            nodeAttribute[e[1]][0]=len(nodeNeighbors[e[1]])
    print("network building end")
    N=len(nodeAttribute.keys())
    for r in range(3,2,-1):
        poolist1 = []
        p1 = multiprocessing.Pool(1)
        for i in range(1):
            op = cm.opinion(nodeAttribute,ValueFlag=True)
            op.rounds=100000
            coverS = cm.coverSet(r)
            coverS.opinion = op
            # poolist1.append(p1.apply_async(cm.Random, args=(copy.deepcopy(nodeAttribute),copy.deepcopy(nodeNeighbors),coverS,evolutionmodel,startsize,)))
            poolist1.append(cm.Random(copy.deepcopy(nodeAttribute),copy.deepcopy(nodeNeighbors),coverS,evolutionmodel,startsize,None,6,op,True,None,None))
        p1.close()
        p1.join()


        sumlist=[]
        opinionlist=[]
        bsSize = []
        for i in range(1):
            # tmp=poolist1[i].get()
            cs,op = poolist1[i]
            sumlist.append(len(cs.bs))
            bsSize.append(op.CSsize)
            print(op.CSsize)
            opinionlist.append(cs.RoundsList)
        Length = len(max(opinionlist, key=len))
        tt = [0] * Length
        count = [0] * Length
        for j in range(Length):
            for k in opinionlist:
                if len(k) > j:
                    tt[j] += k[j]
                    count[j] += 1
            tt[j] = tt[j] / float(count[j])
        Length = len(max(bsSize, key=len))
        ss = [0] * Length
        count = [0] * Length
        for j in range(Length):
            for k in bsSize:
                if len(k) > j:
                    ss[j] += k[j]
                    count[j] += 1
            ss[j] = ss[j] / float(count[j])
        print("=====================")
        print(N)
        print(len(nodeAttribute.keys()))
        with multiprocessing.Lock():
                f = open("experiment//static_"+str(evolutionmodel)+"Control_Random" + ".txt", 'a+', encoding='utf8')
                f.write("模型interval_0:" + str(evolutionmodel) + "\n")
                f.write("initsize:" + str(startsize) + "\n")
                f.write("radius:" + str(r) + "\n")
                f.write("Random:" + str(sumlist) + "\n")
                f.write("ave:"+str(sum(sumlist)/1.0)+"\n")
                # f.write("Opinion:" + str(opinionlist) + "\n")
                # f.write("aveOpinion:" + str(sum(opinionlist) / 4.0) + "\n")
                f.write("Opinion:" + str(tt) + "\n")
                f.write("size:" + str(ss) + "\n")
                # f.write("AVECost:" + str(math.log(N) * sum(sumlist) / 4.0) + "\n")
                f.close()
def Random2(evolutionmodel,startsize):
    nodeAttribute = {}
    nodeNeighbors = {}
    init = 1
    for i in range(init, startsize + 1, 1):
        if evolutionmodel=="cit":
            temp = linecache.getline("dataEpoch//cit.txt", i)
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel=="colledge":
            temp = linecache.getline("dataEpoch//CollegeMsg.txt", i)
            temp1 = temp.split(" ")
            edge = [(eval(temp[0]),eval(temp1[1]))]
        elif evolutionmodel=="bitcoin":
            temp = linecache.getline("dataEpoch//soc-sign-bitcoinotc.txt", i)
            temp1 = temp.split(" ")
            edge = [(eval(temp[0]), eval(temp1[1]))]
        elif evolutionmodel=="election_Data":
            temp = linecache.getline("dataEpoch//election_Data.txt", i)
            edge = eval(temp)
        elif evolutionmodel=="infectious":
            temp = linecache.getline("dataEpoch//infectious_data.txt", i)
            edge = eval(temp)
        elif evolutionmodel=='netScience':
            temp=linecache.getline("dataEpoch//netScienceNew.txt",1)
            temp=temp.strip()
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel=='coDblp':
            temp = linecache.getline("dataEpoch//coDblp.txt", 1)
            temp = temp.strip()
            temp1 = temp.split("--")
            edge = eval(temp1[1])
        elif evolutionmodel=='ca':
            temp = linecache.getline("dataEpoch//ca.txt", 1)
            edge = eval(temp)
        else:
            edge=[]
        for e in edge:
            if e[0] not in nodeAttribute.keys():
                nodeAttribute[e[0]]=[0,0]
                nodeNeighbors[e[0]]=set()
            if e[1] not in nodeAttribute.keys():
                nodeAttribute[e[1]] = [0, 0]
                nodeNeighbors[e[1]] = set()
            nodeNeighbors[e[0]].add(e[1])
            nodeAttribute[e[0]][0]=len(nodeNeighbors[e[0]])
            nodeNeighbors[e[1]].add(e[0])
            nodeAttribute[e[1]][0]=len(nodeNeighbors[e[1]])
    print("network building end")
    N=len(nodeAttribute.keys())
    for r in range(2,1,-1):
        poolist1 = []
        Opinion=cm.opinion(nodeAttribute,ValueFlag=True)
        p1 = multiprocessing.Pool(2)
        coverS = cm.coverSet(r)

        for i in range(1):
            # poolist1.append(p1.apply_async(cm.Random, args=(copy.deepcopy(nodeAttribute),copy.deepcopy(nodeNeighbors),coverS,evolutionmodel,startsize,)))
            poolist1.append(cm.Random(copy.deepcopy(nodeAttribute),copy.deepcopy(nodeNeighbors),coverS,evolutionmodel,startsize,Opinion,None,6,False))
        p1.close()
        p1.join()
        sumlist=[]
        opinionlist=[]
        bsSize = []
        regionSize=[]
        for i in range(1):
            # tmp=poolist1[i].get()
            cs,op = poolist1[i]
            sumlist.append(len(cs.bs))
            opinionlist.append(op.OpValue)
            bsSize.append(op.CSsize)
            regionSize.append(op.Region)
            # opinionlist.append(op.ComputeRounds(nodeNeighbors,cs))
        Length = len(max(opinionlist, key=len))
        tt = [0] * Length
        ss = [0] * Length
        count = [0] * Length
        for j in range(Length):
            for k in opinionlist:
                if len(k) > j:
                    tt[j] += k[j]

                    count[j] += 1
            tt[j] = tt[j] / float(count[j])
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
        kk = [0] * Length
        count = [0] * Length

        for j in range(Length):
            for k in regionSize:
                if len(k) > j:
                    kk[j] += k[j]
                    count[j] += 1
            kk[j] = kk[j] / float(count[j])
        print("=====================")
        print(N)
        print(len(nodeAttribute.keys()))
        with multiprocessing.Lock():
                f = open("experiment//value_"+str(evolutionmodel)+"Control_Random" + ".txt", 'a+', encoding='utf8')
                f.write("模型interval_0:" + str(evolutionmodel) + "\n")
                f.write("initsize:" + str(startsize) + "\n")
                f.write("radius:" + str(r) + "\n")
                f.write("Random:" + str(sumlist) + "\n")
                f.write("ave:"+str(sum(sumlist)/2.0)+"\n")
                f.write("TemporalSize:" + str(ss) + "\n")
                f.write("RegionSIze:" + str(kk) + "\n")
                f.write("OpinionValues:" + str(tt) + "\n")
                f.close()
if __name__ == '__main__':
    x="cit"

    initsize=[1]
    if x == "colledge":
        initsize = [i for i in range(2000, 58000, 2000)]
        """r=4   JumpCost==1"""
    elif x == "bitcoin":
        initsize = [i for i in range(200, 36200, 1000)]
    elif x == "cit":
        initsize = [i for i in range(200+75, 3300, 100)]
    elif x == "election_Data":
        initsize = [i for i in range(2000, 98000, 4000)]
    elif x == "infectious":
        initsize = [i for i in range(100, 1500, 200)]
    elif x=="NAroad":
        initsize=[1]
    elif x=="coDblp":
        initsize=[1]
    elif x=="VariableRadius":
        initsize = [1]

    """For Dynamic networks test1(network name, initial timestamp, cover radius, method name)"""
    # poolist = []
    # p = multiprocessing.Pool(3)
    # for i in initsize[10:]:
    #     poolist.append(p.apply_async(test1, args=(x,i,"Random",)))
    # p.close()
    # p.join()
    # for m in ["BA", "Rich club",  "SFOF1", "SFOF5", "SFOF25"]: #"onion",
    # for i in initsize:
    #     test1(x,i,"Rmax")
    # m="SFOF25"
    # ModelTest2(m,"random",4)
    # ModelTest2(m, "random", 8)
    # ModelTest2(m, "random", 10)
    # ModelTest2(m, "random", 12)
    # ModelTest2(m, "random", 14)
    # for j in ["BA", "Rich club", "SFOF1", "SFOF5", "SFOF25", "onion"]:
    #     for i in [20000,50000,100000]:
    #         ModelTest(j, i, "random")
    # for i in [20000,50000,100000]:
    #     ModelTest("SFOF1", i, "random")


    """For Static networks  test1(network name, 1, cover radius, method name)"""
    # for i in initsize:
    #     if i>475:break
    #     test1(x,i,"Rmax")
    # for i in initsize:
    #     if i > 475: break
    #     test1(x, i, "Smax")

    # test2(x,initsize[int(len(initsize)/2)],"Rmax")
    """For AlternateRandom algorithm, for dynamic networks: statiCases(network name,ending timestamp,cover radius)"""
    # poolist = []
    # p = multiprocessing.Pool(3)
    # for i in initsize[17:]:

    # for i in [2000,5000,10000,20000,50000]:
    #     for m in ["BA", "Rich club", "onion", "SFOF1", "SFOF5", "SFOF25"]:
        # for i in range(10,3,-1):
        #     poolist.append(p.apply_async(statiCases, args=(x,1,i,)))
        # poolist.append(p.apply_async(statiCases, args=(x,i,)))
        #     poolist.append(p.apply_async(ModelTestAR, args=(m, i,)))
    # p.close()
    # p.join()



    # for i in initsize:
        # if i<28000 or i>28000: continue
        # if i<375 or i>375:continue
        # if i < 5200 or i > 5200: continue
        # statiCases2(x, i)
        # statiCases(x, i)
        # test2(x, i, "Rmax",duration=4)
        # test2(x, i, "Smax",duration=3)
        # test2(x, i, "Overlapping",duration=3)
        # Random2(x, i)



    #     print(i.get())
    # for i in range(10, 1, -1):
    # for m in ["BA", "Rich club", "onion", "SFOF1", "SFOF5", "SFOF25"]:
        # for ave in [4,8,10,12,14]:
        # for r in range(2,6):
        # ModelTestAR2(m,5000,3)


    """For Random algorithm"""




    # for i in initsize:
    #     if i > 475: break
    #     Random(x,i)



    # poolist = []
    # p = multiprocessing.Pool(2)
    # for i in initsize[-1:]:
    #     poolist.append(p.apply_async(Random, args=(x, i,)))
    # p.close()
    # p.join()
    # for i in initsize:
    #     # if i<28000 or i>28000: continue
    #     # if i<375 or i>375:continue
    #     # if i < 5200 or i > 5200: continue
    #     test1(x,i,"Smax")
    #     test2(x, i, "Smax")
    #     test1(x, i, "Rmax")
    #     test2(x, i, "Rmax")
    #
    #     test1(x, i, "Overlapping")
    #     test2(x, i, "Overlapping")
    #
    #     #     test1(x,i,"Smax")
    x="ca"
    # statiCases(x,i)
    Random(x,1)
    # test1(x, 1, "Smax")
    # test2(x, 1, "Smax")
    # test1(x, 1, "Rmax")
    # test2(x, 1, "Rmax")
    #
    # test1(x, 1, "Overlapping")
    # test2(x, 1, "Overlapping")

    #     test1(x,i,"Smax")
    # statiCases(x,1)
    # statiCases2(x, 1)
    # Random(x,1)
    # Random2(x,1)
        # if methods == "Smax":
        # elif methods == "Rmax":
        # elif methods=="Overlapping":
        # elif methods== "Overlapping2":
        # elif methods=="OverlappingPercentage":
    # for i in range(1, 1 + 1, 1):
    #
    #     temp = linecache.getline("dataEpoch//ca.txt", 1)
    #     edge = eval(temp)
    # import networkx as nx
    # G=nx.Graph()
    # G.add_edges_from(edge)
    # print(nx.radius(max(nx.connected_component_subgraphs(G), key=len)))
