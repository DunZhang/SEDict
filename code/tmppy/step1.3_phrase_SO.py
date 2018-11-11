# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 17:59:12 2018

@author: Zhang Dun
从数据库中读取数据，去掉噪音，获得最长为三元组的短语，存到本地json文件
"""
from gensim.models.phrases import Phrases, Phraser
import codecs
import MySQLdb
from MySQLdb.cursors import SSCursor
import re
import gc
from multiprocessing import Queue, Value, Process
import json
from DBUtils.PooledDB import PooledDB

def readSODB(g_DataQueue, g_FinishRead):
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='so', port=3306,
                           charset='utf8mb4', cursorclass=SSCursor)
    curs = conn.cursor()
    sql_query = "select Title,Body from sodata"
    curs.execute(sql_query)
    batch_size = 50000  # 一次读取的记录数
    while (True):
        data = list(curs.fetchmany(batch_size))
        if (len(data) == 0):
            break
        g_DataQueue.put(data)
    curs.close()
    conn.close()
    g_FinishRead.value = 1  # 读取结束，设置标志位
def readSODB_FAST(g_DataQueue, g_FinishRead):
    pool = PooledDB(MySQLdb, 5, host='localhost', user='root', passwd='123456', db='so', port=3306,charset='utf8mb4',cursorclass=SSCursor)
    batch_size = 50000  # 一次读取的记录数
    i=0
    while (True):
        # print(i)
        conn = pool.connection()
        curs = conn.cursor()
        sql_query="SELECT Title,Body FROM sodata WHERE Id >= (select Id from sodata limit {0}, 1) limit {1}".format(str(i*batch_size),str(batch_size))

        curs.execute(sql_query)
        data = list(curs.fetchmany(batch_size))
        # print(len(data))
        if (len(data) == 0):
            break
        g_DataQueue.put(data)
        # for ii in data:
        #     print ii
        i+=1
        curs.close()
        del curs
        conn.close()
    pool.close()
    g_FinishRead.value = 1  # 读取结束，设置标志位

def trainSOPhrase(g_DataQueue, g_FinishRead, savePath, priorPhrasePath):
    """

    :param g_DataQueue:全局变量存放数据库中的数据
    :param g_FinishRead:是否读取完数据库的标志
    :param savePath:短语学习器保存的位置
    :param priorPhrasePath:前一个学习器保存的位置
    :return:
    """
    count = 0
    phrase = Phrases(None, min_count=10, threshold=15)
    if (priorPhrasePath is None):
        priorPhraser = None
    else:
        priorPhraser = Phraser(Phrases.load(priorPhrasePath))
    while (g_FinishRead.value == 0 or (not g_DataQueue.empty())):
        data = g_DataQueue.get()
        count += len(data)
        print("have processed:", count)
        words = []
        reSub0 = re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")  # URL
        reSub1 = re.compile("[()\"{},:/-]|[^a-z]'|'[^a-z;?.!]|'$")  # replace with " "
        reSub2 = re.compile("'[.?;!]")  # replace with . 主要考虑所有格问题，核心思想单引号左右的各种复杂情况
        reSplit1 = re.compile("\.[^a-z0-9]|[?!;]")
        # 获取单词
        for t in data:
            if (t[0] is not None):
                st = re.sub(reSub0, " ", t[0].lower())
                st = re.sub(reSub1, ".", st)
                st = re.sub(reSub2, ".", st)
                for sentence in re.split(reSplit1, st):
                    sen_word = sentence.split()
                    if (len(sen_word) > 6):
                        words.append(sen_word)
            if (t[1] is not None):
                st = re.sub(reSub0, " ", t[1].lower())
                st = re.sub(reSub1, ".", st)
                st = re.sub(reSub2, ".", st)
                for sentence in re.split(reSplit1, st):
                    sen_word = sentence.split()
                    if (len(sen_word) > 6):
                        words.append(sen_word)
        del data
        gc.collect()
        # 训练短语
        if (priorPhraser is None):  # 第一次训练
            phrase.add_vocab(words)
        else:  # 已经训练过一次，寻找个数更多的短语
            phrase.add_vocab(priorPhraser[words])
        del words
        # print(len(phrase.vocab))
        gc.collect
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
        data = g_DataQueue.get()
        count += len(data)
        print("have processed:", count)
        words = []
        reSub0 = re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")  # URL
        reSub1 = re.compile("[()\"{},:/-]|[^a-z]'|'[^a-z;?.!]|'$")  # replace with " "
        reSub2 = re.compile("'[.?;!]")  # replace with . 主要考虑所有格问题，核心思想单引号左右的各种复杂情况
        reSplit1 = re.compile("\.[^a-z0-9]|[?!;]")
        # 获取单词
        for t in data:
            if (t[0] is not None):
                st = re.sub(reSub0, " ", t[0].lower())
                st = re.sub(reSub1, ".", st)
                st = re.sub(reSub2, ".", st)
                for sentence in re.split(reSplit1, st):
                    sen_word = sentence.split()
                    if (len(sen_word) > 6):
                        words.append(sen_word)
            if (t[1] is not None):
                st = re.sub(reSub0, " ", t[1].lower())
                st = re.sub(reSub1, ".", st)
                st = re.sub(reSub2, ".", st)
                for sentence in re.split(reSplit1, st):
                    sen_word = sentence.split()
                    if (len(sen_word) > 6):
                        words.append(sen_word)
        del data
        gc.collect()
        # 获取短语
        trigram_list = trigram[bigram[words]]
        del words
        gc.collect
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
def saveTrigramList(g_DataQueue, g_FinishRead, bigramPath, trigramPath):
    """

    :param g_DataQueue:
    :param g_FinishRead:
    :param bigramPath:
    :param trigramPath:
    :return:
    """
    count = 0
    bigram = Phraser(Phrases.load(bigramPath))
    trigram = Phraser(Phrases.load(trigramPath))
    fw=codecs.open("../result/step1.3_SO_TrigramList.txt","w",encoding="utf-8")
    while (g_FinishRead.value == 0 or (not g_DataQueue.empty())):
        data = g_DataQueue.get()
        count += len(data)
        print("have processed:", count)
        words = []
        reSub0 = re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")  # URL
        reSub1 = re.compile("[()\"{},:/-]|[^a-z]'|'[^a-z;?.!]|'$")  # replace with " "
        reSub2 = re.compile("'[.?;!]")  # replace with . 主要考虑所有格问题，核心思想单引号左右的各种复杂情况
        reSplit1 = re.compile("\.[^a-z0-9]|[?!;]")
        # 获取单词
        for t in data:
            if (t[0] is not None):
                st = re.sub(reSub0, " ", t[0].lower())
                st = re.sub(reSub1, ".", st)
                st = re.sub(reSub2, ".", st)
                for sentence in re.split(reSplit1, st):
                    sen_word = sentence.split()
                    if (len(sen_word) > 6):
                        words.append(sen_word)
            if (t[1] is not None):
                st = re.sub(reSub0, " ", t[1].lower())
                st = re.sub(reSub1, ".", st)
                st = re.sub(reSub2, ".", st)
                for sentence in re.split(reSplit1, st):
                    sen_word = sentence.split()
                    if (len(sen_word) > 6):
                        words.append(sen_word)
        del data
        gc.collect()
        # 获取短语
        trigram_list = trigram[bigram[words]]
        del words
        gc.collect()
        # 放入本地文件中
        tres=[]
        for phrase_list in trigram_list:
            sent=u" ".join(phrase_list)
            tres.append(sent)
            tres.append("\n")
        fw.writelines(tres)
        del trigram_list
        del tres
        gc.collect()
    fw.close()


if __name__ == '__main__':
    # step1.3.1 训练bigram模型
    # g_DataQueue = Queue(10)
    # g_FinishRead = Value("I", 0)
    # procRead = Process(target=readSODB, args=(g_DataQueue, g_FinishRead))
    # procPhrase = Process(target=trainSOPhrase,
    #                      args=(g_DataQueue, g_FinishRead, "../result/step1.3_bigram.m", None))
    # procRead.start()
    # procPhrase.start()
    # procPhrase.join()
    # procRead.join()
    # print("done!!!!!!!!!!!!!!!!!!!!!!!!!!")

    # step1.3.2 训练trigram模型

    # g_DataQueue = Queue(6)
    # g_FinishRead = Value("I", 0)
    # procRead = Process(target=readSODB_FAST, args=(g_DataQueue, g_FinishRead))
    # procPhrase = Process(target=trainSOPhrase,
    #                      args=(g_DataQueue, g_FinishRead, "../result/step1.3_trigram.m", "../result/step1.3_bigram.m"))
    # procRead.start()
    # procPhrase.start()
    # procPhrase.join()
    # procRead.join()
    # print("done!!!!!!!!!!!!!!!!!!!!!!!!!!")

    # step.1.3.3 获取词组包括single word
    # g_DataQueue = Queue(10)
#     # g_FinishRead = Value("I", 0)
#     # procRead = Process(target=readSODB_FAST, args=(g_DataQueue, g_FinishRead))
#     # procPhrase = Process(target=getTrigramList,
#     #                      args=(g_DataQueue, g_FinishRead, "../result/step1.3_SOVocabulary.json","../result/step1.3_bigram.m", "../result/step1.3_trigram.m"))
#     # procRead.start()
#     # procPhrase.start()
#     # procPhrase.join()
#     # procRead.join()
#     # print("done!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #step1.3.4 把获取到的短语存到本地文件中
    g_DataQueue = Queue(5)
    g_FinishRead = Value("I", 0)
    procRead = Process(target=readSODB_FAST, args=(g_DataQueue, g_FinishRead))
    procPhrase = Process(target=saveTrigramList,
                         args=(g_DataQueue, g_FinishRead,"../result/step1.3_bigram.m", "../result/step1.3_trigram.m"))
    procRead.start()
    procPhrase.start()
    procPhrase.join()
    procRead.join()
    print("done!!!!!!!!!!!!!!!!!!!!!!!!!!")