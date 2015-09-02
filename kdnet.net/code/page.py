# -*- encoding=utf-8 -*-
'''
http://www.zhihu.com/topic/19776749/questions
according root topic to catch each question and store as a
'''

import urllib2
from BeautifulSoup import BeautifulSoup
import time
import os
import random
import sys
import ConfigParser


class Conf :
	# attributes
	filename = 'settings.ini'

	# methods
	def readConf(self) :
		arr = []
		cf = ConfigParser.ConfigParser()
		cf.read(self.filename)
		arr.append(int(cf.get('zhihu', 'start')))
		arr.append(int(cf.get('zhihu', 'maindelta')))
		arr.append(int(cf.get('zhihu', 'subdelta')))
		return arr

	def writeConf(self, arr) :
		cf = ConfigParser.ConfigParser()
		cf.add_section('zhihu')
		cf.set('zhihu', 'start', str(arr[0]))
		cf.set('zhihu', 'maindelta', str(arr[1]))
		cf.set('zhihu', 'subdelta', str(arr[2]))
		cf.write(open(self.filename, 'w'))


class KDNet :
	# attributes
	mainurl = ''
	qturl = 'http://www.zhihu.com/question/'
	topictree = dict()

	def __init__(self, mainurl) :
		self.mainurl = mainurl
		self.topictree['19776749'] = []

	def getQuestion(self, url) :
		content = urllib2.urlopen(url).read()
		soup = BeautifulSoup(content)
		qtdata = soup.contents[2].contents[3].contents[47].contents[3].findAll('div')
		for div in qtdata :
			if 'class' in [t[0] for t in div.attrs] :
				if div['class'] == 'reply-box' :
					if div.contents[3].contents[1]['class'] == 'replycont-box-r' :
						print div.contents[3].contents[1].contents[1].contents[0].encode('gb18030')
		return qtdata
	
	def getQuestionList(self, url) :
		topic, question, count = [], [], []
		content = urllib2.urlopen(url).read()
		soup = BeautifulSoup(content)
		alist = soup.contents[2].contents[3].contents[5].contents[1].contents[1].contents[5].contents[1].findAll('a')
		metalist = soup.contents[2].contents[3].contents[5].contents[1].contents[1].contents[5].contents[1].findAll('meta')
		t = '19776749'
		qnum = 0
		for i in range(len(alist)) :
			if alist[i]['href'].split('/')[-2] == 'question' :
				self.topictree[t].append([alist[i]['href'].split('/')[-1], int(metalist[qnum*2]['content'])])
				t = '19776749'
				qnum += 1
			else :
				t = alist[i]['href'].split('/')[-1]
				if t not in self.topictree :
					self.topictree[t] = []

	def getPageList(self, startpage, maxpage) :
		for page in range(startpage, startpage + maxpage) :
			try:
				self.getQuestionList(self.mainurl + '?page=' +str(page))
				print 'read page', page, 'finished ...'
			except Exception, e:
				pass
			if (page + 1) % 100 == 0 :
				time.sleep(int(random.random()*100%30))

	def storeTopic(self, maindir) :
		num = 0
		for topic in self.topictree :
			subdir = maindir + '/' + topic
			if not os.path.exists(subdir) :
				os.mkdir(subdir)
			for qt, count in self.topictree[topic] :
				if count != 0 :
					try:
						filepath = subdir + '/' + qt + '.txt'
						qtdata = self.getQuestion(self.qturl + qt)
						num += 1
						with open(filepath, 'w') as fw :
							fw.write(str(qtdata))
					except Exception, e:
						pass
				if (num + 1) % 1000 == 0 :
					time.sleep(int(random.random()*100%30))
			print 'write topic ', topic, 'finished ...' 

	def process(self, startpage, deltapage, subdelta) :
		page = startpage
		while page < (startpage + deltapage) :
			zhihu.getPageList(startpage, subdelta)
			print zhihu.topictree
			zhihu.storeTopic('E://data/zhihu')
			page += subdelta




kdnet = KDNet('http://club.kdnet.net/dispbbs.asp')
kdnet.getQuestion('http://club.kdnet.net/dispbbs.asp?id=11139095&boardid=1')