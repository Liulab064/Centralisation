#coding=utf-8

"""
本程序对数据集做处理：
    1、分割数据集为80份  每份代表一个静态网络状态    输出nodes 和 edges
    2、
"""
dataset=open("T0.txt",'r')
datanums=80
#取时间集 ，
timeGap=[]
edges1=[]
edges2=[]
for i in dataset.readlines():
    # print i
    edges1.append((int(i.split(" ")[0]),int(i.split(" ")[1])))
    temptime=i.split(" ")[2].replace("\n","")
    # print temptime
    timeGap.append(int(temptime))
timeBegain=timeGap[0]
timeEnd=timeGap[-1]
timeInterval=(int(timeEnd)-int(timeBegain))/datanums
net=open("email.txt",'a+')
a=3
for i in range(len(edges1)):
    if int(timeGap[i])>=timeBegain+timeInterval*a and int(timeGap[i])<timeBegain+timeInterval*(a+1):
        edges2.append(edges1[i])
    elif timeGap[i]>=timeBegain+timeInterval*(a+1):
        break
# print timeInterval
b=0
for i in edges2:
    net.write(str(i)+",")
    b+=1
    if b%10==0:
        net.write("\n")

net.close()