# -*- encoding=utf-8 -*-
'''
use gibbs sampling to solute three coins problem
'''

import random
import numpy as np
import matplotlib.pyplot as plt


class ThreeCoins :
	# attibutes
	pi = 0.0
	p = 0.0
	q = 0.0
	n = 0
	w = []
	z = []

	# methods
	def __init__(self, pi=0.5, p=0.5, q=0.5, N=100) :
		self.pi = pi
		self.p = p
		self.q = q
		self.N = N
		self.w = []
		self.z = []

	def constrObservation(self) :
		for i in range(0, self.N) :
			self.z.append(0)
			t1 = random.random()
			t2 = random.random()
			if t1 <= self.pi :
				if t2 <= self.p :
					self.w.append(1)
				else :
					self.w.append(0)
			else :
				if t2 <= self.q :
					self.w.append(1)
				else :
					self.w.append(0)
		print self.w

	def gibbsSampling(self) :
		n = [[0, 0], [0, 0]]
		m = [sum(n[0]), sum(n[1])]
		# initialization
		for i in range(0, self.N) :
			t = random.random()
			if t <= 0.5 :
				self.z[i] = 1
			else :
				self.z[i] = 0
			n[self.z[i]][self.w[i]] += 1
		m = [sum(n[0]), sum(n[1])]
		print n, m
		# sampling
		for iter in range(0, 500) :
			for i in range(0, self.N) :
				n[self.z[i]][self.w[i]] -= 1
				m = [sum(n[0]), sum(n[1])]
				pi = 1.0 * m[1] / (sum(m) + 1)
				p = 1.0 * n[1][1] / (sum(n[1]) + 1)
				q = 1.0 * n[0][1] / (sum(n[0]) + 1)
				# print n, pi, p, q
				pz1 = pi * (p ** self.w[i]) * ((1 - p) ** (1-self.w[i]))
				pz0 = (1-pi) * (q ** self.w[i]) * ((1 - q) ** (1-self.w[i]))
				rate = (pz1 + pz0)*random.random()
				# print rate
				if rate <= pz1 :
					self.z[i] = 1
				else :
					self.z[i] = 0
				# print self.z[i], self.w[i]
				n[self.z[i]][self.w[i]] += 1
				# print '-'*100
		self.pi = 1.0 * m[1] / (sum(m) + 1)
		self.p = 1.0 * n[1][1] / (sum(n[1]) + 1)
		self.q = 1.0 * n[0][1] / (sum(n[0]) + 1)	
		print n, m
		print self.pi, self.p, self.q


class Normal :
	# attibutes
	mu = []
	sigma = []
	rou = 0.0

	# methods
	def __init__(self, mu=[0.0, 0.0], sigma=[0.0, 0.0], rou=0.5) :
		self.mu = mu
		self.sigma = sigma
		self.rou = rou

	def constrObservation(self) :
		pass

	def gibbsSampling(self) :
		theta = [0, 0]
		result = []
		for i in range(0, 500) :
			loc = self.rou*theta[1]
			scale = 1-self.rou**2
			theta[0] = np.random.normal(loc=loc, scale=scale, size=1)
			loc = self.rou*theta[0]
			scale = 1-self.rou**2
			theta[1] = np.random.normal(loc=loc, scale=scale, size=1)
			result.append([theta[0], theta[1]])
		self.mu = [np.mean([t[0] for t in result]), np.mean([t[1] for t in result])]
		self.sigma = [np.var([t[0] for t in result]), np.var([t[1] for t in result])]
		print self.mu, self.sigma
		plt.plot([t[0] for t in result], [t[1] for t in result], 'ro')
		plt.show()


# normal = Normal()
# normal.gibbsSampling()
threeCoins = ThreeCoins(N=1000)
threeCoins.constrObservation()
threeCoins.gibbsSampling()