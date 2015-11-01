# -*- encoding = gb18030 -*-
import codecs
import numpy as np

def importData(datapath, outpath) :
    chardict = dict()
    with codecs.open(datapath, 'r', 'gb18030') as fo :
        dataset = [line.strip() for line in fo.readlines()]
    for data in dataset :
        for char in data :
            if char not in chardict :
                chardict[char] = 0
            chardict[char] += 1
    charlist = sorted(chardict.iteritems(), key=lambda x: x[1], reverse=True)
    with open(outpath, 'w') as fw :
        for char, number in charlist :
            fw.writelines(char.encode('gb18030') + '\n')

importData('../data/punctuation/title', '../data/punctuation/punc')