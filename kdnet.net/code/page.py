# -*- encoding=utf-8 -*-
'''
http://www.zhihu.com/topic/19776749/questions
according root topic to catch each question and store as a
'''

import urllib2
from BeautifulSoup import BeautifulSoup, Tag
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
	homepage = 'http://club.kdnet.net/index.asp'
	mainurl = 'http://club.kdnet.net'
	maindir = 'data'

	def urlOpen(self, url) :
		content = ''
		with codecs.open(url, 'r', 'gb18030') as fo :
			for line in fo.readlines() :
				content += line.strip().encode('utf-8') + '\n'
		return content

	def getQAPair(self, url) :
		qalist = []
		# content = urllib2.urlopen(url).read()
		content = self.urlOpen(url)
		soup = BeautifulSoup(content)
		alltags = soup.findAll(True)
		for tag in alltags :
			if tag.name == 'div' :
				if 'class' in [t[0] for t in tag.attrs] :
					if tag['class'] == 'reply-box' or tag['class'] == 'reply-box nobg' :
						if isinstance((tag.contents[3].contents[1].contents[1].contents[0]), Tag) == True :
							qalist.append([tag.contents[3].contents[1].contents[1].contents[0].contents[0].contents[1], 
								tag.contents[3].contents[1].contents[1].contents[1]])
		return qalist
	
	def getQuestionList(self, url) :
		qslist = []
		# content = urllib2.urlopen(url).read()
		content = self.urlOpen(url)
		soup = BeautifulSoup(content)
		alltags = soup.findAll(True)
		for tag in alltags :
			if tag.name == 'td' and tag['class'] == 'subject' :
				href, page = '', 1
				allspan = tag.findAll('span')
				for span in allspan :
					if span['class'] == 'f14px' :
						alla = span.findAll('a')
						for a in alla :
							href = a['href']
					elif span['class'] == 'c-alarm' :
						alla = span.findAll('a')
						for a in alla :
							page = int(a.contents[0])
				qslist.append([href, page])
		return qslist

	def getTopicList(self, url) :
		topiclist = []
		content = urllib2.urlopen(url).read()
		# content = self.urlOpen(url)
		soup = BeautifulSoup(content)
		alltags = soup.findAll(True)
		for tag in alltags :
			if tag.name == 'h2':
				href, page = '', ''
				allspan = tag.findAll('span')
				for span in allspan :
					print span
					alla = span.findAll('a')
					for a in alla :
						href = self.mainurl + a['href']
				if len(tag.contents) >= 3 :
					print tag.contents[3]
					page = int(tag.contents[3].split(u'\xd6\xf7\xcc\xe2\xa3\xba')[1].split(u')')[0].strip())/50+1
					if href not in topiclist :
						topiclist.append([href, page])
		return topiclist

	def storeQAList(self, storepath, qalist) :
		with codecs.open(storepath, 'w') as fw :
			for q, a in qalist :
				fw.writelines('!!\n')
				fw.writelines('KNOWLEDGE\n')
				fw.writelines('QT' + str(q) + '\n')
				fw.writelines('AS' + str(a) + '\n')
				fw.writelines('SC1.0\n')
				fw.writelines('KNOWLEDGE\n')

	def storeTopicList(self, storepath, topiclist) :
		with codecs.open(storepath, 'w') as fw :
			for topicurl, topicpage in topiclist :
				fw.writelines(str(topicurl) + '\t' + str(topicpage) + '\n')

	def process(self) :
		topiclist = self.getTopicList(self.homepage)
		topiclistpath = self.maindir + '/topiclist'
		self.storeTopicList(topiclistpath, topiclist)
		'''
		for topicurl, topicpage in topiclist :
			topicid = topicurl.split('=')[-1]
			storeqalist = []
			for page in range(1, topicpage) : # every topic
				qslisturl = topicurl + '&page=' + str(page)
				qslist = self.getQuestionList(qslisturl)
				for qsurl, qspage in qslist : # every question
					for p in range(1, qspage) :
						pairurl = qsurl + '&page=' + str(p)
						qalist = self.getQAPair(pairurl)
						storeqalist.extend(qalist)
				if page % 100 == 0 :
					topicdir = self.maindir + '/' + topicid
					storepath = topicdir + '/' + page
					self.storeQAList(storepath, storeqalist)'''



kdnet = KDNet()
# kdnet = KDNet('../input/topic.txt')
kdnet.process()