# coding=utf-8
from numpy import *


def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec=[0,1,0,1,0,1]
    return postingList,classVec

def createVocabList(dataSet):
    #create a word set ,all of the words come from the dataSet
    #and no repeat words.
    #set will filter the same words in the document
    vocabList=set([])
    for document in dataSet:
        vocabList=vocabList | set(document)
    return list(vocabList)


def setOfWords2Vec(vocabSet,inputdoc):
    #set the input document to a vector according to the vocabulary dataSet
    #initialize a 0 vector ,length=len(vocabSet)
    doc2Vec=zeros(len(vocabSet))
    for word in inputdoc:
        if word in vocabSet:
            doc2Vec[vocabSet.index(word)]=1
    return doc2Vec


def trainNaiveBayes(trainMat,trainClass):
    #get each word's probability to per class
    numTrainDocs=len(trainMat)
    vectorSize=len(trainMat[0])
    numInsult=sum(trainClass)
    averProbInsult=numInsult/float(numTrainDocs)
    probNonInsult=ones(vectorSize)
    totalWordsInsult=2
    probInsult=ones(vectorSize)
    totalWordsNonInsult=2
    for i in range(numTrainDocs):
        if trainClass[i]==1:
            probInsult+=trainMat[i]
            totalWordsInsult+=sum(trainMat[i])
        else:
            probNonInsult+=trainMat[i]
            totalWordsNonInsult+=sum(trainMat[i])
    # probInsult=probInsult/totalWordsInsult
    # probNonInsult=probNonInsult/totalWordsNonInsult
    #changed to log to avoid little numbers' add become 0!
    probInsult=log(probInsult/totalWordsInsult)
    probNonInsult=log(probNonInsult/totalWordsNonInsult)

    return probInsult,probNonInsult,averProbInsult

# reload(bayes)
# listWords,listClass=bayes.loadDataSet()
# vocab=bayes.createVocabList(listWords)
# trainMat=[]
# for i in listWords:
#     trainMat.append(bayes.setOfWords2Vec(vocab,i))
#
# p0,p1,pAb=bayes.trainNaiveBayes(trainMat,listClass)
#

def classifyNaiveBayes(testData,vecProbInsult,vecProbNonInsult,aveProbInsult):

    probInsult=sum(testData*vecProbInsult)+log(aveProbInsult)
    probNonInsult=sum(testData*vecProbNonInsult)+log(1-aveProbInsult)
    print probInsult,probNonInsult
    if probInsult>probNonInsult:
        return 1
    else:
        return 0


def testNaiveBayes():
    listWords,listClasses=loadDataSet()
    vocabulary=createVocabList(listWords)
    trainDataMat=[]
    for sen in listWords:
        trainDataMat.append(setOfWords2Vec(vocabulary,sen))
    print trainDataMat
    probInsult,probNonInsult,p=trainNaiveBayes(trainDataMat,listClasses)
    print probInsult,probNonInsult,p
    test1=['love','my','dalmation']
    test2=['stupid','garbage']

    test1=array(setOfWords2Vec(vocabulary,test1))
    print test1
    test2=array(setOfWords2Vec(vocabulary,test2))
    print test2
    #attentation! array()!

    result1=classifyNaiveBayes(test1,probInsult,probNonInsult,p)
    result2=classifyNaiveBayes(test2,probInsult,probNonInsult,p)
    print "result1:%d,result2:%d" % (result1,result2)


def bagOfWords2Vec(vocabSet,inputdoc):
    #set the input document to a vector according to the vocabulary dataSet
    #initialize a 0 vector ,length=len(vocabSet)
    #the value of the element depends on the times of the word appearing in the doc

    doc2Vec=zeros(len(vocabSet))
    for word in inputdoc:
        if word in vocabSet:
            doc2Vec[vocabSet.index(word)]+=1
    return doc2Vec


def textParse(str):
    #split documents to alone words,remove additional blank space
    # ,punctuation marks and those words' length shorter than 2
    import re
    listOfTokens=re.split(r'\W*',str)
    return [tok.lower() for tok in listOfTokens if len(listOfTokens)>2]


def classifyTrashEmail():
    #given a email,judge whether it's a trash email or not.
    #first open training emails,read,and train naive bayes model
    #get the number of files in the directory


    import os
    import random

    docNameSet0=os.listdir("/home/hadoop/Machine_Learning/machinelearninginaction/"
               "Ch04/email/ham")

    numDocs0=len(docNameSet0)
    emailList=[]
    wordList=[]
    classLabel=[]
    for i in range(numDocs0):
        fullEmailName="/home/hadoop/Machine_Learning/machinelearninginaction/Ch04/email/ham/"+docNameSet0[i]
        eachEmail=open(fullEmailName)
        emailList.append(eachEmail)
        wordList.extend(eachEmail)
        classLabel.append(0)

    docNameSet1=os.listdir("/home/hadoop/Machine_Learning/machinelearninginaction/"
               "Ch04/email/spam")
    numDocs1=len(docNameSet1)
    totalNumDocs=numDocs0+numDocs1
    print "total number of docs %d" % totalNumDocs
    for i in range(numDocs1):
        fullEmailName="/home/hadoop/Machine_Learning/machinelearninginaction/Ch04/email/spam/"+docNameSet1[i]
        eachEmail=open(fullEmailName)
        emailList.append(eachEmail)
        wordList.extend(eachEmail)
        classLabel.append(1)

    #construct a vocabulary which contains all the words appeared in all emails
    emailVocabulary=createVocabList(emailList)
    print emailVocabulary
    trainMat=[]
    testMat=[]
    trainLabel=[]
    testLabel=[]

        #random pick up 1/5 emails as testing set,the rest as training set
    randrange=range(totalNumDocs)
    numSamples=totalNumDocs*1/5
    randList=random.sample(randrange,numSamples)
    print "rand list"
    print randList
    a=len(emailList)
    print "number of email List %d" % a

    for i in range(numSamples):
        testMat.append(array(setOfWords2Vec(emailVocabulary,emailList[randList[i]])))
        testLabel.append(classLabel[i])
            #delete those index which used to test
        del(randrange[randList[i]])
    print "randrange"
    b=len(randrange)
    print randrange,b

    for j in randrange:
        trainMat.append(array(setOfWords2Vec(emailVocabulary,emailList[j])))
        trainLabel.append(classLabel[j])


    print "trainMat"
    print shape(trainMat[1])
        #train bayes model
    probTrashEmail,probNonTrashEmail,averageTrashEmailProb=trainNaiveBayes(trainMat,trainLabel)
    print probTrashEmail,probNonTrashEmail,averageTrashEmailProb

    errorCount=0
        #test model
    for i in range(numSamples):
        result=classifyNaiveBayes(testMat[i],probTrashEmail,probNonTrashEmail,averageTrashEmailProb)
        if result!=testLabel[i]:
            errorCount+=1
        print result
    errorRate=errorCount/float(numSamples)
    print 'the error rate is %f' % errorRate


def calcMostFreq(vocablist,fullText):
    import operator
    freqTok={}
    #statistic every word's frequence
    for tok in vocablist:
        freqTok[tok]=fullText.count(tok)
    #sort the frequence
    sortedFreq=sorted(freqTok.iteritems(),key=operator.itemgetter(1),\
                      reverse=True)
    return sortedFreq[:30]


def localWords(feed1,feed0):
    import feedparser
    docList=[]
    classList=[]
    fullText=[]
    minLen=min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList=textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        classList.append(1)
        fullText.extend(wordList)
        wordList=textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        classList.append(0)
        fullText.extend(wordList)
    vocabulary=createVocabList(docList)
    print len(vocabulary)
    top30words=calcMostFreq(vocabulary,docList)
    #removing top 30 frequence words
    for word in top30words:
        if word[0] in vocabulary:
            vocabulary.remove(word[0])

    trainingSet=range(2*minLen)
    testSet=[]
    for i in range(20):
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])

    trainMat=[]
    trainClasses=[]
    for docInx in trainingSet:
        trainMat.append(array(bagOfWords2Vec(vocabulary,docList[docInx])))
        trainClasses.append(classList[docInx])

    #training Naive Bayes
        prob0,prob1,averProb=trainNaiveBayes(trainMat,trainClasses)

    errorCount=0
    for docInx in testSet:
        testVec=bagOfWords2Vec(vocabulary,docList[docInx])
        result=classifyNaiveBayes(testVec,prob0,prob1,averProb)
        if result!=classList[docInx]:
            errorCount+=1

    errorRate=errorCount/float(len(testSet))
    print "the error rate is %f" % errorRate
    return vocabulary,prob0,prob1


def getTopWords(ny,sf):
    import operator
    vocabList,p0,p1=localWords(ny,sf)
    topNy=[]
    topSf=[]

    for i in range(len(p0)):
        if p0[i]>-6.0:
            topNy.append((vocabList[i],p0[i]))
        if p1[i]>-6.0:
            topSf.append((vocabList[i],p1[i]))

    sortedSf=sorted(topSf,key=lambda pair:pair[1],reverse=True)
    print "sortedSf"
    print sortedSf[:10]
    # for item in sortedSf:
    #     print item[0]

    sortedNy=sorted(topNy,key=lambda pair:pair[1],reverse=True)
    print "sortedNy"
    print sortedNy[:10]
    # for item in sortedNy:
    #     print item[0]






