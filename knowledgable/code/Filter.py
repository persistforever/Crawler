# -*- encoding = utf-8 -*-
'''
list of filter
1. CollectionFilter
2. ContentLengthFilter
'''

import codecs
import numpy as np
from BasicClass import Article


class CollectionFilter :
    # attributes
    rate = 0.0
    
    # methods
    def __init__(self, rate=0.1) :
        self.rate = rate
    
    def filtering(self, artlist) :
        restnum = int(self.rate * len(artlist))
        sortedlist = sorted(artlist, key=lambda x: x.collectnum, reverse=True)
        return sortedlist[0:restnum]


class ContentLengthFilter :
    # attributes
    length = 0
    
    # methods
    def __init__(self, length=200) :
        self.length = length
    
    def filtering(self, artlist) :
    	filteredlist = []
    	for article in artlist :
    		if len(article.content) >= self.length :
    			filteredlist.append(article)
        return filteredlist
