#coding=utf-8

"""
本程序对数据集做处理：
    1、数据集分成两部分   点index+度数+color  ----------  点index+Neighbors

"""
import re
import linecache
def DataProcessing(init,end):
    f = open("netScienceNew" + ".txt", 'a+')
    flag=False

    edge = [-1, -1]
    for i in range(init, end + 1, 1):
        temp = linecache.getline("dataEpoch//netSciencEdges.txt", i)

        temp = temp.replace("[","").replace("]","")
        temp=temp.strip()
        if temp=="edge":
            flag=True
            continue

        if flag:
            if temp=="":
                continue
            else:
                temp1=temp.split(" ")

            if temp1[0]=="source":
                edge[0]=eval(temp1[1])
            elif temp1[0]=="target":
                edge[1]=eval(temp1[1])
            elif temp1[0]=="value":
                flag=False
                f.write(str("(%d,%d)"%(edge[0],edge[1]))+ ",")
                edge = [-1, -1]
    f.close()
if __name__ == '__main__':
    DataProcessing(1,16451)

