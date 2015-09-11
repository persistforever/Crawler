# -*- coding = utf-8 -*-
'''
catch category list from zhidao.baidu.com/list
category
	subcate
		tag
'''

import urllib2
from BeautifulSoup import BeautifulSoup

class Catalog :
	# attributes
	cataid = 0
	url = ''
	text = ''
	child = None

	def __init__(self, cataid, url, text) :
		self.cataid = cataid
		self.url = url
		self.text = text
		self.child = []


class Category :
	# attributes
	mainurl = ''
	firstclass = []
	secondclass = []

	def __init__(self, mainurl) :
		self.mainurl = mainurl
	
	def firstClass(self, url) :
		content = urllib2.urlopen(url).read()
		soup = BeautifulSoup(content)
		catlist = soup.contents[4].contents[5].contents[7].contents[5].findAll('a')
		for item in catlist :
			cataid = int(item['href'].split('=')[-1])
			cataurl = self.mainurl + '?cid=' + str(cataid)
			catatext = str(item.contents[0]).strip()
			catalog = Catalog(cataid, cataurl, catatext)
			self.firstclass.append(catalog)
	
	def secondClass(self, url) :
		content = urllib2.urlopen(url).read()
		soup = BeautifulSoup(content)
		catlist = soup.contents[4].contents[5].contents[7].contents[5].findAll('a')
		for item in catlist :
			cataid = int(item['href'].split('=')[-1])
			cataurl = self.mainurl + '?cid=' + str(cataid)
			catatext = str(item.contents[0]).strip()
			catalog = Catalog(cataid, cataurl, catatext)
			self.secondclass.append(catalog)
	
	def tag(self, url) :
		content = urllib2.urlopen(url).read()
		soup = BeautifulSoup(content)
		catlist = soup.contents[4].contents[5].contents[7].contents[5]
		print catlist
		for item in catlist :
			cataid = int(item['href'].split('=')[-1])
			cataurl = self.mainurl + '?cid=' + str(cataid)
			catatext = str(item.contents[0]).strip()
			catalog = Catalog(cataid, cataurl, catatext)
			self.secondclass.append(catalog)

	def createCategoryTree(self) :
		'''
		self.firstClass(category.mainurl)
		for fcl in self.firstclass :
			self.secondclass = []
			self.secondClass(fcl.url)
			for scl in self.secondclass :
				fcl.child.append(scl)
		'''
		self.tag('http://zhidao.baidu.com/list?cid=110101')

	def writeCategoryTree(self, name) :
		with open(name, 'w') as fw :
			for fcl in self.firstclass :
				fw.writelines('- ' + fcl.text + '\t' + str(fcl.cataid) + '\n')
				for scl in fcl.child :
					fw.writelines('\t- ' + scl.text + '\t' + str(scl.cataid) + '\n')

if __name__ == '__main__' :
	category = Category('http://zhidao.baidu.com/list')
	category.createCategoryTree()
	category.writeCategoryTree('../result/categorytree.txt')