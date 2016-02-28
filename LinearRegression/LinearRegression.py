#-*- coding: utf-8 -*-
from numpy import *

def LocalWeightedLN(testPoint,arrX,arrY,k):
    xMat=mat(arrX)
    yMat=mat(arrY).T
    numTrain=shape(yMat)[0]
    # print numTrain
    weightMat=mat(eye(numTrain))

    for i in range(numTrain):
        diff=testPoint - xMat[i,:]
        weightMat[i,i]=exp((diff*diff.T)/(-2.0*k**2))
    # print 'weight Matrix:'
    # print weightMat
    xTx=xMat.T*(weightMat*xMat)
    if linalg.det(xTx)==0:
        print "This matrix is singular,cannot do inverse"
        return
    regressionCoef=xTx.I*(xMat.T*(weightMat*yMat))
    # print regressionCoef
    # print 'the coefficients of regression is:'
    # print regressionCoef
    predictValue=float(testPoint*regressionCoef)
    return predictValue

def loadDataSet(filename):
    fr=open(filename).readline().split('\t')
    numFeats=len(fr)-1
    file=open(filename)
    # numSamples=len(file)
    xArr=[]
    yArr=[]
    for line in file.readlines():
        xtemp=[]
        arrline=line.strip().split('\t')
        for j in range(numFeats):
            xtemp.append(float(arrline[j]))
        xArr.append(xtemp)
        yArr.append(float(arrline[-1]))

    return xArr,yArr


def testLWLN(testArr,arrX,arrY,k):
    testMat=mat(testArr)
    numTest=shape(testMat)[0]
    predVal=[]
    for i in range(numTest):
        temp=LocalWeightedLN(testMat[i,:],arrX,arrY,k)
        predVal.append(temp)

    return predVal


def plotCurve(xArr,predVal):

    import pylab as pl
    predVal=mat(predVal).T
    # m,n=shape(predVal)
    # print m,n
    xMat=mat(xArr)
    xMatRem=xMat[:,1]
    strInd=xMatRem.argsort(0)
    # print 'strInd'
    # print strInd
    # xMatRem=[xMatRem]

    xSortRem=xMatRem[strInd]
    xSortRem=xSortRem[:,:,0]
    m=shape(xSortRem)
    print m
    # print 'xSortRem'
    # print xSortRem
    valSort=predVal[strInd]
    valSort=valSort[:,:,0]
    m=shape(valSort)
    print m
    # print 'valSort'
    # print valSort

    # xSort=xMat[strInd][:,0,:]
    # pl.plot(xMatRem,valSort)
    # pl.show()
    # print xSortRem
    import matplotlib.pyplot as plt
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(xMatRem[:],valSort[:])
    ax.scatter(xMat[:,1].flatten(    plt.show()
).A[0],mat(yArr).T.flatten().A[0],s=2,c='red')
    plt.show()

    return


#岭回归
def ridgeRegres(xMat,yMat,lam):
    # xMat=mat(xArr)
    # yMat=mat(yArr)
    dim=shape(xMat)[1]
    xTx=xMat.T*xMat+lam*eye(dim)
    if linalg.det(xTx)==0:
        print 'this matrix is singular,cannot inverse'
    w=xTx.I*(xMat.T*yMat)

    return w


def ridgeTest(xArr,yArr):
    xMat = mat(xArr); yMat=mat(yArr).T
    yMean = mean(yMat,0)
    yMat = yMat - yMean     #to eliminate X0 take mean off of Y
    #regularize X's
    xMeans = mean(xMat,0)   #calc mean then subtract it off
    xVar = var(xMat,0)      #calc variance of Xi then divide by it
    xMat = (xMat - xMeans)/xVar
    numTestPts = 30
    wMat = zeros((numTestPts,shape(xMat)[1]))
    for i in range(numTestPts):
        ws = ridgeRegres(xMat,yMat,exp(i-10))
        wMat[i,:]=ws.T
    return wMat


from time import sleep
import json
import urllib2
def searchForSet(retX, retY, setNum, yr, numPce, origPrc):
    sleep(10)
    myAPIstr = 'AIzaSyD2cR2KFyx12hXu6PFU-wrWot3NXvko8vY'
    searchURL = 'https://www.googleapis.com/shopping/search/v1/public/products?key=%s&country=US&q=lego+%d&alt=json' % (myAPIstr, setNum)
    pg = urllib2.urlopen(searchURL)
    retDict = json.loads(pg.read())
    for i in range(len(retDict['items'])):
        try:
            currItem = retDict['items'][i]
            if currItem['product']['condition'] == 'new':
                newFlag = 1
            else: newFlag = 0
            listOfInv = currItem['product']['inventories']
            for item in listOfInv:
                sellingPrice = item['price']
                if  sellingPrice > origPrc * 0.5:
                    print "%d\t%d\t%d\t%f\t%f" % (yr,numPce,newFlag,origPrc, sellingPrice)
                    retX.append([yr, numPce, newFlag, origPrc])
                    retY.append(sellingPrice)
        except: print 'problem with item %d' % i

def setDataCollect(retX, retY):
    searchForSet(retX, retY, 8288, 2006, 800, 49.99)
    searchForSet(retX, retY, 10030, 2002, 3096, 269.99)
    searchForSet(retX, retY, 10179, 2007, 5195, 499.99)
    searchForSet(retX, retY, 10181, 2007, 3428, 199.99)
    searchForSet(retX, retY, 10189, 2008, 5922, 299.99)
    searchForSet(retX, retY, 10196, 2009, 3263, 249.99)


#
# lgX=[]
# lgY=[]
# setDataCollect(lgX,lgY)
import urllib2
path='http://www.baidu.com'
a=urllib2.urlopen(path)
retDict = json.loads(a.read())

print a

# xArr,yArr=loadDataSet('Ch08/abalone.txt')
# w=ridgeTest(xArr,yArr)
# import matplotlib.pyplot as plt
# fig=plt.figure()
# ax=fig.add_subplot(111)
# ax.plot(w)
# plt.show()

# print mat(xArr)

# predVal=testLWLN(xArr,xArr,yArr,0.01)
# print predVal
# plotCurve(xArr,predVal)

