# -*- encoding=utf-8 -*-
import codecs
import ConfigParser


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
        return self.name + ' ' + self.feature


class Article :
    # attributes
    id = ''
    url = ''
    title = ''
    content = ''
    collectnum = 0
    klgwordcount = 0
    sptitle = []

    # methods
    def __init__(self, data) :
        if len(data) >= 6 :
            self.id = data[0]
            self.url = data[1]
            self.title = data[3]
            self.content = data[4]
            self.collectnum = int(data[8])

    def importTitle(self, title) :
        self.sptitle = []
        for part in title.split(' ') :
            word = Word(part)
            self.sptitle.append(word)

    def printTitle(self) :
        title = ''
        for word in self.sptitle :
            title += word.name + ' '
        return title