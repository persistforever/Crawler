# -*- encoding=utf8 -*-
import codecs
import numpy as np
from BasicClass import Article

class Corpus :
    # attributes
    artlist = []
    seed = []
    wordbag = dict()
    wordcount = dict()

    # methods
    def importArticle(self, datapath, titlepath, seedpath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            dataset = [line.strip().split('\t') for line in fo.readlines()]
        with codecs.open(titlepath, 'r', 'gb18030') as fo :
            titlelist = [line.strip() for line in fo.readlines()]
        for idx in range(len(dataset)) :
            article = Article(dataset[idx])
            article.importTitle(titlelist[idx])
            self.artlist.append(article)
        with codecs.open(seedpath, 'r', 'gb18030') as fo :
            seedlist = [line.strip() for line in fo.readlines()]
        self.seed = seedlist

    def constrWordBag(self) :
        wordbag = dict()
        for article in self.artlist :
            for word in article.sptitle :
                if word.name not in self.wordbag :
                    self.wordbag[word.name] = word.feature
        for article in self.artlist :
            for word in article.sptitle :
                if word.name not in self.wordcount :
                    self.wordcount[word.name] = {}.fromkeys(self.wordbag, 0)
                for otherword in article.sptitle :
                    if otherword != word :
                        self.wordcount[word.name][otherword.name] += 1

    def wordSim(self, query) :
        wordsim = {}.fromkeys(self.wordcount, 0.0)
        for word in self.wordcount :
            a, b = [], []
            for w in self.wordcount[word] :
                if query in self.wordcount :
                    if self.wordcount[word][w] != 0 and self.wordcount[query][w] != 0 :
                        a.append(self.wordcount[word][w])
                        b.append(self.wordcount[query][w])
            a, b = np.array(a), np.array(b)
            if len(a) >= 20 :
                num = sum([a[idx]*b[idx] for idx in range(len(a))])
                denom = np.linalg.norm(a) * np.linalg.norm(b)
                wordsim[word] = 1.0 * num / denom
        return sorted(wordsim.iteritems(), key=lambda x: x[1], reverse=True)[0:100]

    def selfSearch(self, simpath) :
        similarity = {}.fromkeys(self.wordbag, 0)
        for target in self.seed :
            print target.encode('utf8')
            top = self.wordSim(target)
            for word, sim in top :
                if word not in self.seed :
                    similarity[word] += sim
        similarity = sorted(similarity.iteritems(), key=lambda x: x[1], reverse=True)
        with open(simpath, 'w') as fw :
            for word, sim in similarity :
                fw.writelines(word.encode('utf8') + '\t' + str(sim).encode('utf8') + '\n')

    def filterArticle(self, klgwordpath) :
        for article in self.artlist :
            for word in article.sptitle :
                if word.name in self.seed[0:5] :
                    article.klgwordcount += 1
        sortlist = sorted(self.artlist, key=lambda x: x.klgwordcount*1000+x.collectnum, reverse=True)
        with open(klgwordpath, 'w') as fw :
            for article in sortlist :
                fw.writelines(article.title.encode('utf8') + '\t' + str(article.klgwordcount).encode('utf8') \
                    + '\t' + str(article.collectnum).encode('utf8') + '\n')


# ---------- select knowledgable words ----------

corpus = Corpus()
corpus.importArticle('../data/synonyms/4/unique', '../data/synonyms/4/title_sp', '../data/synonyms/knowledgableword')
corpus.constrWordBag()
corpus.selfSearch('../data/synonyms/4/sortedkglword')


# ---------- use knowledgable word to filter title ----------
'''
corpus = Corpus()
corpus.importArticle('../data/synonyms/4/unique', '../data/synonyms/4/title_sp', '../data/synonyms/knowledgableword')
corpus.filterArticle('../data/synonyms/4/sortedkglword')
'''
