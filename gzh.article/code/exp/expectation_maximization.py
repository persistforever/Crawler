# -*- encoding=utf-8 -*-
'''
use expectation maximization to solute three coins problem
'''

import random
import math
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
	def __init__(self, pi=0.5, p=0.4, q=0.6, N=100) :
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

	def expectationMaximization(self) :
		# initialization
		self.pi, self.p, self.q = 0.5, 0.5, 0.5
		# EM interation
		for iter in range(0, 10) :
			# E step
			posterior = []
			for i in range(0, self.N) :
				pz1 = 1.0 * self.pi * (self.p**self.w[i]) * ((1.0-self.p)**(1-self.w[i]))
				pz0 = 1.0 * (1.0-self.pi) * (self.q**self.w[i]) * ((1.0-self.q)**(1-self.w[i]))
				mu = 1.0 * pz1 / (pz1 + pz0)
				rate = random.random()*(pz1 + pz0)
				if rate < pz1 :
					self.z[i] = 1
				else :
					self.z[i] = 0
				posterior.append(mu)
			print posterior
			# print self.z
			# M step
			self.pi = 1.0 * sum([posterior[i]*self.z[i] for i in range(0, len(self.w))]) \
				/ sum([1+2*posterior[i]*self.z[i]-posterior[i]-self.z[i] for i in range(0, len(self.w))])
			self.p = 1.0 * sum([posterior[i]*self.w[i]*self.z[i] for i in range(0, len(self.w))]) \
				/ sum([posterior[i]*self.z[i] for i in range(0, len(self.w))])
			self.q = 1.0 * sum([(1.0-posterior[i])*self.w[i]*(1-self.z[i]) for i in range(0, len(self.w))]) \
				/ sum([(1-posterior[i])*(1-self.z[i]) for i in range(0, len(self.w))])
			ll = sum( [(posterior[i]*self.z[i]*math.log(self.pi*self.p**(self.w[i])*(1-self.p)**(1-self.w[i])/posterior[i]) + \
				(1-posterior[i])*(1-self.z[i])*math.log((1-self.pi)*self.q**(self.w[i])*(1-self.q)**(1-self.w[i])/(1-posterior[i]))) for i in range(len(self.w))])
			print self.pi, self.p, self.q, ll

	def gibbsSampling(self) :
		n = [[0, 0], [0, 0]]
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
		for iter in range(0, 100) :
			for i in range(0, self.N) :
				n[self.z[i]][self.w[i]] -= 1
				m = [sum(n[0]), sum(n[1])]
				pi = 1.0 * m[1] / (sum(m) + 1)
				p = 1.0 * n[1][1] / (sum(n[1]) + 1)
				q = 1.0 * n[0][1] / (sum(n[0]) + 1)
				pz1 = pi * (p ** self.w[i]) * ((1 - p) ** (1-self.w[i]))
				pz0 = (1-pi) * (q ** self.w[i]) * ((1 - q) ** (1-self.w[i]))
				rate = (pz1 + pz0)*random.random()
				if rate <= pz1 :
					self.z[i] = 1
				else :
					self.z[i] = 0
				n[self.z[i]][self.w[i]] += 1
		self.pi = 1.0 * m[1] / (sum(m) + 1)
		self.p = 1.0 * n[1][1] / (sum(n[1]) + 1)
		self.q = 1.0 * n[0][1] / (sum(n[0]) + 1)	
		print n, m
		print self.pi, self.p, self.q



# normal = Normal()
# normal.gibbsSampling()
threeCoins = ThreeCoins(N=10)
threeCoins.constrObservation()
threeCoins.expectationMaximization()
# threeCoins.gibbsSampling()