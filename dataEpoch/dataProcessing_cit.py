#coding=utf-8

"""
本程序对数据集做处理：
    1、数据集分成两部分   点index+度数+color  ----------  点index+Neighbors
    2、首先将联通图切分出来

"""
import re
import linecache
def Processing(init,end):
    # f = open("coDblp" + ".txt", 'a+')
    f=open("NAroad"+'.txt','a+')
    edge = []
    for i in range(init, end + 1, 1):
        # temp = linecache.getline("dataEpoch//collaboration-dblp.txt", i)
        temp=linecache.getline("dataEpoch//NA.cedge",i)
        temp1 = temp.strip().split(" ")
        edge.append((eval(temp1[1]),eval(temp1[2])))
    f.write(str('static')+"--"+str(edge)+ "\n")
    f.close()
if __name__ == '__main__':
    # Processing(1,1049866)
    Processing(1,179179)

