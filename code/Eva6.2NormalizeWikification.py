# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 10:50:26 2018

@author: Administrator
"""
#import sys
#sys.path.insert(0,"..")
# print(sys.path)
from os.path import dirname
import SEUtils
from gensim.models import Word2Vec,FastText
from sklearn.externals import joblib
import json
import re
import codecs
from lxml import etree
from bs4 import BeautifulSoup
from urllib.parse import unquote    
from collections import defaultdict
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from SEUtils import filterTerms
if(__name__=="__main__"):
    # In[] Eva6.2.1获取 wiki的Url关键字和anchor text，存到字典中
#    context = etree.iterparse("../data/Posts.xml", encoding="utf-8")
#    di={}
#    c = 0
#    for _, elem in context:  # 迭代每一个
#        c += 1
#        if (c % 100000 == 0):
#            print("already pasrse record:", str(c / 10000) + "W")
#        body = elem.get("Body")
#
#        if (body is not None):
#            soup = BeautifulSoup(body, "lxml")
#            res=soup.find_all("a")
#            for i in res:
#                try:
#                    t1,t2=unquote(i.get("href")).lower().strip().replace("-","_"),i.get_text().lower().strip().replace("-","_")
#                except :
#                    continue
#                if t2.startswith("http"):
#                    continue
#                if "en.wikipedia.org" in t1:
#                    key=t1.split("/")[-1].split("#")[0]
#                    if(len(key)<1):
#                        continue
#                    if key not in di:
#                        di[key]=defaultdict(int)
#                    di[key][t2]+=1
#        elem.clear()
#
#    with codecs.open("../result/Eva6.2.1WikiUrlDict.json","w",encoding="utf-8") as fw:
#        fw.write(json.dumps(di))
   # In[] Eva6.2.2 简单的过滤
#    print (dirname(__file__))
#    SEDict1=joblib.load("../result/step5.1.3_ExtSEDict_word2vec_V5.dict")
#    SEDict2=joblib.load("../result/step5.1.3_ExtSEDict_fasttext_V5.dict")
#    SEKeys=set(list(SEDict1.keys())+list(SEDict2.keys()))
#    specialWords=["link","wikipedia","wiki","this","criticism","article","your","concept","very_bad",
#                 "here","a","is","the","and","good","other","or","of","not","are","on",
#                 "has","only","you","should","always","what","that","how","details"]
#    stop_words_set=joblib.load("../result/stopWords.set")
#    with codecs.open("../result/Eva6.2.1WikiUrlDict.json","r",encoding="utf-8") as fr:
#        rawDi=json.load(fr)
#    di={}
#    #开始过滤
#    for key ,value in rawDi.items():
##        key=''.join([i if ord(i) < 128 else "" for i in key])
#        try:
#            key.encode(encoding="ascii")
#        except:
#            continue
#        if len(key)<1:
#            continue
#        if len(re.findall("[?!;\[\]<>`~$\^&*=|%@(){},:\"/'\\\\]",key))>0:
#            continue
#        if not filterTerms(key,stop_words_set):
#            continue
#        if key in SEKeys:
#            t=defaultdict(int)
#            for anchor ,times in value.items():
#                tanchor=anchor.replace(" ","_")
#                try:
#                    key.encode(encoding="ascii")
#                except:
#                    continue
#                if len(re.findall("[?!;\[\]<>`~$\^&*=|%@(){},:\"/'\\\\]",tanchor))>0:
#                    continue
#                if len(tanchor)<2:
#                    continue
#                if not filterTerms(tanchor,stop_words_set):
#                    continue 
#                flag=False
#                for x in tanchor.split("_"):
#                    if x in specialWords:
#                        flag=True
#                        break
#                if flag:
#                    continue  
#                t[tanchor]+=times
#            if len(t)<1:#放低要求
#                continue
#            di[key]=t 
#        else:         
#            pass
#    joblib.dump(di,"../result/Eva6.2.2WikiLink.dict")
    # In[] original precision@K   
    di=joblib.load("../result/Eva6.2.2WikiLink.dict")  
    #先生成 用于测试的字典
    originDict={}      
    for key ,value in di.items():
        t=[(anchor,times) for anchor,times in value.items()]
        t.sort(key=lambda x : x[1],reverse=True)
        t=[x[0] for x in t]
        originDict[key]=t[0:2]  
    stu={}
    count=0.0
    for  key ,value in originDict.items():
        if value[0] == key :
            count+=1
    print("Origin,Presision@K=1:  ",count/len(originDict))
    count=0.0
    for  key ,value in originDict.items():
        flag=True
        for i in value:
            if i ==key :
                count+=1
                flag=False
                break
        if flag:
            stu[key]=value
            
    print("Origin,Presision@K=2:  ",count/len(originDict))    

    # In[]计算SEDict normlize的precision
    SEDict=joblib.load("../result/step5.1.7_ExtSEDict_fasttext_60_V5.dict")
#    #构建推荐字典
    reverseDi=defaultdict(set)
    for key,value in SEDict.items():
        for i in value[0]:
            reverseDi[i].add(key)
        for i in value[1]:
            reverseDi[i].add(key)   
        reverseDi[key].add(key)

#正规化字典
    SEDictNormLinkDict={}
    for key,value in di.items():
        t=defaultdict(int)
        for anchor,times in value.items():
            if anchor in reverseDi and anchor!=key and key in reverseDi[anchor]:
                t[key]+=times
            else:
                t[anchor]+=times
        SEDictNormLinkDict[key]=t
#        #变成列表
    di_list={}
    for key ,value in SEDictNormLinkDict.items():
        t=[(anchor,times) for anchor,times in value.items()]
        t.sort(key=lambda x : x[1],reverse=True)
        t=[x[0] for x in t]
        di_list[key]=t[0:2]   
## 使用正常的测试方法
    stu={}
#    addFF=[]
#    addWV=[]
    count=0.0
    for  key ,value in di_list.items():
        flag=True
        if value[0] == key:
            count+=1
            flag=False
    print("SEDict,Presision@K=1:  ",count/len(di_list))
    count=0.0
    for  key ,value in di_list.items():
        flag=True
        for i in value:
            if i ==key :
                count+=1
                flag=False
                break
        if flag:
            stu[key]=value 
#            addWV.append(key)
#            addFF.append(key)
    print("SEDict,Presision@K=2:  ",count/len(di_list))            
#    

# In[]  porter stem 的 precision  
#    porter_stemmer = PorterStemmer()
##正规化字典
#    NormLinkDict={}
#    for key,value in di.items():
#        t=defaultdict(int)
#        for anchor,times in value.items():
#            if anchor!=key:
#                t[porter_stemmer.stem(anchor)]+=times
#            else:
#                t[anchor]+=times
#        NormLinkDict[key]=t
##        #变成列表
#    di_list={}
#    for key ,value in NormLinkDict.items():
#        t=[(anchor,times) for anchor,times in value.items()]
#        t.sort(key=lambda x : x[1],reverse=True)
#        t=[x[0] for x in t]
#        di_list[key]=t[0:2]   
### 使用正常的测试方法
#    count=0.0
#    for  key ,value in di_list.items():
#        if value[0] == key:
#            count+=1
#    print("porter stem,Presision@K=1:  ",count/len(di_list))
#    count=0.0
#    for  key ,value in di_list.items():
#        for i in value:
#            if i ==key :
#                count+=1
#                break
#    print("porter stem,Presision@K=2:  ",count/len(di_list))          

#    
    
# In[]  wordnet_lemmatizer 的 precision  
#
#    wordnet_lemmatizer = WordNetLemmatizer()  
##正规化字典
#    NormLinkDict={}
#    for key,value in di.items():
#        t=defaultdict(int)
#        for anchor,times in value.items():
#            if anchor!=key:
#                t[wordnet_lemmatizer.lemmatize(anchor)]+=times
#            else:
#                t[anchor]+=times
#        NormLinkDict[key]=t
##        #变成列表
#    di_list={}
#    for key ,value in NormLinkDict.items():
#        t=[(anchor,times) for anchor,times in value.items()]
#        t.sort(key=lambda x : x[1],reverse=True)
#        t=[x[0] for x in t]
#        di_list[key]=t[0:2]   
### 使用正常的测试方法
#    count=0.0
#    for  key ,value in di_list.items():
#        if value[0] == key:
#            count+=1
#    print("wordnet_lemmatizer,Presision@K=1:  ",count/len(di_list))
#    count=0.0
#    for  key ,value in di_list.items():
#        for i in value:
#            if i ==key :
#                count+=1
#                break
#    print("wordnet_lemmatizer,Presision@K=2:  ",count/len(di_list))       
    
    
           