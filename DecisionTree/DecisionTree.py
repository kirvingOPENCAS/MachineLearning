#-*- coding: utf-8 -*-
from math import log
import operator
# import treePlotter

#计算数据集的熵，dataset最后一列为label
def calcShannonEnt(dataSet):
    numentries=len(dataSet)
    labelCounts={}

    for featVec in dataSet:
        currentLabel=featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel]+=1

    shannonEnt=0.0
    for key in labelCounts:
        prob=float(labelCounts[key])/numentries
        shannonEnt-=prob*log(prob,2)
    return shannonEnt


def createDataSet():
    dataSet=[[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels=['no surfacing','flippers']
    return dataSet,labels

#根据某一维度的某个值，将数据集切分
def splitDataSet(dataSet,dim,value):
    remSpecDimData=[]
    numData=len(dataSet)
    for i in range(numData):
        featVec=dataSet[i]
        if featVec[dim]==value:
            frontData=featVec[:dim]
            behindData=featVec[dim+1:]
            frontData.extend(behindData)
            remSpecDimData.append(frontData)

    return remSpecDimData

#从数据集中选择最好的属性作为划分属性
def chooseBestFeat(dataSet):
    numData=len(dataSet)
    baseEnt=calcShannonEnt(dataSet)
    #循环遍历所有的属性，找到最好的
    #计算每一个属性的熵
    #假定所有数据最后一列都为label列
    numFeature=len(dataSet[0])-1
    maxEntAug=0
    bestFeat=-1
    for i in range(numFeature):
        curVec=[]
        #将每一个属性的所有值放入一个列表中
        for featVec in dataSet:
            # temp=featVec[i]
            curVec.append(featVec[i])
        #利用set函数去重
        valuesPerAttri=set(curVec)
        entry=0.0
        #对每一个属性的所有取值，计算概率
        for value in valuesPerAttri:
            subDataSet=splitDataSet(dataSet,i,value)
            prob=len(subDataSet)/float(numData)
            entry+=prob*calcShannonEnt(subDataSet)
        # bestFeat=-1
        valueEntAdd=baseEnt-entry
        print 'infoGain %f' % valueEntAdd
        if (valueEntAdd>maxEntAug):
            maxEntAug=valueEntAdd
            bestFeat=i

    return bestFeat



def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount=sorted(classCount.iteritems(),\
                            key=operator.itemgetter(1),reverse=True)
    return sortedClassCount


#创建决策树
def createDT(dataSet,labels):
    classList=[example[-1] for example in dataSet]
    #所有样本的label都相同时
    if classList.count(classList[0])==len(dataSet):
        return classList[0]
    #使用完所有特征，仍然不能将数据集划分成仅包含唯一类别的分组,
    #则将该组中的类别中的大多数作为反回值
    if len(dataSet[0])==1:
        return majorityCnt(classList)

    bestFeat=chooseBestFeat(dataSet)
    bestFeatLabel=labels[bestFeat]  #?
    myTree={bestFeatLabel:{}}  #存储树结构
    del(labels[bestFeat])  #?
    bestFeatCol=[example[bestFeat] for example in dataSet]
    bestFeatCol=set(bestFeatCol)

    for value in bestFeatCol:
        subLabels=labels[:]
        #复制labels给subLabels，Python中当函数参数为列表时，参数是按照引用来
        #传递，保证再次调用createDT时不改变原始列表的内容
        subDataSet=splitDataSet(dataSet,bestFeat,value)
        myTree[bestFeatLabel][value]=createDT(subDataSet,subLabels)

    return myTree


#使用pickle模块将决策树存储在硬盘上
def storeTree(inputTree,filename):
    import pickle
    fw=open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close()


#从硬盘中读取决策树
def grabTree(filename):
    import pickle
    fr=open(filename)
    return pickle.load(fr)

def judgeLense(dataSet,labels):
    fr=open(dataSet)
    lenses=[inst.strip().split('\t') for inst in fr.readlines()]
    print lenses
    #创建决策树
    lensesTree=createDT(lenses,labels)
    #画出决策树
    # treePlotter.createPlot(lensesTree)

    return lensesTree



myDat,label=createDataSet()
print myDat
# Entry=calcShannonEnt(myDat)
# print Entry
# myDat[0][-1]='maybe'
# print myDat
# Entry=calcShannonEnt(myDat)
# print Entry
# a=splitDataSet(myDat,0,1)
# print a
# b=chooseBestFeat(myDat)
# print b
myTree=createDT(myDat,label)
# print myTree
storeTree(myTree,'classfier.txt')
a=grabTree('classfier.txt')
print a

b=judgeLense('lenses.txt',['age','prescript','astigmatic','tearRate'])
print b