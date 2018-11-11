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
import random
from SEUtils import filterTerms,getLoc,isSynonym
import numpy as np

def getSynonymTerms(modelName,fileCount):
    """
    step4.3.1 获取同义词
    """
    res=[]
    basePath="../result/step4.2_WordsSims_"+modelName.lower()+"/step4.2_WordsSims_"
    for i in xrange(fileCount):
        print i
        data=joblib.load(basePath+str(i)+".array")
        resSort=data.argsort(axis=1)
        for row in xrange(data.shape[0]):
#            t=[]
            for col in xrange(2,data.shape[1]+1):
                if(data[row,resSort[row,-1*col]]<65):
                    break
            if(col<10):
                res.append(list(resSort[row,-10:-1]))
            elif(col>25):
                res.append(list(resSort[row,-25:-1]))
            else:
                res.append(list(resSort[row,-col+1:-1]))

    #把索引转换成字符串
    di={}
    termList=joblib.load("../result/step4.2.4_ExtSETerm_"+modelName.lower()+".list")
    for i in xrange(len(res)):
        t=[]
        for j in res[i]:
            t.append(termList[j])
        di[termList[i]]=t
    joblib.dump(di,"../result/step4.3.1_SynonymTerms_"+modelName.lower()+".dict")
    return di

def filterSynonymTerms(modelName):
    """
    step 4.3.2 过滤术语
    """
    di = joblib.load("../result/step4.3.1_SynonymTerms_"+modelName.lower()+".dict")
    if (modelName.lower() == "fasttext"):
        m = FastText.load("../result/step3.1_FastText/step3.1_FastText.m")
    elif(modelName.lower() == "word2vec"):
        m = Word2Vec.load("../result/step3.1_skipgram/step3.1_skipgram.m")
        m.delete_temporary_training_data(True)
    newdi={}
    c=0
    for key in di:
        c+=1
        if(c%1000==0):
            print (c)
        value=[]
        #.就在key中，不做筛选
        pattern=None
        if("." in key and "+" not in key):
            pattern="[+]"
        elif("." not in key and "+"  in key):
            pattern="[.]"
        elif("." not in key and "+" not in key):
            pattern="[.+]"
        if(pattern is None):
            value=di[key]
        else:
            for i in di[key]:
                if("." not in i and "+" not in i):#值中没有点，也不过滤
                    value.append(i)
                    continue
                flag=False
                for j in re.split(pattern,i):
                    if(len(j)>0):
                        if(j in m.wv.vocab or modelName.lower()=="fasttext"):
                            if(m.wv.similarity(key,j)>0.6):
                                flag=True
                                value.append(j)
                if(not flag):
                    value.append(i)
        t=list(set(value))     
        if(key in t):
            t.remove(key)
        newdi[key]=t
    joblib.dump(newdi,"../result/step4.3.2_SynonymTerms_"+modelName.lower()+".dict")

    return newdi 
def mergeSynonymDict(modelName="fasttext"):
    """
    step4.3.3 合并
    """
    di=joblib.load("../result/step4.3.2_SynonymTerms_"+modelName.lower()+".dict")
    c=0
    print ("start")
    for key in di.keys():
        c+=1
        if(c%1000==0):
            print (c)
        value=di[key]
        tvalue=deepcopy(value)
        if(1<len(value)<50):
            for i in value:#对于value的每个值
                if(i in di):
                    if(SetsSims(value,di[i])>0.6):
                        tvalue.extend(di[i])
#                    elif(MultiSims(m,value,di[i])>0.8):
#                        tvalue.extend(di.pop(i))
            tvalue=list(set(tvalue))
            if(key in tvalue):
                tvalue.remove(key)
            di[key]=tvalue
    joblib.dump(di,"../result/step4.3.3_SynonymMerged_"+modelName.lower()+".dict")
    return di
def MultiSims(m,s1,s2):
    t=0.0
    for i in s1:
        for  j in s2:
            t+=m.wv.similarity(i,j)
    return t/(len(s1)*len(s2))
def SetsSims(s1,s2):
    s1,s2=set(s1),set(s2)
    return float(len(s1.intersection(s2)))/len(s1.union(s2))        
    
if(__name__=="__main__"):
    modelName="word2vec"
    # In[] step4.3.1获取同义词group
    di=getSynonymTerms("word2vec",5)
#    di = json.load(codecs.open("../result/step4.3.1_SynonymGroup_"+"fasttext"+".json","r",encoding="utf-8"))
    
    # In[] step4.3.2 简单过滤
    di=filterSynonymTerms("word2vec")
#
    # In[] step4.3.3合并
    di=mergeSynonymDict(modelName="word2vec")
#    di=joblib.load("../result/step4.3.3_SynonymMerged_"+"fasttext"+".dict")
#    m = Word2Vec.load("../result/step3.1_skipgram/step3.1_skipgram.m")
#    m.delete_temporary_training_data(True)
#    mf = FastText.load("../result/step3.1_FastText/step3.1_FastText.m")
#    s=deepcopy(di["visual_c++"])
#    s.sort(reverse=True, key=lambda x:m.wv.similarity("visual_c++",x))     
#    print mf.wv.similarity("pointer","ptr")
#    print mf.wv.most_similar("visual_c++",topn=40)
#    dif=joblib.load("../result/step4.3.3_SynonymMerged_"+"fasttext"+".dict")
#    print len(di["msvc"])
#    print di["ie"]
#    print m.wv.similarity("ie","internet_explorer")
#    termList=joblib.load("../result/step4.2.4_ExtSETerm_"+modelName.lower()+".list")
#    data=joblib.load("../result/step4.2_WordsSims_word2vec/step4.2_all_similarities_array_word2vec.array")
#    i1,i2=termList.index("ie"),termList.index("internet_explorer")    
#    print data[i2,i1]
#    d=joblib.load("../result/step4.2_WordsSims_word2vec/step4.2_all_similarities_array_word2vec.array")
#    data=joblib.load("../result/step4.2_WordsSims_word2vec/step4.2_WordsSims_23.array")
#    print d[23*800+506,26678],data[506,26678]
#    joblib.dump(d[40000:,:],"../result/step4.2_WordsSims_word2vec/step4.2_WordsSims_4.array")
#    resSort=d[0:10000,:].argsort(axis=1)
#    print data[506,i2-1]
#    print termList[resSort[506,-16]]
#    print data[506,resSort[506,-3]]
        
    
    
    
    
    
        