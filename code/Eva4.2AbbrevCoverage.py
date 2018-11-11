# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 15:36:25 2018

@author: Administrator
"""
from sklearn.externals import joblib
import json
import codecs
import re
from gensim.models.phrases import Phrases, Phraser,original_scorer
from collections import defaultdict
import pandas as pd

def EvaAbbrevCoverage(SEDictPath="",abbrevPath="../result/WikiAbbrev.list"):
    print("==============",SEDictPath,"==================")
    SEDict=joblib.load(SEDictPath)
    WikiAbbrev=joblib.load(abbrevPath)
    fullNames=[x[0] for x in WikiAbbrev]
    terms=[]
    abbrevNums=0
    abbrevs=[]
    fullName_Abbrev_dict=defaultdict(list)    #key:term, value:[abbrev1,abbrev2]
    t=0
    for i in SEDict:
        terms.append(i)
        terms.extend(SEDict[i][1])
        if(len(SEDict[i][0])>0):
            t+=1
            fullName_Abbrev_dict[i].extend(SEDict[i][0])
            abbrevNums+=len(SEDict[i][0])
            abbrevs.extend(SEDict[i][0])
            for key in SEDict[i][1]:
                fullName_Abbrev_dict[key].extend(SEDict[i][0])
    
    print ("number full name in vocabulary",len(set(terms).intersection(set(fullNames))))
    print("SETerm abbrevations",len(set(abbrevs)))
    print("SETerm that has abbrev",t)
    print("Wiki Abbrev Pairs",len(WikiAbbrev))
    
    
    fullName=0 #wiki abbrev中full name 在SEDict的数量
    abbrev=0 # 覆盖到的full name是否含有对应的abbrev
    stu=[]
    for i in WikiAbbrev:
        if(i[0] in fullName_Abbrev_dict ):
            fullName+=1
            if  i[1] in fullName_Abbrev_dict[i[0]]:
                abbrev+=1
                stu.append(i)
            else:
                t=[i[0],i[1]]
#                t.extend(fullName_Abbrev_dict[i[0]])
#                stu.append(t)    #full name,WikiAbbrev,SEDict Abbrev
        else:
#            stu.append(i[0])
            pass
    print("Full Name that has abbreviations",fullName)
    print ("Full Name that has correct abbreviations",abbrev)
#    return list(set(fullNames).difference(set(terms)))
    return stu


if(__name__=="__main__"):
    modelName="fastText"
    res=EvaAbbrevCoverage(SEDictPath="../result/step5.1.8_ExtSEDict_fasttext_final_V5.dict",
                          abbrevPath="../result/WikiAbbrev.list")
    res=EvaAbbrevCoverage(SEDictPath="../result/step5.1.8_ExtSEDict_word2vec_final_V5.dict",
                          abbrevPath="../result/WikiAbbrev.list")
    res=EvaAbbrevCoverage(SEDictPath="../result/step5.1.8_ExtSEDict_mixed_final_V5.dict",
                          abbrevPath="../result/WikiAbbrev.list")
#    res1=EvaAbbrevCoverage(SEDictPath="../result/step5.1.3_ExtSEDict_fasttext_V5.dict",
#                      abbrevPath="../result/WikiAbbrev.list")
#    res2=EvaAbbrevCoverage(SEDictPath="../result/step5.1.3_ExtSEDict_word2vec_V5.dict",
#                          abbrevPath="../result/WikiAbbrev.list")
#    data=pd.DataFrame(res)
#    data.to_csv("../result/Eva4.2WrongAbbrev.csv",index=False,encoding="utf-8")
#    EvaAbbrevCoverage(modelName="FastText",abbrevPath="../result/tutorialspointAbbrev.list")
#    EvaAbbrevCoverage(modelName="FastText",abbrevPath="../result/tutsrajaAbbrev.list")
#    f = codecs.open("../result/step1.2.4_SOVocabulary_V1.json", encoding="utf-8")
#    vocab_so = json.load(f)
#    f.close()
#    WikiAbbrev=joblib.load("../result/WikiAbbrev.list")
#    SETerms = joblib.load("../result/step4.1.3_SETerm.list")
#    print (   len(set([x[0] for x in WikiAbbrev]).intersection(set(SETerms))  ) )
#    SEDict["regular_expression"]


######################################################






