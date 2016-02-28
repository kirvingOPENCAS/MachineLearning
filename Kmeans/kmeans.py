#-*- coding: utf-8 -*-
from numpy import *
from random import *

def kmeans(dataSet,k,iterNum):
    iter=0
    clusterCenter=[]
    m,n=shape(dataSet)
    clusterEleList=mat(zeros((m,2)))

    #random initialize k cluster center points
    minData=min(dataSet)
    maxData=max(dataSet)
    randList=[]

    for i in range(k):
        randValComp=[]
        for j in range(n):
            minVal=minData[j]
            maxVal=maxData[j]
            randValue=uniform(minVal,maxVal)
            randValComp.append(randValue)
        randList.append(randValComp)

    clusterCenter=randList
    oldErr=0.0
    newErr=0.0
    errChanged=100

#when iteration time less than threshold,continue
    while((iter<iterNum) & (errChanged>10)):
        oldErr=newErr
        print iter
#compute the distance between each point and cluster centers
        for i in range(m):
            clusterClass,minDis=computeMinDis(dataSet[i],clusterCenter)
            clusterEleList[i,:]=clusterClass,minDis

#compute the new cluster centers
        for cent in range(k):
            kcluster=[]
            newkcluster=[]
            for j in range(m):
                if(clusterEleList[j,0]==cent):
                    kcluster.append(j)
            for val in kcluster:
                newkcluster.append(dataSet[val])
            newkcluster=mat(newkcluster)
            temp=[]
            for p in range(n):
                temp.append(average(newkcluster[:,p]))
            clusterCenter[cent]=temp
            # kcluster=dataSet[numpy.nonzero(clusterEleList[:,0].A==cent)[0]]
            # clusterCenter[cent,:]=numpy.mean(kcluster,axis=0)

        error=[]
        error=clusterEleList[:,1]
        newErr=sum(error)
        errChanged=(newErr-oldErr)**2


        iter+=1

    return clusterCenter,clusterEleList



def computeMinDis(sample,clusterCenter):
    sample=mat(sample)
    clusterCenter=mat(clusterCenter)
    m,n=shape(clusterCenter)
    sample=mat(sample)
    clusterCenter=mat(clusterCenter)
    minDis=10000.0
    clusterClass=-1

    for i in range(m):
        dis=float((sample-clusterCenter[i])*(sample-clusterCenter[i]).T)
        if dis < minDis:
            minDis=dis
            clusterClass=int(i)

    return clusterClass,minDis


def loadDataSet(filename):
    dataSet=[]
    fr=open(filename)
    for lines in fr.readlines():
        curLine=lines.strip().split('\t')
        fltLine=map(float,curLine)
        dataSet.append(fltLine)

    return dataSet

#二分 K均值算法
def biKmeans(dataSet,k):
    # dataSet=mat(dataSet)
    m,n=shape(dataSet)
    #clusterEleList用来存储每个元素所属的簇以及到簇中心的距离
    clusterEleList=mat(zeros((m,2)))
    #clusterCenter用来存储簇中心坐标
    # clusterCenter=[]

    #初始簇中心
    #此处的tolist()一定要加！！！
    initCenter=mean(dataSet,axis=0).tolist()
    print "initCenter",initCenter
    clusterCenter=[initCenter]
    numCenter=1

    #初始簇设为0，计算初始距离
    for i in range(m):
        clusterClass,minDis=computeMinDis(dataSet[i],initCenter)
        clusterEleList[i,:]=clusterClass,minDis

    #当簇的数目小于K时，循环
    while numCenter<k:

        #未划分的总误差
        notSplitErr=sum(clusterEleList[:,1])
        minErr=notSplitErr

        #将每一个簇一分为二
        for i in range(numCenter):

            #提取这个簇的所有元素
            temp=[]
            curData=[]
            temp=nonzero(clusterEleList[:,0].A==i)[0]
            # curData=dataSet[nonzero(clusterEleList[:,0].A==i)[0]]
            # print temp
            for val in temp:
                # val=int(val)
                # print dataSet[val]
                curData.append(dataSet[val])

            #对这个簇使用k=2的kmeans进行划分
            newTwoCenter,newCluEleList=kmeans(curData,2,100)
            if numCenter>1:
                newCluEleList[:,0]=newCluEleList[:,0]+numCenter-1

            print newCluEleList
            #计算划分后的总误差
            splitErr=sum(newCluEleList[:,1])
            otherErr=sum(clusterEleList[(clusterEleList[:,0].A!=i)[0],1])
            totalSplitErr=splitErr+otherErr

            #将划分后的总误差与最小误差进行比较
            if totalSplitErr<minErr:
                minErr=totalSplitErr
                splitedClu=i
                best2Center=newTwoCenter
                best2CluEleList=newCluEleList
        #最终将得到待划分的簇以及距离
        #更新clusterCenter,clusterEleList
        print best2Center[0],clusterCenter[splitedClu]
        clusterCenter[splitedClu]=best2Center[0]
        clusterCenter.append(best2Center[1])
        # clusterCenter.extend(best2Center)

        clusterEleList[nonzero(clusterEleList[:,0].A==splitedClu)[0],:]=best2CluEleList

        # clusterEleList.pop(nonzero(clusterEleList[:,0].A==splitedClu)[0])
        # clusterEleList.extend(best2CluEleList)

        numCenter+=1
        if numCenter==k:
            print shape(clusterEleList)[0]

    return clusterCenter,clusterEleList


# dataSet3=mat(loadDataSet('testSet2.txt'))
dataSet=loadDataSet('testSet2.txt')

# m,n=shape(dataSet)
clusterCenter,clusterEleList=biKmeans(dataSet,4)
print "clusterCenter",clusterCenter
print "clusterEleList",clusterEleList
