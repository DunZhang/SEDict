# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 23:14:01 2018

@author: Administrator
"""

import codecs
import gc
import json
import re
import random
from multiprocessing import Queue, Value, Process
from xml import sax
from sklearn.externals import joblib
from bs4 import BeautifulSoup
from gensim.models.phrases import Phrases, Phraser


def readWikiXML(g_DataQueue, g_FinishRead):
    handler = xmlHandler(g_DataQueue, g_FinishRead)
    parser = sax.make_parser()
    parser.setContentHandler(handler)
    parser.parse("../data/enwiki-latest-pages-articles.xml")


def trainPhrase(g_DataQueue, g_FinishRead, savePath, priorPhrasePath):
    count = 0
    phrase = Phrases(None, min_count=10, threshold=15)
    if (priorPhrasePath is None):
        priorPhraser = None
    else:
        priorPhraser = Phraser(Phrases.load(priorPhrasePath))
    while (g_FinishRead.value == 0 or (not g_DataQueue.empty())):
        words = g_DataQueue.get()
        if (priorPhraser is None):  # 第一次训练
            phrase.add_vocab(words)
        else:  # 已经训练过一次，寻找个数更多的短语
            phrase.add_vocab(priorPhraser[words])
        del words
        gc.collect()
    phrase.save(savePath)


def getTrigramList(g_DataQueue, g_FinishRead, savePath, bigramPath, trigramPath):
    """

    :param g_DataQueue:
    :param g_FinishRead:
    :param savePath:保存字典路径
    :param bigramPath:
    :param trigramPath:
    :return:
    """
    count = 0
    vocabulary_dic = {}
    bigram = Phraser(Phrases.load(bigramPath))
    trigram = Phraser(Phrases.load(trigramPath))
    while (g_FinishRead.value == 0 or (not g_DataQueue.empty())):
        words = g_DataQueue.get()
        count += len(words)
        print("have processed sentences:", count)
        # 获取短语
        trigram_list = trigram[bigram[words]]
        del words
        gc.collect()
        # 放入字典中
        for phrase_list in trigram_list:
            for phrase in phrase_list:
                if phrase not in vocabulary_dic:
                    vocabulary_dic[phrase] = 0
                vocabulary_dic[phrase] += 1
    # 存入本地
    fw = codecs.open(savePath, "w", encoding="utf-8")
    fw.write(json.dumps(vocabulary_dic))
    fw.close()
    del vocabulary_dic
    gc.collect()


class xmlHandler(sax.ContentHandler):
    def __init__(self, g_DataQueue, g_FinishRead):
        self.currentTag = ""
        self.cont = ""  # 保存每一次的text的文本,相当于一篇文章
        self.batch_size = 2000  # 一次存的文章数目，存到这个数目后往队列里放
        self.g_DataQueue = g_DataQueue
        self.g_FinishRead = g_FinishRead
        self.batch_data = []  # 存了很多篇文章
        self.count=0
        self.zd=0
        ######################################################
        # 预编译一部分    替换匹配模式节省时间
        self.patterns = []
        self.patterns.append(re.compile("\[\[file[\s\S]*?\]\][\r\n]"))  # 匹配[[file开始的段落
        self.patterns.append(re.compile("\[\[image[\s\S]*?\]\][\r\n]"))  # 匹配[[image开始的段落
        self.patterns.append(re.compile("\[\[category[\s\S]*?\]\][\r\n]"))  # 匹配[[category开始的段落
        self.patterns.append(re.compile(r"{{[\s\S]*?}}"))  # filter {{}} 最小匹配
        self.patterns.append(
            re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]"))  # filter URL
        self.patterns.append(re.compile("\[\[[^]]*?\|"))  # 过滤[[ content|
        self.patterns.append("[']{2,3}")  # ''  '''
        self.patterns.append(re.compile("[\[\(\),:\"\}=]|[^a-z]'|'[^a-z;?.!]"))  # 一些替换
        #预编译一部分  文章无用section
        self.patterns_sect=[]
        self.patterns_sect.append(re.compile("[=]{2,8} footnotes [=]{2,8}"))
        self.patterns_sect.append(re.compile("[=]{2,8} endnotes [=]{2,8}"))
        self.patterns_sect.append(re.compile("[=]{2,8} references [=]{2,8}"))
        self.patterns_sect.append(re.compile("[=]{2,8} external links [=]{2,8}"))
        self.patterns_sect.append(re.compile("[=]{2,8} 	criticisms [=]{2,8}"))
        self.patterns_sect.append(re.compile("[=]{2,8} 	see also [=]{2,8}"))
        self.patterns_sect.append(re.compile("[=]{2,8} further reading [=]{2,8}"))
        self.patterns_sect.append(re.compile("[=]{2,8} sources [=]{2,8}"))
        self.patterns_sect.append(re.compile("[=]{2,8} bibliography [=]{2,8}"))
        self.patterns_sect.append(re.compile("[=]{2,8} publications [=]{2,8}"))
    def passageToWords(self, content):
        words = []
        # Step1 获取HTML文本
        content = content.strip().lower()
        content = BeautifulSoup(content, "lxml").get_text()
        # Step 2正则表达式过滤噪音
            #先过滤没必要的section
        ins=[]
        for pat in self.patterns_sect:
            patt=re.search(pat,content)
            if(patt is not None):
                ins.append(patt.span()[0])
        if(len(ins)>0):
            content=content[0:min(ins)]
        re5 = re.compile("\]")  # 不使用空格替换
        reSplit1 = re.compile("\.[^a-z0-9]|[?!;\r\n]")
        for pat in self.patterns:
            content = re.sub(pat, " ", content)
        content = re.sub(re5, "", content)
        # 分句分词

        for sent in re.split(reSplit1, content):
            sen_word = sent.split()
            if (len(sen_word) > 4):
                if (sen_word[0] != "|" and sen_word[0] != "*"):
                    words.append(sen_word)
        return words

    def allPassagesToWord(self):
        allWords = []
        for i in self.batch_data:
            allWords.extend(self.passageToWords(i))
        return allWords

    # 文档启动的时候调用
    def startDocument(self):
        print('XML开始解析中...')

    # 元素开始事件处理
    def startElement(self, name, attrs):
        self.currentTag = name

    # 内容事件处理
    def characters(self, content):
        if (self.currentTag == "text"):
            self.cont += content

    ###################################################
    # 元素结束事件处理
    def endElement(self, name):
        if (self.currentTag == "text"):
            if (len(self.cont) > 200):
                self.count+=1
                if(self.count%10000==0):
                    print("already sotre articles:",self.count)
                self.batch_data.append(self.cont)
                if (len(self.batch_data) == self.batch_size):  # 满了
                    self.g_DataQueue.put(self.allPassagesToWord())
                    self.batch_data = []

            self.currentTag = ""
            self.cont = ""

    # 文档结束的时候调用
    def endDocument(self):
        if (len(self.batch_data) > 0):
            self.g_DataQueue.put(self.allPassagesToWord())
            self.batch_data = []
        self.g_FinishRead.value = 1
        print("all wiki articles numers:",self.count)
        print('XML文档解析结束!')


if __name__ == '__main__':
    # step1.1.1 训练bigram
    # g_DataQueue = Queue(5)
    # g_FinishRead = Value("I", 0)
    # procRead = Process(target=readWikiXML, args=(g_DataQueue, g_FinishRead))
    # procPhrase = Process(target=trainPhrase,
    #                      args=(g_DataQueue, g_FinishRead, "../result/step1.1_bigram.m", None))
    # procRead.start()
    # procPhrase.start()
    # procPhrase.join()
    # procRead.join()
    # print("done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # step1.1.2 训练trigram
#    print(len(Phrases.load( "../result/step1.1_bigram.m").vocab))

    # g_DataQueue = Queue(5)
    # g_FinishRead = Value("I", 0)
    # procRead = Process(target=readWikiXML, args=(g_DataQueue, g_FinishRead))
    # procPhrase = Process(target=trainPhrase,
    #                      args=(g_DataQueue, g_FinishRead, "../result/step1.1_trigram.m", "../result/step1.1_bigram.m"))
    # procRead.start()
    # procPhrase.start()
    # procPhrase.join()
    # procRead.join()
    #
    #
    # print("done!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # procRead.terminate()
    # procPhrase.terminate()

    # step1.1.3 获取phrase
    # print("began to ge phrase")
    # g_DataQueue = Queue(5)
    # g_FinishRead = Value("I", 0)
    # procRead = Process(target=readWikiXML, args=(g_DataQueue, g_FinishRead))
    # procPhrase = Process(target=getTrigramList,
    #                      args=(g_DataQueue, g_FinishRead, "../result/step1.1_WikiVocabulary.json",
    #                            "../result/step1.1_bigram.m", "../result/step1.1_trigram.m"))
    # procRead.start()
    # procPhrase.start()
    # procPhrase.join()
    # procRead.join()
    # print("done!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # procRead.terminate()
    # procPhrase.terminate()
class tt(object):
    """
    step1.2.2短语迭代器，bigram若为None，就是不经处理直接迭代
    """
    def __init__(self):
        pass

    def __iter__(self):
        for line in [["you","are","good","dos"],["you","are","ss"],["you","are","dd"],["ssd","you","are","dd"]]:
            yield line

    ph=Phraser(Phrases(tt(),min_count=2, threshold=1))
    ph[["you","are","good"]]    
#    list(ph[["you","are","good"],["sss","you","are","good"]]   )
#    
#    di=dict([1,2,3])
