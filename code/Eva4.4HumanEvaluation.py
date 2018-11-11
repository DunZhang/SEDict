# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 13:19:04 2018

@author: Administrator
"""

from sklearn.externals import joblib
import pandas as pd
import random

def GetCheckCsv(modelName="FastText"):
    SEDict=joblib.load("../result/step5.1.3_ExtSEDict_"+modelName.lower()+".dict")
    keys=list(SEDict.keys())
    synNum,abbrevNum=800,400
    
    #生成synonym
    data=[]
    random.shuffle(keys)
    for key in keys:
        value=SEDict[key]
        if(len(value[1])>0):
            data.append((key,value[1][0]))
            if(len(data)==synNum):
                break
    pd.DataFrame(data).to_csv("../result/Eva4.4Synonym.csv",index=False,encoding="utf-8")
    
    #生成abbrev
    data=[]
    random.shuffle(keys)
    for key in keys:
        value=SEDict[key]
        if(len(value[0])>0):
            data.append((key,value[0][0]))
            if(len(data)==abbrevNum):
                break
    pd.DataFrame(data).to_csv("../result/Eva4.4Abbrev.csv",index=False,encoding="utf-8")
    print("done")
















if(__name__=="__main__"):
    GetCheckCsv()
    

