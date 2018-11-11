# -*- coding: utf-8 -*-
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
from gensim.models.phrases import Phrases, Phraser,original_scorer,npmi_scorer
from lxml import etree
from bs4 import BeautifulSoup
import gc
from collections import defaultdict
def default_scorer(worda_count,wordb_count,bigram_count,min_count):
    return original_scorer(worda_count,wordb_count,bigram_count,59543584,15,0)
if(__name__=="__main__"):
    WikiAbbrev=joblib.load("../result/WikiAbbrev.list")
#    pp=Phrases.load("../result/step1.2.2_trigram_V1.m")
#    v=pp.vocab    
#    res=[]
#    for i in WikiAbbrev:
#       if(i[0].encode() not in v  ):
#           res.append(i[0])   
#    c3,c33=0,0
#    for i in res:
#        if len(re.findall("_",i))==2:
#            c3+=1
#        elif len(re.findall("_",i))>2:
#            c33+=1
#            
#            bytes("123".encode())
#         
#    "internet_explorer_7" in v
#    c=0
#    for i in v:
#        print (i)
#        c+=1
#        if(c>200):
#            break
    # In[]
    f = codecs.open("../result/step1.2.4_SOVocabulary_V1.json", encoding="utf-8")
    vocab_so = json.load(f)
    f.close()
    c=0
    res=[]
    for i in WikiAbbrev:
       if(i[1] in vocab_so and vocab_so[i[1]]>5 ):
           c+=1
           res.append(i[1])
    print(c)
           
#    c1,c2,c3,c4more=0,0,0,0
#    for i in res:
#        if(len(re.findall("_",i))==2):
#            c3+=1
#        elif(len(re.findall("_",i))>2):
#            c4more+=1
##################################################################################     
#    pp=Phrases.load("../result/step1.2.2_bigram_V1.m")
#    v=pp.vocab
#    "integrated_development_environment" in v
#    "development_environment" in v
#    "integrated_development" in v
#    print pp.score_item("integrated","development",["integrated","development"],scorer)
#    print v["integrated"],v["development"],v["integrated_development"]
#    res1=[]
#    for i in res:
#        if(i not in v):
#            res1.append(i)
#   joblib.dump(res1,"zd1.list")     
# In[] 看一看xml里有没有
#    res=joblib.load("zd1.list")      
#    resdict=dict([(i.replace("_"," "),0) for i in res])
#    res=list(resdict.keys())
#    context = etree.iterparse("../data/Posts.xml", encoding="utf-8")
#    c = 0
#    zd=0
#    for _, elem in context:  # 迭代每一个
#        c += 1
#        if (c % 100000 == 0):
#            print("already pasrse record:", str(c / 10000) + "W      ",zd)
#        title, body = elem.get("Title"), elem.get("Body")     
#        elem.clear()
#        if(title is not None):
#            if("integrated development environment" in title):
#                print title
#                x=raw_input()
#        if(body is not None):
#            if("integrated development environment" in body):
#                print body
#                x=raw_input()
#            for i in res:
#                if(i in title):
#                    zd+=1
#                    resdict[i]+=1
#        if(body is not None):
#            for i in res:
#                if(i in body):
#                    zd+=1
#                    resdict[i]+=1        
        
# In[] 看一看txt里有没有
#    fr=codecs.open("C:/SE/step1.2.1_SOCleaned_V1.txt","r",encoding="utf-8")
#    fr=codecs.open("C:/SE/step1.2.3_SOTrigramList_V1.txt","r",encoding="utf-8")
#    c=0
#    for line in fr:
#        if("integrated development environment" in line):
#            c+=1
#            print c
#            x=raw_input()
        
        
 # 记录出问题的数据       
#    res=joblib.load("zd1.list")         
#    f = codecs.open("../result/step1.2.4_SOVocabulary_V1.json", encoding="utf-8")
#    vocab_so = json.load(f)
#    f.close()
#    res1=[]
#    for i in res:
#        if(i.replace("_","").isalpha()):
#            res1.append(i)
#    joblib.dump(res1,"missingTrigram.list")
#    data=[]
#    pp=Phrases.load("../result/step1.2.2_bigram_V1.m")
#    voc=pp.vocab
#    lenVocab=len(voc)
#    min_count=15
#    for i in res1:
#        w1,w2,w3=i.split("_")
#        w1w2,w2w3=w1+"_"+w2,w2+"_"+w3
#        w1Num,w2Num,w3Num,w1w2Num,w2w3Num=float(voc[w1]),float(voc[w2]),float(voc[w3]),float(voc[w1w2]),float(voc[w2w3])
#        if(w1Num>0 and w2Num>0):
#            phraseValue_w1w2=(w1w2Num-min_count)/w1Num/w2Num*lenVocab
#        else:
#            phraseValue_w2w3 =-1
#        if(w2Num>0 and w3Num>0):
#            phraseValue_w2w3=(w2w3Num-min_count)/w2Num/w3Num*lenVocab
#        else:
#            phraseValue_w2w3=-1        
#        data.append((w1,w1Num
#        ,w2,w2Num
#        ,w3,w3Num
#        ,w1w2,w1w2Num,phraseValue_w1w2
#        ,w2w3,w2w3Num,phraseValue_w2w3))
#        
#    cnmes=("w1","w1 num","w2","w2 num","w3","w3 num","w1w2","w1w2 num","w1w2 score","w2w3","w2w3 num","w2w3 score")
#    pd.DataFrame(data,columns=cnmes).to_csv("zd.csv",index=False,encoding="utf-8")
    
    # In[] 查看wiki 的abbreviation中在原始 SO中出现的次数
    #首先获取字典
#    WikiAbbrev=joblib.load("../result/WikiAbbrev.list")
#    wiki_phrases=[]
#    for i in WikiAbbrev:
#        wiki_phrases.append(i[0].replace("_"," "))
#        wiki_phrases.append(i[1].replace("_"," "))
#    wiki_phrases=set(wiki_phrases)
#    count_dict={}
#    for i in wiki_phrases:
#        count_dict[i]=0
#    
#    context = etree.iterparse("../data/Posts.xml", encoding="utf-8")
#    datas = []  # 存储title 和 answers
#    c = 0
#    for _, elem in context:  # 迭代每一个
#        c += 1
#        if (c % 100000 == 0):
#            print("already pasrse record:", str(c / 10000) + "W")
#        title, body, typeId = elem.get("Title"), elem.get("Body"), elem.get("PostTypeId")
#        elem.clear()
#        if (typeId is None):
#            continue
#        if (int(typeId) != 1 and int(typeId) != 2):
#            continue
#        if (body is not None):
#            soup = BeautifulSoup(body, "lxml")
#            for pre in soup.find_all("pre"):
#                if (len(pre.find_all("code")) > 0):
#                    pre.decompose()
#            datas.append(soup.get_text())
##            for item in wiki_phrases:
##                    count_dict[item]+=len(re.findall(item,t))
#        if (title is not None):
#            datas.append(BeautifulSoup(title, "lxml").get_text())
#        
#        if len(datas)>200000:
#            s="!".join(datas)
#            for item in wiki_phrases:
#                    count_dict[item]+=len(re.findall(item,s))
#            del datas
#            del s
#            datas=[]
#    joblib.dump(count_dict,"../result/studyWikiCountsSO.dict")
#    res= [x for x in count_dict.items()]
#    pd.DataFrame(res).to_csv("../result/zd.csv",index=False,encoding="utf-8")
#    
#    
    
    
    
    # In[] 查看wiki清洗过的SO中出现的次数
#    WikiAbbrev=joblib.load("../result/WikiAbbrev.list")
#    wiki_phrases=[]
#    for i in WikiAbbrev:
#        t=i[0].replace("_"," ").strip()
#        wiki_phrases.append()
##        wiki_phrases.append(i[1].replace("_"," "))
#    wiki_phrases=set(wiki_phrases)  
#    count_dict={}
#    for i in wiki_phrases:
#        count_dict[i]=0        
#    fr=codecs.open("C:/SE/step1.2.1_SOCleaned_V1.txt","r",encoding="utf-8")
#    c=0
#    datas=[]
#    for line in fr:    
#        c+=1
#        if c%100000 ==0:
#            print(c/10000,"w")
#        datas.append(line)
#        if len(datas) > 1000000:
#            ts="!".join(datas)
#            for x in count_dict:
#                count_dict[x]+=len( re.findall(x,ts) )
#            del ts
#            del datas
#            datas=[]
#            gc.collect()
#    if len(datas) > 0:
#        ts="!".join(datas)
#        for x in count_dict:
#            print(x)
#            count_dict[x]+=len( re.findall(x,ts) )
#        del ts
#        del datas
#        gc.collect()
#        datas=[]
#    joblib.dump(count_dict,"../result/studyWikiCountsCleanedSO.dict")
#    res=joblib.load("../result/Eva4.2WikiCountsCleanedSO.dict")
#    res=[(i,res[i]) for i in res]
#    pd.DataFrame(res).to_csv("../result/Eva4.2WikiCountsCleanedSO.csv",index=False,encoding="utf-8")        
    
    # In[] 生成二元和三元短语的npmi_socre
    #获取二元短语和三元短语
    
#    bigram = Phrases.load("../result/step1.2.2_bigram_V1.m")
#    corpus_word_count=bigram.corpus_word_count
#    min_count=bigram.min_count
#    v=bigram.vocab
#    len_vocab=len(v)
#    WikiFullNames=[x[0]  for x in  joblib.load("../result/WikiAbbrev.list")]
#    p2,p3=[],[]
#    for i in WikiFullNames:
#        t=len(re.findall("_",i))
#        if t==1:
#            p2.append(i)
#        if t==2:
#            p3.append(i)
#    #统计p2的值
#    res2=[]
#    for i in p2:
#        w1,w2=i.split("_")
#        w1w2=i
#        w1Num,w2Num,w1w2Num=v[w1.encode("utf-8")],v[w2.encode("utf-8")],v[w1w2.encode("utf-8")]
#        if w1Num ==0 or w2Num==0:
#            w1w2_defaultScore=-99
#            w1w2_nomiScore=-99
#        else:
#            w1w2_defaultScore=original_scorer(w1Num,w2Num,w1w2Num,len_vocab,min_count,corpus_word_count)
#            if w1w2Num==0:
#                w1w2_nomiScore=-99
#            else:
#                w1w2_nomiScore=npmi_scorer(w1Num,w2Num,w1w2Num,len_vocab,min_count,corpus_word_count)
#        res2.append(   (w1,w1Num,w2,w2Num,w1w2,w1w2Num,w1w2_defaultScore,w1w2_nomiScore)  )
#
#    #统计p3 
#    res3=[]       
#    for i in p3:
#        w1,w2,w3=i.split("_")
#        w1w2,w2w3=w1+"_"+w2,w2+"_"+w3
#        w1Num,w2Num,w3Num,w1w2Num,w2w3Num=v[w1.encode("utf-8")],v[w2.encode("utf-8")],v[w3.encode("utf-8")],v[w1w2.encode("utf-8")],v[w2w3.encode("utf-8")]
#        if w1Num ==0 or w2Num==0:
#            w1w2_defaultScore=-99
#            w1w2_nomiScore=-99
#        else:
#            w1w2_defaultScore=original_scorer(w1Num,w2Num,w1w2Num,len_vocab,min_count,corpus_word_count)
#            if w1w2Num==0:
#                w1w2_nomiScore=-99
#            else:
#                w1w2_nomiScore=npmi_scorer(w1Num,w2Num,w1w2Num,len_vocab,min_count,corpus_word_count)
#        if w2Num ==0 or w3Num==0:
#            w2w3_defaultScore=-99
#            w2w3_nomiScore=-99
#        else:
#            w2w3_defaultScore=original_scorer(w2Num,w3Num,w2w3Num,len_vocab,min_count,corpus_word_count)
#            if w2w3Num==0:
#                w2w3_nomiScore=-99
#            else:
#                w2w3_nomiScore=npmi_scorer(w2Num,w3Num,w2w3Num,len_vocab,min_count,corpus_word_count)
#
#      
#        res3.append((w1,w1Num
#        ,w2,w2Num
#        ,w3,w3Num
#        ,w1w2,w1w2Num,w1w2_defaultScore,w1w2_nomiScore
#        ,w2w3,w2w3Num,w2w3_defaultScore,w2w3_nomiScore))    
#        
#        
#    pd.DataFrame(res2,columns=["w1","w1Num","w2","w2Num","w1w2","w1w2Num","w1w2 default score","w1w2 npmi score"]).to_csv("../result/Eva4.2bigram.csv",index=False,encoding="utf-8")
#    pd.DataFrame(res3,columns=["w1","w1Num","w2","w2Num","w3","w3Num","w1w2","w1w2Num","w1w2 default score","w1w2 npmi score","w2w3","w2w3Num","w2w3 default score","w2w3 npmi score"])\
#    .to_csv("../result/Eva4.2trigram.csv",index=False,encoding="utf-8")
    pass
    
    
    
    
    
    