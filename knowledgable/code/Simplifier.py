# -*- encoding = utf-8 -*-
'''
title simplifier
'''

import codecs
import numpy as np
import re
from BasicClass import Article
import gensim


class TitleSimplifier :
    # attributes
    sppath = 'E://file/knowledgable/input/tools/titlespst'
    spdict = dict()
    
    # methods    
    def __init__(self) :
        self.spdict = self.importSpDict(self.sppath)
        self.vecmodel = gensim.models.Word2Vec.load('vectors.txt')
        
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

    def featureSentenceScore(self, sentence, keyword) :
        top = 0
        bottem = len(sentence) + len(keyword)
        stc = ''
        keyline = ''
        for word in keyword :
            keyline += word.name
        for word in sentence :
            stc += word.name
            for char in word.name :
                if char in keyline :
                    top += 1
                    break
        score = 1.0 * top / bottem + len([1 for t in sentence if t.feature == 'n']) * 0.01 + len(sentence) * 0.01
        return [stc, score]
    
    def modelSentenceScore(self, sentence, keyword) :
        stc = ''
        score = 0.0
        for worda in sentence :
            stc += worda.name
            for wordb in keyword :
                try:
                    score += self.vecmodel.similarity(worda.name.encode('utf8'), wordb.name.encode('utf8'))
                except Exception, e:
                    pass
        return [stc, score]

    def splitTitle(self, artlist) :
        splitchar = '[\[\]\|?'
        for sp in self.spdict :
            splitchar += sp
        splitchar += ' ]'
        for article in artlist :
            sentenceset = self.splitSentence(article, splitchar)
            article.subtitle = []
            for sentence in sentenceset :
                if sentence.strip() != '' :
                    article.subtitle.append(sentence)
                    
    def featureSimplifying(self, artlist) :
        for article in artlist :
            sentencelist = []
            for sentence in article.subtitle :
                sentencescore = self.featureSentenceScore(sentence, [t[0] for t in article.keyword[0:20]])
                sentencelist.append(sentencescore)
            sentencelist = sorted(sentencelist, key=lambda x: x[1], reverse=True)
            article.simplytitle = sentencelist[0][0]
                    
    def modelSimplifying(self, artlist) :
        for article in artlist :
            sentencelist = []
            for sentence in article.subtitle :
                sentencescore = self.modelSentenceScore(sentence, [t[0] for t in article.keyword[0:20]])
                sentencelist.append(sentencescore)
            sentencelist = sorted(sentencelist, key=lambda x: x[1], reverse=True)
            article.simplytitle = sentencelist[0][0]
