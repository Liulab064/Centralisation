#coding=utf-8
path=r"E:\视频\北邮人\DataEvelien_98_99\stu98t2.txt"
upath=unicode(path,'utf-8')
fread=open(upath,'r')
edges=[]
a=0
for i in fread.readlines():
    i=i.replace('\n','')
    temp=i.split("\t")
    # print temp
    for j in range(1,35):
        if int(temp[j])<=3 and int(temp[j])>0:
            edges.append((a,j))
    a+=1
# print edges
realedges=[]
for i in edges:
    if (i[1],i[0]) in edges and i[1]<i[0]:
        continue
    if i[1]==i[0]:
        continue
    if i[1]<i[0]:
        i1=(i[1],i[0])
    else:
        i1=i
    realedges.append(i1)
print realedges