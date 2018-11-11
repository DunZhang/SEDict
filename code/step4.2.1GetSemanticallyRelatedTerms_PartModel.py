# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 14:54:06 2018

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
def getSRTerms_Single_Part(termDicts,term):
    """
    为术语term获取最相似的一部分单词
    """
    termLists=[i[term]  for i in termDicts if term in i]
    di=defaultdict(list)
    for i in termLists:
        for j in i:
            di[j[0]].append(j[1])   
    res=[]
    for key,value in di.items():
        res.append( (key,sum(value)/len(value)*math.log(len(value)+1,len(termLists)+1)   )  )
    res.sort(key=lambda x: x[1],reverse=True)
    return res
if __name__=="__main__":
    # In[]使用每个模型获取到一个近义词词组
#    SETermPath="../result/step4.1.3_SETerm_V5.list"
#    SETerms = joblib.load(SETermPath)
    WikiAbbrev=joblib.load("../result/WikiAbbrev.list") 
    wikiFullNameToAbbrev={}
    for i in WikiAbbrev:
        wikiFullNameToAbbrev[i[0]]=i[1]
#    fullNames=[i[0] for i in WikiAbbrev]
#    for i in range(11):
#        print (i)
#        m=FastText.load("../result/step3.1_FastText_Part_V5/fasttext_"+str(i)+".m")   
#        di={}
#        for term in SETerms:
#            if term not in fullNames or term not in m.wv.vocab :
#                continue       
#            di[term]=m.wv.most_similar(term,topn=500)
#    #        di[i]=1
#        del m        
#        joblib.dump(di,"../result/step4.2.1SemanticallyRelatedTerms_fasttext_Part_V5/SemanticallyRelatedTerms_"+str(i)+".dict")
#        del di
#        gc.collect()
#        break
        
    # In[]获取真正词典
    termDicts=[ joblib.load("../result/step4.2.1SemanticallyRelatedTerms_fasttext_Part_V5/SemanticallyRelatedTerms_"+str(i)+".dict") for i in range(11)]
    wikiTerms=[]
    for i in termDicts:
        wikiTerms.extend(i.keys())
    wikiTerms=list(set(wikiTerms))
    
    di={}
    for term in wikiTerms:
        di[term]=getSRTerms_Single_Part(termDicts,term)
    
    
    
    c=0
    for term in di:
        abb=wikiFullNameToAbbrev[term]
        if abb in [i[0] for i in di[term]]:
            c+=1
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    