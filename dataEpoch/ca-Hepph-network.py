#coding=utf-8

"""
本程序对数据集做处理：


"""
dataset=open("ca-HepPh.txt",'r')

nodes=set()
edges=[]
for i in dataset.readlines():
    tempsource=int(i.split("\t")[0])
    temptarget=int(i.split("\t")[1].replace("\n",""))
    if not tempsource in nodes:
        nodes.add(tempsource)
    if not temptarget in nodes:
        nodes.add(temptarget)
    edges.append((tempsource,temptarget))
f=open("ca.txt",'w')
# f.write(str(list(nodes)))
# f.write("\n")
f.write(str(list(edges)))
