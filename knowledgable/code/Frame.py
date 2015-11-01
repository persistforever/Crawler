# -*- encoding = gb18030 -*-
import codecs
import numpy as np
import Filter
import Extractor
import Classifier
import TitleSimplifier
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
            data = [np.array(line.strip().split('\t')) for line in fo.readlines()]
        dataset = [t[1:] for t in data]
        self.testdataset = np.array(dataset, dtype=float)
        self.testdataset = self.normalization(self.testdataset)
        for idx in range(len(data)) :
            id = data[idx][0]
            if id in self.iddict :
                self.iddict[id].importFeatureSet(list(self.testdataset[idx]))
        print 'importing testing dataset finished ...'
            
    # ----- process methods -----
    def canImport(self, data) :
        if len(data) >= 4 :
            if len(data[0]) > 0 and len(data[1]) > 0 and len(data[2]) > 0 and len(data[3]) > 0 :
                return True
            return False
        
    def constrIdDict(self) :
        self.iddict = dict()
        for article in self.artlist :
            if article.id not in self.iddict :
                self.iddict[article.id] = article

    def filtering(self) :
        print len(self.artlist)
        filter = Filter.CollectionFilter(rate=0.5)
        self.artlist = filter.filtering(self.artlist)
        print len(self.artlist)
        filter = Filter.ContentLengthFilter(length=200)
        self.artlist = filter.filtering(self.artlist)
        print len(self.artlist)
        return self.artlist
    
    def selectKeyWord(self) : 
        self.length = len(self.artlist)
        for wordlist in [t.spcontent for t in self.artlist] :
            wordset = set([t.toString() for t in wordlist])
            for word in wordset :
                if word not in self.idfdict.keys() :
                    self.idfdict[word] = 0
                self.idfdict[word] += 1
        for word in self.idfdict :
            self.idfdict[word] = math.log(1.0 * self.length / (self.idfdict[word] + 1), math.e)
        print 'cal IDF value finished ...'
        for article in self.artlist :
            article.calTFIDF(self.idfdict)
            article.selectKeyWord(keywordnum=200)
        print 'selecting keyword finished ...'
    
    def extracting(self) :
        extractor = Extractor.KnowledgableWordExtractor()
        extractor.extractFeature(self.artlist)
        extractor = Extractor.PosExtractor()
        extractor.extractFeature(self.artlist)
        extractor = Extractor.PersonExtractor()
        extractor.extractFeature(self.artlist)
        extractor = Extractor.TokenExtractor()
        extractor.extractFeature(self.artlist)
        print 'extracting feature finished ...'

    def constrDataSet(self) :
        self.dataset, self.label = [], []
        for article in self.artlist :
            article.constrFeatureSet()
            self.dataset.append(np.array(article.featureset))
            self.label.append(article.label)
        self.dataset = np.array(self.dataset)
        self.label = np.array(self.label)
        print 'constructing dataset finished ...'

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
    
    def testClassifier(self) :
        classifier = Classifier.SVMClassifier()
        classifier.comparisonExperiments(self.traindataset, self.trainlabel)
        # classifier.plotDistribution(self.traindataset, 20)
        print 'testing classifier finished ...'
    
    def classifying(self) :
        classifier = Classifier.SVMClassifier()
        clf = classifier.training(self.traindataset[:, :], self.trainlabel)
        # clf = classifier.training(self.traindataset[:, 11:], self.trainlabel)
        print 'training classifier finished ...'
        outartlist = []
        for article in self.artlist :
            if article.label == -1 and article.featureset != [] :
                article.label = classifier.testing(np.array(article.featureset[:]), clf)
                outartlist.append(article)
        sortedlist = list(sorted(outartlist, key=lambda x: x.label[0][1], reverse=True))
        return sortedlist
        print 'testing classifier finished ...'

    def titleSimplifying(self) :
        simplifier = TitleSimplifier.TitleSimplifier()
        simplifier.simplifying(self.artlist)
        print 'simpltfying title finished ...'
            
    # ----- write methods -----
    def writeArticle(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
                fw.writelines(article.printLine().encode('gb18030') + '\n')

    def writeSimplyArticle(self, datapath) :
        with open(datapath, 'w') as fw :
            for article in self.artlist :
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
                
    def writeResult(self, datapath, artlist, num=100) :
        outartlist =artlist[0:num]
        with open(datapath, 'w') as fw :
            for article in outartlist :
                print article.label[0][1]
                fw.writelines(article.printLine().encode('gb18030') + '\n')


# ---------- use collect number to filter ----------
'''
corpus = Corpus()
corpus.importArticle('../data/4/article')
corpus.filtering()
corpus.writeArticle('../output/4/filtereddata')
'''

# ---------- construct keyword ------------
'''
corpus = Corpus()
corpus.importArticle('../data/4/article')
corpus.importSplit('../data/4/split')
corpus.importLabel('../data/4/label')
corpus.selectKeyWord()
corpus.writeKeyWord('../output/4/keyword')
'''

# ---------- construct dataset ----------
'''
corpus = Corpus()
corpus.importArticle('../output/4/filtereddata')
corpus.importSplit('../data/4/split')
corpus.importInfo('../data/4/info')
corpus.importLabel('../data/4/label')
corpus.importKeyWord('../output/4/keyword')
corpus.extracting()
corpus.constrDataSet()
corpus.writeTrainDataSet('../output/4/traindataset')
corpus.writeTestDataSet('../output/4/testdataset')
'''

# ---------- testing classifier ----------
'''
corpus = Corpus()
corpus.importTrainDataSet('../output/4/traindataset')
corpus.testClassifier()
'''

# ---------- classifying ----------
'''
corpus = Corpus()
corpus.importArticle('../output/4/filtereddata')
corpus.importTrainDataSet('../output/4/traindataset')
corpus.importTestDataSet('../output/4/testdataset')
sortedlist = corpus.classifying()
corpus.writeResult('../output/4/knowledgablearticle', sortedlist, num=100)
'''

# ---------- title simplifying ----------
'''
corpus = Corpus()
corpus.importArticle('../output/4/knowledgablearticle')
corpus.importSplit('../data/4/split')
corpus.importKeyWord('../output/4/keyword')
corpus.titleSimplifying()
corpus.writeSimplyArticle('../output/4/simplyknowledgablearticle')
'''