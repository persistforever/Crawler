# -*- encoding = utf-8 -*-
import codecs
import ConfigParser
import math


class Conf :
    # attributes
    filename = '../data/labeling/settings.ini'

    # methods
    def readConf(self) :
        arr = []
        cf = ConfigParser.ConfigParser()
        cf.read(self.filename)
        arr.append(int(cf.get('article', 'startidx')))
        return arr

    def writeConf(self, arr) :
        cf = ConfigParser.ConfigParser()
        cf.add_section('article')
        cf.set('article', 'startidx', str(arr[0]))
        cf.write(open(self.filename, 'w'))


class Word :
    # attributes
    name = ''
    feature = ''

    # methods
    def __init__(self, line) :
        if len(line.split(':')) == 2 :
            self.name = line.split(':')[0]
            self.feature = line.split(':')[1]

    def toString(self) :
        return self.name + ':' + self.feature


class Article :
    # ----- attributes -----
    id = ''
    url = ''
    title = ''
    content = ''
    sptitle = [] # sequence of title
    spcontent = [] # sequence of content
    label = -1 # label
    keyword = [] # list of keyword
    tfdict = dict() # value of term frequency
    tfidfdict = dict() # TF-IDF
    featureset = [] # list of feature value

    # ----- features -----
    # --- 1. token level ---
    artlength = 0 # length of article
    wordnum = 0 # number of distinct word
    distwordnum = 0 # number of distinct word
    puncnum = 0 # number of punctuation
    stnum = 0 # average length of sentence
    avgstlength = 0 # average length of sentence
    # --- 2. user level ---
    forwardnum = 0 # number of forward
    zannum = 0 # number of zan
    clicknum = 0 # number of click
    collectnum = 0 # number of collect
    readtime = 0 # number of read time
    finishrate = 0 # number of finish rate
    # --- 3. word level ---
    klwordnum = 0 # number of knowledgable word
    firpronum = 0 # number of first pronouns word
    secpronum = 0 # number of first pronouns word
    thrpronum = 0 # number of first pronouns word
    namenum = 0 # number of name word
    # --- 4. pos level ---
    navg = 0.0 # average number of noun word
    nvar = 0.0 # varance of noun word
    aavg = 0.0 # average number of adjective word
    avar = 0.0 # varance of adjective word
    vavg = 0.0 # average number of verb word
    vvar = 0.0 # varance of verb word
    davg = 0.0 # average number of adverb word
    dvar = 0.0 # varance of adverb word
    cavg = 0.0 # average number of conjunction word
    cvar = 0.0 # varance of conjunction word
    mavg = 0.0 # average number of mood word
    mvar = 0.0 # varance of mood word
    qavg = 0.0 # average number of quantity word
    qvar = 0.0 # varance of quantity word

    # ----- init method -----
    def __init__(self, data) :
        if len(data) >= 4 :
            self.id = data[0]
            self.url = data[1]
            self.title = data[2]
            self.content = data[3]
            self.label = -1
                
    # ----- import methods -----
    def importInfo(self, data) :
        if len(data) >= 8 :
            self.forwardnum = int(data[2])
            self.zannum = int(data[3])
            self.clicknum = int(data[4])
            self.collectnum = int(data[5])
            self.readtime = float(data[6])
            self.finishrate = float(data[7])

    def importSplit(self, data) :
        self.sptitle, self.spcontent = [], []
        if len(data) >= 3 :
            title, content = data[1], data[2]
            for part in title.split(' ') :
                word = Word(part)
                self.sptitle.append(word)
            for part in content.split(' ') :
                word = Word(part)
                self.spcontent.append(word)

    def importLabel(self, data) :
        self.label = int(data[1])
        if self.label == 2 :
            self.label = 1
        elif self.label == -1 :
            self.label = -1
        else :
            self.label = 0
            
    def importKeyWord(self, data) :
        self.keyword = []
        wordlist = data[1:]
        for w in wordlist :
            word = Word(w.split('#')[0])
            tfidf = float(w.split('#')[1])
            self.keyword.append([word, tfidf])
            
    def importFeatureSet(self, data) :
        self.featureset = []
        for value in data :
            self.featureset.append(float(value))
            
    # ----- process methods -----
    def calTF(self) :
        self.tfdict = dict()
        for word in self.spcontent :
            word = word.toString()
            if word not in self.tfdict :
                self.tfdict[word] = 0
            self.tfdict[word] += 1
        maxcount = max(self.tfdict.values())
        for word in self.tfdict.keys() :
            self.tfdict[word] = 1.0 * self.tfdict[word] / maxcount
    
    def calTFIDF(self, idfdict) :
        self.calTF()
        self.tfidfdict = dict()
        for word in self.tfdict :
            self.tfidfdict[word] = self.tfdict[word] * idfdict[word]
            
    def selectKeyWord(self, keywordnum=50) :
        self.keyword = []
        for word, tfidf in sorted(self.tfidfdict.iteritems(), key=lambda x:x[1], reverse=True) :
            w = Word(word)
            self.keyword.append([w, tfidf])
            if len(self.keyword) >= keywordnum :
                break

    def constrFeatureSet(self) :
        self.featureset = []
        self.featureset.extend([self.artlength, self.wordnum, self.distwordnum, self.puncnum, self.stnum, self.avgstlength])
        self.featureset.extend([self.forwardnum, self.zannum, self.clicknum, self.collectnum, self.readtime, self.finishrate])
        self.featureset.extend([self.klwordnum, self.firpronum, self.secpronum, self.thrpronum, self.namenum])
        self.featureset.extend([self.navg, self.nvar, self.aavg, self.avar, self.vavg, self.vvar, self.davg, self.dvar, \
                self.cavg, self.cvar, self.mavg, self.mvar, self.qavg, self.qvar])

    # ----- print methods -----
    def printTitle(self) :
        title = ''
        for word in self.sptitle :
            title += word.name + ' '
        return title

    def printId(self) :
        return self.id

    def printLabel(self) :
        return str(self.label)
    
    def printLine(self) :
        line = ''
        line += self.id + u'\t'
        line += self.url + u'\t'
        line += self.title + u'\t'
        line += self.content + u'\t'
        return line   
    
    def printSimplyLine(self) :
        line = ''
        line += self.id + u'\t'
        line += self.url + u'\t'
        line += self.simplytitle + u'\t'
        line += self.content + u'\t'
        return line   
            
    def printKeyWord(self) :
        line = ''
        for word, tfidf in self.keyword :
            line += word.toString() + '#' + str(round(tfidf, 4)) + '\t'
        return line
    
    def printFeatureSet(self) :
        line = ''
        for value in self.featureset :
            if math.isnan(value) :
                value = 0.0
            line += str(value) + '\t'
        return line
