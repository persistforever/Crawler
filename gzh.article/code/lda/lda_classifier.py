# -*- encoding=gb18030 -*-
'''
use lda to classify
'''
import codecs 
import numpy as np
from sklearn.lda import LDA
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn import svm

charset = 'gb18030'


class LDAClassifier :
    # attributes
    posi_dataset = []
    nega_dataset = []
    train_dataset = []
    test_dataset = []

    # methods
    def __init__(self) :
        self.posi_dataset = []
        self.nega_dataset = []
        self.train_dataset = []
        self.train_label = []
        self.test_dataset = []
        self.test_label = []

    def importDataSet(self, posipath, negapath) :
        with codecs.open(posipath, 'r', charset) as fo :
            posi_dataset = [line.strip().split('\t') for line in fo.readlines()]
        with codecs.open(negapath, 'r', charset) as fo :
            nega_dataset = [line.strip().split('\t') for line in fo.readlines()]
        self.posi_dataset, self.nega_dataset = np.array(posi_dataset, dtype=float), np.array(nega_dataset, dtype=float)
        for data in self.posi_dataset :
            self.train_dataset.append(data)
        for data in self.nega_dataset :
            self.train_dataset.append(data)
        self.train_dataset = np.array(self.train_dataset)
        for data in self.posi_dataset :
            self.train_label.append(1)
        for data in self.nega_dataset :
            self.train_label.append(0)
        self.train_label = np.array(self.train_label)
        self.normalization()

    def normalization(self) :
        for col in range(len(self.train_dataset[0])) :
            mean = np.mean([t[col] for t in self.train_dataset])
            var = np.var([t[col] for t in self.train_dataset])
            for row in range(len(self.train_dataset)) :
                if var != 0 :
                    self.train_dataset[row, col] = (self.train_dataset[row, col] - mean)/var
        print self.train_dataset

    def featureSelection(self) :
        skb = SelectKBest(f_classif, k=2)
        vr_train = skb.fit_transform(self.train_dataset, self.train_label)
        # print vr_train
        print skb.pvalues_
        plt.figure()
        for c, i in zip("br", [0, 1]):
            plt.scatter(vr_train[self.train_label == i, 0], vr_train[self.train_label == i, 1], c=c)
        plt.show()

    def vrPCA(self) :
        pca = PCA(n_components=2)
        vr_train = pca.fit(self.train_dataset).transform(self.train_dataset)
        print vr_train
        plt.figure()
        for c, i in zip("br", [0, 1]):
            plt.scatter(vr_train[self.train_label == i, 0], vr_train[self.train_label == i, 1], c=c)
        plt.show()

    def classifyLDA(self) :
        print self.train_dataset
        clf = LDA(n_components=2)
        vr_train = clf.fit(self.train_dataset, self.train_label).transform(self.train_dataset)
        print vr_train
        plt.figure()
        for c, i in zip("br", [0, 1]):
            plt.scatter(vr_train[self.train_label == i], [0]*len(vr_train[self.train_label == i]), c=c)
        plt.show()


ldaclf = LDAClassifier()
ldaclf.importDataSet('data/positive', 'data/negative')
ldaclf.featureSelection()
# ldaclf.vrPCA()
# ldaclf.classifyLDA()