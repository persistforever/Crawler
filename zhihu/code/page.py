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
		arr.append(int(cf.get('zhihu', 'pageidx')))
		# arr.append(int(cf.get('zhihu', 'subdelta')))
		return arr

	def writeConf(self, arr) :
		cf = ConfigParser.ConfigParser()
		cf.add_section('zhihu')
		cf.set('zhihu', 'topicidx', str(arr[0]))
		cf.set('zhihu', 'pageidx', str(arr[1]))
		# cf.set('zhihu', 'subdelta', str(arr[2]))
		cf.write(open(self.filename, 'w'))


class Zhihu :
	# attributes
	mainurl = ''
	maindir = ''
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
		self.mainurl = 'http://www.zhihu.com'
		self.maindir = '../result/data'

	def getQuestion(self, url) :
		qtdata = ''
		content = urllib2.urlopen(url).read()
		soup = BeautifulSoup(content)
		alltag = soup.findAll('div')
		for tag in alltag :
			if 'class' in [t[0] for t in tag.attrs] :
				if tag['class'] == 'zg-wrap zu-main question-page' :
					qtdata = tag
					break
		return qtdata
	
	def getQuestionList(self, url) :
		qtlist = []
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
					allmeta = tag.findAll('meta')
					for meta in allmeta :
						if 'content' in [t[0] for t in meta.attrs] :
							if meta['itemprop'] == 'answerCount' :
								if int(meta['content']) == 0 :
									selfqs = False
									break
					if selfqs == True :
						alla = tag.findAll('a')
						for a in alla :
							qt = ''
							if a['class'] == 'question_link' :
								qtlist.append(self.mainurl + a['href'])

		return qtlist

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
		if pageset == [] :
			return 1
		else :
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

	def storeQuestion(self, topic, name, data) :
		subdir = self.maindir + '/' + str(topic)
		if not os.path.exists(subdir) :
			os.mkdir(subdir)
		filepath = subdir + '/' + str(name)
		with open(filepath, 'a+') as fw :
			fw.writelines('!!\n')
			fw.writelines(str(data))
			fw.writelines('\n')

	def importURL(self, name) :
		with codecs.open(name, 'r', 'utf-8') as fo :
			for line in fo.readlines() :
				self.urlset.append(line.strip())

	def process(self) :
		self.importURL('../result/url.txt')
		conf = Conf()
		[topicidx, pageidx] = conf.readConf()
		while topicidx < len(self.urlset) :
			topicurl = self.urlset[topicidx]
			print 'topic url is', topicurl
			if topicurl in self.nqurlset :
				topicidx += 1
				continue
			maxpage = zhihu.getPageNum(topicurl)
			print 'topic max page is', maxpage
			while pageidx < maxpage+1 :
				pageurl = topicurl + '?page=' + str(pageidx)
				print 'now page url is', pageurl
				qsurlset = []
				try:
					qsurlset = self.getQuestionList(pageurl)
				except Exception, e:
					pass
				for qsurl in qsurlset :
					print 'now question url is', qsurl
					try:
						data = self.getQuestion(qsurl)
						name = pageidx / 100
						self.storeQuestion(topicidx, name, data)
					except Exception, e:
						pass
				pageidx += 1
				conf.writeConf([topicidx, pageidx])
				if pageidx % 100 == 0 :
					time.sleep(int(random.random()*30%30)+1)
			topicidx += 1
			pageidx = 1
			conf.writeConf([topicidx, pageidx])
			time.sleep(int(random.random()*60%60)+1)



zhihu = Zhihu()
zhihu.process()
