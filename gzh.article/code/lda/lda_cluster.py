# -*- encoding=utf-8 -*-

import lda
import codecs
import lda.datasets
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn import cluster, metrics
from mpl_toolkits.mplot3d import Axes3D

class LDA_GENRE :
	# attibutes
	pos = []
	dataset = []
	label = []
	titles = []
	score = []
	nearest = []

	# methods
	def importData(self, datapath, pospath, titlepath) :
		with codecs.open(datapath, 'r', 'utf-8') as fo :
			dataset = [line.strip().split('\t') for line in fo.readlines()]
		with codecs.open(pospath, 'r', 'utf-8') as fo :
			self.pos = [line.strip() for line in fo.readlines()]
		with codecs.open(titlepath, 'r', 'gb18030') as fo :
			self.titles = [line.strip() for line in fo.readlines()]
		self.dataset = np.array(dataset, dtype=float)
		# print self.dataset

	def ldaProcess(self) :
		ldamodel = lda.LDA(n_topics=3, n_iter=100, random_state=1).fit(self.dataset)
		kmeans = cluster.KMeans(n_clusters=2)
		kmeans.fit(ldamodel.doc_topic_)
		self.label = kmeans.labels_
		self.plotCluster(kmeans.cluster_centers_, ldamodel.doc_topic_)
		for center in kmeans.cluster_centers_ :
			for idx in range(ldamodel.doc_topic_) :
				print metrics.pairwise.pairwise_distances(ldamodel.doc_topic_[i]+center)[0,1]

	def plotSaving(self) :
		# ax = plt.subplot(111, projection='3d')
		for idx in range(len(self.dataset[0])) :
			fig = plt.figure()
			if len([t[idx] for t in self.dataset if t[idx] <= 500 and t[idx] > 0]) > 1 :
				plt.hist([t[idx] for t in self.dataset if t[idx] <= 500 and t[idx] > 0], bins=50)
			print 'fig', idx
			fig.savefig('../output/distribution/' + str(idx+1) + '.png', format='png')  
		# plt.show()

	def plotConj(self) :
		# ax = plt.subplot(111, projection='3d')
		h, x, y, p = plt.hist2d([t[5] for t in self.dataset if t[5] < 500 and t[15] < 500], \
			[t[15] for t in self.dataset if t[5] < 500 and t[15] < 500], bins=70)
		plt.imshow(h)
		plt.show()

	def writeTitle(self, posipath, negapath) :
		posititle = [self.titles[idx] for idx in range(len(self.titles)) if self.label[idx] == 1]
		negatitle = [self.titles[idx] for idx in range(len(self.titles)) if self.label[idx] == 0]
		with open(posipath, 'w') as fw :
			for title in posititle :
				fw.writelines(title.encode('utf-8') + '\n')
		with open(negapath, 'w') as fw :
			for title in negatitle :
				fw.writelines(title.encode('utf-8') + '\n')


lda_genre = LDA_GENRE()
lda_genre.importData('../data/ldaclassifying/lda_dataset', '../data/ldaclassifying/lda_dataset', '../data/ldaclassifying/lda_dataset')
lda_genre.plotSaving()
# lda_genre.ldaProcess()
# lda_genre.writeTitle('../output/positive', '../output/negative')