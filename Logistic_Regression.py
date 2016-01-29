# coding=utf-8

'''
Created on Oct 27, 2010
Logistic Regression Working Module
@author: Peter
'''
from numpy import *

def loadDataSet():
    dataMat = []; labelMat = []
    fr = open('/home/hadoop/Machine_Learning/machinelearninginaction/Ch05/testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn)             #convert to NumPy matrix
    labelMat = mat(classLabels).transpose() #convert to NumPy matrix
    m,n = shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    weights = ones((n,1))
    for k in range(maxCycles):              #heavy on matrix operations
        h = sigmoid(dataMatrix*weights)     #matrix mult
        error = (labelMat - h)              #vector subtraction
        weights = weights + alpha * dataMatrix.transpose()* error #matrix mult
    return weights

#
# from numpy import *
# import math
#
# def loadDataSet():
#     dataMat=[];labelMat=[]
#     # fr=open('/home/hadoop/Machine_Learning/machinelearninginaction/Ch05/testSet.txt')
#     fr=open('testSet.txt')
#     for line in fr.readlines():
#         lineArr=line.strip().split()
#         dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
#         #add column of number 1 because of the constant term
#         labelMat.append(int(lineArr[2]))
#     return dataMat,labelMat
#
#
# def sigmoid(x):
#     return 1.0/(1+exp(-x))
#
#
# # def gradAscent(dataMat,labelVec,maxIter,stepDistance):
# def gradAscent(dataMat,labelVec):
#     #dataMat:traing data.labelVect:training data's labels
#     #maxIter:max number of iteration.
#     dataMatrix=mat(dataMat)
#     labelMat=mat(labelVec).transpose()
#     #tranpose：turn row to column
#     numRow,numCol=shape(dataMatrix)
#     print '%d' % numCol
#     w=ones((numCol,1))
#     maxIter=500
#     stepDistance=0.001
#
#     for i in range(maxIter):
#         predictRes=sigmoid(dataMatrix*w)
#         error=(labelVec-predictRes)
#         #update weight matrix according to error
#         w=w+stepDistance*dataMatrix.transpose()*error
#     print w


def plotBestFit(dataMat,labelVec,weights):
    #if excute with plotBestFit(dataMat,labelVec,weights)
    #there will be an eror:"x and y must have same first dimension"
    import matplotlib.pyplot as plt
    dataMat=array(dataMat)
    #if this sentence doesn't exist,there will be an error:
    # "list indices must be integers, not tuple"

    numData=shape(dataMat)[0]
    class1Cordx=[]
    class1Cordy=[]
    class2Cordx=[]
    class2Cordy=[]
    for i in range(numData):
        if int(labelVec[i])==1:
            class1Cordx.append(dataMat[i,1])
            class1Cordy.append(dataMat[i,2])
        else:
            class2Cordx.append(dataMat[i,1])
            class2Cordy.append(dataMat[i,2])
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(class1Cordx,class1Cordy,s=30,c='red',marker='s')
    ax.scatter(class2Cordx,class2Cordy,s=30,c='green')
    x=arange(-3.0,3.0,0.1)
    y=(-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x,y)
    plt.xlabel('X1')
    plt.ylabel('Y1')
    plt.show()


def stoGradAscent(dataMat,labelVec,maxIter=150):
    #default maxIter is 150
    #stocastic gradient ascent algorithm
    dataMat=array(dataMat)
    numData,numFeature=shape(dataMat)
    print 'the number of training data is %d,the feature number' \
          'of the data is %d' % (numData,numFeature)

    weights=ones(numFeature)
    for i in range(maxIter):
        dataIndex=range(numData)
        for j in range(numData):
            #alpha is changed in every step
            alpha=4/(1+i+j)+0.01
            #first pick a traing data randomly
            randIndex=int(random.uniform(0,len(dataIndex)))
            temp=sum(dataMat[randIndex]*weights)
            predictRes=sigmoid(temp)
            #if change to predictRes-labelVec[randIndex]
            #the result will be totally different!
            error=labelVec[randIndex]-predictRes
            #updata weights according to error and alpha
            weights=weights+alpha*error*dataMat[randIndex]
            del(dataIndex[randIndex])
            # print weights

    return weights


def modelTraining(maxIter):
    #open,load training data
    td=open('/home/hadoop/Machine_Learning/machinelearninginaction/Ch05/horseColicTraining.txt')
    trainDataMat=[]
    trainLabelVec=[]
    for line in td.readlines():
        eachLine=line.strip().split('\t')
        #temporary line for store each line read from origin file
        tempLine=[]
        for i in range(21):
            tempLine.append(float(eachLine[i]))
        #appen each line to training data
        trainDataMat.append(tempLine)
        #append training data's label
        trainLabelVec.append(float(eachLine[21]))

    #training model
    weights=stoGradAscent(trainDataMat,trainLabelVec,maxIter)

    #examin accurancy
    tf=open('/home/hadoop/Machine_Learning/machinelearninginaction/Ch05/horseColicTest.txt')
    testDataMat=[]
    testDataLab=[]
    for line in tf.readlines():
        eachLine=line.strip().split('\t')
        tempLine=[]
        for i in range(21):
            tempLine.append(float(eachLine[i]))
        testDataMat.append(tempLine)
        testDataLab.append(float(eachLine[21]))

    testDataMat=mat(testDataMat)
    numTest=shape(testDataMat)[0]
    print 'number of test samples is :%d' % numTest
    errorCount=0

    #the dot multiply is important here!
    # if change to testDataMat*weights there will be error occurs!
    tempRes=dot(testDataMat,weights)
    # print tempRes
    m,n=shape(tempRes)
    # tempRes=sum(testDataMat*weights)
    predictRes=sigmoid(tempRes)
    # print predictRes
    # m,n=shape(predictRes)
    # print m,n

    for i in range(numTest):
        if predictRes[0,i]<0.5:
            predictRes[0,i]=0
        else:
            predictRes[0,i]=1
        if predictRes[0,i]!=testDataLab[i]:
            errorCount+=1

    errorRate=float(errorCount)/numTest
    print "the error rate is %f" % errorRate





