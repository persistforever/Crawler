# -*- encoding=gb18030 -*-
'''
use lda to classify
'''
import codecs 
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, cross_validation
from sklearn.cross_validation import KFold

charset = 'gb18030'


class Classifier :
    # attributes
    posi_dataset = []
    nega_dataset = []
    dataset = []
    label = []
    selected_feature = []

    # methods
    def __init__(self) :
        self.posi_dataset = []
        self.nega_dataset = []
        self.dataset = []

    def importDataSet(self, posipath, negapath) :
        self.posi_dataset, self.nega_dataset, self.dataset, self.label = [], [], [], []
        with codecs.open(posipath, 'r', charset) as fo :
            posi_dataset = [line.strip().split('\t') for line in fo.readlines()]
        with codecs.open(negapath, 'r', charset) as fo :
            nega_dataset = [line.strip().split('\t') for line in fo.readlines()]
        self.posi_dataset, self.nega_dataset = np.array(posi_dataset, dtype=float), np.array(nega_dataset, dtype=float)
        for data in self.posi_dataset :
            self.dataset.append(data)
        for data in self.nega_dataset :
            self.dataset.append(data)
        self.dataset = np.array(self.dataset)
        for data in self.posi_dataset :
            self.label.append(1)
        for data in self.nega_dataset :
            self.label.append(0)
        self.label = np.array(self.label)

    def svmClassifier(self, train_dataset, train_label, test_dataset) :
    	clf = svm.SVC(kernel='linear', degree=3)
    	clf.fit(train_dataset, train_label)
    	test_class = []
    	for data in test_dataset :
    		test_class.append(clf.predict(data))
    	return test_class

    def randomClassifier(self, train_dataset, train_label, test_dataset) :
        test_class = []
        for data in test_dataset :
            test_class.append(round(random.random()))
        return test_class

    def evaluation(self, test_class, test_label) :
    	acnum = 0
    	for idx in range(len(test_class)) :
    		if test_class[idx] == test_label[idx] :
    			acnum += 1
    	if len(test_class) == 0 :
    		accurancy = 0.0
    	else :
    		accurancy = 1.0 * acnum / len(test_class)
    	return accurancy

    def crossValidation(self, classifier, dataset, label, n_folds=4) :
        kf = KFold(len(dataset), n_folds=n_folds, shuffle=True)
        accurancy = []
        for train, test in kf :
            train_dataset, test_dataset, train_label, test_label = dataset[train], dataset[test], label[train], label[test]
            test_class = np.array(classifier(train_dataset, train_label, test_dataset))
            accurancy.append(self.evaluation(test_class, test_label))
        return np.mean(accurancy)

    def featureSelection(self, classifier, n_folds=4) :
        x = range(0, len(self.dataset))
        condidate = range(0, len(self.dataset[0]))
        maxacc = 0.0
        for idx in range(0, len(self.dataset[0])) :
            y = condidate
            data = []
            for i in range(len(self.dataset)) :
                line = []
                for j in condidate :
                    line.append(self.dataset[i, j])
                data.append(line)
            data = np.array(data)
            accurancy = clf.crossValidation(classifier, data, self.label, n_folds=n_folds)
            if accurancy < maxacc :
                condidate.remove(idx)
            else :
                maxacc = accurancy
        self.selected_feature = condidate
        return maxacc

    def comparisonExperiments(self) :
        experiments = []
        for n in range(2, 11) :
            experiment = []
            self.importDataSet('../data/positive2', '../data/negative2')
            # print 'n_folds', n, ' + no-tfidf + no-fs + random'
            experiment.append(clf.crossValidation(clf.randomClassifier, clf.dataset, clf.label, n_folds=n))
            # print 'n_folds', n, ' + no-tfidf + no-fs + svm'
            experiment.append(clf.crossValidation(clf.svmClassifier, clf.dataset, clf.label, n_folds=n))
            # print 'n_folds', n, ' + no-tfidf + fs + svm'
            experiment.append(clf.featureSelection(clf.svmClassifier, n_folds=n))
            self.importDataSet('../data/positive2_tfidf', '../data/negative2_tfidf')
            # print 'n_folds', n, ' + tfidf + no-fs + svm'
            experiment.append(clf.crossValidation(clf.svmClassifier, clf.dataset, clf.label, n_folds=n))
            # print 'n_folds', n, ' + tfidf + fs + svm'2
            experiment.append(clf.featureSelection(clf.svmClassifier, n_folds=n))
            print experiment
            experiments.append(experiment)
        color = ['yo--', 'ro--', 'go--', 'bo--', 'mo--']
        p = []
        for idx in range(len(experiments[0])) :
            p.append(plt.plot(range(2, 11), [t[idx] for t in experiments], color[idx]))
        plt.title('different model evaluation')
        plt.xlabel('# folds of cross validation')
        plt.ylabel('accurancy')
        plt.axis([1, 11, 0.4, 0.9])
        plt.legend((p[0][0], p[1][0], p[2][0], p[3][0], p[4][0]), ('random', 'svm', 'fs+svm', 'tfidf+svm', 'tfidf+fs+svm'), 'best', numpoints=1)
        plt.show()


clf = Classifier()
clf.comparisonExperiments()