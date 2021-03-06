# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 12:44:29 2018

@author: Administrator
"""

import json
import re
import string
import jellyfish
import random
import codecs
from gensim.models import Word2Vec,FastText
from sklearn.externals import  joblib
import networkx as nx
import pandas as pd
from datetime import date
from copy import deepcopy
import random
import gc
from gensim.models.word2vec import LineSentence
import time
from SEUtils import filterTerms,isSynonym,isAbrreviation
from collections import defaultdict
import logging
import math
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
def f(s):
    t=deepcopy(s)
    for c in (string.punctuation.replace(".","") + " _-"):
        t=t.replace(c,"")
    return t


def GetSemanticallyRelatedTerms(modelName="word2vec",modelPath="",SETermPath="",
                                savePath=""):
    """
    step4.2.1 为每一个术语获取近义词组
    """
    if (modelName.lower() == "fasttext"):
        m = FastText.load(modelPath)
    else:
        m = Word2Vec.load(modelPath)
        m.delete_temporary_training_data(True)    
    SETerms = joblib.load(SETermPath)
    di={}
    c=0
    for i in SETerms:
        c+=1
        if(c%500==0):
            print (c)
        if i not in m.wv.vocab:
            continue       
        t=m.wv.most_similar(i,topn=600)
        value=[]
        for j in t:
            if(j[1]<0.5):
                break
            value.append(j)
        di[i]=value
#        di[i]=1
    del m
    gc.collect()
    joblib.dump(di,savePath) 
    return di
#def GetSemanticallyRelatedTermsMixedModel(fasttextDictPath="",word2vecDictPath="",savePath=""):
#    """
#    step4.2.1 为混合模型每一个术语获取近义词组
#    """
#    di1=joblib.load(fasttextDictPath)
#    print("already load",fasttextDictPath)
#    di2=joblib.load(word2vecDictPath)
#    print("already load",word2vecDictPath)
#    newDi={}
#    c=0
#    for key in di1:
#        c+=1
#        if c%500==0:
#            print(c)
#        t=[]
#        t1,t2=di1[key][0:100],di2[key][0:100]
#        for i in range(min(len(t2),len(t1))):
#            t.append(t2[i])
#            t.append(t1[i])
##        t.sort(key=lambda x : x[1],reverse=True)
#        newDi[key]=t
#    del di1
#    del di2    
#    joblib.dump(newDi,savePath)
#    return newDi
    
def FilterSemanticallyRelatedTerms(dictPath="",modelPath="",savePath=""):
    """
    step4.2.2 对近义词组进行过滤
    """
    stopWords_set = joblib.load("../result/stopWords.set")
    di = joblib.load(dictPath)
    newdi={}
    c=0
    for key in di:#对于每一个key
        c+=1
        if(c%500==0):
            print (c)         
        #开始过滤
        values=[] 
        for word_sim in di[key]:#对于key的每一value   
            i=word_sim[0]
            if "." not in key and "." in i:
                continue
            if "++" not in key and "+" in i:
                continue
            #过滤一次
            if (not filterTerms(i, stopWords_set)):
                continue   
            # 去除一些符号后若完全相等，则不作为术语
            if  f(key) == f(i):
                continue                    
            #开始处理 .和+的情况
            values.append(word_sim)
        newdi[key]=values
    joblib.dump(newdi,savePath)
    return newdi

def SelectSemanticallyRelatedTerms(threshold=0.1,topn=40,dictPath="",savePath=""):
    """
    step4.2.3 根据相似度选择一定数量的语义相关的单词
    """
    raw_dic = joblib.load(dictPath)
    di={}
    for key,value in raw_dic.items():
        t=[]
        for i in value:
            if(i[1]>threshold):
                t.append(i)
            else:
                continue
            if(len(t)>=topn):
                break
        di[key]=t
    joblib.dump(di,savePath)
    return di
def DiscriminateTerms(dictPath="",savePath=""):
    """
    step4.2.4 对近义词组做分类
    """
    raw_dic = joblib.load(dictPath)
    seperate_dic = {}  # store synonyms and abbreviation
    c=0
    for key in raw_dic:
        c+=1
        if(c%1000==0):
            print (c)
        t = [[], [],[]]  # 0abbreviation, 1synonyms and the 2 other
        for term in raw_dic[key]:
            if isSynonym(key, term[0]):
                t[1].append(term)
            elif isAbrreviation(key,term[0]):
                t[0].append(term)
            else:
                t[2].append(term)
        seperate_dic[key]=t 
    joblib.dump(seperate_dic,savePath)   
    return seperate_dic

def RemoveSimilarity(dictPath="",savePath=""):
    """
    step4.2.6
    """
    di=joblib.load(dictPath)
    newdi={}
    for key,value in di.items():
        t=[]
        t.append(    [x[0].replace(" ","_").replace("-","_") for x in value[0]]   )
        t.append(    [x[0].replace(" ","_").replace("-","_") for x in value[1]]   )
        t.append(    [x[0].replace(" ","_").replace("-","_") for x in value[2]]   )
        newdi[key]=t
    joblib.dump(newdi,savePath)    
    return newdi        
if(__name__=="__main__"):
    modelName="FastText"
    # In[] step4.2.1 生成近义词词组
#    di=GetSemanticallyRelatedTerms(modelName="Word2Vec",modelPath="../result/step3.1_word2vec_V5/word2vec.m",
#                                   SETermPath="../result/step4.1.3_SETerm_V5.list",
#                                   savePath="../result/step4.2.1_SemanticallyRelatedTerms_word2vec_V5.dict")
    
#    di=GetSemanticallyRelatedTermsMixedModel(fasttextDictPath="../result/step4.2.1_SemanticallyRelatedTerms_fasttext_V5.dict",
#                                             word2vecDictPath="../result/step4.2.1_SemanticallyRelatedTerms_word2vec_V5.dict",
#                                             savePath="../result/step4.2.1_SemanticallyRelatedTerms_mixed_V5.dict")
#    di421=joblib.load("../result/step4.2.1_SemanticallyRelatedTerms_mixed_V5.dict")
    # In[] step4.2.2 Filter Semantically Related Terms
#    di=FilterSemanticallyRelatedTerms(dictPath="../result/step4.2.1_SemanticallyRelatedTerms_mixed_V5.dict",
#                                      savePath="../result/step4.2.2_SemanticallyRelatedTermsFiltered_mixed_V5.dict")
    ffDi=joblib.load("../result/step4.2.2_SemanticallyRelatedTermsFiltered_fasttext_V5.dict") 
    wvDi=joblib.load("../result/step4.2.2_SemanticallyRelatedTermsFiltered_word2vec_V5.dict")   
    # In[]step4.2.3 根据相似度选择一定数量的语义相关的单词
    di=SelectSemanticallyRelatedTerms(threshold=0.1,topn=40,
                                      dictPath="../result/step4.2.2_SemanticallyRelatedTermsFiltered_word2vec_V5.dict",
                                      savePath="../result/step4.2.3_SemanticallyRelatedTermsFiltered_word2vec_V5.dict")
#    di423=joblib.load("../result/step4.2.3_SemanticallyRelatedTermsFiltered_"+"fasttext"+".dict")
  # In[]step4.2.4 DiscriminateTerms
    di=DiscriminateTerms(dictPath="../result/step4.2.3_SemanticallyRelatedTermsFiltered_word2vec_V5.dict",
                         savePath="../result/step4.2.4_DiscriminatedDict_word2vec_V5.dict")
#    di424=joblib.load("../result/step4.2.4_DiscriminatedDict_"+"fasttext"+".dict")
  # In[]step4.2.5 根据SOtimes相似度值进行过滤 暂时放弃

# In[] step4.2.6 去除相似度值  
    di=RemoveSimilarity(dictPath="../result/step4.2.4_DiscriminatedDict_word2vec_V5.dict",
                        savePath="../result/step4.2.6_DiscriminatedDict_woed2vec_V5.dict")
#    di=joblib.load("../result/step4.2.6_DiscriminatedDict_fasttext.dict")
#    s="stribiżew"
#    s.encode(encoding="ascii")
    
    
#    res=[]
#    seterms=joblib.load("../result/step4.1.3_SETerm_V5.list")
#    for i in seterms:
#        if i[-1]=="_":
#            print(i)
    
    
    
    
    
    
    
    