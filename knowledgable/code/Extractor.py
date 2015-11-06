# -*- encoding = utf-8 -*-
'''
list of extractor
1. PosExtractor
2. KnowledgableWordExtractor
3. PersonExtractor
4. TokenExtractor
'''

import codecs
import math
import numpy as np
import re


class PosExtractor :
    # attributes
    pospath = '../data/postag'
    w = 0
    posdict = dict()
    # posidxset = [noun, adjective, verb, adverb, conjunction, mood, quantity]
    noun = [5, 11, 12, 14, 15, 16, 37]
    adjective = [3, 22, 23, 28]
    verb = [2, 4, 29, 45]
    adverb = [9, 27]
    conjunction = [24, 39]
    mood = [36, 46, 10]
    quantity = [34, 38, 27, 18]
    
    # methods    
    def __init__(self, w=10) :
        self.w = w
        self.posdict = self.importPosDict(self.pospath)
        
    def importPosDict(self, pospath) :
        posdict = dict()
        with codecs.open(pospath, 'r', 'gb18030') as fo :
            for line in fo.readlines() :
                if line.strip() not in posdict :
                    posdict[line.strip()] = None
        return posdict
    
    def extractFeature(self, artlist) :
        for article in artlist :
            l = len(article.keyword)
            numlist = []
            for x in range(0, l - self.w + 1) :
                pos_hist = dict()
                for key in self.posdict.keys() :
                    pos_hist[key] = 0
                for i in range(x, x + self.w) :
                    if article.keyword[i][0].feature in pos_hist :
                        pos_hist[article.keyword[i][0].feature] += 1
                numlist.append(pos_hist.values())
            meanset, varset = [], []
            for j in range(len(numlist[0])) :
                meanset.append(np.mean([line[j] for line in numlist]))
                varset.append(np.var([line[j] for line in numlist]))
            article.navg, article.nvar = 0.0, 0.0
            article.aavg, article.avar = 0.0, 0.0
            article.vavg, article.vvar = 0.0, 0.0
            article.davg, article.dvar = 0.0, 0.0
            article.cavg, article.cvar = 0.0, 0.0
            article.mavg, article.mvar = 0.0, 0.0
            article.qavg, article.qvar = 0.0, 0.0
            for idx in self.noun :
                article.navg += meanset[idx]
                article.nvar += varset[idx]
            for idx in self.adjective :
                article.aavg += meanset[idx]
                article.avar += varset[idx]
            for idx in self.verb :
                article.vavg += meanset[idx]
                article.vvar += varset[idx]
            for idx in self.adverb :
                article.davg += meanset[idx]
                article.dvar += varset[idx]
            for idx in self.conjunction :
                article.cavg += meanset[idx]
                article.cvar += varset[idx]
            for idx in self.mood :
                article.mavg += meanset[idx]
                article.mvar += varset[idx]
            for idx in self.quantity :
                article.qavg += meanset[idx]
                article.qvar += varset[idx]


class KnowledgableWordExtractor :
    # attributes
    wordpath = '../data/knowledgableword'
    worddict = dict()
    
    # methods    
    def __init__(self) :
        self.worddict = self.importWordDict(self.wordpath)
        
    def importWordDict(self, wordpath) :
        worddict = dict()
        with codecs.open(wordpath, 'r', 'gb18030') as fo :
            for line in fo.readlines() :
                if line.strip() not in worddict :
                    worddict[line.strip()] = None
        return worddict
    
    def extractFeature(self, artlist) :
        for article in artlist :
            worddict = {}.fromkeys(self.worddict, 0)
            for word in article.sptitle :
                if word.name in worddict :
                    worddict[word.name] += 1
            for word in article.spcontent :
                if word.name in worddict :
                    worddict[word.name] += 1
            article.klwordnum = sum(worddict.values())


class PersonExtractor :
    # attributes
    firpath = '../data/knowledgableword'
    secpath = '../data/knowledgableword'
    thrpath = '../data/knowledgableword'
    firstdict = dict()
    seconddict = dict()
    thirddict = dict()
    
    # methods       
    def __init__(self) :
        self.firstdict = self.importPersonDict(self.firpath)
        self.seconddict = self.importPersonDict(self.secpath)
        self.thirddict = self.importPersonDict(self.thrpath)
        
    def importPersonDict(self, personpath) :
        worddict = dict()
        with codecs.open(personpath, 'r', 'gb18030') as fo :
            for line in fo.readlines() :
                if line.strip() not in worddict :
                    worddict[line.strip()] = 0
        return worddict
    
    def extractFeature(self, artlist) :
        for article in artlist :
            first, second, third, name = 0, 0, 0, 0
            for word in article.sptitle :
                if word.name in self.firstdict :
                    first += 1
                elif word.name in self.seconddict :
                    second += 1
                elif word.name in self.thirddict :
                    third += 1
                if word.feature in [u'nrg', u'nrf'] :
                    name += 1
            for word in article.spcontent :
                if word.name in self.firstdict :
                    first += 1
                elif word.name in self.seconddict :
                    second += 1
                elif word.name in self.thirddict :
                    third += 1
                if word.feature in [u'nrg', u'nrf'] :
                    name += 1
            article.firpronum = first
            article.secpronum = second
            article.thrpronum = third
            article.namenum = name


class TokenExtractor :
    # attributes
    sppath = '../data/contentspst'
    pcpath = '../data/punctuation'
    spdict = dict()
    
    # methods    
    def __init__(self) :
        self.spdict = self.importSpDict(self.sppath)
        self.pcdict = self.importPcDict(self.pcpath)
        
    def importSpDict(self, sppath) :
        spdict = dict()
        with codecs.open(sppath, 'r', 'gb18030') as fo :
            for line in fo.readlines() :
                if line.strip() not in spdict :
                    spdict[line.strip()] = None
        return spdict
        
    def importPcDict(self, pcpath) :
        pcdict = dict()
        with codecs.open(pcpath, 'r', 'gb18030') as fo :
            for line in fo.readlines() :
                if line.strip() not in pcdict :
                    pcdict[line.strip()] = None
        return pcdict
    
    def extractFeature(self, artlist) :
        for article in artlist :
            article.artlength = len(article.content)
            article.wordnum = len(article.sptitle) + len(article.spcontent)
            worddict = dict()
            for word in article.sptitle :
                if word.name not in worddict :
                    worddict[word.name] = None
            for word in article.spcontent :
                if word.name not in worddict :
                    worddict[word.name] = None
            article.distwordnum = len(worddict)
            article.puncnum = sum([1 for char in article.content if char in self.pcdict])
            splitchar = '['
            for sp in self.spdict :
                splitchar += sp
            splitchar += ']'
            sentenceset = re.split(splitchar, article.content)
            article.stnum = len(sentenceset)
            article.avgstlength = 1.0 * sum([len(line.strip()) for line in sentenceset]) / len(sentenceset)