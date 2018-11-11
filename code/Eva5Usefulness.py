# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from lxml import etree
import re
import codecs
import random
from collections import defaultdict
from os.path import dirname
from sklearn.externals import joblib
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
def getSOTrainingSet(filePath="",diPath=""):
    SOtags=joblib.load("../result/step2.1_SOTags.dict")
    SEDict=joblib.load(diPath)
    reverseDict={}
    for key,value in SEDict.items():
        for i in value[0]:
            reverseDict[i]=key      
        for i in value[1]:
            reverseDict[i]=key        
    
    
    
    context = etree.iterparse(filePath, encoding="utf-8")
    datas, dataTags = [], []  # 存储title 和 answers
    c = 0
    reSub0 = re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")  # URL
    reSub1 = re.compile("[\[\]<>`~$\^&*=|%@(){},:\"/'\\\\]")  # replace with " "
    rePlus = re.compile("[^+]\+[^+]")
    reSplit1 = re.compile("\.[^a-z0-9]|[?!;\n\r]")
#    flag=True
    for _, elem in context:  # 迭代每一个
        c += 1
        if (c % 10000 == 0):
            print("already get record:", str(len(datas) / 10000) + "W")
#        if c>5000000:
#            flag=False
#        if flag:
#            elem.clear()
#            continue
        title, body, typeId, tags = elem.get("Title"), elem.get("Body"), elem.get("PostTypeId"), elem.get("Tags")
        elem.clear()
        if (typeId is None or int(typeId) != 1):
            continue
        if (body is not None and title is not None and tags is not None):
            if (random.random() < 0.3):
                continue
            soup = BeautifulSoup(body, "lxml")
            for pre in soup.find_all("pre"):
                if (len(pre.find_all("code")) > 0):
                    pre.decompose()
            #select sometags
            tagList=tags.replace(" ", "").replace("<", " ").replace(">", " ").replace("-", "_").lower().split()
#            print(len(tagList))
            hasSynonym=0
            for tag in tagList:
                if SOtags[tag]<80:
                    continue
                hasSynonym+=1
#                if tag in reverseDict:
#                    value=SEDict[reverseDict[tag]]
#                    if (len(value[0])+len(value[1]))>1:
#                        hasSynonym+=1
            if hasSynonym<2:
                continue
            datas.append(soup.get_text() + "\n" + BeautifulSoup(title, "lxml").get_text())
            dataTags.append(tags)

        # 开始存储到本地
        sentences = []
        if (len(datas) > 100000):
            for strText, strTags in zip(datas, dataTags):
                strText = strText.lower()
                strText = re.sub(reSub0, " ", strText)
                strText = re.sub(reSub1, " ", strText)
                # 开始处理最复杂的加号情况
                for sub in set(re.findall(rePlus, strText)):
                    strText = strText.replace(sub, sub[0] + " " + sub[2])
                # 开始分割
                strText=strText.replace("-","_")
                sent_words = []
                for sentence in re.split(reSplit1, strText):
                    t = sentence.split()
                    if (len(t) > 6):
                        sent_words.extend(t)
                sent_words.append("****")
                sent_words.extend(
                    strTags.replace(" ", "").replace("<", " ").replace(">", " ").replace("-", "_").lower().split())
                sent_words.append("\n")
                sentences.append(" ".join(sent_words))
            fw = codecs.open("../result/Eva5SO.txt", "w", encoding="utf-8")
            fw.writelines(sentences)
            fw.close()
            sentences = []
            return True


def getCPTrainingSet(diPath=""):
    SEDict=joblib.load(diPath)
    reverseDict={}
    for key,value in SEDict.items():
        for i in value[0]:
            reverseDict[i]=key      
        for i in value[1]:
            reverseDict[i]=key       
    sentences = []
    basePath = "../data/CPData/"
    reSub0 = re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")  # URL
    reSub1 = re.compile("[\[\]<>`~$\^&*=|%@(){},:\"/'\\\\]")  # replace with " "
    rePlus = re.compile("[^+]\+[^+]")
    reSplit1 = re.compile("\.[^a-z0-9]|[?!;\n\r]")
    
    fileIns=list(range(2, 116))
    fileIns.remove(72)
    for i in fileIns:
        print("file:", i,len(sentences))
        data = joblib.load(basePath + "data" + str(i) + ".d")
        for j in data:
            if (len(j) < 3):
                continue
            sent_words = []
            strText = j[0] + "\n" + j[1]
            strText = strText.lower()
            strText = re.sub(reSub0, " ", strText)
            strText = re.sub(reSub1, " ", strText)
            # 开始处理最复杂的加号情况
            for sub in set(re.findall(rePlus, strText)):
                strText = strText.replace(sub, sub[0] + " " + sub[2])
            # 开始分割
            strText=strText.replace("-","_")
            for sentence in re.split(reSplit1, strText):
                t = sentence.split()
                if (len(t) > 6):
                    sent_words.extend(t)
            sent_words.append("****")
            sent_words.extend(j[2:])
            
            #########去除没有synonym的tag
            tagList=[x.strip().lower().replace(" ","_").replace("-","_")   for x in j[2:]]
            hasSynonym=0
            for tag in tagList:
                if tag in reverseDict:
                    value=SEDict[reverseDict[tag]]
                    if (len(value[0])+len(value[1]))>1:
                        hasSynonym+=1
            if hasSynonym<1:
                continue            
            
            sent_words.append("\n")
            sentences.append(" ".join(sent_words))        
    fw = codecs.open("../result/Eva5CP.txt", "w", encoding="utf-8")
    fw.writelines(sentences)
    print(len(sentences))
    fw.close()
    return True

def Eva(filePath="", SEDictPath=""):
    print(SEDictPath)
    porter_stemmer = PorterStemmer()
    wordnet_lemmatizer = WordNetLemmatizer()
    fr = codecs.open(filePath, "r", encoding="utf-8")
    SEDict = joblib.load(SEDictPath)
    mergeSynonyms=[]
    for key,value in SEDict.items():
        t=[key]
        t.extend(value[0])
        t.extend(value[1])
        mergeSynonyms.append(t)
    #####################################################################################
    mergeSynonymsSpace=[]
    for i in mergeSynonyms:
        mergeSynonymsSpace.append([ j.replace("_"," ") for j in i])
    rdict=defaultdict(list)
    for i in range(len(mergeSynonymsSpace)):
        for j in mergeSynonymsSpace[i]:
            if i not in rdict[j]:
                rdict[j].append(i)
    #######################################################################################
    coverageOrigin, coverageSEDict, coverageWordNet, coveragePorter = [], [], [], []
    c=0
    for line in fr:   
#        c+=1
#        if c>40000:
#            break
        words, tags = line.split("****")
        words, tags =' '+words+' ', set([x.replace("_"," ") for x in tags.split()])
        # 开始计算原始的覆盖率
        
        tcount=0
        for tag in tags:
            if ' '+tag+' ' in words :
                tcount+=1
#                print (tag)
#        break
        coverageOrigin.append(tcount / float(len(tags)))
        # 计算SEDict的覆盖率
        tcount=0
        for tag in tags:
            if ' '+tag+' ' in words:
                tcount+=1
                continue
            if tag in rdict:
#                print("ZHDUN!")
                flag=False
                for okey in rdict[tag]:
                    for x in mergeSynonymsSpace[okey]:
                        if ' '+x+' ' in words:
                            tcount+=1
                            flag=True
                            break
                    if flag:
                        break
        coverageSEDict.append(tcount / float(len(tags)))
#
##        # 计算WordNet的覆盖率
        newWords=' '+" ".join([ wordnet_lemmatizer.lemmatize(x) for x in words.split(" ")])+' '
        newTags=[wordnet_lemmatizer.lemmatize(x) for x in tags]
        tcount=0
        for tag in newTags:
            if ' '+tag+' ' in newWords:
                tcount+=1
        coverageWordNet.append(tcount / float(len(tags)))
##        # 计算PorterStemmer的覆盖率
        newWords=' '+" ".join([ porter_stemmer.stem(x) for x in words.split(" ")])+' '
        newTags=[porter_stemmer.stem(x) for x in tags]
        tcount=0
        for tag in newTags:
            if ' '+tag+' ' in newWords:
                tcount+=1
        coveragePorter.append(tcount / float(len(tags)))

    # 输出结果
    print("coverageOrigin:", sum(coverageOrigin) / len(coverageOrigin))

    print("coveragePorter:", sum(coveragePorter) / len(coveragePorter))
    print("coverageWordNet:", sum(coverageWordNet) / len(coverageWordNet))
    print("coverageSEDict:", sum(coverageSEDict) / len(coverageSEDict))
    fr.close()
    return coverageSEDict

def getTestSetTags():
    res=[]
    fr=codecs.open("../result/Eva5SO.txt",encoding="utf-8")
    for line in fr:   
        words, tags = line.split("****")
        words, tags =' '+words+' ',   tags.split()
        for tag in tags:
            if ' '+tag.replace("_"," ")+' ' not in words:
                res.append(tag)
    fr.close()
    fr=codecs.open("../result/Eva5CP.txt",encoding="utf-8")
    for line in fr:   
        words, tags = line.split("****")
        words, tags =' '+words+' ',   tags.split()
        for tag in tags:
            if ' '+tag.replace("_"," ")+' ' not in words:
                res.append(tag)
    fr.close()
    res=list(set(res))
    di={}
    for i in res:
        di[i]=500
    joblib.dump(di,"../result/Eva5Tags.dict")
    return res
if (__name__ == "__main__"):
    print("start")
#    print(dirname(__file__))
#    getSOTrainingSet(filePath=dirname(dirname(__file__))+"/data/Posts.xml",
#                     diPath="../result/step5.1.3_ExtSEDict_fasttext_V5.dict")
#    getCPTrainingSet(diPath="../result/step5.1.3_ExtSEDict_fasttext_V5.dict")
    print("====================================SO=============================")
#    res=Eva(filePath="../result/Eva5SO.txt",SEDictPath="../result/step5.1.5_ExtSEDict_fasttext_500_V5.dict")
#    res=Eva(filePath="../result/Eva5SO.txt",SEDictPath="../result/step5.1.5_ExtSEDict_word2vec_500_V5.dict")
#    res=Eva(filePath="../result/Eva5SO.txt",SEDictPath="../result/step5.1.5_ExtSEDict_mixed_500_V5.dict")
#    res=getTestSetTags()
    print("====================================CP=============================")
#    res=Eva(filePath="../result/Eva5CP.txt",SEDictPath="../result/step5.1.5_ExtSEDict_fasttext_500_V5.dict")
#    res=Eva(filePath="../result/Eva5CP.txt",SEDictPath="../result/step5.1.5_ExtSEDict_word2vec_500_V5.dict")
#    res=Eva(filePath="../result/Eva5CP.txt",SEDictPath="../result/step5.1.5_ExtSEDict_mixed_500_V5.dict")
    pass