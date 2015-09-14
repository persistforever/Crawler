# -*- encoding=utf-8 -*-
'''
http://www.zhihu.com/topic/19776749/questions
according root topic to catch each question and store as a
'''

import urllib2
<<<<<<< HEAD
from BeautifulSoup import BeautifulSoup
=======
from BeautifulSoup import BeautifulSoup, Tag, NavigableString
>>>>>>> dfbd900696f6ace3b761ff13e151b6920a154c40
import time
import os
import random
import sys
import ConfigParser
<<<<<<< HEAD
=======
import codecs
>>>>>>> dfbd900696f6ace3b761ff13e151b6920a154c40


class Conf :
	# attributes
	filename = 'settings.ini'

	# methods
	def readConf(self) :
		arr = []
		cf = ConfigParser.ConfigParser()
		cf.read(self.filename)
<<<<<<< HEAD
		arr.append(int(cf.get('zhihu', 'start')))
		arr.append(int(cf.get('zhihu', 'maindelta')))
		arr.append(int(cf.get('zhihu', 'subdelta')))
=======
		arr.append(int(cf.get('kdnet', 'topic')))
		arr.append(int(cf.get('kdnet', 'page')))
>>>>>>> dfbd900696f6ace3b761ff13e151b6920a154c40
		return arr

	def writeConf(self, arr) :
		cf = ConfigParser.ConfigParser()
<<<<<<< HEAD
		cf.add_section('zhihu')
		cf.set('zhihu', 'start', str(arr[0]))
		cf.set('zhihu', 'maindelta', str(arr[1]))
		cf.set('zhihu', 'subdelta', str(arr[2]))
=======
		cf.set('kdnet', 'topic', str(arr[0]))
		cf.set('kdnet', 'page', str(arr[1]))
>>>>>>> dfbd900696f6ace3b761ff13e151b6920a154c40
		cf.write(open(self.filename, 'w'))


class KDNet :
	# attributes
<<<<<<< HEAD
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
						print div.contents[3].contents[1].contents[1].contents[0]
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
=======
	homepage = 'http://club.kdnet.net/index.asp'
	mainurl = 'http://club.kdnet.net'
	maindir = 'data'
	conf = Conf()

	def urlOpen(self, url) :
		content = ''
		with codecs.open(url, 'r', 'gb18030') as fo :
			for line in fo.readlines() :
				content += line.strip().encode('utf-8') + '\n'
		return content

	def getQAPair(self, url) :
		qalist = []
		content = urllib2.urlopen(url).read()
		# content = self.urlOpen(url)
		soup = BeautifulSoup(content)
		alltags = soup.findAll(True)
		for tag in alltags :
			if tag.name == 'div' :
				if 'class' in [t[0] for t in tag.attrs] :
					if tag['class'] == 'reply-box' or tag['class'] == 'reply-box nobg' :
						targetset = tag.contents[3].contents[1].contents[1].findAll('span')
						if targetset != [] :
							question, answer = '', ''
							for target in targetset :
								if 'class' in [s[0] for s in target.attrs] :
									if target['class'] == 'quote-cont2' :
										for part in target.contents :
											if isinstance(part, NavigableString) == True :
												question += part
							for part in tag.contents[3].contents[1].contents[1].contents :
								if isinstance(part, NavigableString) == True :
									answer += part
							qalist.append([question, answer])
		return qalist
	
	def getQuestionList(self, url) :
		qslist = []
		content = urllib2.urlopen(url).read()
		# content = self.urlOpen(url)
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
							href = self.mainurl + '/' + a['href']
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
						href = self.mainurl + '/' + a['href']
				if len(tag.contents) >= 3 :
					print tag.contents[3]
					page = int(tag.contents[3].split(u'\xd6\xf7\xcc\xe2\xa3\xba')[1].split(u')')[0].strip())/50+1
					if href not in topiclist :
						topiclist.append([href, page])
		return topiclist

	def storeQAList(self, storeqalist) :
		for topic, idx, qalist in storeqalist :
			topicdir = self.maindir + '/' + str(topic)
			if not os.path.exists(topicdir) :
				os.mkdir(topicdir)
			path = topicdir + '/' + str(idx)
			with codecs.open(path, 'w+') as fw :
				for q, a in qalist :
					fw.writelines('!!\n')
					fw.writelines('KNOWLEDGE\n')
					fw.writelines('QT' + q.encode('utf-8') + '\n')
					fw.writelines('AS' + a.encode('utf-8') + '\n')
					fw.writelines('SC1.0\n')
					fw.writelines('KNOWLEDGE\n')

	def storeTopicList(self, storepath, topiclist) :
		with codecs.open(storepath, 'w') as fw :
			for topicurl, topicpage in topiclist :
				fw.writelines(str(topicurl) + '\t' + str(topicpage) + '\n')

	def readTopicList(self, path) :
		topiclist = []
		with codecs.open(path, 'r', 'utf-8') as fo :
			for line in fo.readlines() :
				url, page = line.strip().split('\t')
				topiclist.append([url, int(page)])
		return topiclist

	def process(self) :
		topiclistpath = self.maindir + '/topiclist'
		# topiclist = self.getTopicList(self.homepage)
		# self.storeTopicList(topiclistpath, topiclist)
		topiclist = self.readTopicList(topiclistpath)
		print 'read topiclist finished ...'
		[topicidx, page] = self.conf.readConf()
		print 'read configuration finished ...'
		while topicidx < len(topiclist) :
			topicurl = topiclist[topicidx][0]
			print 'process topicurl is', topicurl
			for p in range(page, page + 1) : # every page
				print '  process page is', p
				qslisturl = topicurl + '&page=' + str(p)
				qslist = self.getQuestionList(qslisturl)
				for qsurl, qspage in qslist : # every question
					try:
						storeqalist = []
						for pp in range(1, qspage) :
							pairurl = qsurl + '&page=' + str(pp)
							qalist = self.getQAPair(pairurl)
							topicdir = qsurl.split('=')[-1]
							idx = int(qsurl.split('?')[-1].split('&')[0].split('=')[-1])%100
							storeqalist.append([topicdir, idx, qalist])
						self.storeQAList(storeqalist)
						print '    questionurl', qsurl, 'is finished ...'
					except Exception, e:
						pass
				print '  page', p, 'is finished ...'
				time.sleep(int(random.random()*60%60)+1)
			print 'topic', topicidx, 'page', page, 'is finished ...'
			topicidx += 1
			page += 1
			self.conf.writeConf([topicidx, page])
			time.sleep(int(random.random()*60%60)+1)



kdnet = KDNet()
# kdnet = KDNet('../input/topic.txt')
kdnet.process()
>>>>>>> dfbd900696f6ace3b761ff13e151b6920a154c40
