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
import codecs


class Conf :
	# attributes
	filename = 'settings.ini'

	# methods
	def readConf(self) :
		arr = []
		cf = ConfigParser.ConfigParser()
		cf.read(self.filename)
		arr.append(int(cf.get('zhihu', 'topicidx')))
		# arr.append(int(cf.get('zhihu', 'maindelta')))
		# arr.append(int(cf.get('zhihu', 'subdelta')))
		return arr

	def writeConf(self, arr) :
		cf = ConfigParser.ConfigParser()
		cf.add_section('zhihu')
		cf.set('zhihu', 'topicidx', str(arr[0]))
		# cf.set('zhihu', 'maindelta', str(arr[1]))
		# cf.set('zhihu', 'subdelta', str(arr[2]))
		cf.write(open(self.filename, 'w'))


class Zhihu :
	# attributes
	mainurl = ''
	qturl = 'http://www.zhihu.com/question/'
	urlset = []
	nqurlset = dict()
	topictree = dict()

	def __init__(self) :
		self.urlset = []
		self.nqurlset['http://www.zhihu.com/topic/19776749/questions'] = None
		self.nqurlset['http://www.zhihu.com/topic/19778317/questions'] = None
		self.nqurlset['http://www.zhihu.com/topic/19776751/questions'] = None
		self.nqurlset['http://www.zhihu.com/topic/19778298/questions'] = None
		self.nqurlset['http://www.zhihu.com/topic/19618774/questions'] = None
		self.nqurlset['http://www.zhihu.com/topic/19778287/questions'] = None
		self.nqurlset['http://www.zhihu.com/topic/19560891/questions'] = None
		qturl = 'http://www.zhihu.com/question/'

	def getQuestion(self, url) :
		content = urllib2.urlopen(url).read()
		soup = BeautifulSoup(content)
		qtdata = soup.contents[2].contents[3].contents[9]
		return qtdata
	
	def getQuestionList(self, url) :
		topic, question, count = [], [], []
		content = urllib2.urlopen(url).read()
		soup = BeautifulSoup(content)
		alltag = soup.findAll('div')
		for tag in alltag :
			if 'class' in [t[0] for t in tag.attrs] :
				if tag['class'] == 'feed-item feed-item-hook question-item' :
					selfqs = True
					alldiv = tag.findAll('div') 
					for div in alldiv :
						if 'class' in [t[0] for t in div.attrs] :
							if div['class'] == 'subtopic' :
								selfqs = False
								break
					if selfqs == True :
						alla = tag.findAll('a')
						for a in alla :
							if a['class'] == 'question_link' :
								print a['href']

	def getPageNum(self, url) :
		pageset = []
		content = urllib2.urlopen(url).read()
		soup = BeautifulSoup(content)
		alldiv = soup.findAll('div')
		for div in alldiv :
			if 'class' in [t[0] for t in div.attrs] :
				if div['class'] == 'zm-invite-pager' :
					alla = div.findAll('a')
					for a in alla :
						pageset.append(int(a['href'].split('=')[-1]))
		return max(pageset)

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

	def importURL(self, name) :
		with codecs.open(name, 'r', 'utf-8') as fo :
			for line in fo.readlines() :
				self.urlset.append(line.strip())

	def process(self) :
		self.importURL('../result/url.txt')
		conf = Conf()
		[topicidx] = conf.readConf()
		while topicidx < len(self.urlset) :
			topicurl = self.urlset[topicidx]
			maxpage = zhihu.getPageNum(topicurl)
			print maxpage
			for page in range(1, min(maxpage, 10)) :
				pageurl = topicurl + '?page=' + str(page)
				qsurlset = self.getQuestionList(pageurl)
			# topicidx += 1
			# conf.writeConf([topicidx])
			break



zhihu = Zhihu()
zhihu.process()