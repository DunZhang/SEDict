# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 14:54:57 2018

@author: Administrator
"""
import json
import codecs
import random
import gc
from gensim.models import FastText
from sklearn.externals import joblib
from SEUtils import filterTerms
def isEqual(d1,d2):
    for item in zip(d1,d2):
        if item[0]!=item[1]:
            return False
    return True









if __name__=="__main__":
#    stopWords_set = joblib.load("../result/stopWords.set")
#    sopath="../result/step1.2.4_SOVocabulary_V5.json"
#    modelPath="../result/step3.1_fasttext_V5/fasttext.m"
#    m=FastText.load(modelPath)
#    with codecs.open(sopath, encoding="utf-8") as fr:
#        vocab_so = json.load(fr)
#    newWord=[]
#    for key,value in vocab_so.items():
#        try:
#            key.encode(encoding="ascii")
#        except:
#            continue
#        if value<5 and filterTerms(key,stopWords_set):
#            newWord.append(key)
#    
#    del vocab_so
#    gc.collect()
    #获取向量
#    word_vec=[]
#    c=0
#    count=0
#    for word in newWord:
#        c+=1
#        if c%10000==0:
#            print(c//10000,"W")
#        try:
#            vec=m.wv[word]
#        except:
#            continue
#        word_vec.append((word,vec))
#        if len(word_vec)==500000:
#            joblib.dump(word_vec,"../result/NewWordVecs/word_vec_"+str(count)+".list")
#            count+=1
#            del word_vec
#            gc.collect()
#            word_vec=[]
#            
#    if len(word_vec)>0:
#        joblib.dump(word_vec,"../result/NewWordVecs/word_vec_"+str(count)+".list")
#        count+=1
#        del word_vec
#        gc.collect()
#        word_vec=[]            
    #开始添加
#    c=0
#    for fileNum in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]:
#        
#        word_vec=joblib.load("../result/NewWordVecs/word_vec_"+str(fileNum)+".list")
#        word_list=[x[0] for x in word_vec]
#        vec_list=[x[1] for x in word_vec]
#        print (fileNum)
#        m.wv.add(word_list,vec_list)
    #重新开始计算L2向量
#    m.wv.init_sims()

    
# In[] 获取所有需要添加的单词
    addedWord=[]
    # Eva4.2 wiki abbrev
    wikiAbbrev=joblib.load("../result/WikiAbbrev.list")
    for i in wikiAbbrev:
        addedWord.extend(i)
        
    # Eva4.3 synonym coverage
    SOSPairs=joblib.load("../result/SOSynonymPairs1.list")
    for i in SOSPairs:
        addedWord.extend(i)    
    # Eva 6.2 wiki link
    di=joblib.load("../result/Eva6.2.2WikiLink.dict")  
    for key,value in di.items():
        addedWord.append(key)
        addedWord.extend(value.keys())
    addedWord=list(set(addedWord))
    
# In[] 确定要添加的
    sopath="../result/step1.2.4_SOVocabulary_V5.json"
    modelPath="../result/step3.1_fasttext_V5/fasttext.m"
    m=FastText.load(modelPath)
    with codecs.open(sopath, encoding="utf-8") as fr:
        vocab_so = json.load(fr)
    wordToBeAdded=[]
    for i in addedWord:
        if i not in m.wv.vocab and i in vocab_so:
            wordToBeAdded.append(i)
    joblib.dump(wordToBeAdded,"../result/WordToBeAdded.list")
# In[] 开始添加
    words=joblib.load("../result/WordToBeAdded.list")
    words_vec=[]
    for i in words:
        words_vec.append(m.wv[i])
    m.wv.add(words,words_vec)
    
    m.wv.init_sims(replace=False)
    m.save("../result/step3.1_fasttext_V6/fasttext.m")




















