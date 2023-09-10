#coding=utf-8

"""
本程序对数据集做处理：
    1、按照年月日分割数据集
    2、输出每个年月日的点集  边集

"""
import re
dataset=open("cit-HepPh-dates.txt",'r')

yearnodes={}
for i in dataset.readlines():

    tempnode=int(i.split("\t")[0])
    if re.match(re.compile("^11.+"),str(tempnode)):
        continue
    tempyear=int(i.split("\t")[1].replace("\n",""))
    if not tempyear in yearnodes.keys():
        yearnodes[tempyear]=set()
    yearnodes[tempyear].add(tempnode)
f=open("citData.txt",'w')
sortyear=sorted(yearnodes.keys())
for i in sortyear:
    f.write(str(list(yearnodes[i])))
    f.write("\n")
