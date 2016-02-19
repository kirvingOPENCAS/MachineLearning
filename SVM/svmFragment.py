#-*- coding: utf-8 -*-
#照照自己理解写的，训练alpha值和b值
#完整版 Platt SMO 的外循环代码
def svmFragment(dataMat,labelMat,maxIter,C,tol,kernelType):
    #构造结构体数据
    dataStruct=optStruce(mat(dataMat),mat(labelMat).transpose(),C,tol)
    iter=0
    entireSet=1
    #循环条件,只要达到跌代次数 或者 alphas 值不再改变
    #循环在整个数据集和非边界点之间来回切换，目的是？
    while(iter<maxIter and （alphasChangedPairs>0 or entireSet)
        alphasChangedPairs=0
        #遍历所有数据集
        if(entireSet):
             #首先外循环选择一个alphasI,选择违反KKT条件的
            for i in range(dataStruct.m):
                Ei=calcEk(dataStruct,i)
                if((dataStruct.labelMat[i]*Ei<-dataStruct.tol) and dataStruct.alphas[i]<dataStruct.C \
                or (dataStruct.labelMat[i]*Ei>dataStruct.tol) and dataStruct.alphas[i]>0):
                #内循环选择最优的alphasJ，根据（Ei-Ej)最大对应的j值,其中b值的更新也在内循环中进行
                alphasChangedPairs+=(i,dataStruct)
                print "entireSet iter: %d,alphasCangedPairs:%d" % (iter,alphasChangedPairs)
                iter+=1
            #遍历非边界值，即 0<alpha<C
            else:
                nonBoundIs=nonzero((dataStruct.alphas.A>0) * (dataStruct.alphas.A<C))[0]
                for i in nonBoundIs:

                      #首先外循环选择一个alphasI,选择违反KKT条件的
                    Ei=calcEk(dataStruct,i)
                    if((dataStruct.labelMat[i]*Ei<-dataStruct.tol) and dataStruct.alphas[i]<dataStruct.C \
                    or (dataStruct.labelMat[i]*Ei>dataStruct.tol) and dataStruct.alphas[i]>0):
                    #内循环选择最优的alphasJ，根据（Ei-Ej)最大对应的j值
                    alphasChangedPairs+=(i,dataStruct)
                    print "nonbound iter: %d,alphasCangedPairs:%d" % (iter,alphasChangedPairs)
                    iter+=1
            #在整个数据集与非边界点集之间切换
            if(entireSet):
                entireSet=0
            elif(alphasChangedPairs==0):
                entireSet=1
            print "iteration number: %d " % iter

    return dataStruct.alphas,dataStruct.b























