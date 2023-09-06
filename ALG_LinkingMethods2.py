#coding=utf-8
import random
import linecache
import math
import evolution_models
import copy
import ALG_Metrics as cm
"""
G is replaced by:
nodeAttribute:{nodeindex:deg+color,.....}
nodeNeighbors:{nodeindex:[neighbors],....}

"""
def networkEvolution(nodeAttribute,nodeNeighbors,end,a,interval,coverS,evolutionModel,rounds=0,edges=[],avedeg=None):
    """
    network G_0 evolve to a new network G_1
    :param nodeAttribute: network parameter 1
    :param nodeNeighbors: network parameter 2

    :param end: endsize
    :param a: a* interval indicates the current size
    :param interval: gap between dynamics

    :param coverS:
    :param evolutionModel:
    :param edges:
    :param avedeg:
    :return:
    """
    if avedeg is None:
        avedeg=6
    NodesInvolved=set()
    gama = {6: 4, 8: 2.9, 10: 2.52, 12: 2.3, 14: 2.1}
    SFOF = {4: [(4.0, 4.0, 0.25, 0.25), (2.0, 2.0, 0.5, 0.5), (2, 1, 0.75, 0.75), (1.0, 1.0, 1, 1)],
            6: [(6.0, 6.0, 0.25, 0.25), (3.0, 3.0, 0.5, 0.5), (2.0, 2.0, 0.75, 0.75), (2, 1, 1, 1)],
            8: [(8.0, 8.0, 0.25, 0.25), (4.0, 4.0, 0.5, 0.5), (3, 2, 0.75, 0.75), (2.0, 2.0, 1, 1)],
            10: [(10.0, 10.0, 0.25, 0.25), (5.0, 5.0, 0.5, 0.5), (4, 3, 0.75, 0.75), (3, 2, 1, 1)],
            12: [(12.0, 12.0, 0.25, 0.25), (6.0, 6.0, 0.5, 0.5), (4.0, 4.0, 0.75, 0.75), (3.0, 3.0, 1, 1)],
            14: [(14.0, 14.0, 0.25, 0.25), (7.0, 7.0, 0.5, 0.5), (5, 4, 0.75, 0.75), (4, 3, 1, 1)]}
    if evolutionModel == "facebook-ww":
        interval=13
    elif evolutionModel=="enron":
        interval=2
    elif evolutionModel=="colledge":
        interval=32
    for i in range(end + a * interval, end + a * interval + interval):
        if evolutionModel=="cit":
            if i<=3308:
                temp = linecache.getline("dataEpoch//cit.txt", i)
                temp1 = temp.split("--")
                edge = eval(temp1[1])
            else:
                edge=[]
        elif evolutionModel=="facebook-ww":
            if i<=876993:
                temp=linecache.getline("dataEpoch//facebook-wosn-wall.txt",i)
                temp=temp.split()
                edge=[(eval(temp[0]),eval(temp[1]))]
            else:
                edge=[]
        elif evolutionModel=="enron":
            if i<=220363:
                edge=[]
                temp=linecache.getline("dataEpoch//enron.txt",i)
                # temp=temp.split()
                edge.extend(eval(temp))
            else:
                edge=[]
        elif evolutionModel=="epinoins":
            if i<=940:
                edge=[]
                temp=linecache.getline("dataEpoch//epinions.txt",i)
                # temp=temp.split()
                edge.extend(eval(temp))
            else:
                edge=[]
        elif evolutionModel=="wiki":
            if i<=55197:
                edge=[]
                temp=linecache.getline("dataEpoch//wiki.txt",i)
                # temp=temp.split()
                edge.extend(eval(temp))
            else:
                edge=[]
        elif evolutionModel=="colledge":
            if i<=59835:
                temp = linecache.getline("dataEpoch//CollegeMsg.txt", i)
                temp1 = temp.split(" ")
                edge = [(eval(temp[0]),eval(temp1[1]))]
            else:
                edge=[]
        # elif evolutionModel=="bitcoin":
        #     if i<=35592:
        #         temp = linecache.getline("dataEpoch//soc-sign-bitcoinotc.txt", i)
        #         temp1 = temp.split(" ")
        #         edge = [(eval(temp[0]), eval(temp1[1]))]
        #     else:
        #         edge=[]
        # elif evolutionModel=="election_Data":
        #     if i<=98026:
        #         temp = linecache.getline("dataEpoch//election_Data.txt", i)
        #         edge = eval(temp)
        #     else:
        #         edge=[]
        # elif evolutionModel=="infectious":
        #     if i<=1392:
        #         temp = linecache.getline("dataEpoch//infectious_data.txt", i)
        #         edge = eval(temp)
        #     else:
        #         edge=[]
        elif evolutionModel=="BA":
            newEdges=evolution_models.BA_evolution2(nodeAttribute,nodeNeighbors, 1,  int(avedeg/2))
            edge=set(newEdges)-set(edges)
        # elif evolutionModel=="onion":
        #     if avedeg in gama.keys():
        #         newEdges = evolution_models.onionEvolution2(nodeAttribute,nodeNeighbors, gama[avedeg])
        #     edge = set(newEdges) - set(edges)
        elif evolutionModel=="Rich club":
            newEdges = evolution_models.rich_club2(nodeAttribute,nodeNeighbors,  2.0/(avedeg), len(nodeAttribute.keys()) + 1)
            edge = set(newEdges) - set(edges)
        elif evolutionModel=="SFOF5":
            newEdges= evolution_models.Friends_FoF2(nodeAttribute,nodeNeighbors, len(nodeAttribute.keys()) + 1, int(SFOF[avedeg][1][0]), int(SFOF[avedeg][1][1]), SFOF[avedeg][1][2], SFOF[avedeg][1][3])
            edge = set(newEdges) - set(edges)
        # elif evolutionModel=="SFOF1":
        #     newEdges = evolution_models.Friends_FoF2(nodeAttribute,nodeNeighbors, len(nodeAttribute.keys()) + 1, int(SFOF[avedeg][3][0]), int(SFOF[avedeg][3][1]), SFOF[avedeg][3][2], SFOF[avedeg][3][3])
        #     edge = set(newEdges) - set(edges)
        # elif evolutionModel=="SFOF25":
        #     newEdges = evolution_models.Friends_FoF2(nodeAttribute,nodeNeighbors,len(nodeAttribute.keys()) + 1, int(SFOF[avedeg][0][0]), int(SFOF[avedeg][0][1]), SFOF[avedeg][0][2],SFOF[avedeg][0][3])
        #     edge = set(newEdges) - set(edges)
        elif evolutionModel=="SBM":
            newEdges = evolution_models.SBM(nodeAttribute, nodeNeighbors, len(nodeAttribute.keys()) + 1,avedeg)
            edge = set(newEdges)
        else:
            edge=[]

        for e in edge:
            #首先判断是否涉及coverS.CS
            if e[0] in coverS.CS:
                NodesInvolved.add(e[1])
            if e[1] in coverS.CS:
                NodesInvolved.add(e[0])
            # 作更新
            if evolutionModel not in [ "BA","Rich club", "onion","SFOF1","SFOF5","SFOF25","SBM"]:
                if e[0] not in nodeAttribute.keys():
                    nodeAttribute[e[0]] = [0, 0]
                    nodeNeighbors[e[0]] = set()
                if e[1] not in nodeAttribute.keys():
                    nodeAttribute[e[1]] = [0, 0]
                    nodeNeighbors[e[1]] = set()
                nodeNeighbors[e[0]].add(e[1])
                nodeAttribute[e[0]][0]=len(nodeNeighbors[e[0]])
                nodeNeighbors[e[1]].add(e[0])
                nodeAttribute[e[1]][0] = len(nodeNeighbors[e[1]])

    return NodesInvolved
class opinion:
    def __init__(self,nodeAttribute,rounds=None,ValueFlag=False):
        self.W = {x: 0 for x in nodeAttribute.keys()}
        self.count=0
        self.rounds=rounds
        self.OpValueFlag=ValueFlag
        self.OpValue=[]
        self.CSsize=[]
        self.Region=[]
    # def checkRound(self):
    #     flag=False
    #     if self.rounds is not None:
    #         if self.count>=self.rounds:
    #             flag=True
    #     return flag
    def updateOpinion(self,nodeAttribute):
        for x in set(nodeAttribute.keys()).difference(set(self.W.keys())):
            self.W[x]=0
    def updateW(self,nodeAttribute,nodeNeighbors,coverS):

        # Dor=nx.dominating_set(G)
        # Dor=[i for i in range(0,429)]
        # Dor = [0]
        # print("len:%d" % len(Dor))
        for i in coverS.bs:
            self.W[i] = 1
        for i in nodeAttribute.keys():
            if i not in self.W.keys():
                self.W[i] = 0
        old = copy.deepcopy(self.W)
        # coverS.infmap = coverS.updateInfMap(nodeNeighbors)
        for i in nodeAttribute.keys():
            if i in coverS.bs: continue
            NEI = list(nodeNeighbors[i])
            Deg = len(NEI)
            self.W[i] = 0
            tmp = 0
            for j in NEI:
                if j in coverS.bs:
                    tmp+=1
                    continue
                self.W[i] += old[j]
            if i in coverS.CS:
                self.W[i]+=1
            # if Deg+coverS.infmap[i]-tmp<1:
            #     print(Deg)
                # print(coverS.infmap[i])
                # print(tmp)
            if Deg!=0:
                self.W[i]= self.W[i]/float(Deg+min(1-tmp,0))
            else:
                self.W[i]=0
        self.count+=1
        # flag=False
        # if self.rounds is not None:
        #     flag=self.checkRound()
        if self.OpValueFlag:
            self.OpValue.append(self.ComputeOpinion(nodeAttribute))

        # print(self.OpValue)
        return
    # def hasNoPath(self,nodeNeighbors,node,bs,unconnected):
    #     cur = {node}
    #     old = {node}
    #     times=0
    #     while len(cur)>0 and len(old.intersection(set(bs)))==0:
    #         times+=1
    #         tmp = set()
    #         for j in cur:
    #             tmp |= set(nodeNeighbors[j])
    #         old = old|cur
    #         cur = tmp.difference(old)
    #         if len(old.intersection(set(unconnected)))>0:return True
    #     t=old.intersection(set(bs))
    #     # print(old.intersection(set(bs)))
    #     return len(t)==0
    def ConnectedGraph(self,nodeNeighbors,bs):
        cur = set(bs)
        old = set(bs)
        times=0
        while len(cur)>0:
            times+=1
            tmp = set()
            for j in cur:
                tmp |= set(nodeNeighbors[j])
            old = old|cur
            cur = tmp.difference(old)
        return old
    def ComputeRounds(self,nodeNeighbors,coverS):
        if self.rounds is None:return None
        BS=coverS.bs
        W = {x: 0 for x in nodeNeighbors.keys()}
        connected=self.ConnectedGraph(nodeNeighbors,BS)
        print("size of component:%d"%len(connected))
        # coverS.updateInfMap(nodeNeighbors)
        for i in BS:
            W[i] = 100
        instable = True
        count = 0
        while instable:
            count += 1
            instable = False
            old = {x: W[x] for x in nodeNeighbors.keys()}
            for i in nodeNeighbors.keys():
                if i in BS:
                    W[i] = 100
                    continue
                if i not in connected:continue
                NEI = list(nodeNeighbors[i])
                Deg = len(NEI)
                W[i] = 0
                tmp=0
                for j in NEI:
                    if j in BS:
                        tmp+=1
                        continue
                    W[i] += old[j]
                if i in coverS.CS:
                    # W[i] += coverS.infmap[i]*100
                    W[i] += 100

                W[i] = W[i]/float((Deg+ min(1-tmp,0)))
                if W[i]<80:
                    instable=True
            if count>150: break
        print(count)
        return count
    def ComputeOpinion(self,nodeAttribute):
        # opinion = sum(self.W.values())/ float(len(self.W.keys()))
        opinion=min(self.W.values())
        print(opinion)
        return opinion
class coverSet:
    def __init__(self,r,opinion=None):
        self.bs=[]
        self.r=r
        self.CS=set()
        self.opinion=opinion
        self.RoundsList=[]
        self.infmap=dict()
        self.frontier=set()
        self.exterior=set()
        self.Nset=set()
        self.Bset=set()
        self.Bflag=True
    # def updateInfMap(self, nodeNeighbors):
    #     self.infmap={x:0 for x in nodeNeighbors.keys()}
    #     # for i in self.CS:
    #     #     self.infmap[i]=1
    #
    #     for i in self.bs:
    #         times = 0
    #         cur = {i}
    #         old = {i}
    #         while times < self.r:
    #             tmp = set()
    #             for j in cur:
    #                 tmp |= set(nodeNeighbors[j])
    #             old = old|cur
    #             cur = tmp.difference(old)
    #             times += 1
    #
    #         for j in old:
    #             self.infmap[j]+=1
    #     return self.infmap
    def updateExterior(self,nodeNeighbors):

        for i in self.frontier:
            self.exterior.update(nodeNeighbors[i])
            # for j in nodeNeighbors[i]:
            #     if j not in self.CS:
            #         self.exterior.add(j)
        self.exterior = self.exterior - self.CS
        if self.Bflag:
            self.BuildBset(nodeNeighbors)
        # else: self.updateBset(nodeNeighbors,bs)

        return


    def BuildBset(self,nodeNeighbors):
        if len(self.exterior)==0:
            self.Bset.clear()
            return
        self.Bset.clear()
        # self.Bset.update(self.exterior)
        for i in self.exterior:
            times = 0
            tmp = {i}
            cur = tmp
            while times < max(self.r,2):
                tmp = set()
                for j in cur:
                    self.Bset.add(j)
                    tmp.update(nodeNeighbors[j])
                times += 1
                cur = tmp - cur
        return
    def updateBS(self,nodeNeighbors,newMonitors):
        tmp=set(self.bs)
        tmp.update(set(newMonitors))
        self.bs=list(tmp)
        # self.updateInfMap(nodeNeighbors)
        return self.Build(nodeNeighbors,newMonitors)
    def Build(self,nodeNeighbors,bs=None):
        times=0
        #partial or whole
        if bs is None:
            cur=set(self.bs)
            old=set(self.bs)
        else:
            cur = set(bs)
            old = set(bs)
        while times < self.r:
            tmp = set()
            for i in cur:
                tmp |= set(nodeNeighbors[i])
            old|=cur
            cur = tmp -old
            times += 1
            if times==1:
                self.Nset.update(tmp)
                self.Nset.update(cur)
        for i in old:
            self.CS.add(i)
        for i in cur:
            self.CS.add(i)
            self.frontier.add(i)
        self.updateExterior(nodeNeighbors)
        # self.updateInfMap(nodeNeighbors)
        # if self.opinion:
        #     self.RoundsList.append(opinion.ComputeRounds(self.opinion,nodeNeighbors,self))
        return self.CS
    def updateCS(self,nodesInvolved,nodeNeighbors):
        if len(nodesInvolved)==0:
            return self.CS
        motivatorUpdate=set()
        #looking for motivators needed to be update
        for i in nodesInvolved:
            times = 0
            tmp = {i}
            cur=tmp
            while times <= self.r:
                tmp = set()
                flag=False
                for j in cur:
                    if j in self.bs:
                        flag=True
                        motivatorUpdate.add(i)
                        break
                    tmp.update(nodeNeighbors[j])
                if flag:
                    break
                times += 1
                cur=tmp-cur
        #motivators BFS to update
        return self.Build(nodeNeighbors,motivatorUpdate)

def UncoverS_up(nodeAttribute,nodeNeighbors,radius,cur,CS,Cost,times=None,opinion=None,coverS=None,clock=None,duration=None):
    if times==None:
        times=len(nodeAttribute)
    if duration is not None:
        times=min(times,duration)
    # print(times)
    if len(CS)==0:
        print("initial uncoverS")
        tmp=cur
        max_Nof=cur
        for i in range(times):
            for j in nodeNeighbors[tmp]:
                if nodeAttribute[j][0] > nodeAttribute[max_Nof][0]:
                    max_Nof = j
            if tmp==max_Nof:
                break
            # if opinion is not None:
            #     # opinion.updateOpinion(nodeAttribute)
            #     flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
            #     opinion.CSsize.append(len(coverS.bs))
            #     opinion.Region.append(len(coverS.CS))
            #     if flag:return None,Cost
            Cost[1] += math.log(nodeAttribute[tmp][0])
            tmp=max_Nof
    else:
        tmp = cur
        max_Nof = cur
        for i in range(times):
            for j in nodeNeighbors[tmp]:
                if nodeAttribute[j][0] > nodeAttribute[max_Nof][0] and j not in CS:
                    max_Nof = j

            if tmp==max_Nof:
                break
            # if opinion is not None:
            #     # opinion.updateOpinion(nodeAttribute)
            #     flag=opinion.updateW(nodeAttribute,nodeNeighbors,coverS)
            #     opinion.CSsize.append(len(coverS.bs))
            #     opinion.Region.append(len(coverS.CS))
            #     if flag: return None,Cost
            Cost[1] += math.log(nodeAttribute[tmp][0])
            tmp=max_Nof
    return max_Nof,Cost

def UncoverS_down(nodeAttribute,nodeNeighbors,cur,CS,Cost,times=None,opinion=None,coverS=None,duration=None):
    Cost=0
    if times==None:
        times=len(nodeAttribute.keys())
    if duration is not None:
        times=min(times,max(duration-1,0))
    if len(CS)==0:
        print("initial uncoverS")
        min_Nof=cur
        tmp=cur
        for i in range(times):
            for j in nodeNeighbors[tmp]:
                if nodeAttribute[j][0] < nodeAttribute[min_Nof][0]:
                    min_Nof = j
            if tmp==min_Nof:
                break
            # if opinion is not None:
            #     # opinion.updateOpinion(nodeAttribute)
            #     flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
            #     opinion.CSsize.append(len(coverS.bs))
            #     opinion.Region.append(len(coverS.CS))
            #     if flag: return None,Cost
            # Cost[1] += math.log(nodeAttribute[tmp][0])
            tmp=min_Nof

    else:
        tmp = cur
        min_Nof = cur
        for i in range(times):
            # print("UncoverDown", i)
            for j in nodeNeighbors[tmp]:
                if  (j not in CS) and (nodeAttribute[j][0] < nodeAttribute[min_Nof][0]):
                        min_Nof = j
                        Cost+=1
            if tmp==min_Nof:
                break
            # if opinion is not None:
            #     # opinion.updateOpinion(nodeAttribute)
            #     flag=opinion.updateW(nodeAttribute,nodeNeighbors,coverS)
            #     opinion.CSsize.append(len(coverS.bs))
            #     opinion.Region.append(len(coverS.CS))
            #     if flag: return None,Cost
            # Cost[1] += math.log(nodeAttribute[tmp][0])
            tmp=min_Nof
    return min_Nof,Cost
# def softmax(pis):
#     newpis=[]
#     sum=0
#     for i in pis:
#         sum+=math.exp(i)
#     for i in pis:
#         newpis.append(math.exp(i)/sum)
#     return newpis
# def UncoverS_down_stochastic(nodeAttribute,nodeNeighbors,cur,CS,Cost,times=None,opinion=None,coverS=None,duration=None):
#     Cost=0
#     if times==None:
#         times=len(nodeAttribute.keys())
#     if duration is not None:
#         times=min(times,max(duration-1,0))
#     if len(coverS.CS)==0:
#         print("initial uncoverS")
#         min_Nof = cur
#         tmp = cur
#         for i in range(times):
#             pis = []
#             sumdeg = 0
#             if len(nodeNeighbors[tmp]) == 1:
#                 tmp = list(nodeNeighbors[tmp])[0]
#                 continue
#             for j in nodeNeighbors[tmp]:
#                 pis.append([j, nodeAttribute[j][0]])
#                 sumdeg += nodeAttribute[j][0]
#             for j in range(len(pis)):
#                 pis[j][1] = pis[j][1] / sumdeg
#             selected = cm.prob_select([x[0] for x in pis], softmax([x[1] for x in pis]))
#             min_Nof = selected[0]
#             tmp = min_Nof
#     else:
#         # print("this pass")
#         tmp = cur
#         min_Nof = cur
#         # if cur in CS:
#         #     print("wrong here ===========================3")
#         for i in range(times):
#             # print("UncoverDown", i)
#             # if tmp in CS:
#             #     print("wrong here ===========================4")
#             # if len(nodeNeighbors[tmp]-set(CS)) == 1:
#             #     tmp = list(nodeNeighbors[tmp])[0]
#             #     continue
#             if len(nodeNeighbors[tmp]-set(CS)) == 0:
#                 return tmp,Cost
#             pis = []
#             sumdeg = 0
#             for j in nodeNeighbors[tmp]:
#                 if j in coverS.CS: continue
#                 pis.append([j, nodeAttribute[j][0]])
#                 sumdeg += nodeAttribute[j][0]
#             for j in range(len(pis)):
#                 pis[j][1] = 1-pis[j][1] / sumdeg
#                 # if pis[j][0] in CS:
#                 #     print("wrong here ===========================5")
#
#             selected = cm.prob_select([x[0] for x in pis], softmax([x[1] for x in pis]))
#             # for j in selected:
#             #     if j in CS:
#             #         print("wrong here ===========================6")
#             min_Nof = selected[0]
#             tmp=min_Nof
#         # if tmp in CS:
#         #     print("wrong here ===========================7")
#     return tmp,Cost
# def UncoverS_down_random(nodeAttribute,nodeNeighbors,cur,CS,Cost,times=None,opinion=None,coverS=None):
#     epsilon=0.3
#     if times==None:
#         times=len(nodeAttribute.keys())
#     if len(CS)==0:
#         print("initial uncoverS")
#         min_Nof=cur
#         tmp=cur
#         for i in range(times):
#             for j in nodeNeighbors[tmp]:
#                 if nodeAttribute[j][0] < nodeAttribute[min_Nof][0]:
#                     min_Nof = j
#
#             if tmp==min_Nof:
#                 break
#             if opinion is not None:
#                 opinion.updateOpinion(nodeAttribute)
#                 flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#                 opinion.CSsize.append(len(coverS.bs))
#                 opinion.Region.append(len(coverS.CS))
#                 if flag: return None,Cost
#             Cost[1] += math.log(nodeAttribute[tmp][0])
#             tmp=min_Nof
#
#     else:
#         tmp = cur
#         min_Nof = cur
#         for i in range(times):
#             for j in nodeNeighbors[tmp]:
#                 if  (j not in CS) and (nodeAttribute[j][0] < nodeAttribute[min_Nof][0]):
#                         min_Nof = j
#             if tmp==min_Nof:
#                 break
#             if random.random()<epsilon:
#                 min_Nof=random.choice(list(set(nodeNeighbors[tmp]).difference(set(CS))))
#             if opinion is not None:
#                 opinion.updateOpinion(nodeAttribute)
#                 flag=opinion.updateW(nodeAttribute,nodeNeighbors,coverS)
#                 opinion.CSsize.append(len(coverS.bs))
#                 opinion.Region.append(len(coverS.CS))
#                 if flag: return None,Cost
#             Cost[1] += math.log(nodeAttribute[tmp][0])
#             tmp=min_Nof
#     return min_Nof,Cost
# def UncoverS_down_random1(nodeAttribute,nodeNeighbors,cur,CS,Cost,times=None,opinion=None,coverS=None):
#     epsilon=0.1
#     if times==None:
#         times=len(nodeAttribute.keys())
#     if len(CS)==0:
#         print("initial uncoverS")
#         min_Nof=cur
#         tmp=cur
#         for i in range(times):
#             for j in nodeNeighbors[tmp]:
#                 if nodeAttribute[j][0] < nodeAttribute[min_Nof][0]:
#                     min_Nof = j
#
#             if tmp==min_Nof:
#                 break
#             if opinion is not None:
#                 opinion.updateOpinion(nodeAttribute)
#                 flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#                 opinion.CSsize.append(len(coverS.bs))
#                 opinion.Region.append(len(coverS.CS))
#                 if flag: return None,Cost
#             Cost[1] += math.log(nodeAttribute[tmp][0])
#             tmp=min_Nof
#
#     else:
#         tmp = cur
#         min_Nof = cur
#         for i in range(times):
#             for j in nodeNeighbors[tmp]:
#                 if  (j not in CS) and (nodeAttribute[j][0] < nodeAttribute[min_Nof][0]):
#                         min_Nof = j
#             if tmp==min_Nof:
#                 break
#             if random.random()<epsilon:
#                 break
#             if opinion is not None:
#                 opinion.updateOpinion(nodeAttribute)
#                 flag=opinion.updateW(nodeAttribute,nodeNeighbors,coverS)
#                 opinion.CSsize.append(len(coverS.bs))
#                 opinion.Region.append(len(coverS.CS))
#                 if flag: return None,Cost
#             Cost[1] += math.log(nodeAttribute[tmp][0])
#             tmp=min_Nof
#     return min_Nof,Cost
def RemoteS_up(nodeAttribute,nodeNeighbors, radius, leaf,Cost,times=None,opinion=None,coverS=None,duration=None):
    # if times==None:
    #     times=max(radius-1,1)
    # if duration is not None:
    #     times=min(times,duration)
    times=duration

    tmp = leaf
    max_Nof=leaf

    for i in range(times):
        Xset=set(nodeNeighbors.keys())-coverS.CS
        candidates=nodeNeighbors[tmp].intersection(coverS.Bset.union(Xset))
        # candidates=nodeNeighbors[tmp]
        for j in candidates:
            if nodeAttribute[j][0] > nodeAttribute[max_Nof][0]:
                max_Nof = j
        if tmp==max_Nof:
            break
        # if opinion is not None:
        #     # opinion.updateOpinion(nodeAttribute)
        #     flag=opinion.updateW(nodeAttribute,nodeNeighbors,coverS)
        #     opinion.CSsize.append(len(coverS.bs))
        #     opinion.Region.append(len(coverS.CS))
        #     if flag:return None,Cost
        #     print(opinion.ComputeOpinion(nodeAttribute))
        Cost[1] += math.log(nodeAttribute[tmp][0])
        tmp=max_Nof
    return max_Nof,Cost
def RemoteS_up_new(nodeAttribute,nodeNeighbors, radius, leaf,Cost,times=None,opinion=None,coverS=None,duration=None):
    # if times==None:
    #     times=max(radius-1,1)
    # if duration is not None:
    #     times=min(times,duration)
    times=duration

    tmp = leaf
    max_Nof=leaf
    a=set()

    for i in range(times):
        Xset=set(nodeNeighbors.keys())-coverS.CS
        candidates=nodeNeighbors[tmp].intersection(coverS.Bset.union(Xset))
        # candidates=nodeNeighbors[tmp]
        for j in candidates:
            if coverS.r==1:
                if j in coverS.CS:
                    if len(nodeNeighbors[j]-coverS.Nset) > len(nodeNeighbors[max_Nof]-coverS.Nset):
                        max_Nof = j
                else:
                    if len(nodeNeighbors[j]) > len(nodeNeighbors[max_Nof]):
                        max_Nof = j
            else:
                if len(nodeNeighbors[j]-coverS.Nset) > len(nodeNeighbors[max_Nof]-coverS.Nset):
                    max_Nof = j
        if tmp==max_Nof:
            break
        # if opinion is not None:
        #     # opinion.updateOpinion(nodeAttribute)
        #     flag=opinion.updateW(nodeAttribute,nodeNeighbors,coverS)
        #     opinion.CSsize.append(len(coverS.bs))
        #     opinion.Region.append(len(coverS.CS))
        #     if flag:return None,Cost
        #     print(opinion.ComputeOpinion(nodeAttribute))
        Cost[1] += math.log(nodeAttribute[tmp][0])
        tmp=max_Nof
    return max_Nof,Cost
# def RemoteS_up_stochastic(nodeAttribute,nodeNeighbors, radius, leaf,Cost,times=None,opinion=None,coverS=None,duration=None):
#     if times==None:
#         times=max(radius-1,1)
#     if duration is not None:
#         times=min(times,duration)
#     tmp = leaf
#     max_Nof=leaf
#     for i in range(times):
#         pis = []
#         sumdeg = 0
#         if len(nodeNeighbors[tmp])==1:
#             tmp=list(nodeNeighbors[tmp])[0]
#             continue
#         for j in nodeNeighbors[tmp]:
#             pis.append([j, nodeAttribute[j][0]])
#             sumdeg += nodeAttribute[j][0]
#         for j in range(len(pis)):
#             pis[j][1] = pis[j][1] / sumdeg
#         selected = cm.prob_select([x[0] for x in pis], softmax([x[1] for x in pis]))
#         max_Nof = selected[0]
#         tmp = max_Nof
#     return max_Nof,Cost

# def OverlappingDown(nodeAttribute,nodeNeighbors,cur,CS,Cost,times=None,opinion=None,coverS=None,duration=None):
#     if times == None:
#         times = len(nodeAttribute)
#     if duration is not None:
#         times=min(times,duration)
#     if len(CS) == 0:
#         print("initial uncoverS")
#         tmp = cur
#         max_Nof = cur
#         max_diff =0
#         for i in range(times):
#
#             for j in nodeNeighbors[tmp]:
#                 tmp_diff = len(set(nodeNeighbors[j]).difference(set(nodeNeighbors[max_Nof])))
#                 if nodeAttribute[j][0] > nodeAttribute[max_Nof][0] and tmp_diff>=max_diff:
#                     max_Nof = j
#                     max_diff=tmp_diff
#             if tmp == max_Nof:
#                 break
#             if opinion is not None:
#                 # opinion.updateOpinion(nodeAttribute)
#                 flag = opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#                 opinion.CSsize.append(len(coverS.bs))
#                 opinion.Region.append(len(coverS.CS))
#                 if flag: return None, Cost
#             Cost[1] += math.log(nodeAttribute[tmp][0])
#             tmp = max_Nof
#     else:
#         tmp = cur
#         max_Nof = cur
#         max_diff = 0
#         for i in range(times):
#             t1 = max_Nof
#
#             for j in nodeNeighbors[tmp]:
#                 tmp_diff = len(set(nodeNeighbors[j] - set(nodeNeighbors[max_Nof]) - set(CS)))
#                 if nodeAttribute[j][0] > nodeAttribute[max_Nof][0] and j not in CS and tmp_diff>max_diff:
#                     max_Nof = j
#                     max_diff=tmp_diff
#
#             if tmp == max_Nof:
#                 break
#             if opinion is not None:
#                 # opinion.updateOpinion(nodeAttribute)
#                 flag = opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#                 opinion.CSsize.append(len(coverS.bs))
#                 opinion.Region.append(len(coverS.CS))
#                 if flag: return None, Cost
#             Cost[1] += math.log(nodeAttribute[tmp][0])
#             tmp = max_Nof
#     return max_Nof, Cost
# def OverlappingDown2(nodeAttribute,nodeNeighbors,cur,CS,Cost,times=None,opinion=None,coverS=None):
#     if times == None:
#         times = len(nodeAttribute)
#     if len(CS) == 0:
#         print("initial uncoverS")
#         tmp = cur
#         max_Nof = cur
#         max_diff =0
#         for i in range(times):
#
#             for j in nodeNeighbors[tmp]:
#                 tmp_diff = len(set(nodeNeighbors[j]).difference(set(nodeNeighbors[max_Nof])))
#                 if nodeAttribute[j][0] > nodeAttribute[max_Nof][0] and tmp_diff/float(nodeAttribute[j][0])>=max_diff/float(nodeAttribute[max_Nof][0]):
#                     max_Nof = j
#                     max_diff=tmp_diff
#             if tmp == max_Nof:
#                 break
#             if opinion is not None:
#                 # opinion.updateOpinion(nodeAttribute)
#                 flag = opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#                 opinion.CSsize.append(len(coverS.bs))
#                 opinion.Region.append(len(coverS.CS))
#                 if flag: return None, Cost
#             Cost[1] += math.log(nodeAttribute[tmp][0])
#             tmp = max_Nof
#     else:
#         tmp = cur
#         max_Nof = cur
#         max_diff = 0
#         for i in range(times):
#             t1 = max_Nof
#
#             for j in nodeNeighbors[tmp]:
#                 tmp_diff = len(set(nodeNeighbors[j] - set(nodeNeighbors[max_Nof]) - set(CS)))
#                 if nodeAttribute[j][0] > nodeAttribute[max_Nof][0] and j not in CS and tmp_diff>max_diff:
#                     max_Nof = j
#                     max_diff=tmp_diff
#
#             if tmp == max_Nof:
#                 break
#             if opinion is not None:
#                 # opinion.updateOpinion(nodeAttribute)
#                 flag = opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#                 opinion.CSsize.append(len(coverS.bs))
#                 opinion.Region.append(len(coverS.CS))
#                 if flag: return None, Cost
#             Cost[1] += math.log(nodeAttribute[tmp][0])
#             tmp = max_Nof
#     return max_Nof, Cost
# def OverlappingUp(nodeAttribute,nodeNeighbors,cur,CS,Cost,times=None,opinion=None,coverS=None):
#     if times == None:
#         times = len(nodeAttribute)
#     if len(CS) == 0:
#         print("initial uncoverS")
#         tmp = cur
#         max_Nof = cur
#         max_inter =0
#         for i in range(times):
#
#             for j in nodeNeighbors[tmp]:
#                 tmp_inter = len(set(nodeNeighbors[j]).intersection(set(nodeNeighbors[max_Nof])))
#                 if nodeAttribute[j][0] > nodeAttribute[max_Nof][0] and tmp_inter>=max_inter:
#                     max_Nof = j
#                     max_diff=tmp_inter
#             if tmp == max_Nof:
#                 break
#             if opinion is not None:
#                 # opinion.updateOpinion(nodeAttribute)
#                 flag = opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#                 opinion.CSsize.append(len(coverS.bs))
#                 opinion.Region.append(len(coverS.CS))
#                 if flag: return None, Cost
#             Cost[1] += math.log(nodeAttribute[tmp][0])
#             tmp = max_Nof
#     else:
#         tmp = cur
#         max_Nof = cur
#         max_inter = 0
#         for i in range(times):
#             t1 = max_Nof
#
#             for j in nodeNeighbors[tmp]:
#                 tmp_inter = len(set(nodeNeighbors[j]).intersection( set(nodeNeighbors[max_Nof])) - set(CS))
#                 if nodeAttribute[j][0] > nodeAttribute[max_Nof][0] and j not in CS and tmp_inter>max_inter:
#                     max_Nof = j
#                     max_inter=tmp_inter
#
#             if tmp == max_Nof:
#                 break
#             if opinion is not None:
#                 # opinion.updateOpinion(nodeAttribute)
#                 flag = opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#                 opinion.CSsize.append(len(coverS.bs))
#                 opinion.Region.append(len(coverS.CS))
#                 if flag: return None, Cost
#             Cost[1] += math.log(nodeAttribute[tmp][0])
#             tmp = max_Nof
#     return max_Nof, Cost
# def RemoteS_up_random(nodeAttribute,nodeNeighbors, radius, leaf,Cost,times=None,opinion=None,coverS=None):
#     epsilon=0.3
#     if times==None:
#         times=radius-1
#     tmp = leaf
#     max_Nof=leaf
#
#     for i in range(times):
#         for j in nodeNeighbors[tmp]:
#             if nodeAttribute[j][0] > nodeAttribute[max_Nof][0]:
#                 max_Nof = j
#         if tmp==max_Nof:
#             break
#         if random.random()<epsilon:
#             max_Nof=random.choice(list(nodeNeighbors[tmp]))
#         if opinion is not None:
#             opinion.updateOpinion(nodeAttribute)
#             flag=opinion.updateW(nodeAttribute,nodeNeighbors,coverS)
#             opinion.CSsize.append(len(coverS.bs))
#             opinion.Region.append(len(coverS.CS))
#             if flag:return None,Cost
#             print(opinion.ComputeOpinion(nodeAttribute))
#         Cost[1] += math.log(nodeAttribute[tmp][0])
#         tmp=max_Nof
#     return max_Nof,Cost
# def RemoteS_up_random1(nodeAttribute,nodeNeighbors, radius, leaf,Cost,times=None,opinion=None,coverS=None):
#     epsilon=0.1
#     if times==None:
#         times=radius-1
#     tmp = leaf
#     max_Nof=leaf
#
#     for i in range(times):
#         for j in nodeNeighbors[tmp]:
#             if nodeAttribute[j][0] > nodeAttribute[max_Nof][0]:
#                 max_Nof = j
#         if tmp==max_Nof:
#             break
#         if random.random()<epsilon:
#             break
#         if opinion is not None:
#             opinion.updateOpinion(nodeAttribute)
#             flag=opinion.updateW(nodeAttribute,nodeNeighbors,coverS)
#             opinion.CSsize.append(len(coverS.bs))
#             opinion.Region.append(len(coverS.CS))
#             if flag:return None,Cost
#             print(opinion.ComputeOpinion(nodeAttribute))
#         Cost[1] += math.log(nodeAttribute[tmp][0])
#         tmp=max_Nof
#     return max_Nof,Cost
def US_localAlg(nodeAttribute,nodeNeighbors,radius,Cost,coverS,opinion=None,clock=None,duration=None):
    """
    Uset，随机从当前region的边外一层里找一点 游走到最大，方向上升方向
    然后再次游走
    直到无uncover
    :param G:
    :return:
    """
    CS = coverS.CS
    US=set(nodeAttribute.keys())-set(CS)
    # deg=dict(nx.degree(G))
    if len(US)==0:
        print("US is empty")
    else:
        #Pick initial node
        if len(CS)==0 or len(coverS.exterior)==0:
            print(len(CS))
            cur = random.choice(list(US))
        else:
            cur=random.choice(list(coverS.exterior))
        # if opinion is not None:
        #     # opinion.updateOpinion(nodeAttribute)
        #     flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
        #     opinion.CSsize.append(len(coverS.bs))
        #     opinion.Region.append(len(coverS.CS))
        #     if flag: return None,Cost
        "jump cost"
        Cost[0]+=1
        # walkCost+=math.log(nodeAttribute[cur][0])
        res,Cost = UncoverS_up(nodeAttribute,nodeNeighbors, radius, cur, CS,Cost, len(nodeAttribute.keys()),opinion=opinion,coverS=coverS,clock=clock,duration=duration)
        # uncoverS.update(res)
        return res,Cost
def US_rdm(nodeAttribute,nodeNeighbors,radius,Cost,coverS,opinion=None,clock=None,duration=None):
    """
    Uset，随机游走
    直到无uncover
    :param G:
    :return:
    """
    CS = coverS.CS
    US=set(nodeAttribute.keys())-set(CS)
    # deg=dict(nx.degree(G))
    if len(US)==0:
        print("US is empty")
    else:
        #Pick initial node
        if len(CS)==0 or len(coverS.exterior)==0:
            print(len(CS))
            cur = random.choice(list(US))
        else:
            cur=random.choice(list(coverS.exterior))
        # if opinion is not None:
        #     # opinion.updateOpinion(nodeAttribute)
        #     flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
        #     opinion.CSsize.append(len(coverS.bs))
        #     opinion.Region.append(len(coverS.CS))
        #     if flag: return None,Cost
        "jump cost"
        Cost[0]+=1
        # walkCost+=math.log(nodeAttribute[cur][0])
        for _ in [0] * duration:
            candidates=set(nodeNeighbors[cur])-CS
            if len(candidates)>0:
                cur=random.choice(list(candidates))
            else:
                break

        # res,Cost = UncoverS_up(nodeAttribute,nodeNeighbors, radius, cur, CS,Cost, len(nodeAttribute.keys()),opinion=opinion,coverS=coverS,clock=clock,duration=duration)
        # uncoverS.update(res)
        return cur,Cost
def local_rdm(nodeAttribute,nodeNeighbors,radius,Cost,coverS,opinion=None,clock=None,duration=None):
    """
    Uset，随机游走
    直到无uncover
    :param G:
    :return:
    """
    CS = coverS.CS
    US=set(nodeAttribute.keys())-set(CS)
    # deg=dict(nx.degree(G))
    if len(US)==0:
        print("US is empty")
    else:
        #Pick initial node
        if len(CS)==0 or len(coverS.exterior)==0:
            print(len(CS))
            cur = random.choice(list(US))
        else:
            cur=random.choice(list(coverS.exterior))
        return cur,Cost

def local_deg_new(nodeAttribute, nodeNeighbors, radius, Cost, coverS, opinion=None, clock=None, duration=None):
    """
    Uset，随机游走
    直到无uncover
    :param G:
    :return:
    """
    CS = coverS.CS
    US = set(nodeAttribute.keys()) - set(CS)
    # deg=dict(nx.degree(G))
    if len(US) == 0:
        print("US is empty")
    else:
        # Pick initial node
        if len(CS) == 0 or len(coverS.exterior) == 0:
        #     print(len(CS))
            max_Nof = random.choice(list(US))
        else:
            #     cur = random.choice(list(coverS.exterior))
            max_Nof=list(coverS.frontier-set(coverS.bs))[0]
            for j in (coverS.frontier-set(coverS.bs)):
                if len(nodeNeighbors[j]-coverS.Nset)>len(nodeNeighbors[max_Nof]-coverS.Nset):
                    max_Nof=j
        return max_Nof, Cost
def RS_rdm(nodeAttribute,nodeNeighbors,radius,Cost, coverS,opinion=None,duration=None):
    """
    开局随机局部最大值
    Rset 先下降方向（uncover)找叶子，再上升方向（all)找r-1邻居
    直到无uncoverS
    :param G:
    :return:
    """
    # 一步式迭代
    CS = coverS.CS
    US=set(nodeAttribute.keys())-set(CS)
    if len(US) == 0:
        print("US is empty")
    else:
        # Pick initial node
        if len(CS) == 0 or len(coverS.exterior) == 0:
            print(len(CS))
            cur = random.choice(list(US))
        else:
            cur = random.choice(list(coverS.exterior))
        Cost[0] += 1
        # if opinion is not None:
        #     opinion.updateOpinion(nodeAttribute)
        #     flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
        #     opinion.CSsize.append(len(coverS.bs))
        #     opinion.Region.append(len(coverS.CS))
        #     if flag: return None,Cost
        # leaf,durationCost  = UncoverS_down(nodeAttribute,nodeNeighbors, cur, CS,Cost,coverS=coverS,opinion=opinion,duration=duration)
        for _ in [0] * (duration):
            candidates=set(nodeNeighbors[cur]).intersection(coverS.Bset)
            candidates.update(nodeNeighbors[cur]-set(coverS.CS))
            if len(candidates)>0:
                cur=random.choice(list(candidates))
            else:
                break
        # if leaf is None: return None,Cost
        # print(cur)
        # print(leaf)
        # if duration is not None and durationCost is not None: duration-=durationCost
        # for _ in [0] * (radius-1):
        #     candidates=set(nodeNeighbors[cur])
        #     if len(candidates)>0:
        #         cur=random.choice(list(candidates))
        #     else:
        #         break
        # res,Cost  = RemoteS_up(nodeAttribute,nodeNeighbors, radius, leaf,Cost,coverS=coverS,opinion=opinion,duration=duration)
        # uncoverS.update(res)
        # print(res)
        return cur,Cost

# def RS_Stochastic(nodeAttribute,nodeNeighbors,radius,Cost, coverS,opinion=None,duration=None):
#     """
#     开局随机局部最大值
#     Rset 先下降方向（uncover)找叶子，再上升方向（all)找r-1邻居
#     直到无uncoverS
#     :param G:
#     :return:
#     """
#     # 一步式迭代
#     CS = coverS.CS
#     US = set(nodeAttribute.keys()) - set(CS)
#     if len(US) == 0:
#         print("US is empty")
#     else:
#         # Pick initial node
#         if len(CS) == 0 or len(coverS.exterior) == 0:
#             print(len(CS))
#             cur = random.choice(list(US))
#         else:
#             cur = random.choice(list(coverS.exterior))
#         Cost[0] += 1
#         if cur in CS:
#             print("================================wrong")
#         if duration-radius+1>0:
#             leaf, durationCost = UncoverS_down_stochastic(nodeAttribute, nodeNeighbors, cur, CS, Cost, coverS=coverS, opinion=opinion,
#                                            duration=max(duration-radius+1,0))
#             # if leaf is None: return None, Cost
#             # if duration is not None and durationCost is not None: duration -= durationCost
#         else:
#             leaf=cur
#         if leaf in CS:
#             print("================================wrong===1")
#         res, Cost = RemoteS_up_stochastic(nodeAttribute, nodeNeighbors, radius, leaf, Cost, coverS=coverS, opinion=opinion,
#                                duration=duration)
        # return res, Cost
# def RS_upStochastic(nodeAttribute,nodeNeighbors,radius,Cost, coverS,opinion=None,duration=None):
#     """
#     开局随机局部最大值
#     Rset 先下降方向（uncover)找叶子，再上升方向（all)找r-1邻居
#     直到无uncoverS
#     :param G:
#     :return:
#     """
#     # 一步式迭代
#     CS = coverS.CS
#     US = set(nodeAttribute.keys()) - set(CS)
#     if len(US) == 0:
#         print("US is empty")
#     else:
#         # Pick initial node
#         if len(CS) == 0 or len(coverS.exterior) == 0:
#             print(len(CS))
#             cur = random.choice(list(US))
#         else:
#             cur = random.choice(list(coverS.exterior))
#         Cost[0] += 1
#         if cur in CS:
#             print("================================wrong")
#         res, Cost = RemoteS_up_stochastic(nodeAttribute, nodeNeighbors, radius, cur, Cost, coverS=coverS, opinion=opinion,
#                                duration=duration)
#         return res, Cost
def RS_up(nodeAttribute,nodeNeighbors,radius,Cost, coverS,opinion=None,duration=None):
    """
    开局随机局部最大值
    Rset 先下降方向（uncover)找叶子，再上升方向（all)找r-1邻居
    直到无uncoverS
    :param G:
    :return:
    """
    # 一步式迭代
    CS = coverS.CS
    US=set(nodeAttribute.keys())-set(CS)
    if len(US) == 0:
        print("US is empty")
    else:
        # Pick initial node
        if len(CS) == 0 or len(coverS.exterior) == 0:
            print(len(CS))
            cur = random.choice(list(US))
        else:
            cur = random.choice(list(coverS.exterior))
        Cost[0] += 1
        # print(cur in CS)
        # if opinion is not None:
        #     opinion.updateOpinion(nodeAttribute)
        #     flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
        #     opinion.CSsize.append(len(coverS.bs))
        #     opinion.Region.append(len(coverS.CS))
        #     if flag: return None,Cost
        # leaf,durationCost  = UncoverS_down(nodeAttribute,nodeNeighbors, cur, CS,Cost,coverS=coverS,opinion=opinion,duration=duration)
        # if leaf is None: return None,Cost
        # print(cur)
        # print(leaf)
        # if duration is not None and durationCost is not None: duration-=durationCost
        # print(len(coverS.CS))
        # print(cur in coverS.CS)
        res,Cost  = RemoteS_up(nodeAttribute,nodeNeighbors, radius, cur,Cost,coverS=coverS,opinion=opinion,duration=duration)
        # uncoverS.update(res)
        # print(res)
        # print(res in coverS.CS)
        return res,Cost
def RS_up_new(nodeAttribute,nodeNeighbors,radius,Cost, coverS,opinion=None,duration=None):
    """
    开局随机局部最大值
    Rset 先下降方向（uncover)找叶子，再上升方向（all)找r-1邻居
    直到无uncoverS
    :param G:
    :return:
    """
    # 一步式迭代
    CS = coverS.CS
    US=set(nodeAttribute.keys())-set(CS)
    if len(US) == 0:
        print("US is empty")
    else:
        # Pick initial node
        if len(CS) == 0 or len(coverS.exterior) == 0:
            print(len(CS))
            cur = random.choice(list(US))
        else:
            cur = random.choice(list(coverS.exterior))
        Cost[0] += 1
        # print(cur in CS)
        # if opinion is not None:
        #     opinion.updateOpinion(nodeAttribute)
        #     flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
        #     opinion.CSsize.append(len(coverS.bs))
        #     opinion.Region.append(len(coverS.CS))
        #     if flag: return None,Cost
        # leaf,durationCost  = UncoverS_down(nodeAttribute,nodeNeighbors, cur, CS,Cost,coverS=coverS,opinion=opinion,duration=duration)
        # if leaf is None: return None,Cost
        # print(cur)
        # print(leaf)
        # if duration is not None and durationCost is not None: duration-=durationCost
        # print(len(coverS.CS))
        # print(cur in coverS.CS)
        res,Cost  = RemoteS_up_new(nodeAttribute,nodeNeighbors, radius, cur,Cost,coverS=coverS,opinion=opinion,duration=duration)
        # uncoverS.update(res)
        # print(res)
        # print(res in coverS.CS)
        return res,Cost
# def RS_localAlg(nodeAttribute,nodeNeighbors,radius,Cost, coverS,opinion=None,duration=None):
#     """
#     开局随机局部最大值
#     Rset 先下降方向（uncover)找叶子，再上升方向（all)找r-1邻居
#     直到无uncoverS
#     :param G:
#     :return:
#     """
#     # 一步式迭代
#     CS = coverS.CS
#     US=set(nodeAttribute.keys())-set(CS)
#     if len(US) == 0:
#         print("US is empty")
#     else:
#         # Pick initial node
#         if len(CS) == 0 or len(coverS.exterior) == 0:
#             print(len(CS))
#             cur = random.choice(list(US))
#         else:
#             cur = random.choice(list(coverS.exterior))
#         Cost[0] += 1
#         # if opinion is not None:
#         #     opinion.updateOpinion(nodeAttribute)
#         #     flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#         #     opinion.CSsize.append(len(coverS.bs))
#         #     opinion.Region.append(len(coverS.CS))
#         #     if flag: return None,Cost
#         leaf,durationCost  = UncoverS_down(nodeAttribute,nodeNeighbors, cur, CS,Cost,coverS=coverS,opinion=opinion,duration=duration//2)
#         if leaf is None: return None,Cost
#         # print(cur)
#         # print(leaf)
#         # if duration is not None and durationCost is not None: duration-=durationCost
#         res,Cost  = RemoteS_up(nodeAttribute,nodeNeighbors, radius, leaf,Cost,coverS=coverS,opinion=opinion,duration=duration-duration//2)
#         # uncoverS.update(res)
#         # print(res)
#         return res,Cost
# def RS_localAlg_new(nodeAttribute,nodeNeighbors,radius,Cost, coverS,opinion=None,duration=None):
#     """
#     开局随机局部最大值
#     Rset 先下降方向（uncover)找叶子，再上升方向（all)找r-1邻居
#     直到无uncoverS
#     :param G:
#     :return:
#     """
#     # 一步式迭代
#     CS = coverS.CS
#     US=set(nodeAttribute.keys())-set(CS)
#     if len(US) == 0:
#         print("US is empty")
#     else:
#         # Pick initial node
#         if len(CS) == 0 or len(coverS.exterior) == 0:
#             print(len(CS))
#             cur = random.choice(list(US))
#         else:
#             cur = random.choice(list(coverS.exterior))
#         Cost[0] += 1
#         # if opinion is not None:
#         #     opinion.updateOpinion(nodeAttribute)
#         #     flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#         #     opinion.CSsize.append(len(coverS.bs))
#         #     opinion.Region.append(len(coverS.CS))
#         #     if flag: return None,Cost
#         leaf,durationCost  = UncoverS_down(nodeAttribute,nodeNeighbors, cur, CS,Cost,coverS=coverS,opinion=opinion,duration=duration-duration//2)
#         if leaf is None: return None,Cost
#         # print(cur)
#         # print(leaf)
#         # if duration is not None and durationCost is not None: duration-=durationCost
#         res,Cost  = RemoteS_up_new(nodeAttribute,nodeNeighbors, radius, leaf,Cost,coverS=coverS,opinion=opinion,duration=duration//2)
#         # uncoverS.update(res)
#         # print(res)
#         return res,Cost
# def NumofNewEdge(nodeAttribute,nodeNeighbors,radius,Cost, coverS,opinion=None,duration=None):
#     """
#     初始degree 最高节点
#     贪心找未发掘的节点最多的一个，直到没有未发现的节点为止
#     直到无uncoverS
#     :param G:
#     :return:
#     """
#     # 一步式迭代
#     CS = coverS.CS
#     US=set(nodeAttribute.keys())-set(CS)
#     if len(US) == 0:
#         print("US is empty")
#     else:
#         # Pick initial node
#         if len(CS) == 0 or len(coverS.exterior) == 0:
#             print(len(CS))
#             cur = random.choice(list(US))
#         else:
#             cur = random.choice(list(coverS.exterior))
#         Cost[0] += 1
#         if opinion is not None:
#             # opinion.updateOpinion(nodeAttribute)
#             flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#             opinion.CSsize.append(len(coverS.bs))
#             opinion.Region.append(len(coverS.CS))
#             if flag: return None,Cost
#         res,Cost = OverlappingDown(nodeAttribute,nodeNeighbors, cur, CS,Cost, radius,opinion=opinion,coverS=coverS,duration=duration)
#         # uncoverS.update(res)
#         return res,Cost
# def NumofNewEdgePercentage(nodeAttribute,nodeNeighbors,radius,Cost, coverS,opinion=None):
#     """
#     初始degree 最高节点
#     贪心找未发掘的节点最多的一个，直到没有未发现的节点为止
#     直到无uncoverS
#     :param G:
#     :return:
#     """
#     # 一步式迭代
#     CS = coverS.CS
#     US=set(nodeAttribute.keys())-set(CS)
#     if len(US) == 0:
#         print("US is empty")
#     else:
#         cur = random.choice(list(US))
#         Cost[0] += 1
#         if opinion is not None:
#             # opinion.updateOpinion(nodeAttribute)
#             flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#             opinion.CSsize.append(len(coverS.bs))
#             opinion.Region.append(len(coverS.CS))
#             if flag: return None,Cost
#         res,Cost = OverlappingDown2(nodeAttribute,nodeNeighbors, cur, CS,Cost, radius,opinion=opinion,coverS=coverS)
#         # uncoverS.update(res)
#         return res,Cost
# def NumofNewEdgeUp(nodeAttribute,nodeNeighbors,radius,Cost, coverS,opinion=None):
#     """
#     初始degree 最高节点
#     贪心找未发掘的节点最多的一个，直到没有未发现的节点为止
#     直到无uncoverS
#     :param G:
#     :return:
#     """
#     # 一步式迭代
#     CS = coverS.CS
#     US=set(nodeAttribute.keys())-set(CS)
#     if len(US) == 0:
#         print("US is empty")
#     else:
#         cur = random.choice(list(US))
#         Cost[0] += 1
#         if opinion is not None:
#             # opinion.updateOpinion(nodeAttribute)
#             flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#             opinion.CSsize.append(len(coverS.bs))
#             opinion.Region.append(len(coverS.CS))
#             if flag: return None,Cost
#         res,Cost = OverlappingUp(nodeAttribute,nodeNeighbors, cur, CS,Cost, radius,opinion=opinion,coverS=coverS)
#         # uncoverS.update(res)
#         return res,Cost
# def RandomWalktest(nodeAttribute,nodeNeighbors,radius,Cost, coverS,opinion=None):
#     """
#     开局随机局部最大值
#     Rset 先下降方向（uncover)找叶子，再上升方向（all)找r-1邻居
#     直到无uncoverS
#     :param G:
#     :return:
#     """
#     # 一步式迭代
#     CS = coverS.CS
#     US=set(nodeAttribute.keys())-set(CS)
#     if len(US) == 0:
#         print("US is empty")
#     else:
#         cur = random.choice(list(US))
#         Cost[0] += 1
#         if opinion is not None:
#             # opinion.updateOpinion(nodeAttribute)
#             flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#             opinion.CSsize.append(len(coverS.bs))
#             opinion.Region.append(len(coverS.CS))
#             if flag: return None,Cost
#
#         leaf,Cost  = UncoverS_down(nodeAttribute,nodeNeighbors, cur, CS,Cost,coverS=coverS,opinion=opinion)
#         if leaf is None: return None,Cost
#         for _ in [0] * 1:
#             leaf=random.choice(list(nodeNeighbors[leaf]))
#         res,Cost  = RemoteS_up(nodeAttribute,nodeNeighbors, radius, leaf,Cost,coverS=coverS,opinion=opinion)
#         # uncoverS.update(res)
#         return res,Cost
# def RandomWalktest2(nodeAttribute,nodeNeighbors,radius,Cost, coverS,opinion=None):
#     """
#     Walk-后 随机  接walk+
#     """
#     # 一步式迭代
#     CS = coverS.CS
#     US=set(nodeAttribute.keys())-set(CS)
#     if len(US) == 0:
#         print("US is empty")
#     else:
#         cur = random.choice(list(US))
#         Cost[0] += 1
#         if opinion is not None:
#             opinion.updateOpinion(nodeAttribute)
#             flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#             opinion.CSsize.append(len(coverS.bs))
#             opinion.Region.append(len(coverS.CS))
#             if flag: return None,Cost
#
#         leaf,Cost  = UncoverS_down_random1(nodeAttribute,nodeNeighbors, cur, CS,Cost,coverS=coverS,opinion=opinion)
#         if leaf is None: return None,Cost
#         for _ in [0]*1:
#             leaf=random.choice(list(nodeNeighbors[leaf]))
#         res,Cost  = RemoteS_up_random1(nodeAttribute,nodeNeighbors, radius, leaf,Cost,coverS=coverS,opinion=opinion)
#         # uncoverS.update(res)
#         return res,Cost
# def RandomWalktest1(nodeAttribute,nodeNeighbors,radius,Cost, coverS,opinion=None):
#     """
#     Walk-时随机+walk+时随机
#     """
#     # 一步式迭代
#     CS = coverS.CS
#     US=set(nodeAttribute.keys())-set(CS)
#     if len(US) == 0:
#         print("US is empty")
#     else:
#         cur = random.choice(list(US))
#         Cost[0] += 1
#         if opinion is not None:
#             opinion.updateOpinion(nodeAttribute)
#             flag=opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#             opinion.CSsize.append(len(coverS.bs))
#             opinion.Region.append(len(coverS.CS))
#             if flag: return None,Cost
#
#         leaf,Cost  = UncoverS_down_random(nodeAttribute,nodeNeighbors, cur, CS,Cost,coverS=coverS,opinion=opinion)
#         if leaf is None: return None,Cost
#         for _ in [0]*1:
#             leaf=random.choice(list(nodeNeighbors[leaf]))
#         res,Cost  = RemoteS_up_random(nodeAttribute,nodeNeighbors, radius, leaf,Cost,coverS=coverS,opinion=opinion)
#         # uncoverS.update(res)
#         return res,Cost
# def AlternateRandom2(nodeAttribute,nodeNeighbors,coverS,cost=None,opinion=None,timebound=None,sizebound=None,evolutionmodel=None,initsize=None):
#     count = 1
#
#     # 1: Select an arbitrary node u from the graph and initialize S = {u}.
#     a=1
#     x = random.choice(list(nodeNeighbors.keys()))
#     if cost:
#         cost[0]+=1
#     coverS.updateBS(nodeNeighbors, [x])
#
#     if coverS.opinion:
#         # coverS.opinion.updateOpinion(nodeAttribute)
#         coverS.opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#         coverS.opinion.CSsize.append(len(coverS.bs))
#         coverS.opinion.Region.append(len(coverS.CS))
#
#         # if coverS.opinion.rounds and len(coverS.bs) <=10:
#         # print(opinion.ComputeOpinion(nodeAttribute))
#         if coverS.opinion.ComputeOpinion(nodeAttribute) > 0.9: return coverS,cost,opinion
#         # if opinion.ComputeOpinion(nodeAttribute) < 0.99:
#
#     if coverS.opinion.rounds and len(coverS.bs) > 200:
#         if len(coverS.bs) in range(100,1000,100):
#             tt = coverS.opinion.ComputeRounds(nodeNeighbors, coverS)
#             if tt:
#                 coverS.RoundsList.append(tt)
#             # if len(coverS.bs)>100: break
#     zeroS = {0: set(coverS.bs)}
#     Appeared = {x: 0 for x in coverS.bs}
#     a+=1
#     while len(coverS.CS) < len(nodeNeighbors.keys()):  # 2: while D(S) 6= V do
#
#         # nodesInvolved = networkEvolution(nodeAttribute, nodeNeighbors, initsize, a, 1, coverS, evolutionmodel)
#         # coverS.updateCS(nodesInvolved, nodeNeighbors)
#
#         if coverS.opinion and timebound and coverS.opinion.count > timebound:break
#         maxt = 0
#         maxGroup = set()
#         # 3: Choose x ∈ argmaxv∈N(S){|N(v)\D(S)|} and add x to S.
#         for i in range(max(zeroS.keys()) + 1, 0, -1):
#             tmp = coverS.CS
#             if i > max(zeroS.keys()):
#                 for k in range(0, i):
#                     if k in zeroS.keys():
#                         tmp = tmp - set(zeroS[k])
#             elif i not in zeroS.keys():
#                 continue
#             else:
#                 tmp = set(zeroS[i])
#             for node in tmp:
#                 tgroup = disRNeighbors(node, coverS.r, nodeNeighbors)
#                 if cost:
#                     cost[1]+=math.log(len(tgroup))
#                 tgroup-= coverS.CS
#                 tt = len(tgroup)
#
#
#                 if node not in Appeared.keys():
#                     Appeared[node] = tt
#                     if tt not in zeroS.keys():
#                         zeroS[tt] = set()
#                     zeroS[tt].add(node)
#                 elif not Appeared[node] == tt:
#                     beforeLayer = Appeared[node]
#                     Appeared[node] = tt
#                     if tt not in zeroS.keys():
#                         zeroS[tt] = set()
#                     zeroS[tt].add(node)
#                     zeroS[beforeLayer].remove(node)
#
#                 if tt > maxt:
#                     x = node
#                     maxt = tt
#                     maxGroup = tgroup
#                     if i <= max(zeroS.keys()) and maxt ==i:break
#             if i <= max(zeroS.keys()) and maxt==i:break
#
#             if maxt > 0 or maxt >= i - 1:
#                 break
#         if sizebound is None or len(coverS.bs) < sizebound-1:
#             if maxt > 0:
#                 NS = maxGroup
#                 coverS.updateBS(nodeNeighbors, [x])
#
#                 if coverS.opinion:
#                     # coverS.opinion.updateOpinion(nodeAttribute)
#                     coverS.opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#                     coverS.opinion.CSsize.append(len(coverS.bs))
#                     coverS.opinion.Region.append(len(coverS.CS))
#                     # print(opinion.ComputeOpinion(nodeAttribute))
#                     if coverS.opinion.ComputeOpinion(nodeAttribute) > 0.9: break
#                     # if opinion.ComputeOpinion(nodeAttribute) > 0.99:
#                     #     break
#                 if coverS.opinion.rounds and len(coverS.bs) > 200:
#                     if len(coverS.bs) in range(100,1000,100):
#                         tt = coverS.opinion.ComputeRounds(nodeNeighbors, coverS)
#                         if tt:
#                             coverS.RoundsList.append(tt)
#                     if len(coverS.bs) > 902: break
#                 zeroS[0].add(x)
#                 if not Appeared[x] == 0:
#                     beforeLayer = Appeared[x]
#                     Appeared[x] = 0
#                     if 0 not in zeroS.keys():
#                         zeroS[0] = set()
#                     zeroS[beforeLayer].remove(x)
#                 # 4: if N(x)\S 6= ∅ then
#                 # 5: Choose y ∈ N(x)\S uniformly at random and add y to S.
#                 # 6: end if
#                 if len(NS) > 0:
#                     y = random.choice(list(NS))
#                     coverS.updateBS(nodeNeighbors, [y])
#
#                     if coverS.opinion:
#                         # coverS.opinion.updateOpinion(nodeAttribute)
#                         coverS.opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#                         coverS.opinion.CSsize.append(len(coverS.bs))
#                         coverS.opinion.Region.append(len(coverS.CS))
#
#                         # print(opinion.ComputeOpinion(nodeAttribute))
#                         if coverS.opinion.ComputeOpinion(nodeAttribute) > 0.9: break
#                         # if opinion.ComputeOpinion(nodeAttribute) > 0.99:
#                         #     break
#                     # if coverS.opinion.rounds and len(coverS.bs) > 200:
#                     #     if len(coverS.bs) in range(100,1000,100):
#                     #         tt = coverS.opinion.ComputeRounds(nodeNeighbors, coverS)
#                     #         if tt:
#                     #             coverS.RoundsList.append(tt)
#                     #     if len(coverS.bs) > 902: break
#                     zeroS[0].add(y)
#                     if y not in Appeared.keys():
#                         Appeared[y] = 0
#                     elif not Appeared[y] == 0:
#                         beforeLayer = Appeared[y]
#                         Appeared[y] = 0
#                         if 0 not in zeroS.keys():
#                             zeroS[0] = set()
#                         zeroS[beforeLayer].remove(y)
#             else:
#                 print("jump component")
#                 y = random.choice(list(set(nodeAttribute.keys()) - set(coverS.CS)))
#                 coverS.updateBS(nodeNeighbors, [y])
#
#                 if coverS.opinion:
#                     # coverS.opinion.updateOpinion(nodeAttribute)
#                     coverS.opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#                     coverS.opinion.CSsize.append(len(coverS.bs))
#                     coverS.opinion.Region.append(len(coverS.CS))
#
#                     # print(opinion.ComputeOpinion(nodeAttribute))
#                     if coverS.opinion.ComputeOpinion(nodeAttribute) > 0.9: break
#                     # if opinion.ComputeOpinion(nodeAttribute) > 0.99:
#                     #     break
#                 # if coverS.opinion.rounds and len(coverS.bs) > 200:
#                 #     if len(coverS.bs) in range(100,1000,100):
#                 #         tt = coverS.opinion.ComputeRounds(nodeNeighbors, coverS)
#                 #         if tt:
#                 #             coverS.RoundsList.append(tt)
#                 #     if len(coverS.bs) > 902: break
#                 zeroS[0].add(y)
#                 if y not in Appeared.keys():
#                     Appeared[y] = 0
#                 elif not Appeared[y] == 0:
#                     beforeLayer = Appeared[y]
#                     Appeared[y] = 0
#                     if 0 not in zeroS.keys():
#                         zeroS[0] = set()
#                     zeroS[beforeLayer].remove(y)
#         else:
#             pass
#             if coverS.opinion:
#                 # coverS.opinion.updateOpinion(nodeAttribute)
#                 coverS.opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#                 coverS.opinion.CSsize.append(len(coverS.bs))
#                 coverS.opinion.Region.append(len(coverS.CS))
#                 # print(opinion.ComputeOpinion(nodeAttribute))
#                 if coverS.opinion.ComputeOpinion(nodeAttribute)>0.9: break
#         print("count:%d" % count)
#         count += 1
#         a+=2
#     return coverS,cost,opinion


# def Random(nodeAttribute,nodeNeighbors,coverS,evolutionmodel,initsize,edge=None,avedeg=6,opinion=None,static=False,timebound=None, sizebound=None):
#     # US = list(set(nodeAttribute.keys()) - set(coverS.CS))
#     count = 0
#     a = 0
#     interval = 1
#
#     N=1
#     while N > 0:
#         if opinion and timebound and opinion.count>timebound: break
#         """
#         网络演化
#         """
#         # nodesInvolved = set()
#         if not static:
#             nodesInvolved=networkEvolution(nodeAttribute, nodeNeighbors, initsize, a, interval, coverS,
#                                                 evolutionmodel,edges=edge,avedeg=avedeg)
#             coverS.updateCS(nodesInvolved, nodeNeighbors)
#
#         a += 1
#         count += 1
#         print("第%d次演化" % count)
#
#         """
#         策略
#         """
#         if sizebound is None or len(coverS.bs)<sizebound:
#             US = list(set(nodeAttribute.keys()) - set(coverS.CS))
#             if len(US)==0:
#                 break
#             w = random.choice(US)
#             if opinion is not None:
#                 # opinion.updateOpinion(nodeAttribute)
#                 opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#                 opinion.CSsize.append(len(coverS.bs))
#                 opinion.Region.append(len(coverS.CS))
#
#             coverS.updateBS(nodeNeighbors, [w])
#         else:
#             print("enter sizebound")
#             if opinion is not None:
#                 # opinion.updateOpinion(nodeAttribute)
#                 opinion.updateW(nodeAttribute, nodeNeighbors, coverS)
#                 opinion.CSsize.append(len(coverS.bs))
#                 opinion.Region.append(len(coverS.CS))
#                 if opinion.ComputeOpinion(nodeAttribute)>0.9: break
#
#         # print(opinion.ComputeOpinion(nodeAttribute))
#         if opinion.ComputeOpinion(nodeAttribute)>0.99:
#             break
#         # if coverS.opinion and coverS.opinion.rounds and len(coverS.bs) >= 700:
#             # print("size:%d"%len(nodeNeighbors))
#             # print("bs:%d" % len(coverS.bs))
#             # if len(coverS.bs) in range(100,1000,100):
#             #     tt=opinion.ComputeRounds(nodeNeighbors, coverS)
#             #     if tt:
#             #         coverS.RoundsList.append(tt)
#             # if coverS.opinion.rounds and len(coverS.bs) > 902: break
#         # print("count:%d" % count)
#         N= len(set(US) - set(coverS.CS))
#         cost=0
#         if count > 52: break
#     return coverS,opinion

def disRNeighbors(v,r,nodeNeighbors):
    times = 1
    tmp = {v}
    while times < r:
        cur = list(tmp)[:]
        for i in cur:
            tmp.update(nodeNeighbors[i])
        times += 1
    return tmp
# def networkEvolve(nodeAttribute,nodeNeighbors,walkCost, coverS,a,initsize,interval):
#     """
#                             网络演化
#                             """
#     walkCost+=1
#     a+=1
#     nodesInvolved = networkEvolution(nodeAttribute, nodeNeighbors, initsize, a, interval, coverS)
#     coverS.updateCS(nodesInvolved, nodeNeighbors)
#     return walkCost,a

# def AlternateRandom(nodeAttribute,nodeNeighbors,coverS,Cost):
#     US = list(set(nodeAttribute.keys()) - set(coverS.CS))
#     # deg=dict(nx.degree(G))
#     count=1
#     # flag={}
#     Cost=[0,0]
#     zeroS=set(coverS.bs)
#     while len(US)>0:
#
#         if len(coverS.CS) == 0:
#             w=random.choice(US)
#             Cost[0]+=1
#             x,Cost=RemoteS_up(nodeAttribute,nodeNeighbors,coverS.r,w,Cost,len(nodeAttribute.keys()))
#         else:
#             maxt=0
#             tmp=coverS.CS - zeroS
#             for node in tmp:
#                 # if node not in flag.keys():
#                 #     delta = len(disRNeighbors(node, coverS.r, nodeNeighbors) - coverS.CS)
#                 #     flag[node]=delta
#
#                 tt=len(disRNeighbors(node, coverS.r, nodeNeighbors) - coverS.CS)
#                 if tt==0:
#                     zeroS.add(node)
#                     continue
#                 if tt>maxt:
#                     x=node
#                     maxt=tt
#         NS = disRNeighbors(x, coverS.r, nodeNeighbors) - set(coverS.CS)
#         coverS.updateBS(nodeNeighbors, [x])
#         zeroS.add(x)
#         US = list(set(nodeAttribute.keys()) - set(coverS.CS))
#         if len(NS)>0:
#             # walkCost += 1
#             y=random.choice(list(NS))
#             coverS.updateBS(nodeNeighbors, [y])
#             zeroS.add(y)
#         else:
#             y=random.choice(list(US))
#             coverS.updateBS(nodeNeighbors, [y])
#             zeroS.add(y)
#             # uncoverS.update(res)
#         print("count:%d"%count)
#         count += 1
#         US = list(set(nodeAttribute.keys()) - set(coverS.CS))
#     return coverS
# def TestAlternateRandom(nodeAttribute,nodeNeighbors,coverS):
#     count = 1
#     #1: Select an arbitrary node u from the graph and initialize S = {u}.
#     x = random.choice(list(nodeNeighbors.keys()))
#     coverS.updateBS(nodeNeighbors,[x])
#
#     zeroS = {0: set(coverS.bs)}
#     Appeared = {x: 0 for x in coverS.bs}
#
#     while len(coverS.CS)<len(nodeNeighbors.keys()): #2: while D(S) 6= V do
#         print(coverS.bs)
#         maxt = 0
#         maxGroup=set()
#         # 3: Choose x ∈ argmaxv∈N(S){|N(v)\D(S)|} and add x to S.
#         for i in range(max(zeroS.keys()) + 1, 0, -1):
#             tmp = coverS.CS
#             if i > max(zeroS.keys()):
#                 for k in range(0, i):
#                     if k in zeroS.keys():
#                         tmp = tmp - set(zeroS[k])
#             elif i not in zeroS.keys():continue
#             else: tmp = set(zeroS[i])
#             for node in tmp:
#                 tgroup=disRNeighbors(node, 2, nodeNeighbors) - coverS.CS
#                 tt = len(tgroup)
#
#                 if node not in Appeared.keys():
#                     Appeared[node] = tt
#                     if tt not in zeroS.keys():
#                         zeroS[tt] = set()
#                     zeroS[tt].add(node)
#                 elif not Appeared[node] == tt:
#                     beforeLayer = Appeared[node]
#                     Appeared[node] = tt
#                     if tt not in zeroS.keys():
#                         zeroS[tt] = set()
#                     zeroS[tt].add(node)
#                     zeroS[beforeLayer].remove(node)
#
#                 if tt > maxt:
#                     x = node
#                     maxt = tt
#                     maxGroup=tgroup
#
#             if maxt >0 or maxt >= i - 1:
#                 break
#         print("maxt is %d" % maxt)
#         if maxt> 0:
#             NS = maxGroup
#             coverS.updateBS(nodeNeighbors, [x])
#
#             zeroS[0].add(x)
#             if not Appeared[x] == 0:
#                 beforeLayer = Appeared[x]
#                 Appeared[x] = 0
#                 if 0 not in zeroS.keys():
#                     zeroS[0] = set()
#                 zeroS[beforeLayer].remove(x)
#             # 4: if N(x)\S 6= ∅ then
#             # 5: Choose y ∈ N(x)\S uniformly at random and add y to S.
#             # 6: end if
#             if len(NS) > 0:
#                 y = random.choice(list(NS))
#                 coverS.updateBS(nodeNeighbors, [y])
#                 zeroS[0].add(y)
#                 if y not in Appeared.keys():
#                     Appeared[y] = 0
#                 elif not Appeared[y] == 0:
#                     beforeLayer = Appeared[y]
#                     Appeared[y] = 0
#                     if 0 not in zeroS.keys():
#                         zeroS[0] = set()
#                     zeroS[beforeLayer].remove(y)
#         else:
#             print("jump component")
#             y = random.choice(list(set(nodeAttribute.keys()) - set(coverS.CS)))
#             coverS.updateBS(nodeNeighbors, [y])
#             zeroS[0].add(y)
#             if y not in Appeared.keys():
#                 Appeared[y] = 0
#             elif not Appeared[y] == 0:
#                 beforeLayer = Appeared[y]
#                 Appeared[y] = 0
#                 if 0 not in zeroS.keys():
#                     zeroS[0] = set()
#                 zeroS[beforeLayer].remove(y)
#         print("count:%d" % count)
#         count += 1
#     return coverS
# def Max_rth_of_u_U(nodeAttribute,nodeNeighbors,radius,firstL,Cost):
#     """
#     BFS find rth layer
#     :param G:
#     :param radius:
#     :param u:
#     :return:
#     """
#     times=1
#     cur=set(firstL)
#     old=set(firstL)
#     while times<=radius:
#         times+=1
#         tmp=set()
#         for i in cur:
#             tmp|=set(nodeNeighbors[i])
#         old|=cur
#         tmp=tmp-old
#         cur=tmp
#         if len(cur)==0:
#             print("cur==0")
#             return True,Cost
#     # deg=dict(nx.degree(G,cur))
#     # for i in deg.keys():
#     #     deg[i]=deg[i]-len(set(nx.neighbors(G,i))&old)
#     deg={}
#     tt=0
#     MaxI=list(cur)[0]
#     for i in cur:
#         deg[i]=len(set(nodeNeighbors[i])-set(old))
#         if deg[i]>tt:
#             tt=deg[i]
#             MaxI=i
#         Cost[1]+=math.log(nodeAttribute[i][0])
#     # MaxI= max(deg.items(),key=lambda x: x[1])
#     return MaxI,Cost
#
# def CS_localAlg(nodeAttribute,nodeNeighbors,radius,Cost,coverS):
#     """
#     开局局部最大节点
#     每次找第r层里面和uset度数最大的，更新第r层，直到uset为0
#     :param G:
#     :param radius:
#     :return:
#     """
#     # 一步式迭代
#     CS = coverS.CS
#     BS=coverS.bs
#     US = set(nodeAttribute.keys()) - set(CS)
#     if len(CS)==0:
#         highest = random.choice(list(US))
#         "jump cost"
#         # walkCost += 1
#         res, Cost = RemoteS_up(nodeAttribute, nodeNeighbors, radius, highest, Cost,len(nodeAttribute))
#         return res,Cost
#     if len(CS) == len(nodeAttribute.keys()):
#         print("US is empty")
#     else:
#         cur,Cost = Max_rth_of_u_U(nodeAttribute,nodeNeighbors, radius, BS,Cost)
#         if type(cur) is bool:
#             if cur:
#                 highest = random.choice(list(US))
#                 "jump cost"
#                 # walkCost += 1
#                 Cost[0]+=1
#                 res, Cost = RemoteS_up(nodeAttribute, nodeNeighbors, radius, highest, Cost, len(nodeAttribute))
#         else:
#             res=cur
#             Cost[1]+=math.log(nodeAttribute[res][0])
#         return res,Cost
if __name__ == '__main__':
    nodeAttribute={}
    nodeNeighbors={}
    import networkx as nx
    G=nx.Graph()
    # for i in range(1, 3308 + 1, 1):
    #     temp = linecache.getline("dataEpoch//cit.txt", i)
    #     temp1 = temp.split("--")
    #     edge = eval(temp1[1])
        # for e in edge:
        #     if e[0] not in nodeAttribute.keys():
        #         nodeAttribute[e[0]]=[0,0]
        #         nodeNeighbors[e[0]]=set()
        #     if e[1] not in nodeAttribute.keys():
        #         nodeAttribute[e[1]] = [0, 0]
        #         nodeNeighbors[e[1]] = set()
        #     nodeNeighbors[e[0]].add(e[1])
        #     nodeAttribute[e[0]][0]=len(nodeNeighbors[e[0]])
        #     nodeNeighbors[e[1]].add(e[0])
        #     nodeAttribute[e[1]][0]=len(nodeNeighbors[e[1]])
        # G.add_edges_from(edge)
    temp = linecache.getline("dataEpoch//ca.txt", 1)
    edge = eval(temp)
    G.add_edges_from(edge)
    print("network building end")
    # print(nx.number_of_edges(G))
    # print(nx.number_of_nodes(G))
    import ALG_Metrics as cm
    # print(cm.networkProperty(G))
    # print(cm.log_log_regression(G))
    G=max(nx.connected_component_subgraphs(G),key=len)
    G.remove_edges_from(G.selfloop_edges())
    print(cm.test_cp(G))
    # print(len(list(nx.connected_component_subgraphs(G))))
    # cs=coverSet(2)
    # csn=TestAlternateRandom(nodeAttribute,nodeNeighbors,cs)
    # print(len(csn.CS))
    #1.34877