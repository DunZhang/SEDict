# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 14:16:54 2018

@author: Administrator
清洗so数据；检测短语；保存短语到本地
"""
from multiprocessing import Queue, Value, Process
import codecs
from bs4 import BeautifulSoup
from lxml import etree
import re
from collections import defaultdict
import logging
import json
from sklearn.externals import joblib
import time
import gc
from gensim.models import Word2Vec,FastText
from gensim.models.phrases import Phrases, Phraser,npmi_scorer,original_scorer
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
def readSOXML(g_DataQueue, g_FinishRead, filePath):
    """
    step1.2.1 读取Posts数据
    :param g_DataQueue: 存储数据的队列，将被存到数据库
    :param g_FinishRead:是否读取完xml，0是没有读完，1是读完
    :param filePath:xml文件地址
    :return:无
    """
    context = etree.iterparse(filePath, encoding="utf-8")
    datas = []  # 存储title 和 answers
    c = 0
    for _, elem in context:  # 迭代每一个
        c += 1
        if (c % 100000 == 0):
            print("already pasrse record:", str(c / 10000) + "W")
        title, body, typeId = elem.get("Title"), elem.get("Body"), elem.get("PostTypeId")
        elem.clear()
        if (typeId is None):
            continue
        if (int(typeId) != 1 and int(typeId) != 2):
            continue
        if (body is not None):
            soup = BeautifulSoup(body, "lxml")
            for pre in soup.find_all("pre"):
                if (len(pre.find_all("code")) > 0):
                    pre.decompose()
            datas.append(soup.get_text())
        if (title is not None):
            datas.append(BeautifulSoup(title, "lxml").get_text())
        if (len(datas) > 100000):
            g_DataQueue.put(datas)
            print (g_DataQueue.qsize())
            datas = []

    if (len(datas) > 0):
        g_DataQueue.put(datas)
        datas = []
    g_FinishRead.value = 1


def saveCleanSOToLocal(g_DataQueue, g_FinishRead, filePath):
    """
    Step1.2.1 将数据存储到本地
    :param g_DataQueue: 公共队列放置数据
    :param g_FinishRead: 0还没有放完，1已经放完了
    :param filePath: 文件存储路径
    :return:
    """
    fw = codecs.open(filePath, "w", encoding="utf-8")
    reSub0 = re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")  # URL
    reSub1 = re.compile("[\[\]<>`~$\^&*=|%@(){},:\"/'\\\\]")  # replace with " "
    rePlus = re.compile("[^+]\+[^+]")
    reSplit1 = re.compile("\.[^a-z0-9]|[?!;\n\r]")
    sentences = []
    while (g_FinishRead.value == 0 or (not g_DataQueue.empty())):
        datas = g_DataQueue.get()
        for strText in datas:
            strText = strText.lower()

            strText = re.sub(reSub0, " ", strText)
            strText = re.sub(reSub1, " ", strText)
            # 开始处理最复杂的加号情况
            for sub in set(re.findall(rePlus, strText)):
                strText = strText.replace(sub, sub[0] + " " + sub[2])

            strText=strText.replace("-","_")
            for sentence in re.split(reSplit1, strText):
                if (len(sentence.split()) > 6):
                    sentence += "\n"
                    sentences.append(sentence)
        if (len(sentences) > 500000):
            fw.writelines(sentences)
            sentences = []
    if (len(sentences) > 0):
        fw.writelines(sentences)
    fw.close()


class SOTxtIter(object):
    """
    step1.2.2短语迭代器，bigram若为None，就是不经处理直接迭代
    """

    def __init__(self, path, bigram):
        self.times = 0
        self.path = path
        self.bigram = bigram
        pass

    def __iter__(self):
        self.times += 1
        count = 0
        fread = codecs.open(self.path, "r", encoding="utf-8")
        if (self.bigram is None):
            for line in fread:
                count += 1
                if (count % 500000 == 0):
                    logger.warning("step" + str(self.times) + ": already processe:" + str(count / 10000) + "w")
                yield line.split()
            fread.close()
        else:
            for line in fread:
                count += 1
                if (count % 500000 == 0):
                    logger.warning("step" + str(self.times) + ": already processe:" + str(count / 10000) + "w")
                yield self.bigram[line.split()]
            fread.close()


#def ff(worda_count, wordb_count, bigram_count):
#    return original_scorer(worda_count, wordb_count, bigram_count, 11, 1, None)
def SavePhrase(filePath,bigram,trigram,savePath):
    """
    :param filePath:
    :param bigram:
    :param trigram:
    :param savePath:
    :return:
    """
    fr = codecs.open(filePath, "r", encoding="utf-8")
    fw = codecs.open(savePath, "w", encoding="utf-8")
    sens = []
    c = 0
    for line in fr:
        c += 1
        if (c % 500000 == 0):
            print(str(c / 10000) + "w")
        sens.append(line.split())
        if (len(sens) > 10000):
            tres = []
            if(trigram is not  None):
                for x in trigram[bigram[sens]]:
                    tres.append(u" ".join(x))
                    tres.append("\n")
            else:
                for x in bigram[sens]:
                    tres.append(u" ".join(x))
                    tres.append("\n")
            fw.writelines(tres)
            del tres
            del sens
            sens = []
    if (len(sens) > 0):
        tres = []
        if (trigram is not None):
            for x in trigram[bigram[sens]]:
                tres.append(u" ".join(x))
                tres.append("\n")
        else:
            for x in bigram[sens]:
                tres.append(u" ".join(x))
                tres.append("\n")
        fw.writelines(tres)
    fw.close()
    fr.close()

if (__name__ == "__main__"):
    #################################################################################################
    # In[] step1.2.1 清洗SO数据并存储到本地，存储到txt文件中，一行为一句话

    # g_DataQueue = Queue(10)  # 一次最多只有1000组数据放到内存中
    # g_FinishRead = Value("I", 0)
    # readProc = Process(target=readSOXML, args=(g_DataQueue, g_FinishRead, "../data/Posts.xml"))
    # writeProc = Process(target=saveCleanSOToLocal, args=(g_DataQueue, g_FinishRead,"C:/SE/step1.2.1_SOCleaned_V1.txt"))
    # readProc.start()
    # writeProc.start()
    # readProc.join()
    # writeProc.join()
    # print("done!!!!!!!!!!!!!!")
    # In[] step1.2.2 训练praser
    # 训练bigram
    # so=SOTxtIter("C:/SE/step1.2.1_SOCleaned_V1.txt",None)
    # bigram=Phrases(sentences=so,max_vocab_size=40000000,min_count=15 ,threshold=10)
    # bigram.save("../result/step1.2.2_bigram_V1.m")
    # del bigram
    # del so
    # gc.collect()
    # time.sleep(30)
    # 训练trigram
    for i in [0.7]:
        bigram = Phrases.load("../result/step1.2.2_bigram_V1.m")
        bigram.scoring=npmi_scorer
        bigram.threshold=i
        bigram=Phraser(bigram)
        so=SOTxtIter("C:/SE/step1.2.1_SOCleaned_V1.txt",bigram)
    ##
        trigram = Phrases(sentences=so, min_count=15, threshold=i, max_vocab_size=40000000,scoring="npmi")
        trigram.save("../result/step1.2.2_trigram_15_"+str(i)+"_npmi_V1.m")

        trigram=Phraser(trigram)
        time.sleep(30)
    # In[] step1.2.3 get and save trigramlist
    #    bigram = Phraser(Phrases.load("../result/step1.2.2_bigram_V1.m"))
    #    trigram = Phraser(Phrases.load("../result/step1.2.2_trigram_V1.m"))
        SavePhrase("C:/SE/step1.2.1_SOCleaned_V1.txt",bigram,trigram,"C:/SE/step1.2.3_SOTrigramList_15_"+str(i)+"_npmi_V1.txt")
        del bigram
        del trigram
        gc.collect()
        time.sleep(30)
    # In[] step1.2.4 gengerate and  vocabso
        fr = codecs.open("C:/SE/step1.2.3_SOTrigramList_15_"+str(i)+"_npmi_V1.txt", "r", encoding="utf-8")
        vocab_so = defaultdict(int)
        c=0
        for line in fr:
            c+=1
            if (c % 500000 == 0):
                print(str(c / 10000) + "w")
            for word in line.split():
                vocab_so[word] += 1
        with codecs.open("../result/step1.2.4_SOVocabulary_15_"+str(i)+"_npmi_V1.json", "w", encoding="utf-8") as fw:
           fw.write(json.dumps(vocab_so))
        fr.close()
        del vocab_so
        gc.collect()

#####################################################################################################################################
    # In[] 寻找阈值
#    bigram =Phrases.load("../result/step1.2.2_bigram_V1.m")
#    bigram.scoring=npmi_scorer
#    bigram.threshold=0.6
#    bigram.min_count=15
##    
##    
#    pr=Phraser(bigram)
#    SavePhrase("C:/SE/step1.2.1_SOCleaned_V1.txt",bigram,None,"E:/watch0.6.txt")
#    print( )    
    
#    pass
# In[]
#    s=[["this","is","test","a"],["this","is","st","a"],["this","is","tst","a"],["this","no","test","a"] ]
#     
#    big=Phrases(s,min_count=1,threshold=5)
#    vv=big.vocab
#    big.scoring=npmi_scorer
#    big.threshold=2
    
#    print( Phraser(big)[["this","is","test","a"]])
    
#    fr=codecs.open("C:/SE/step1.2.3_SOTrigramList_V1.txt")
#    datas=[]
#    for i in fr:
#        print(re.sub("(a)|(use)","(a_)|(c)",i))
#        break
#    fr.close()






















