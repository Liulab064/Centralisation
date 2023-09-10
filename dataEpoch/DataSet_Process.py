#coding=utf-8

"""
本程序对数据集做处理：
    1、按照年月日分割数据集
    2、输出每个年月日的点集  边集

"""
import re
dataset=open("election.txt",'r')

yearnodes={}
for i in dataset.readlines():
    temp=i.split(" ")
    tempEdge=(int(temp[0]),int(temp[1]))
    # if re.match(re.compile("^11.+"),str(tempnode)):
    #     continue
    if int(temp[2]==-1):
        continue
    tempyear=int(temp[-1].replace("\n",""))
    if not tempyear in yearnodes.keys():
        yearnodes[tempyear]=set()
    yearnodes[tempyear].add(tempEdge)
    # print i
f=open("election_Data.txt",'w')
sortyear=sorted(yearnodes.keys())
sum=0
# print sortyear
for i in sortyear:

    f.write(str(list(yearnodes[i])))
    f.write("\n")
    # print yearnodes[i]
