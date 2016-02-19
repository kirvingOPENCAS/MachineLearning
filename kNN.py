# coding=utf-8
from numpy import *
import operator
from os import listdir

def createDataSet():
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return group,labels

def classify0(inX,dataSet,labels,k):
    #shape函数是numpy.core.fromnumeric中的函数，它的功能是读取矩阵的长度，比如shape[0]就是读取矩阵第一维度的长度。
    dataSetSize=dataSet.shape[0]
    #def tile(A, reps)，Construct an array by repeating A the number of times given by reps.
    diffMat=tile(inX,(dataSetSize,1))-dataSet
    sqDiffMat=diffMat**2
    #对向量差平方求和，按照第一维求和
    sqDistance=sqDiffMat.sum(axis=1)
    distance=sqDistance**0.5
    #对距离进行排序
    sortedDistIndicies=distance.argsort()
    classCount={}
    #统计前k个距离最小的样本各自的label
    for i in range(k):
        #index=sortedDistIndicies[i]
        voteIlabel=labels[sortedDistIndicies[i]]
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
        #统计出现次数最多的label，将其作为待判定数据的label
    sortedClassCount=sorted(classCount.iteritems(),
                            key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

#将文本数据转化成标准格式
def file2matrix(filename):
    fr=open(filename)
    arrayOLines=fr.readlines()
    numberOfLines=len(arrayOLines)
    returnMat=zeros((numberOfLines,3))
    classLabelVector=[]
    index=0
    for line in arrayOLines:
        line=line.strip()
        #使用line.strip()截取掉所有的回车字符
        # strip():Return a copy of the string with the leading and
        # trailing characters removed.  If omitted or None, the
        # chars argument defaults to removing whitespace.
        #使用'\t'字符分割成一个元素列表
        listFromLine=line.split('\t')
        returnMat[index,:]=listFromLine[0:3]
        #索引-1表示最后一列元素
        transf=listFromLine[-1]
        if transf=='largeDoses':
            label=3
        elif transf=='smallDoses':
                label=2
        else: label=1
        classLabelVector.append(int(label))
        index+=1
    return returnMat,classLabelVector

#归一化数据
def autoNorm(dataset):
    maxValue=dataset.max(0)
    minValue=dataset.min(0)
    ranges=maxValue-minValue
    row_num=dataset.shape[0]
    normDataSet=zeros(shape(dataset))
    normDataSet=dataset-tile(minValue,(row_num,1))
    normDataSet=normDataSet/tile(ranges,(row_num,1))
    return normDataSet,ranges,minValue

#测试函数，测试数据从datingTestSet中选取十分之一出来
def datingClassTest():
    pickRate=0.1
    data,labels=file2matrix('datingTestSet.txt')
    normData,ranges,minVals=autoNorm(data)
    num_row=normData.shape[0]
    num_test=int(pickRate*num_row)
    countErrors=0.0
    for i in range(num_test):
        predict_label=classify0(normData[i,:],
                                    normData[num_test:num_row,:],
                                    labels[num_test:num_row],
                                    3)
        if predict_label!=labels[i]:
            countErrors+=1.0
        print "the predict result is %d,the real label is %d"\
            % (predict_label,labels[i])
    error_rate=countErrors/num_test
    print "the total error rate is :%f" %error_rate

def classifyPerson():
    train_data,train_labels=file2matrix('datingTestSet.txt')
    norm_train_data,ranges,minVals=autoNorm(train_data)
    percentTats=float(raw_input(\
        "percentage of time spent playing video games?"))
    ffMiles=float(raw_input("frequent flier miles earned per year?"))
    iceCream=float(raw_input("liters of ice cream consumed per year?"))
    input=array([ffMiles,percentTats,iceCream])
    predict_result=classify0((input-minVals),norm_train_data,train_labels,3)
    resultList=['you must hate him!','he may be a good boyfriend',
                'oh,god! he is the reason why god made a boy!']
    print resultList[predict_result]


def img2vector(filename):
    file=open(filename)
    vector=zeros((1,1024))
    for i in range(32):
        file_oneline=file.readline()
        for j in range(32):
            vector[0,i*32+j]=int(file_oneline[j])
    return vector


def handwritingClassTest():
    #首先把训练数据转化成一维向量
    #获取目录列表
    list_train_file=listdir('trainingDigits')
    num_train_digits=len(list_train_file)
    #构造一个矩阵，num_train_digits*1024大小
    train_data=zeros((num_train_digits,1024))
    train_labels=[]
    #读取每一个数据文件，存入train_data
    for i in range(num_train_digits):
        #获取每个文件的文件名
        digit_filename=list_train_file[i]
        #获取每个文件的label
        digit_value=int(digit_filename.split('_')[0])
        #将label添加到一个列表中
        train_labels.append(digit_value)
        #将每一个文件转化为一维列表并存入train_data
        train_data[i,:]=img2vector('trainingDigits/%s' % digit_filename)
    #获取测试文件列表
    list_test_file=listdir('testingDigits')
    num_test_digits=len(list_test_file)
    test_labels=[]
    err_num=0
    #预测每一个测试数据
    for i in range(num_test_digits):
        test_file_name=list_test_file[i]
        #get real labels
        test_digit_value=int(test_file_name.split('_')[0])
        test_labels.append(test_digit_value)
        #transfer first
        test_data=img2vector('testDigits/%s' % test_file_name)
        #predict
        predict_digit=classify0(test_data,train_data,train_labels,3)
        #error sum
        if predict_digit!=test_digit_value: err_num+=1;
    print "the accurancy is: %f " % (err_num/num_test_digits)


def handwritingClassTest1():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')           #load the training set
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    testFileList = listdir('testDigits')        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
        if (classifierResult != classNumStr): errorCount += 1.0
    print "\nthe total number of errors is: %d" % errorCount
    print "\nthe total error rate is: %f" % (errorCount/float(mTest))

    handwritingClassTest1()