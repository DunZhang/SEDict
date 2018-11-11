# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 21:15:08 2018

@author: Administrator
"""
import codecs
import json
from sklearn.externals import joblib
from gensim.models import Word2Vec, FastText
import re

def replaceByFullName(modelName="FastText"):
    """
    step4.4.1 对于每一个key和value，找出[key,value]里的最具代表性的单词放到列表第一个位置
    """
    f = codecs.open("../result/step1.3_SOVocabulary.json", encoding="utf-8")
    vocab_so = json.load(f)
    f.close()
    di=joblib.load("../result/step4.3.3_SynonymMerged_"+modelName.lower()+".dict")
    newDi={}
    c=0
    for key in di.keys():
        c+=1
        if(c%1000==0):
            print (c)
        value=di[key]
        value.append(key)
#        value.sort(reverse=True,key= lambda x:len(x))
        
        tvalue=[]
        for i in value:
            if(len(i)>2):
                tvalue.append(i)
        if(len(tvalue)==0):
            representWord=key
        else:
            representWord=max(tvalue,key=lambda x: vocab_so[x] if x in vocab_so else 0)
        if(key==representWord):
            value.remove(key)
            value.insert(0,None)
        else:
            value.remove(key)
            value.remove(representWord)
            value.insert(0,representWord)
        newDi[key]=value
    joblib.dump(newDi,"../result/step4.4.1_SynonymFullName_"+modelName.lower()+".dict")
    return newDi

if(__name__=="__main__"):
#    f = codecs.open("../result/step1.3_SOVocabulary.json", encoding="utf-8")
#    vocab_so = json.load(f)
#    f.close()
#    m1 = FastText.load("../result/step3.1_FastText/step3.1_FastText.m")
    di=replaceByFullName("fasttext")
#    di=joblib.load("../result/step4.4.1_SynonymFullName_"+"fasttext"+".dict")
#    print di["debug"]
#    m = Word2Vec.load("../result/step3.1_skipgram/step3.1_skipgram.m")
#    m.delete_temporary_training_data(True)
#    print "ie" in m.wv.vocab
#    res=joblib.load("../result/step4.4.1_SynonymFullName_fasttext.dict")
#    print res["msvc"]
#    print res["js"]
#    print res["python"]
#    print res["c++"]
#    print res["c#"]
#    print res[".net"]
#    print res["java"]
#    print res["visual_c++"]
#    m = FastText.load("../result/step3.1_FastText/step3.1_FastText.m")
#    print m.wv.similarity("msvc","c++")
#    termList=joblib.load("../result/step4.2.4_ExtSETerm_"+"fasttext"+".list")
