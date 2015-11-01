# -*- encoding=utf-8 -*-

import lda
import codecs
import lda.datasets
import numpy as np
from sklearn import cluster, metrics
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class LDA_GENRE :
	# attibutes
	pos = []
	dataset = []
	posidata = []
	negadata = []
	label = []
	titles = []

	# methods
	def importData(self, posipath, negapath, pospath, titlepath) :
		with codecs.open(posipath, 'r', 'utf-8') as fo :
			posi_dataset = [line.strip().split('\t') for line in fo.readlines()]
		with codecs.open(negapath, 'r', 'utf-8') as fo :
			nega_dataset = [line.strip().split('\t') for line in fo.readlines()]
		with codecs.open(pospath, 'r', 'utf-8') as fo :
			self.pos = [line.strip() for line in fo.readlines()]
		with codecs.open(titlepath, 'r', 'utf-8') as fo :
			self.titles = [line.strip() for line in fo.readlines()]
		posi_dataset = np.array(posi_dataset, dtype=int)
		nega_dataset = np.array(nega_dataset, dtype=int)
		self.posidata = [[sum([t[3], t[22], t[23], t[28]]), \
							sum([t[5], t[18], t[34], t[37]]), \
							sum([t[2], t[4], t[23], t[45]])] for t in posi_dataset]
		self.negadata = [[sum([t[3], t[22], t[23], t[28]]), \
							sum([t[5], t[18], t[34], t[37]]), \
							sum([t[2], t[4], t[23], t[45]])] for t in nega_dataset]
		# self.dataset = posi_dataset + nega_dataset
		self.label = [1]*len(posi_dataset)
		self.label.extend([0]*len(nega_dataset))
		# print self.dataset.shape, len(posi_dataset), len(nega_dataset), len(self.label), len(self.titles)

	def ldaProcess(self) :
		ldamodel = lda.LDA(n_topics=3, n_iter=100, random_state=1).fit(self.dataset)
		kmeans = cluster.KMeans(n_clusters=2)
		kmeans.fit(ldamodel.doc_topic_)
		print kmeans.labels_
		print metrics.normalized_mutual_info_score(self.label, kmeans.labels_)

	def ploting(self) :
		# print self.posidata, self.negadata
		ax = plt.subplot(111, projection='3d')
		for cen, color in zip([self.posidata, self.negadata], 'rg') :
			ax.scatter([t[0] for t in cen], [t[1] for t in cen], [t[2] for t in cen], c=color)
		plt.show()


lda_genre = LDA_GENRE()
lda_genre.importData('../data/ldaclassifying/lda_positive', '../data/ldaclassifying/lda_negative', \
	'../data/ldaclassifying/lda_posdict', '../data/ldaclassifying/lda_title')
lda_genre.ploting()
# lda_genre.ldaProcess()