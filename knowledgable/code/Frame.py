# -*- encoding = gb18030 -*-
import codecs
import numpy as np
import Filter
import Extractor
import Classifier
import Simplifier
import math
from BasicClass import Article


class Corpus :
    # attributes
    artlist = []
    iddict = dict()
    seed = []
    wordbag = dict()
    wordcount = dict()
    idfdict = dict() # word idf dictionary
    traindataset = [] # train dataset
    trainlabel = [] # train label
    testdataset = [] # test data
    testlabel = [] # test label

    # ----- import methods -----
    def importArticle(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            datalist = [line.strip().split('\t') for line in fo.readlines()]
        for data in datalist :
            article = Article(data)
            self.artlist.append(article)
        self.constrIdDict()
        print 'importing article finished ...'

    def importInfo(self, infopath) :
        with codecs.open(infopath, 'r', 'gb18030') as fo :
            infolist = [line.strip().split('\t') for line in fo.readlines()]
        print 'importing info started ...'
        for data in infolist :
            id = data[0]
            if id in self.iddict :
                self.iddict[id].importInfo(data)
        print 'importing info finished ...'

    def importSplit(self, splitpath) :
        with codecs.open(splitpath, 'r', 'gb18030') as fo :
            splitlist = [line.strip().split('\t') for line in fo.readlines()]
        for data in splitlist :
            id = data[0]
            if id in self.iddict :
                self.iddict[id].importSplit(data)
        print 'importing split finished ...'
            
    def importLabel(self, labelpath) :
        with codecs.open(labelpath, 'r', 'gb18030') as fo :
            labellist = [line.strip().split('\t') for line in fo.readlines()]
        for data in labellist :
            id = data[0]
            if id in self.iddict :
                self.iddict[id].importLabel(data)
        print 'importing label finished ...'
            
    def importKeyWord(self, keywordpath) :
        with codecs.open(keywordpath, 'r', 'gb18030') as fo :
            keywordlist = [line.strip().split('\t') for line in fo.readlines()]
        for data in keywordlist :
            id = data[0]
            if id in self.iddict :
                self.iddict[id].importKeyWord(data)
        print 'importing keyword finished ...'
            
    def importTrainDataSet(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            data = [np.array(line.strip().split('\t')) for line in fo.readlines()]
        datasetlist = [t[0:-1] for t in data]
        labellist = [t[-1] for t in data]
        self.traindataset = np.array(datasetlist, dtype=float)
        self.traindataset = self.normalization(self.traindataset)
        self.trainlabel = np.array(labellist, dtype=float)
        print 'importing training dataset finished ...'
            
    def importTestDataSet(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            datalist = [np.array(line.strip().split('\t')) for line in fo.readlines()]
        dataset = [t[1:] for t in datalist]
        testdataset = np.array(dataset, dtype=float)
        testdataset = self.normalization(testdataset)
        self.testdataset = dict()
        for idx in range(len(datalist)) :
            id = datalist[idx][0]
            if id not in self.testdataset :
                self.testdataset[id] = list(testdataset[idx])
        print 'importing testing dataset finished ...'
        
    def importKnowledgable(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            datalist = [line.strip() for line in fo.readlines()]
        for id in datalist :
            if id in self.iddict :
                self.iddict[id].label = 1
        print 'importing knowledgable finished ...'
        
    def importSubTitle(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            splitlist = [line.strip().split('\t') for line in fo.readlines()]
        for data in splitlist :
            id = data[0]
            if id in self.iddict :
                self.iddict[id].importSubTitle(data)
        print 'importing subtitle finished ...'
            
    # ----- process methods -----
    def constrIdDict(self) :
        self.iddict = dict()
        for article in self.artlist :
            if article.id not in self.iddict :
                self.iddict[article.id] = article
    
    def testClassifier(self) :
        classifier = Classifier.SVMClassifier()
        classifier.comparisonExperiments(self.traindataset, self.trainlabel)
        # classifier.plotDistribution(self.traindataset, 20)
        print 'extracting feature finished ...'

    def normalization(self, dataset) :
        for col in range(dataset.shape[1]) :
            maximum = max(dataset[:, col])
            minimum = min(dataset[:, col])
            for row in range(dataset.shape[0]) :
                if maximum - minimum == 0 :
                    dataset[row, col] = 0.0
                else :
                    dataset[row, col] = 1.0 * (maximum - dataset[row, col]) / (maximum - minimum)
        return dataset
    
    def classifying(self) :
        classifier = Classifier.SVMClassifier()
        clf = classifier.training(self.traindataset[:, :], self.trainlabel)
        # clf = classifier.training(self.traindataset[:, 11:], self.trainlabel)
        print 'training classifier finished ...'
        self.testlabel = {}.fromkeys(self.testdataset.keys(), -1)
        for artid in self.testdataset :
        	self.testlabel[artid] = classifier.testing(np.array(self.testdataset[artid][0:]).reshape(1, -1), clf)
        	self.testlabel[artid] = self.testlabel[artid][0][1]
        sortedlist = list(sorted(self.testlabel.iteritems(), key=lambda x: x[1], reverse=True))
        return sortedlist
        print 'testing classifier finished ...'

    def titleSimplifying(self) :
        artlist = []
        for article in self.artlist :
            if article.label == 1 :
                artlist.append(article)
        simplifier = Simplifier.TitleSimplifier()
        # simplifier.featureSimplifying(artlist)
        simplifier.modelSimplifying(artlist)
        print 'simpltfying title finished ...'
            
    # ----- write methods -----
    def writeLine(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                fw.writelines(article.printLine().encode('gb18030') + '\n')
                
    def writeArticle(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                fw.writelines(article.printArticle().encode('gb18030') + '\n')
                
    def writeInfo(self, infopath) :
        with open(infopath, 'w') as fw :
            for article in self.artlist :
                fw.writelines(article.printInfo().encode('gb18030') + '\n')
                
    def writeSplit(self, splitpath) :
        with open(splitpath, 'w') as fw :
            for article in self.artlist :
                fw.writelines(article.printSplit().encode('gb18030') + '\n')

    def writeSimplyArticle(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                if article.label == 1 :
                    fw.writelines(article.printSimplyLine().encode('gb18030') + '\n')
                
    def writeKeyWord(self, keywordpath) :
        with open(keywordpath, 'w') as fw :
            for article in self.artlist :
                fw.writelines(article.printId().encode('gb18030')  + '\t' + article.printKeyWord().encode('gb18030') + '\n')
                
    def writeTrainDataSet(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                if article.printLabel() != '-1' :
                    fw.writelines(article.printFeatureSet().encode('gb18030') + article.printLabel().encode('gb18030') + '\n')
                
    def writeTestDataSet(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                if article.printLabel() == '-1' :
                    fw.writelines(article.printId().encode('gb18030') + '\t' + article.printFeatureSet().encode('gb18030') + '\n')
                    
    def writeSplitTitle(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                if article.label == 1 :
                    for sub in article.subtitle :
                        fw.writelines(article.printId().encode('gb18030') + '\t' + sub.encode('gb18030') + '\n')
                
    def writeKnowledgableArticle(self, datapath, artlist, rate=0.1) :
        outnum = int(rate * len(artlist))
        outartlist =artlist[0: (outnum+1)]
        with open(datapath, 'w') as fw :
            for article in outartlist :
                fw.writelines(article[0].encode('gb18030') + '\n')


# ---------- FilePath : list of file path ----------
class FilePath :
    # attributes
    maindir = 'E://file/knowledgable/'
    
    # methods
    def getInputArticle(self, type) :
        return self.maindir + 'input/' + type + '/article'
    
    def getInputInfo(self, type) :
        return self.maindir + 'input/' + type + '/info'
    
    def getInputTraindataset(self, type) :
        return self.maindir + 'input/' + type + '/traindataset'
    
    def getOuputOrigindata(self, type) :
        return self.maindir + 'output/' + type + '/origindata'
    
    def getOutputArticle(self, type) :
        return self.maindir + 'output/' + type + '/article'
    
    def getOutputInfo(self, type) :
        return self.maindir + 'output/' + type + '/info'
    
    def getOutputSplit(self, type) :
        return self.maindir + 'output/' + type + '/split'
    
    def getOutputKeyword(self, type) :
        return self.maindir + 'output/' + type + '/keyword'
    
    def getOutputTestdataset(self, type) :
        return self.maindir + 'output/' + type + '/testdataset'
    
    def getOutputKnowledgablearticle(self, type) :
        return self.maindir + 'output/' + type + '/knowledgablearticle'
    
    def getOutputSubtitle(self, type) :
        return self.maindir + 'output/' + type + '/subtitle'
    
    def getOutputSimplyArticle(self, type) :
        return self.maindir + 'output/' + type + '/simplyknowledgablearticle'
    

# ---------- classifying ----------
def classifying(type) :
	corpus = Corpus()
	filepath = FilePath()
	corpus.importTrainDataSet(filepath.getInputTraindataset(type))
	corpus.importTestDataSet(filepath.getOutputTestdataset(type))
	sortedlist = corpus.classifying()
	corpus.writeKnowledgableArticle(filepath.getOutputKnowledgablearticle(type), sortedlist, rate=0.2)

# ---------- title simplifying ----------
def titleSimplifying(type) :
	corpus = Corpus()
	filepath = FilePath()
	corpus.importArticle(filepath.getOutputArticle(type))
	corpus.importKnowledgable(filepath.getOutputKnowledgablearticle(type))
	corpus.importSubTitle(filepath.getOutputSubtitle(type))
	corpus.importKeyWord(filepath.getOutputKeyword(type))
	corpus.titleSimplifying()
	corpus.writeSimplyArticle(filepath.getOutputSimplyArticle(type))


# ---------- MAIN ----------
type = '4'
# classifying(type)
titleSimplifying(type)