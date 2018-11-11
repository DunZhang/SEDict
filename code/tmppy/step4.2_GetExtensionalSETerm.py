# -*- coding: utf-8 -*-
import json
import re
import string
import jellyfish
import random
import codecs
from gensim.models import Word2Vec, FastText
from sklearn.externals import joblib
import networkx as nx
import pandas as pd
from datetime import date
from copy import deepcopy
from SEUtils import filterTerms, getLoc
import numpy as np
import time
"""
主要根据高质量术语获取外扩术语
"""

def getMostSimWords(m=None,modelName="word2vec"):
    """
    为每个高质量软工术语获取最相似的500个单词
    :param modelName:
    :return:
    """
    if(m is  None):
        if (modelName.lower() == "fasttext"):
            m = FastText.load("../result/step3.1_FastText/step3.1_FastText.m")
        else:
            m = Word2Vec.load("../result/step3.1_skipgram/step3.1_skipgram.m")
            m.delete_temporary_training_data(True)

    HiQSETerms = list(joblib.load("../result/step4.1_HiQSETerm.dict").keys())

    res = {}
    count = 0
    for i in HiQSETerms:
        count += 1
        if (count % 1000 == 0):
            print (count)
        try:
            res[i] = m.wv.most_similar(i, topn=500)
        except:
            pass
    fw = codecs.open("../result/step4.2.1_MostSimWords_" + modelName.lower() + ".json", "w", encoding="utf-8")
    fw.write(json.dumps(res))
    fw.close()


def __filterSimWord(key, simWord, m):
    """
    判断key的近义词simWord是否合格
    """
    # 近义词首字母是.
    try:
        if (simWord[0] == "."):
            if (m.wv.similarity(key, simWord[1:]) > 0.73):
                return False
        # 近义词最后字母是.
        if (simWord[-1] == "."):
            if (m.wv.similarity(key, simWord[0:-1]) > 0.73):
                return False
    except:
        pass
    # 都是近义词相点的情况：  ie11.ie8.ie9
    t = str(simWord).split(".")
    tt = []
    for i in t:
        if len(i) > 0:
            tt.append(i)
    count = 0
    if (len(tt) > 1):
        for i in tt:
            try:
                if (m.wv.similarity(key, i) > 0.73):
                    count += 1
            except:
                pass
        if (count == len(tt)):
            return False
    # 去除一些符号后若完全相等，则不作为术语
    if (str(key).translate(string.maketrans("", ""), string.punctuation + " _-") == str(simWord).translate(
            string.maketrans("", ""), string.punctuation + " _-")):
        return False
    # key就存在近义词中的情况
    if (key in simWord):
        if (len(simWord.replace(key, "")) == 0):
            return False
        try:
            if (m.wv.similarity(key, simWord.replace(key, "")) > 0.73):
                return False
        except:
            pass
    # .不在key中，但是在近义词中的情况
    if ("." not in key):
        if ("." in simWord):
            t = simWord.split(".")
            if (key in t):
                return False
        return True
    return True


def __filterSimWords(key, simWords, m, stopWords_set):
    """
    每个高质量软工术语可以获得一组同义词，本函数抽取靠谱的同义词
    :param key:
    :param simWords:
    :param m:
    :param stopWords_set:
    :return:
    """
    res = []
    for i in simWords:
        if (i[1] < 0.73):
            break
        if (not filterTerms(i[0], stopWords_set)):
            continue
        if (__filterSimWord(key, i[0], m)):
            res.append(i)
        if (len(res) > 20):  # 最多生成20个同义词
            break
    return res


def filterMostSimWords(modelName="FastText", model=None):
    """
    过滤所有的软工高质量术语的同义词
    :return:
    """
    if (model is not None):
        m = model
    else:
        if (modelName.lower() == "fasttext"):
            m = FastText.load("../result/step3.1_FastText/step3.1_FastText.m")
        else:
            m = Word2Vec.load("../result/step3.1_skipgram/step3.1_skipgram.m")
            m.delete_temporary_training_data(True)
    stopWords_set = joblib.load("../result/stopWords.set")
    fr = codecs.open("../result/step4.2.1_MostSimWords_" + modelName.lower() + ".json", "r", encoding="utf-8")
    di = json.load(fr)
    fr.close()
    for key in di:
        di[key] = __filterSimWords(key, di[key], m, stopWords_set)
#        if(key=="c"):
#            print di["c"]
    # 保存di
    fw = codecs.open("../result/step4.2.2_MostSimWords_filtered_" + modelName.lower() + ".json", "w", encoding="utf-8")
    fw.write(json.dumps(di))
    fw.close()
    # 保存成csv
    data = []
    for key in di:
        if(len(di[key])==0):
            data.append([key,None,None])
            continue
        for value in di[key]:
            t = [key]
            t.extend(value)
            data.append(t)
    pd.DataFrame(data, columns=["SETerm", "Synonym", "Similarity"]).to_csv(
        "../result/step4.2.2_MostSimWords_filtered_" + modelName.lower() + ".csv", encoding="utf-8", index=False
    )


def filterAccordingToSO_WikiTimes(modelName):
    f = codecs.open("../result/step1.3_SOVocabulary.json", encoding="utf-8")
    vocab_so = json.load(f)
    f.close()
    f = codecs.open("../result/step1.1_WikiVocabulary.json", encoding="utf-8")
    vocab_wiki = json.load(f)
    f.close()
    count_so = 2471663568.0
    count_wiki = 3158666603.0
    fr = codecs.open("../result/step4.2.2_MostSimWords_filtered_" + modelName.lower() + ".json", "r", encoding="utf-8")
    di = json.load(fr)
    fr.close()
    new_di = {}
    for key in di:
        t = []
        for i in di[key]:
            if (i[1] < 0.88):
                if (vocab_so[i[0]] < 44):
                    continue
                if (i[0] in vocab_wiki):
                    if (((vocab_so[i[0]] / count_so) / (vocab_wiki[i[0]] / count_wiki)) < 10.0):
                        continue
            t.append(i)
        new_di[key] = t
    di = new_di
    fw = codecs.open("../result/step4.2.3_MostSimWords_filtered_" + modelName.lower() + ".json", "w",
                     encoding="utf-8")
    fw.write(json.dumps(di))
    fw.close()
    # 保存成csv
    data = []
    for key in di:
        if(len(di[key])==0):
            data.append([key,None,None])
            continue
        for value in di[key]:
            t = [key]
            t.extend(value)
            data.append(t)
    pd.DataFrame(data, columns=["SETerm", "Synonym", "Similarity"]).to_csv(
        "../result/step4.2.3_MostSimWords_filtered_"+ modelName.lower()+".csv", encoding="utf-8", index=False
    )


def generateFinalSETerm(modelName):
    fr = codecs.open("../result/../result/step4.2.3_MostSimWords_filtered_" + modelName.lower() + ".json", "r",
                     encoding="utf-8")
    di = json.load(fr)
    fr.close()
    res = []
    for i in di:
        res.append(i)
        for j in di[i]:
            res.append(j[0])
    termSet = set(res)
    termList = list(termSet)
    joblib.dump(termSet, "../result/step4.2.4_ExtSETerm_" + modelName.lower() + ".set")
    joblib.dump(termList, "../result/step4.2.4_ExtSETerm_" + modelName.lower() + ".list")
    print (len(termList))
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
# def getAllSimilarity(modelName="FastText",model=None,num_batch=0,numWords=92265,batch_size=10000000 ):
#     """
#     batch_size=10000000    10^7
#     :param modelName:
#     :param model:
#     :param num_batch:
#     :return:
#     """
#     termList=joblib.load("../result/step4.2_ExtSETerm_"+modelName.lower()+".list")
#     if (model is not None):
#         m = model
#     else:
#         if (modelName.lower() == "fasttext"):
#             m = FastText.load("../result/step3.1_FastText/step3.1_FastText.m")
#         else:
#             m = Word2Vec.load("../result/step3.1_skipgram/step3.1_skipgram.m")
#             m.delete_temporary_training_data(True)
#     ###################
#     start,end=int(num_batch*batch_size),int((num_batch+1)*batch_size)#[start,end)
#     if(end>int((numWords**2-numWords)//2+numWords)):
#         end=int((numWords**2-numWords)//2+numWords)
#         print ("This is the last compution")
#     if(start>end):
#         return False
#     data = np.ndarray(shape=(1, end - start), dtype=np.uint8)
#     count = end - start
#     ind=0
#     flag=False
#     for i in xrange(numWords):
#         for j in xrange(i+1):
#             if(not flag):
#                 if((((i+1)*i)//2+j)>=start):
#                     flag=True
#                 else:
#                     continue
#             sim=m.wv.similarity(termList[i],termList[j])
#             if(sim<0):
#                 sim=0
#             data[0,ind]=sim*100
#             ind+=1
#             if(ind % 1000000==0):
#                 print (num_batch,ind)
#             if(ind==count):
#                 joblib.dump(data,"../result/step4.2_similarities_"+modelName.lower()+"_"+str(num_batch)+".array")
#                 return True
# def getAllSimilarityArray(num_batch=0,batch_size=20000,numWords=92265):
#
#     #[start,end)
#     start=int(num_batch*batch_size)
#     end=int((num_batch+1)*batch_size)
#     if(end>=numWords):
#         end=numWords
#         print("last compute")
#     data=np.ndarray(shape=(end-start,numWords),dtype=np.uint8)
#     wordSimilities=joblib.load("../result/step4.2_similarities.array")
#     for i in xrange(data.shape[0]):
#         if(i%1000==0):
#             print (i)
#         for j in xrange(numWords):
#             data[i,j]=wordSimilities[0,getLoc(i+start,j)]
#     del wordSimilities
#     joblib.dump(data,"step4.2_similarities_array_"+str(num_batch)+".array")


def getAllSimilarityArray(m=None, modelName="word2vec", num_batch=0, batch_size=800):
    # [start,end)
    SETermList = joblib.load("../result/step4.2.4_ExtSETerm_" + modelName.lower() + ".list")
    rowStart = int(num_batch * batch_size)
    rowEnd = int((num_batch + 1) * batch_size)
    if (rowEnd > len(SETermList)):
        rowEnd = len(SETermList)
    if (rowStart >= rowEnd):
        print("already finished")
        return False
    data = np.ndarray(shape=(rowEnd - rowStart, len(SETermList)), dtype=np.uint8)
    for i in xrange(rowStart, rowEnd, 1):
#        for j in xrange(len(SETermList)):
        for j in xrange(i+1):
            sim = m.wv.similarity(SETermList[i], SETermList[j])
            if (sim < 0):
                sim = 0
            data[i - rowStart, j] = sim * 100
    joblib.dump(data,
                "../result/step4.2_WordsSims_" + modelName.lower() + "/step4.2_similarities_array_" + modelName.lower() + "_" + str(
                    num_batch) + ".array")


if (__name__ == "__main__"):
    # step 4.2.1 为高质量软工术语获取最相似的500个单词
#    m = Word2Vec.load("../result/step3.1_skipgram/step3.1_skipgram.m")
#    m.delete_temporary_training_data(True)
#    getMostSimWords(m=None,modelName="Word2Vec")
# step 4.2.2 过滤每个术语的相似度最高的500个单词
#    filterMostSimWords("word2vec")
# step 4.2.3 根据SOTimes进一步过滤
#    filterAccordingToSO_WikiTimes(modelName="word2vec")
# step 4.2.4 generateSETermSet
#    generateFinalSETerm(modelName="word2vec")
# step4.2.5 get all similities for every word
#    m = Word2Vec.load("../result/step3.1_skipgram/step3.1_skipgram.m")
#    m.delete_temporary_training_data(True)
#    print(m.wv.most_similar("c",topn=10))
#    print(time.localtime())
#    for i in xrange(40,46):
#        print i
#        getAllSimilarityArray(m=m,modelName="word2vec",num_batch=i,batch_size=800)
#    data=[]
#    for i in xrange(62):
#        print i
#        data.append(joblib.load("../result/step4.2_WordsSims_word2vec/step4.2_similarities_array_word2vec_" + str(i) + ".array"))
#    data=np.vstack(data)
#    for i in xrange(data.shape[0]):
#        for j in xrange(i,data.shape[1]):
#            data[i,j]=data[j,i]
#    joblib.dump(data,"../result/step4.2_WordsSims_word2vec/step4.2_all_similarities_array_word2vec.array")
