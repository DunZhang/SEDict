# -*- coding: utf-8 -*-
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
from SEUtils import filterTerms
def GetSETerms(sopath,wipath,savepath):
    with codecs.open(sopath, encoding="utf-8") as fr:
        vocab_so = json.load(fr)
    with codecs.open(wipath, encoding="utf-8") as fr:
        vocab_wiki = json.load(fr)
    
    
    soTags=joblib.load("../result/SOTagsExt.set")
#    WikiLinkTerm=joblib.load("../result/WikiLinkTerm.set")
    stopWords_set = joblib.load("../result/stopWords.set")
    count_so = 0.0
    count_wiki = 3627029375.0
    for _,value in vocab_so.items():
        count_so+=value
    res=[]
    c=0
    for key,value in vocab_so.items():
        if value<20:
            continue
        if(c%50000==0):
            print (c)
        c+=1
        if(not filterTerms(key,stopWords_set)):
            continue
        if(key in soTags):
            res.append(key)
            continue 
#        if(key in WikiLinkTerm):
#            res.append(key)
#            continue 
        if(value>100):
            if(key in vocab_wiki):
                if (((value / count_so) / (vocab_wiki[key] / count_wiki)) > 10.0):                    
                        res.append(key)
            else:
                res.append(key)
    del vocab_so
    del vocab_wiki
    gc.collect()
    joblib.dump(res,savepath,protocol=2)      
    return res
    
if (__name__=="__main__"):
    GetSETerms(sopath="../result/step1.2.4_SOVocabulary_15_0.5_npmi_V1.json",
               wipath="../result/step1.1.3_WikiVocabulary_V1.json",
               savepath="../result/step4.1.3_SETerm_15_0.5_npmi_V1.list")

    GetSETerms(sopath="../result/step1.2.4_SOVocabulary_15_0.7_npmi_V1.json",
               wipath="../result/step1.1.3_WikiVocabulary_V1.json",
               savepath="../result/step4.1.3_SETerm_15_0.7_npmi_V1.list")

#    GetSETerms(sopath="../result/step1.2.4_SOVocabulary_15_60_default_V1.json",
#               wipath="../result/step1.1.3_WikiVocabulary_V1.json",
#               savepath="../result/step4.1.3_SETerm_15_60_default_V1.list")
#    
#    GetSETerms(sopath="../result/step1.2.4_SOVocabulary_15_100_default_V1.json",
#               wipath="../result/step1.1.3_WikiVocabulary_V1.json",
#               savepath="../result/step4.1.3_SETerm_15_100_default_V1.list")


    pass
    
    