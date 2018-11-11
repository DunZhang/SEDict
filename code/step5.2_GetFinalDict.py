# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 18:13:54 2018

@author: Administrator
"""
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
import json
from SEUtils import filterTerms,getLoc
import numpy as np
from SEUtils import isSynonym,isAbrreviation
def query(raw_di,di,word):
    #最好的情况是
    if(word in di.keys()):
        return True   
    else:#其次是在abbrv中
        for i in di.keys():
            if(word in di[i][0]):
                return True
        for i in di.keys():
            if(word in di[i][1]):
                return True
    return False   
def trans(di,savePath):
    keys=list(di.keys())
    newdi={}
    c=0
    for key in keys:
        c+=1
        if(c%1000==0):
            print (c)
        value=di[key]
        t=key.replace("-"," ").replace("_"," ")
        t1=[x.replace("-"," ").replace("_"," ") for x in value[0]]
        t2=[x.replace("-"," ").replace("_"," ") for x in value[1]]
        t3=[x.replace("-"," ").replace("_"," ") for x in value[2]]
        if(t not in newdi):
            newdi[t]=[t1,t2,t3]
    joblib.dump(newdi,savePath)
if(__name__=="__main__"):
    # In[]
#    di=joblib.load("../result/step5.1.3_ExtSEDict.dict")
#    raw_dict=joblib.load("../result/step4.2.3_DiscriminatedDict.dict")
#    newDi=deepcopy(di)
#    for key in raw_dict:
#        if( not query(raw_dict,di,key)):
#            t=deepcopy(raw_dict[key])
    # In[]
    di=joblib.load("E:/ExtSEDictword2vec.dict")
    trans(di,"D:/ExtSEDictword2vec.dict")
    
    
    
    
    
    
    
    
    
    
    
    