#coding=utf-8

"""
本程序对数据集做处理：


"""
import linecache
# dataset=open("facebook-wosn-wall.txt",'r')
a=[]
for i in range(1,1148072):
    temp=linecache.getline("outdblp_coauthor.txt",i)
    temp1=temp.split()
    a.append(temp1)
    # a.append((eval(temp1[0]),eval(temp1[1])))
    # a.add(eval(temp1[0]))
    # a.add(eval(temp1[1]))
    # print(len(a))
a.sort(key=lambda x:eval(x[3]))
f=open("enron.txt",'w')
old=0
oldedges=[]
# edges=[]
for i in a:
    if eval(i[3])==old:
        oldedges.append((eval(i[0]),eval(i[1])))
    else:
        f.write(str(oldedges))
        oldedges.clear()
        oldedges.append((eval(i[0]),eval(i[1])))
        old=eval(i[3])
        f.write("\n")
f.write(str(oldedges))
f.write("\n")