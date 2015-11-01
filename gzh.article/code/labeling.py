# -*- encoding = gbk -*-
import wx
import codecs
import ConfigParser
import webbrowser
import wx.webkit as webkit


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


class Article :
    label = 0

    def __init__(self, data, label) :
        if len(data) >= 4 :
            self.id = data[0]
            self.url = data[1]
            self.title = data[2]
            self.content = data[3]
            self.label = label


class Corpus :
    # attributes
    artlist = []
    ukllist = []
    uklist = []
    kllist = []

    # methods
    def importArticle(self, datapath, labelpath) :
        with codecs.open(datapath, 'r', 'gb18030') as fo :
            dataset = [line.strip().split('\t') for line in fo.readlines()[0:1000]]
        with codecs.open(labelpath, 'r', 'gb18030') as fo :
            labellist = [line.strip() for line in fo.readlines()]
        for idx in range(len(dataset)) :
            if idx >= len(labellist) :
                article = Article(dataset[idx], -1)
            else :
                article = Article(dataset[idx], labellist[idx])
            self.artlist.append(article)

    def writeLabel(self, labelpath) :
        with open(labelpath, 'w') as fw :
            for label in [t.label for t in self.artlist] :
                fw.writelines(str(label).encode('gb18030') + u'\n'.encode('gb18030'))

    def writeData(self, uklpath, ukpath, klpath) :
        with open(uklpath, 'a') as fw :
            for article in self.ukllist :
                fw.writelines(article.id.encode('gb18030') + u'\t'.encode('gb18030') + \
                                article.url.encode('gb18030') + u'\t'.encode('gb18030') + \
                                article.title.encode('gb18030') + u'\t'.encode('gb18030') + \
                                article.content.encode('gb18030') + u'\t'.encode('gb18030'))
        with open(ukpath, 'a') as fw :
            for article in self.uklist :
                fw.writelines(article.id.encode('gb18030') + u'\t'.encode('gb18030') + \
                                article.url.encode('gb18030') + u'\t'.encode('gb18030') + \
                                article.title.encode('gb18030') + u'\t'.encode('gb18030') + \
                                article.content.encode('gb18030') + u'\t'.encode('gb18030'))
        with open(klpath, 'a') as fw :
            for article in self.kllist :
                fw.writelines(article.id.encode('gb18030') + u'\t'.encode('gb18030') + \
                                article.url.encode('gb18030') + u'\t'.encode('gb18030') + \
                                article.title.encode('gb18030') + u'\t'.encode('gb18030') + \
                                article.content.encode('gb18030') + u'\t'.encode('gb18030'))


class StaticTextFrame(wx.Frame):  
    def __init__(self):  
        wx.Frame.__init__(self, None, -1, 'labeling', size=(1000, 350))  
        self.panel = wx.Panel(self, -1)
        self.corpus = Corpus()
        self.corpus.importArticle('../data/labeling/money', '../data/labeling/label.txt')

        self.conf = Conf()
        [self.idx] = self.conf.readConf()
        self.title = self.corpus.artlist[self.idx].title
        self.content = self.corpus.artlist[self.idx].content[0:2500]
        self.url = self.corpus.artlist[self.idx].url
        self.corpus.ukllist, self.corpus.uklist, self.corpus.kllist = [], [], []

        self.titletext = wx.StaticText(self.panel, -1, self.title, pos=(50, 20), size=(900, 50), style=wx.ALIGN_CENTER) 
        self.titletext.SetBackgroundColour(wx.Colour(232,232,255))
        self.titletext.SetForegroundColour(wx.Colour(0,0,0))
        font = wx.Font(18, wx.FONTFAMILY_TELETYPE, wx.FONTWEIGHT_NORMAL, wx.NORMAL)
        self.titletext.SetFont(font)
        self.titletext.SetSize((900, 30))
        self.contenttext = wx.HyperlinkCtrl(self.panel, -1, self.url, self.url, pos=(50, 70), size=(900, 50), style=wx.ALIGN_CENTER)
        self.contenttext.SetBackgroundColour(wx.Colour(232,232,255))
        self.contenttext.SetForegroundColour(wx.Colour(0,0,0))
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.NORMAL)
        self.contenttext.SetFont(font)
        self.contenttext.SetSize((900, 50))
        self.pagetext = wx.StaticText(self.panel, -1, str(self.idx)+'/'+str(len(self.corpus.artlist)), pos=(375, 230), size=(250, 30), style=wx.ALIGN_CENTER)
        self.pagetext.SetBackgroundColour(wx.Colour(232,232,255))
        self.pagetext.SetForegroundColour(wx.Colour(0,0,0))
        font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.NORMAL)
        self.pagetext.SetFont(font)
        self.pagetext.SetSize((250, 30))

        goodbutton = wx.Button(self.panel, label=u'knowledgeable', pos=(50, 150), size=(250, 50))
        goodbutton.Bind(wx.EVT_BUTTON, self.markGood, goodbutton)
        badbutton = wx.Button(self.panel, label=u'unknowledgeable', pos=(375, 150), size=(250, 50))
        badbutton.Bind(wx.EVT_BUTTON, self.markBad, badbutton)
        unknowbutton = wx.Button(self.panel, label=u'unknow', pos=(700, 150), size=(250, 50))
        unknowbutton.Bind(wx.EVT_BUTTON, self.markUnknow, unknowbutton)
        upperbutton = wx.Button(self.panel, label=u'nextpage', pos=(50, 230), size=(250, 50))
        upperbutton.Bind(wx.EVT_BUTTON, self.frontPage, upperbutton)
        savebutton = wx.Button(self.panel, label=u'save', pos=(700, 230), size=(250, 50))
        savebutton.Bind(wx.EVT_BUTTON, self.save, savebutton)

    def markGood(self, event):
        self.corpus.artlist[self.idx].label = 2
        self.corpus.kllist.append(self.corpus.artlist[self.idx])
        if self.idx < len(self.corpus.artlist)-1 :
            self.idx += 1
        self.title = self.corpus.artlist[self.idx].title
        self.content = self.corpus.artlist[self.idx].content[0:2500]
        self.url = self.corpus.artlist[self.idx].url
        self.titletext.SetLabel(self.title)
        self.titletext.SetSize((900, 30))
        self.contenttext.SetLabel(self.url)
        self.contenttext.SetURL(self.url)
        self.contenttext.SetSize((900, 30))
        self.pagetext.SetLabel(str(self.idx)+'/'+str(len(self.corpus.artlist)))
        self.pagetext.SetSize((250, 30))

    def markBad(self, event): 
        self.corpus.artlist[self.idx].label = 0
        self.corpus.ukllist.append(self.corpus.artlist[self.idx])
        if self.idx < len(self.corpus.artlist)-1 :
            self.idx += 1
        self.title = self.corpus.artlist[self.idx].title
        self.content = self.corpus.artlist[self.idx].content[0:2500]
        self.url = self.corpus.artlist[self.idx].url
        self.titletext.SetLabel(self.title)
        self.titletext.SetSize((900, 30))
        self.contenttext.SetLabel(self.url)
        self.contenttext.SetURL(self.url)
        self.contenttext.SetSize((900, 30))
        self.pagetext.SetLabel(str(self.idx)+'/'+str(len(self.corpus.artlist)))
        self.pagetext.SetSize((250, 30))

    def markUnknow(self, event):
        self.corpus.artlist[self.idx].label = 1
        self.corpus.uklist.append(self.corpus.artlist[self.idx])
        if self.idx < len(self.corpus.artlist)-1 :
            self.idx += 1
        self.title = self.corpus.artlist[self.idx].title
        self.content = self.corpus.artlist[self.idx].content[0:2500]
        self.url = self.corpus.artlist[self.idx].url
        self.titletext.SetLabel(self.title)
        self.titletext.SetSize((900, 30))
        self.contenttext.SetLabel(self.url)
        self.contenttext.SetURL(self.url)
        self.contenttext.SetSize((900, 30))
        self.pagetext.SetLabel(str(self.idx)+'/'+str(len(self.corpus.artlist)))
        self.pagetext.SetSize((250, 30))

    def frontPage(self, event):
        if self.idx > 0 :
            self.idx -= 1
        self.title = self.corpus.artlist[self.idx].title
        self.content = self.corpus.artlist[self.idx].content[0:2500]
        self.url = self.corpus.artlist[self.idx].url
        self.titletext.SetLabel(self.title)
        self.titletext.SetSize((900, 30))
        self.contenttext.SetLabel(self.url)
        self.contenttext.SetURL(self.url)
        self.contenttext.SetSize((900, 30))
        self.pagetext.SetLabel(str(self.idx)+'/'+str(len(self.corpus.artlist)))
        self.pagetext.SetSize((250, 30))

    def save(self, event):
        if self.idx < len(self.corpus.artlist)-1 :
            self.idx += 1
        self.conf.writeConf([self.idx])
        self.corpus.writeLabel('../data/labeling/label.txt')
        self.corpus.writeData('../output/labeling/money/unknowledgeable', \
        	'../output/labeling/money/unknow', '../output/labeling/money/knowledgeable')
        print 'already save'


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = StaticTextFrame()
    # frame.showArticle()
    frame.Show()
    app.MainLoop()