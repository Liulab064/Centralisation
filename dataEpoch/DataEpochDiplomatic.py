#coding=utf-8

"""
本程序对数据集做处理：
    1、按照年份分割数据集 输出每个年份的点集  边集

"""
dataset=open("Diplomatic.txt",'r')

yearnodes={}
yearedges={}
for i in dataset.readlines():
    temp2=i.split(" ")[2].replace("\n","")
    if not temp2 in yearnodes.keys():
        yearnodes[temp2]=set()
    if not temp2 in yearedges.keys():
        yearedges[temp2]=set()
    temp0=int(i.split(" ")[0])
    temp1=int(i.split(" ")[1])

    yearnodes[temp2].update([temp0,temp1])
    yearedges[temp2].add((temp0,temp1))
f=open("diplomaticData.txt",'w')
sortyear=sorted(yearedges.keys())
for i in sortyear:
    f.write(str(list(yearnodes[i])))
    f.write("\n")
    f.write(str(list(yearedges[i])))
    f.write("\n")
