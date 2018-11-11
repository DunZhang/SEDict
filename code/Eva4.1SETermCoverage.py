# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 14:32:51 2018

@author: Administrator
"""
from sklearn.externals import joblib
import string
import re
import json
import codecs
from gensim.models import Word2Vec,FastText
from os.path import dirname
modelName="fasttext"
def GetCovergeSOTags(modelName="fasttext"):
    """
    测试我们的词典在tags中的覆盖率
    :param modelName:
    :return:
    """
    # 不同单词个数的覆盖率
#    modelName = "fastText"
    tagTerms, tagTerms_1, tagTerms_2, tagTerms_3, tagTerms_4more = [], [], [], [], []  # n元术语
    di = joblib.load("../result/step2.1_SOTags.dict")
    tagnums = 0
    for key, value in di.items():
        tagnums += 1
        if (value > 30):
            tagTerms.append(key)
            t = len(re.findall("_", key))
            if (t == 0):
                tagTerms_1.append(key)
            elif (t == 1):
                tagTerms_2.append(key)
            elif (t == 2):
                tagTerms_3.append(key)
            else:
                tagTerms_4more.append(key)
    #    return tagTerms_4more
    print("All SO Tags Numbers", tagnums)
    print("SO Tags Num>30times", len(tagTerms))
    SEDict = joblib.load( "../result/step5.1.3_ExtSEDict_" + modelName.lower() + "_V5.dict")
    #    SEDict=json.load(codecs.open("../result/cleanDic.json",'r',encoding="utf-8"))
    SETerms = []
    for i in SEDict:
        SETerms.extend(SEDict[i][0])
        SETerms.extend(SEDict[i][1])
        SETerms.append(i)
    SETerms = set(SETerms)
    tagTerms = set(tagTerms)
    tagTerms_1, tagTerms_2, tagTerms_3, tagTerms_4more = \
        set(tagTerms_1), set(tagTerms_2), set(tagTerms_3), set(tagTerms_4more)

    print("SEDict software specifc terms num", len(SEDict))
    print("SOTags coverged", len(SETerms.intersection(tagTerms)))
#    return list(tagTerms_2.difference(SETerms))
    print("all coverage ratio", len(SETerms.intersection(tagTerms)) / float(len(tagTerms)))
    print("1-tag number and coverage ratio", len(tagTerms_1),
          len(SETerms.intersection(tagTerms_1)) / float(len(tagTerms_1)))
    print("2-tag number and coverage ratio", len(tagTerms_2),
          len(SETerms.intersection(tagTerms_2)) / float(len(tagTerms_2)))
    print("3-tag number and coverage ratio", len(tagTerms_3),
          len(SETerms.intersection(tagTerms_3)) / float(len(tagTerms_3)))
    print("4more-tag number and coverage ratio", len(tagTerms_4more),
          len(SETerms.intersection(tagTerms_4more)) / float(len(tagTerms_4more)))
    # 不同频次 的覆盖率
    tagTerms_1, tagTerms_2, tagTerms_3, tagTerms_4more = [], [], [], []  #代表不同的频次
    totalUsageTimes, usageTimes30_100 = 0, 0 #tag被使用的次数
    for key, value in di.items():
        if (value > 30):
            totalUsageTimes += value
            if (value < 100):
                usageTimes30_100 += value
                tagTerms_1.append(key)
            elif (value < 1000):
                tagTerms_2.append(key)
            elif (value < 10000):
                tagTerms_3.append(key)
            else:
                tagTerms_4more.append(key)
    print("total usage times", totalUsageTimes)
    print("30-100 total times", usageTimes30_100)
    tagTerms_1, tagTerms_2, tagTerms_3, tagTerms_4more = \
        set(tagTerms_1), set(tagTerms_2), set(tagTerms_3), set(tagTerms_4more)

    print("term freq30-100 number and coverage ratio", len(tagTerms_1),
          len(SETerms.intersection(tagTerms_1)) / float(len(tagTerms_1)))
    print("term freq100-1000 number and coverage ratio", len(tagTerms_2),
          len(SETerms.intersection(tagTerms_2)) / float(len(tagTerms_2)))
    print("term freq1000-10000 number and coverage ratio", len(tagTerms_3),
          len(SETerms.intersection(tagTerms_3)) / float(len(tagTerms_3)))
    print("term freq10000+ number and coverage ratio", len(tagTerms_4more),
          len(SETerms.intersection(tagTerms_4more)) / float(len(tagTerms_4more)))

def GetCovergeSOTags1(SETermPath=""):
    """
    测试我们的词典在tags中的覆盖率
    :param modelName:
    :return:
    """
    # 不同单词个数的覆盖率
#    modelName = "fastText"
    print("SO",SETermPath)
    tagTerms, tagTerms_1, tagTerms_2, tagTerms_3, tagTerms_4more = [], [], [], [], []  # n元术语
    di = joblib.load("../result/step2.1_SOTags.dict")
    tagnums = 0
    for key, value in di.items():
        tagnums += 1
        if (value > 30):
            tagTerms.append(key)
            t = len(re.findall("_", key))
            if (t == 0):
                tagTerms_1.append(key)
            elif (t == 1):
                tagTerms_2.append(key)
            elif (t == 2):
                tagTerms_3.append(key)
            else:
                tagTerms_4more.append(key)
    print("All SO Tags Numbers", tagnums)
    print("SO Tags Num>30times", len(tagTerms))
    SETerms=set(joblib.load(SETermPath))
    tagTerms = set(tagTerms)
    tagTerms_1, tagTerms_2, tagTerms_3, tagTerms_4more = \
        set(tagTerms_1), set(tagTerms_2), set(tagTerms_3), set(tagTerms_4more)

#    print("SEDict software specifc terms num", len(SEDict))
    print("SOTags coverged", len(SETerms.intersection(tagTerms)))
#    return list(tagTerms_2.difference(SETerms))
    print("all coverage ratio", len(SETerms.intersection(tagTerms)) / float(len(tagTerms)))
    print("1-tag number and coverage ratio", len(tagTerms_1),
          len(SETerms.intersection(tagTerms_1)) / float(len(tagTerms_1)))
    print("2-tag number and coverage ratio", len(tagTerms_2),
          len(SETerms.intersection(tagTerms_2)) / float(len(tagTerms_2)))
    print("3-tag number and coverage ratio", len(tagTerms_3),
          len(SETerms.intersection(tagTerms_3)) / float(len(tagTerms_3)))
    print("4more-tag number and coverage ratio", len(tagTerms_4more),
          len(SETerms.intersection(tagTerms_4more)) / float(len(tagTerms_4more)))
    # 不同频次 的覆盖率
    tagTerms_1, tagTerms_2, tagTerms_3, tagTerms_4more = [], [], [], []  #代表不同的频次
    totalUsageTimes, usageTimes30_100 = 0, 0 #tag被使用的次数
    for key, value in di.items():
        if (value > 30):
            totalUsageTimes += value
            if (value < 100):
                usageTimes30_100 += value
                tagTerms_1.append(key)
            elif (value < 1000):
                tagTerms_2.append(key)
            elif (value < 10000):
                tagTerms_3.append(key)
            else:
                tagTerms_4more.append(key)
    print("total usage times", totalUsageTimes)
    print("30-100 total times", usageTimes30_100)
    tagTerms_1, tagTerms_2, tagTerms_3, tagTerms_4more = \
        set(tagTerms_1), set(tagTerms_2), set(tagTerms_3), set(tagTerms_4more)

    print("term freq30-100 number and coverage ratio", len(tagTerms_1),
          len(SETerms.intersection(tagTerms_1)) / float(len(tagTerms_1)))
    print("term freq100-1000 number and coverage ratio", len(tagTerms_2),
          len(SETerms.intersection(tagTerms_2)) / float(len(tagTerms_2)))
    print("term freq1000-10000 number and coverage ratio", len(tagTerms_3),
          len(SETerms.intersection(tagTerms_3)) / float(len(tagTerms_3)))
    print("term freq10000+ number and coverage ratio", len(tagTerms_4more),
          len(SETerms.intersection(tagTerms_4more)) / float(len(tagTerms_4more)))
def GetCovergeCPTags(modelName="fasttext"):
    """
    测试我们的词典在tags中的覆盖率
    :param modelName:
    :return:
    """
    CPTags = joblib.load("../result/CPTags.list")

    tagTerms = set([i[0] for i in CPTags])
    print("CPTags num", len(tagTerms))
    SEDict = joblib.load("../result/step5.1.3_ExtSEDict_" + modelName.lower() + "_V5.dict")
    SETerms = []
    for i in SEDict:
        SETerms.extend(SEDict[i][0])
        SETerms.extend(SEDict[i][1])
        SETerms.append(i)
    SETerms=set(SETerms)
    print("coverage number and ratio in CPTags",len(SETerms.intersection(tagTerms)),len(SETerms.intersection(tagTerms))/float(len(tagTerms)))

def GetCovergeCPTags1(SETermPath=""):
    """
    测试我们的词典在tags中的覆盖率
    :param modelName:
    :return:
    """
    print("CP",SETermPath)
    CPTags = joblib.load("../result/CPTags.list")

    tagTerms = set([i[0] for i in CPTags])
    print("CPTags num", len(tagTerms))
#    SEDict = joblib.load("../result/step5.1.3_ExtSEDict_" + modelName.lower() + "_V5.dict")
#    SETerms = []
#    for i in SEDict:
#        SETerms.extend(SEDict[i][0])
#        SETerms.extend(SEDict[i][1])
#        SETerms.append(i)
    SETerms=set(joblib.load(SETermPath))
    print("coverage number and ratio in CPTags",len(SETerms.intersection(tagTerms)),len(SETerms.intersection(tagTerms))/float(len(tagTerms)))

if (__name__ == "__main__"):
#    setrems=joblib.load(PROJ_PATH+"/result/step4.1.3_SETerm.list")
#    res=GetCovergeSOTags1(SETermPath="../result/step4.1.3_SETerm_15_60_default_V1.list")
    res=GetCovergeSOTags1(SETermPath="../result/step4.1.3_SETerm_15_0.7_npmi_V1.list")
    
    
#    res=GetCovergeCPTags1(SETermPath="../result/step4.1.3_SETerm_15_40_default_V1.list")
#    res=GetCovergeCPTags1(SETermPath="../result/step4.1.3_SETerm_15_20_default_V5.list")
#    m=FastText.load(PROJ_PATH+"/result/step3.1_FastText_V1/fasttext.m")
#    t=[]
#    for i in setrems:
#        if i not in m.wv.vocab:
#            t.append(i)
#    print (len(  set(setrems).intersection(set(res))  ))
#    GetCovergeCPTags("fasttext")
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     