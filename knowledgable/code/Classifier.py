# -*- encoding = utf-8 -*-
'''
use lda to classify
'''
import codecs 
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, cross_validation
from sklearn.cross_validation import KFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression

class SVMClassifier :
    # attributes
    kernel = ''

    # ---------- init -----------
    def __init__(self, kernel='linear') :
        self.kernel = kernel

    # ---------- training and test ----------
    def training(self, dataset, label) :
        clf = svm.SVC(kernel=self.kernel, probability=True)
        clf.fit(dataset, label)
        return clf

    def testing(self, data, clf) :
        return clf.predict_proba(data)

    # ---------- process methods ----------
    def crossValidation(self, dataset, label, n_folds=4) :
        kf = KFold(len(dataset), n_folds=n_folds, shuffle=True)
        accurancy = []
        for train, test in kf :
            train_dataset, test_dataset, train_label, test_label = dataset[train], dataset[test], label[train], label[test]
            clf = self.training(train_dataset, train_label)
            test_class = []
            for data in test_dataset :
                test_class.append(clf.predict(data))
            test_class = np.array(test_class)
            accurancy.append(self.evaluation(test_class, test_label))
        return np.mean(accurancy)

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

    def comparisonExperiments(self, dataset, label) :
        experiments = []
        for n in range(2, 6) :
            experiment = []
            # print 'n_folds', n, ' + no-tfidf + no-fs + random'
            # experiment.append(self.crossValidation(self.randomClassifier, dataset, label, n_folds=n))
            # print 'n_folds', n, ' + tfidf + no-fs + svm'
            experiment.append(self.crossValidation(dataset[:, 0:6], label, n_folds=n))
            experiment.append(self.crossValidation(dataset[:, 6:12], label, n_folds=n))
            experiment.append(self.crossValidation(dataset[:, 12:17], label, n_folds=n))
            experiment.append(self.crossValidation(dataset[:, 17:], label, n_folds=n))
            experiment.append(self.crossValidation(dataset[:, :], label, n_folds=n))
            print experiment
            experiments.append(experiment)
        color = ['yo--', 'ro--', 'go--', 'bo--', 'mo--']
        legend = ['token', 'info', 'word', 'pos', 'all']
        p = []
        for idx in range(len(experiments[0])) :
            p.append(plt.plot(range(2, 6), [t[idx] for t in experiments], color[idx]))
        plt.title('different model evaluation')
        plt.xlabel('# folds of cross validation')
        plt.ylabel('accurancy')
        # plt.axis([1, 11, 0.6, 0.8])
        plt.legend(([t[0] for t in p]), (legend[0: len(experiments[0])]), 'best', numpoints=1)
        plt.show()

    def plotDistribution(self, dataset, col) :
        plt.hist(dataset[:, col], bins=20)
        plt.title('distribution')
        plt.xlabel('value')
        plt.ylabel('frequence')
        plt.show()