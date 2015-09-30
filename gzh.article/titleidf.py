'''
statistic idf value of title
'''
import codecs
import numpy as np

charset = 'gbk'

class Topic :
    # attributes
    negatitlelist = []
    postitlelist = []
    nageswlist = []
    posswlist = []
    titlelist = []
    swlist = []
    wordpool = dict()
    punc = []
    
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
                
    def statistic(self) :
        for wordlist in self.swlist :
            wordset = set(wordlist)
            for word in wordset :
                if word not in self.punc :
                    if word not in self.wordpool.keys() :
                        self.wordpool[word] = 0
                    self.wordpool[word] += 1
                    
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
                        
topic = Topic()
topic.nagetitlelist = topic.importTitle('labeled/nega')
topic.nageswlist = topic.importData('labeled/nega_out')
topic.postitlelist = topic.importTitle('labeled/pos')
topic.posswlist = topic.importData('labeled/pos_out')
topic.titlelist = topic.importTitle('summary/title')
topic.swlist = topic.importData('summary/title_out')
topic.statistic()
# topic.printPool()
print 'nagetive start ...'
print 'nagetice average variance is', topic.keyWord(topic.nageswlist, topic.nagetitlelist)
print 'positive start ...'
print 'positive average variance is', topic.keyWord(topic.posswlist, topic.postitlelist)
