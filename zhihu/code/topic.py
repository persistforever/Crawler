# -*- encoding=utf-8 -*-
'''
catch topic tree model of zhihu
'''

import urllib2
from BeautifulSoup import BeautifulSoup
import ConfigParser
import random
import time
import xml.dom.minidom
import codecs

class TopicNode :
    # attributes
    id = 0
    url = ''
    name = ''
    child = []

    # methods
    def __init__(self, id, url, name, child) :
        self.id = id
        self.url = url
        self.name = name
        self.child = child

class TopicTree :
    # attributes
    mainurl = 'http://www.zhihu.com'
    roottopicurl = '/topic/19776749'
    topicdict = dict()

    # methods
    def getChildTopic(self, url) :
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content)
        childlist = []
        alldiv = soup.findAll('div')
        for div in alldiv :
            if 'class' in [t[0] for t in div.attrs] and 'id' in [t[0] for t in div.attrs]:
                if div['class'] == 'zm-side-section' and div['id'] == 'zh-topic-side-children-list' :
                    alla = div.findAll('a')
                    for a in alla :
                        if 'class' in [t[0] for t in a.attrs] :
                            if a['class'] == 'zm-item-tag' :
                                childlist.append([a['data-token'], self.mainurl+a['href'], a.contents[0].strip()])
        return childlist

    def createTree(self, node, height) :
        childlist = self.getChildTopic(node.url)
        for id, url, name in childlist :
            if id not in self.topicdict :
                self.topicdict[id] = None
                subnode = TopicNode(int(id), url, name, [])
                node.child.append(subnode)
                self.createTree(subnode, height+1)
        time.sleep(int(random.random() * 10 % 10 + 1))

    def storeTree(self, node, parentdom, dom) :
        # print '*'*height, node.name.encode('utf-8')
        for subnode in node.child :
            topic = dom.createElement('topic')
            url = dom.createElement('url')
            urltext = dom.createTextNode(subnode.url)
            url.appendChild(urltext)
            topic.appendChild(url)
            name = dom.createElement('name')
            nametext = dom.createTextNode(subnode.name)
            name.appendChild(nametext)
            topic.appendChild(name)
            child = dom.createElement('child')
            self.storeTree(subnode, child, dom)
            topic.appendChild(child)
            parentdom.appendChild(topic)    

    def readXML(self, name) :
    	dom = xml.dom.minidom.parse(name)
    	root = dom.documentElement
    	nodeset = root.getElementsByTagName('url')
    	urlset = []
    	for node in nodeset :
    		urlset.append(node.firstChild.data.strip())
    	return urlset

    def storeXML(self, filename, root) :
        impl = xml.dom.minidom.getDOMImplementation()
        dom = impl.createDocument(None, 'zhihu', None)
        r = dom.documentElement
        topic = dom.createElement('topic')
        r.appendChild(topic)
        # store topic start
        url = dom.createElement('url')
        urltext = dom.createTextNode(root.url)
        url.appendChild(urltext)
        topic.appendChild(url)
        name = dom.createElement('name')
        nametext = dom.createTextNode(root.name)
        name.appendChild(nametext)
        topic.appendChild(name)
        child = dom.createElement('child')
        self.storeTree(root, child, dom)
        topic.appendChild(child)
        # store root end
        with codecs.open(filename, 'w', 'utf-8') as fo :
            dom.writexml(fo, addindent='  ', newl='\n',encoding='utf-8')

    def storeURL(self, name, urlset) :
        with open(name, 'w') as fw :
        	for url in urlset :
        		fw.writelines(url.encode('utf-8') + '/questions\n'.encode('utf-8'))

    def process(self) :
        rootid = 19776749
        rooturl = self.mainurl + self.roottopicurl
        rootname = 'root topic'
        root = TopicNode(rootid, rooturl, rootname, [])
        # self.createTree(root, 0)
        # self.storeXML('treexml.xml', root)
        urlset = self.readXML('../result/treexml.xml')
        self.storeURL('../result/url.txt', urlset)


topictree = TopicTree()
topictree.process()
