'''
statistic idf value of title
'''
import codecs
import numpy as np
import math

charset = 'gb18030'

class Article :
    # attributes
    title = []
    content = []
    score = 0
    keyword = []
    
    # method
    def __init__(self, title, content) :
        self.title = title
        self.content = content
        
    def calTF(self) :
        tfdict = dict()
        for word in self.content :
            if word not in tfdict :
                tfdict[word] = 0
            tfdict[word] += 1
        maxcount = max(tfdict.values())
        for word in tfdict.keys() :
            tfdict[word] = 1.0*tfdict[word]/maxcount
        return tfdict
    
    def calTFIDF(self, tfdict, idfdict) :
        tfidfdict = dict()
        for word in tfdict :
            tfidfdict[word] = tfdict[word] * idfdict[word]
        self.keyword = sorted(tfidfdict.iteritems(), key=lambda x:x[1], reverse=True)[0:10]

class Corpus :
    # attributes
    # negatitlelist = []
    # postitlelist = []
    # nageswlist = []
    # posswlist = []
    tllist = []
    tlsplist = []
    ctlist = []
    ctsplist = []
    swlist = []
    idfdict = dict()
    length = 0
    
    # methods
    def importTitle(self, name) :
        titlelist = []
        with codecs.open(name, 'r', charset) as fo :
            for line in fo.readlines() :
                title = line.strip()
                titlelist.append(title)
        return titlelist
    
    def importData(self, name) :
        swlist = []
        with codecs.open(name, 'r', charset) as fo :
            for line in fo.readlines() :
                wordlist = line.strip().split(' ')
                swlist.append(wordlist)
        return swlist
                
    def calIDF(self) :
        self.length = len(self.ctsplist)
        for wordlist in self.ctsplist :
            wordset = set(wordlist)
            for word in wordset :
                if word not in self.idfdict.keys() :
                    self.idfdict[word] = 0
                self.idfdict[word] += 1
        for word in self.idfdict :
            self.idfdict[word] = math.log(1.0 * self.length / (self.idfdict[word] + 1), math.e)
                
    def articleKeyWord(self) :
        articlelist = []
        for idx in range(len(self.tlsplist)) :
            article = Article(self.tlsplist[idx], self.ctsplist[idx])
            tfdict = article.calTF()
            article.calTFIDF(tfdict, self.idfdict)
            '''
            print 'title ...'
            for word in self.tlsplist[idx] :
                print word.encode(charset), 
            print 
            for word, tfidf in keyword :
                print word.encode(charset), tfidf
            '''
            score = 0
            for word, tfidf in article.keyword :
                if word in self.tlsplist[idx] :
                    score += self.idfdict[word]
            article.score = 1.0 * score / len(self.tlsplist[idx])
            articlelist.append(article)
        articlelist = sorted(articlelist, key=lambda x: x.score, reverse=True)
        for article in articlelist :
            print 'title ...', article.score
            for word in article.title :
                print word.encode(charset), 
            print 
            for word, tfidf in article.keyword :
                print word.encode(charset), tfidf
                    
    def keyWord(self, swlist, titlelist) :
        varlist = []
        for idx in range(len(swlist)) :
            wordlist = []
            for word in swlist[idx] :
                if self.wordpool[word] <= 200 :
                    wordlist.append([word, self.wordpool[word]])
            wordlist = sorted(wordlist, key=lambda x: x[1])
            print titlelist[idx].encode(charset), np.var([t[1] for t in wordlist])
            varlist.append(np.var([t[1] for t in wordlist]))
        return np.mean(varlist)
            
    def printPool(self) :
        for word in self.wordpool :
            print word.encode(charset), self.wordpool[word]
                        
corpus = Corpus()
# topic.nagetitlelist = topic.importTitle('labeled/nega')
# topic.nageswlist = topic.importData('labeled/nega_out')
# topic.postitlelist = topic.importTitle('labeled/pos')
# topic.posswlist = topic.importData('labeled/pos_out')
corpus.tlsplist = corpus.importData('data/title_out.top')
corpus.ctsplist = corpus.importData('data/content_out.top')
corpus.calIDF()
print 'calculate idf finished ...'
corpus.articleKeyWord()
print 'calculate keyword finished ...'
'''
corpus.statistic()
topic.printPool()
print 'nagetive start ...'
print 'nagetice average variance is', corpus.keyWord(corpus.nageswlist, corpus.nagetitlelist)
print 'positive start ...'
print 'positive average variance is', corpus.keyWord(corpus.posswlist, corpus.postitlelist)
'''
