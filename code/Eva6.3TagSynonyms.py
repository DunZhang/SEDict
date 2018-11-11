# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 21:54:10 2018

@author: Administrator
"""

from collections import defaultdict
from lxml import etree
from gensim.models import Word2Vec,FastText
import codecs
from SEUtils import filterTerms,isSynonym,isAbrreviation,StrSims
import networkx as nx
from sklearn.externals import joblib 
from copy import deepcopy
import logging
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)






if __name__=="__main__":
    # In[] Eva6.3.1 Get Tag Sentence
#    context = etree.iterparse("../data/Posts.xml", encoding="utf-8")
#    sentences = []  # 存储title 和 answers
#    c = 0
#    for _, elem in context:  # 迭代每一个
#        c += 1
#        if (c % 100000 == 0):
#            print("already pasrse record:", str(c / 10000) + "W")
#        tags = elem.get("Tags")
#        if tags is not None:
#            sentences.append(tags.replace("<"," ").replace(">"," ").replace("-","_")+"\n")  
#        elem.clear()
#    with codecs.open("../result/Eva6.3.1TagsSentences.txt","w",encoding="utf-8") as fw:
#        fw.writelines(sentences)

    
    
    # In[] Eva6.3.2 训练模型
    with codecs.open("../result/Eva6.3.1TagsSentences.txt","r",encoding="utf-8") as fr:
        sentences=fr.readlines()
    sentences=[x.split() for x in sentences]
#    word2vec = Word2Vec(sentences=sentences, min_count=10, size=200, sg=1, workers=3, window=4)
#    word2vec.delete_temporary_training_data(True)
    fasttext = FastText(sentences=sentences, min_count=10, size=200, sg=1,workers=3, window=4)      
#    word2vec.save("../result/Eva6.3word2vec/word2ve.model")
#    fasttext.save("../result/Eva6.3fasttext/fasttext.model")
    # In[] 构建近义词词典
#    m=FastText.load("../result/Eva6.3fasttext/fasttext.model")
##     m=Word2Vec.load("../result/Eva6.3word2vec/word2vec.model")
#    semanticRelatedDict={}
##     #获取近义词
#    for word in m.wv.vocab:
#        semanticRelatedDict[word]=m.wv.most_similar(word,topn=40)
#    # 简单过滤
#    newDict={}
#    for key,value in semanticRelatedDict.items():
#        t=[]
#        for i in value:
#            if i[1]<0.65:
#                break
#            t.append(i[0])
#        if len(t)<2:
#            t=[x[0] for x in value[0:3]]
#        newDict[key]=t
#    # 区分单词
#    seperate_dic={}
#    for key,value in newDict.items():
#        abbrev,synonym,other=[],[],[]
#        for i in value:
#            if isAbrreviation(key.replace("_"," "),i.replace("_"," ")):
#                abbrev.append(i)
#            elif isSynonym(key.replace("_"," "),i.replace("_"," ")):
#                synonym.append(i)
#            else:
#                other.append(i)
#        seperate_dic[key]=[abbrev,synonym,other]
#    
#    # 合并synonym单词
#    G=nx.Graph()
#    nodes,edges=[],[]
#    for key,value in seperate_dic.items():
#        nodes.append(key)
#        if len(value[1])>0:
#            edges.extend ( [ (key,x) for x in value[1]] )
#    G.add_nodes_from(nodes)
#    G.add_edges_from(edges)
#    
#    res=[]
#    for i in nx.connected_component_subgraphs(G):
#        res.append(list(i))
#     # Replace By FullName
#    vocab_tag=joblib.load("../result/step2.1_SOTags.dict")
#    di_fullname={}
#    for i in res:
#        key=max(i,key=lambda x : vocab_tag[x] if x in vocab_tag else 0)
#        i.remove(key)
#        di_fullname[key]=i
#    
#    # 再次扩展
#    extDict={}
#    for key,value in di_fullname.items():
#        abbrev,synonym,other=[],[],[]
#        abbrev.extend(seperate_dic[key][0])
#        synonym=deepcopy(value)
#        tvalue=deepcopy(value)
#        tvalue.append(key)
#        
#        for i in tvalue:
#            other.extend(seperate_dic[i][2])
#        extDict[key]=[list(set(abbrev)),synonym,list(set(other))]
#    
#    joblib.dump(extDict,"../result/Eva6.3ExtDict.dict")
#    
    
    
    
    
    
    
    
################################ In[] 一些测试
#    exitingPairs=joblib.load("../result/SOSynonymPairs.list")
#    t=[]
#    for i in exitingPairs:
#        t.append(i[0]+"<>"+i[1])
#        t.append(i[1]+"<>"+i[0])
#    exitingPairs=set(t)
#    
#    di=joblib.load("../result/Eva6.3ExtDict.dict")
#    synoymParis,abbrevPairs=[],[]
#    for key,value in di.items():
#        if len(value[0])>0:
#            for i in value[0]:
#                abbrevPairs.append((key,i))
#        if len(value[1])>0:
#            for i in value[1]:
#                if StrSims(key,i)<0.2:
#                    synoymParis.append((key,i))
#    res=[]
#    for i in synoymParis:
#        res.append(i[0]+"<>"+i[1])
#    rrrr=[]
#    for i in res:
#        if i not in exitingPairs:
#            rrrr.append(i)
#    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

