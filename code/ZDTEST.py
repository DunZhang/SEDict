# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 20:43:13 2018

@author: Administrator
"""

import json
import re
import string
#import jellyfish
import random
import codecs
from gensim.models import Word2Vec, FastText
from sklearn.externals import joblib
#import networkx as nx
import pandas as pd
from datetime import date
import datetime
import numpy as np
from gensim.models.phrases import Phrases, Phraser,original_scorer
from lxml import etree
from bs4 import BeautifulSoup
from collections import defaultdict
from SEUtils import isAbrreviation
import os,sys
if __name__=="__main__":

    # In[]Eva4.2
#    WikiAbbrev=joblib.load("../result/WikiAbbrev.list")
#    fullNames=[i[0] for i in WikiAbbrev]
#    abbrevs=[i[1] for i in WikiAbbrev]
#    f = codecs.open("../result/step1.2.4_SOVocabulary_V4.json", encoding="utf-8")
#    vocab_so = json.load(f)
#    f.close()
#    m = FastText.load("../result/step3.1_FastText_V1/fasttext.m")
#    bigram = Phrases.load("../result/step1.2.2_bigram_V1.m")
#    missingFullNames=[]
#    replacePairs=[]
#    c=0
#    for i in fullNames:
#        t=len(re.findall("_",i))
#        if t<3:
#            if i not in vocab_so:
#                c+=1
#    joblib.dump(replacePairs,"../result/replacePairs_with4moreWiki.list")
    
#    for i in fullNames:
#        if i.encode("utf-8") not in bigram.vocab and len(re.findall("_",i))==1:
#            missingFullNames.append(i)
#    for key,value in bigram.vocab.items():
#        if value<10         :
#            print (key)
#            
#            
#    c1,c2,c3,c4m=0,0,0,0
#    for i in missingFullNames:
#        t=len(re.findall("_",i))
#        if t==0:
#            c1+=1
#        elif t==1:
#            c2+=1
#        elif t==2:
#            c3+=1
#        else:
#            c4m+=1
#    res=joblib.load("../result/studyWikiCountsSO.dict")
#    newres={}
#    for i in fullNames:
#        if i.replace("_"," ") in res:
#            newres[i.replace("_"," ")]=res[i.replace("_"," ")]        
#     t=[(i,newres[i])  for i in newres]   
#     pd.DataFrame(WikiAbbrev).to_csv("WikiAbbreviationPairs.csv",index=False,encoding="utf-8")   
        
###################################################################################################################


#    WikiAbbrev=joblib.load("../result/WikiAbbrev.list")      
#    abbrev1=joblib.load("../result/tutorialspointAbbrev.lsit")
#    abbrev2=joblib.load("../result/tutsrajaAbbrev.lsit")
#    m = FastText.load("../result/step3.1_FastText_V5/fasttext.m")
#    SETerms=joblib.load("../result/step4.1.3_SETerm_V5.list")
#    res=[]
#    for i in abbrev1:
#        if i[1] in m.wv.vocab and i[1] in SETerms:
#            res.append(i)
#        
#    res1=[]
#    c=0
#    for i in res:
#        c+=1
#        print(c)
#        if i[1] in [x[0] for x in m.wv.most_similar(i[0],topn=100)]:
#            res1.append(i)
        
###################################################################################################################       
#    WikiAbbrev=joblib.load("../result/WikiAbbrev.list")
#    fullNames=[i[0] for i in WikiAbbrev]
#    abbrevs=[i[1] for i in WikiAbbrev]
#    SETerms=joblib.load("../result/step4.1.3_SETerm_V5.list")  
#    f = codecs.open("../result/step1.2.4_SOVocabulary_V4.json", encoding="utf-8")
#    vocab_so = json.load(f)
#    f.close()
#    m=FastText.load("../result/step3.1_FastText_V5/fasttext.m")
#    wiki=[]
#    ground_truth={}
#    for i in WikiAbbrev:
#        if i[0] in SETerms and i[0] in m.wv.vocab:
#            ground_truth[i[0]]=i[1]
#            wiki.append(i)
#            
#    res=[]
#    c=0
#    for i in wiki:
#        c+=1
#        print(c)
#        if i[1] in [ x[0] for x in m.wv.most_similar(i[0],topn=100000)]:
#            res.append(i)
#        
#    #现在res是在10w里能找到的，现在看一下10w里是不是有很多符合条件的abbrev
#    di_abbrev={}
#    for i in wiki:
#        simwords=[ x[0] for x in m.wv.most_similar(i[0],topn=100000)]
#        t=[]
#        for j in simwords:
#            if isAbrreviation(i[0],j):
#                t.append(j)
#        di_abbrev[i[0]]=t
#        print(len(t))
#        
#    
## ground_truth  和 di_abbrev
#    c=0
#    cc=0
#    for i in di_abbrev:
#        if len(di_abbrev[i])>0:
#            cc+=1
#            if ground_truth[i] in di_abbrev[i][0:20]:
#                c+=1
        
#############################比较word2vec和fasttext的差异性#################################################################
    # fasttextDictPath="../result/step4.2.1_SemanticallyRelatedTerms_fasttext_V5.dict"
    # word2vecDictPath="../result/step4.2.1_SemanticallyRelatedTerms_word2vec_V5.dict"
    # di1=joblib.load(fasttextDictPath)
    # print("already load",fasttextDictPath)
    # di2=joblib.load(word2vecDictPath)
    # print("already load",word2vecDictPath)
    # columnNames=["Term","A Intersection B"]
    # res=[]
    # for key in di1:
    #     t1=set([ x[0] for x in di1[key][0:200] ])
    #     t2=set([ x[0] for x in di2[key][0:200] ])
    #     res.append((key,len(t1.intersection(t2))))
    # del di1
    # del di2
    # pd.DataFrame(data=res,columns=columnNames).to_csv("ModelDifference.csv",index=False,encoding="utf-8")
    
#############################比较word2vec和fasttext的差异性#############################################################    
#    mixdi=joblib.load("../result/step4.2.1_SemanticallyRelatedTerms_mixed_V5.dict")
#    res=[]
#    for key,value in mixdi.items():
#        if len(value)<80:
#            continue
#        word2vec,fasttext=[],[]
#        for i in range(0,80,2):
#            word2vec.append(value[i][0])
#        for i in range(1,80,2):
#            fasttext.append(value[i][0])  
#        res.append( (key,len(set(word2vec).intersection(set(fasttext))) ))
#    pd.DataFrame(data=res,columns=["term","interCount"]).to_csv("../result/ModelDifference.csv",index=False,encoding="utf-8")
#    
#
#    c=0
#    for i in res:
#        if 36<=i[1]<=40:
#            c+=1
#    print (c)
#        
###############################################################################
    ffdi=joblib.load("../result/step4.2.3_SemanticallyRelatedTermsFiltered_fasttext_V5.dict")
    wvdi=joblib.load("../result/step4.2.3_SemanticallyRelatedTermsFiltered_word2vec_V5.dict")
    print(ffdi["msbuild"][0:6])
    print(wvdi["msbuild"][0:6])    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

    # In[]Eva4.2