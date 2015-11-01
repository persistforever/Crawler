# -*- encoding=utf-8 -*-
import codecs


class Article :
    # attributes 
    personal_count = 0

    def __init__(self, data) :
        if len(data) == 5 :
            self.id = data[0]
            self.url = data[1]
            self.title = data[2]
            self.content = data[3]
            self.score = data[4]

    def countPersonal(self) :
        count = 0
        for char in self.content :
            if char in [u'你', u'您', u'我', u'他', u'她', u'它'] :
                count += 1
        self.personal_count = count


class Corpus :
    # attributes
    artlist = []

    # methods
    def importArticle(self, datapath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            dataset = [line.strip().split('\t') for line in fo.readlines()[0:100]]
        for data in dataset :
            article = Article(data)
            self.artlist.append(article)

    def sorting(self) :
        for article in self.artlist :
            article.countPersonal()
        self.artlist = sorted(self.artlist, key=lambda x: x.personal_count, reverse=False)
        for article in self.artlist :
            print article.title.encode('utf-8'), article.personal_count


corpus = Corpus()
corpus.importArticle('../data/labeling/car')
corpus.sorting()
