# -*- encoding = utf-8 -*-
'''
title simplifier
'''

import codecs
import numpy as np
import re
from BasicClass import Article


class TitleSimplifier :
    # attributes
    sppath = '../data/titlespst'
    spdict = dict()
    
    # methods    
    def __init__(self) :
        self.spdict = self.importSpDict(self.sppath)
        
    def importSpDict(self, sppath) :
        spdict = dict()
        with codecs.open(sppath, 'r', 'gb18030') as fo :
            for line in fo.readlines() :
                if line.strip() not in spdict :
                    spdict[line.strip()] = None
        return spdict

    def splitSentence(self, article, splitchar) :
        sentenceset = re.split(splitchar, article.title)
        return sentenceset

    def sentenceScore(self, sentence, keyword) :
        top = 0
        bottem = len(keyword)
        for char in sentence :
            if char in keyword :
                top += 1
            else :
                bottem += 1
        score = 1.0 * top / bottem + len(sentence) * 0.25
        return score
    
    def simplifying(self, artlist) :
        splitchar = '[\]\['
        for sp in self.spdict :
            splitchar += sp
        splitchar += ' ]'
        for article in artlist :
            sentenceset = self.splitSentence(article, splitchar)
            sentencelist = []
            for sentence in sentenceset :
                if sentence != '' :
                    keyword = ''
                    for word in article.keyword[0:5] :
                        keyword += word[0].name
                    sentencelist.append([sentence, self.sentenceScore(sentence, keyword)])
            sentencelist = sorted(sentencelist, key=lambda x: x[1], reverse=True)
            article.simplytitle = sentencelist[0][0]