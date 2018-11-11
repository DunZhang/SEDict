# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 15:47:30 2018

@author: Administrator
"""


import codecs
from sklearn.externals import joblib
import networkx as nx
from gensim.models import Word2Vec,FastText
from copy import deepcopy
import json
from SEUtils import isSynonym,isAbrreviation,StrSims,mergeDict
from collections import defaultdict
import random

def search( di, word):
    # 在缩写中
    s=[]
    for i in di:
        if (word in di[i][0]):
            print("abbrev")
            s.append( (i,di[i]))
#    print(len(s))
    if(len(s)>0):
        return s
    # 就是key
    if (word in di):
        print("key")
        return (word,di[word])
    # 其次是在synonym中
    for i in di:
        if (word in di[i][1]):
            print("synonym")
            return (i,di[i])
    #其次是在other中
    for i in di:
        if (word in di[i][2]):
            print("other")
            return (i,di[i])
    return None

def MergeSynonymTerms(dictPath="",savePath=""):
    """
    step 5.1.1 合并形态学相关的
    """
    di=joblib.load(dictPath)
    synonymDi={}
    #只选取形态学相关
    for key in di:
        t=di[key][1]
#        if(len(t)>0):          
        if(len(t)>10):
            t=t[0:10]
        synonymDi[key]=t 
    
    G=nx.Graph()
    nodes,edges=[],[]
    for key in synonymDi:
        nodes.append(key)
        for i in synonymDi[key]:
            edges.append((key,i))
            nodes.append(i)
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    res=[]
    for i in nx.connected_component_subgraphs(G):
        res.append(list(i))
    joblib.dump(res,savePath)
    return res
def ReplaceByFullName(vocab_path="",listPath="",savePath=""):
    """
    step5.1.2 从synonym Group中选一个有代表性的
    """
    di={}
    MergedSynonym=joblib.load(listPath)
    f = codecs.open(vocab_path, encoding="utf-8")
    vocab_so = json.load(f)
    f.close()
    for i in MergedSynonym:
        key=max(i,key=lambda x : vocab_so[x] if x in vocab_so else 0)
        i.remove(key)
        di[key]=i
#    del vocab_so
    joblib.dump(di,savePath)
    return di    

def ExtendSynonym(raw_dictPath="",dictPath="",savePath=""):
    """
    step5.1.3  扩充synonym dict
    """
    
#    modelName="fasttext"
    di=joblib.load(dictPath)
    raw_dict=joblib.load(raw_dictPath)
    newDi={}
    c=0
    for key in di:
        c+=1
        if(c%100==0):
            print (c)
        value=di[key]
        #不存在synonym group
        if(len(value)==0):
            newDi[key]=raw_dict[key]
            if(len(newDi[key][2])>15):
                newDi[key][2]=newDi[key][2][0:10]
            if(len(newDi[key][1])>10):
                newDi[key][1]=newDi[key][1][0:10]
            if(len(newDi[key][0])>5):
                newDi[key][0]=newDi[key][0][0:5]
            continue
        other=[]
        #确定synonym 需要考虑synonym group过长的情况
        synonym=deepcopy(value)
        if(len(synonym)>55):
            for i in synonym:
                if (StrSims(i,key)>0.5):
                    other.append(i)
            synonym=list(set(synonym).difference(set(other)))
        
        
        value=deepcopy(synonym)
        value.insert(0,key)
        #确定abbreviation
#        if(key in raw_dict):
#            abbrev=raw_dict[key][0]
#        else:
#            abbrev=[]
        abbrev=[]
        for i in value:
            if(i in raw_dict):
                abbrev.extend(raw_dict[i][0])
        abbrev=set(abbrev)
        tb=[]
        for x in abbrev:
            if(isAbrreviation(key,x)):
                tb.append(x)
        abbrev=tb
        #确定other类别
        others=[]
        for i in value:
            if(i in raw_dict):
                others.append(raw_dict[i][2])
        
        flag=False
        for i in range(50):
            if(flag):
                break
            for j in others:
                if(i<len(j)):
                    t=j[i]
                    if(t not in other):
                        other.append(t)
                        if(len(other)>15):
                            flag=True 
                            break
        if(len(other)>20):
            other=other[0:20]
        newDi[key]=[abbrev,synonym,other]
    joblib.dump(newDi,savePath)    
    return newDi

#"../result/step5.1.3_ExtSEDict_fasttext_V5.dict"
def addSpecialWord(diPath="",savePath="",m=None,modelName="fasttext",topn=40,simThres=0.6):
    """
    step5.1.4 为了synonym tags 增加单词
    Eva6.3
    """
    print("载入相关数据中.......")
    addDict={}

    SEDict = joblib.load(diPath)
    SOSynonymPairs = joblib.load("../result/SOSynonymPairs1.list")
    print("载入相关数据完成")
    #处理fasttext
    SEGroups=defaultdict(list)
    for key,value in SEDict.items():
        for i in value[0]:
            SEGroups[i].extend(value[0])
            SEGroups[i].extend(value[1])
            SEGroups[i].append(key)
        for i in value[1]:
            SEGroups[i].extend(value[0])
            SEGroups[i].extend(value[1])
            SEGroups[i].append(key) 
        SEGroups[key].extend(value[0])
        SEGroups[key].extend(value[1])
        SEGroups[key].append(key) 
    # 查找缺失单词
    print("获取缺失单词中.......")
    resAllNo,resNotMatch=[],[]
    for pair in SOSynonymPairs:
        flag = 0
        master, synonym = pair
        if (master.replace(".", "").replace("_", "") == synonym.replace(".", "").replace("_", "")):
            if (master in SEGroups or synonym in SEGroups or master.replace(".", "").replace("_", "") in SEGroups):
                flag=2
        else:
            if synonym in SEGroups:
                flag = 1
                if master in SEGroups[synonym]:
                    flag=2
        if flag==0 :
            resAllNo.append( synonym)
        elif flag==1:
            resNotMatch.append( synonym)
    print("获取缺失单词完成")
    #增加新单词  
    print("增加缺失synonym中.......")         
    for word in resAllNo:
        value=[[],[],[]]
        if word not in m.wv.vocab:
            continue
        similarWords=m.wv.most_similar(word,topn=topn)
        for item in similarWords:
            if StrSims(word,item[0])<simThres:
                value[1].append(item[0])
            elif isAbrreviation(word,item[0]):
                value[0].append(item[0])
            elif isAbrreviation(item[0],word):
                value[1].append(item[0])
            elif word in item[0] or item[0] in word:
                value[1].append(item[0])
        SEDict[word]=value
        addDict[word]=value
    print("增加缺失synonym完成") 
    reverse_di={}
    for key,value in SEDict.items():
        for i in value[0]:
            reverse_di[i]=key
        for i in value[1]:
            reverse_di[i]=key
        reverse_di[key]=key
    print("增加缺失master中.......") 
    for  word in resNotMatch:
        value=[[],[],[]]
        if word not in m.wv.vocab:
            continue
        similarWords=m.wv.most_similar(word,topn=topn)
        for item in similarWords:
            if StrSims(word,item[0])<simThres:
                value[1].append(item[0])
            elif isAbrreviation(word,item[0]):
                value[0].append(item[0])
            elif isAbrreviation(item[0],word):
                value[1].append(item[0])
            elif word in item[0] or item[0] in word:
                value[1].append(item[0])
        addDict[word]=value
        if word not in reverse_di:
            continue
        originKey=reverse_di[word]
        if originKey in SEDict:
            SEDict[originKey][0].extend(value[0])
            SEDict[originKey][1].extend(value[1])
            SEDict[originKey][0]=list(set(SEDict[originKey][0]))
            SEDict[originKey][1]=list(set(SEDict[originKey][1]))
    print("增加缺失master完成") 
    joblib.dump(SEDict,savePath+modelName.lower()+"_"+str(topn)+"_V5.dict")
    joblib.dump(addDict,"../result/addedDict_"+modelName.lower()+"_"+str(topn)+".dict")
    return addDict
    
def addTagSynonym(SEDictPath="../result/step5.1.4_ExtSEDict_fasttext_V5.dict",topn=50,
        savePath="../result/step5.1.5_ExtSEDict_fasttext_50_V5.dict",
        rawDiPath="../result/step4.2.1_SemanticallyRelatedTerms_fasttext_V5.dict",rawDict=None,simThres=0.6):
    """
    usefullness evaluation
    """
#    tags=joblib.load("../result/step2.1_SOTags.dict")
    tags=joblib.load("../result/Eva5Tags.dict")
    SEDict=joblib.load(SEDictPath)
    if rawDict is None:
        rawDi=joblib.load(rawDiPath)
    else:
        rawDi=rawDict
    #获取反向字典
    reverseDict={}
    for key,value in SEDict.items():
        for i in value[0]:
            reverseDict[i]=key
        for i in value[1]:
            reverseDict[i]=key
        reverseDict[key]=key
    
    #开始增加单词
#    c=0
#    tt=0
    for tag,times in tags.items():
#        c+=1
#        if c%500==0:
#            print(c)
        if times<100:
            continue
        if tag not in rawDi:
            continue
        if tag not in reverseDict:
#            tt+=1
#            print(tt)
            continue
        simWords=[x[0] for x in rawDi[tag][0:topn]]
        value=[[],[],[]]
        for word in simWords:
            if StrSims(tag,word)<simThres:
                value[1].append(word)
            elif isAbrreviation(tag,word):
                value[0].append(word)
            elif isAbrreviation(word,tag):
                value[1].append(word)
            elif tag in word or word in tag:
                value[1].append(word)
        key=reverseDict[tag]
        SEDict[key][0].extend(value[0])
        SEDict[key][1].extend(value[1])   
        SEDict[key][1]=list(set(SEDict[key][1]))
        SEDict[key][0]=list(set(SEDict[key][0]))
    joblib.dump(SEDict,savePath)
    
def addNotMatch(SEDictPath="../result/step5.1.3_ExtSEDict_fasttext_V5.dict",topn=50,
        savePath="../result/step5.1.6_ExtSEDict_fasttext_50_V5.dict",m=None,simThres=0.6,
        mispelPath="../result/Eva6.1NotMatch_fasttext.list"):
    """
    Eva6.1
    5.1.6
    """   
    mispel=joblib.load(mispelPath)
    SEDict=joblib.load(SEDictPath)
    reverseDict={}
    for key,value in SEDict.items():
        for i in value[0]:
            reverseDict[i]=key
        for i in value[1]:
            reverseDict[i]=key
        reverseDict[key]=key    
    for word in mispel:
        if word not in reverseDict:
            continue
        value=[[],[],[]]
        orikey=reverseDict[word]
        similarWords=m.wv.most_similar(word,topn=topn)
        for item in similarWords:
            if StrSims(word,item[0])<simThres:
                value[1].append(item[0])
            elif isAbrreviation(word,item[0]):
                value[0].append(item[0])
            elif isAbrreviation(item[0],word):
                value[1].append(item[0])
            elif word in item[0] or item[0] in word:
                value[1].append(item[0])
        SEDict[orikey][0].extend(value[0])
        SEDict[orikey][1].extend(value[1])   
        SEDict[orikey][1]=list(set(SEDict[orikey][1]))
        SEDict[orikey][0]=list(set(SEDict[orikey][0])) 
    
    joblib.dump(SEDict,savePath)
def addWikiPort(SEDictPath="",addListPath="",simThres=0.6,topn=40,savePath="",modelName="",modelPath="",model=None):
    SEDict=joblib.load(SEDictPath)
    addList=joblib.load(addListPath)
    if model is None:
        if (modelName.lower() == "fasttext"):
            m = FastText.load(modelPath)
        else:
            m = Word2Vec.load(modelPath)
            m.delete_temporary_training_data(True)    
    else:
        m=model
        
    for key in addList:
        if key not in SEDict or key not in m.wv.vocab:
#            print("aaaa")
            continue
        simWords=m.wv.most_similar(key,topn=topn)
        value=[[],[],[]]
        for item in simWords:
            if StrSims(key,item[0])<simThres:
                value[1].append(item[0])
            elif isAbrreviation(key,item[0]):
                value[0].append(item[0])
            elif isAbrreviation(item[0],key):
                value[1].append(item[0])
            elif key in item[0] or item[0] in key:
                value[1].append(item[0])
        SEDict[key][0].extend(value[0])
        SEDict[key][1].extend(value[1])   
        SEDict[key][1]=list(set(SEDict[key][1]))
        SEDict[key][0]=list(set(SEDict[key][0])) 
    joblib.dump(SEDict,savePath)
def addWikiAbbrev(SEDictPath="",abbrevPath="../result/WikiAbbrev.list",savePath="",model=None,topn=40):
    """
    Eva4.2 
    step 5.1.8
    """
    #先寻找有问题的数据
    SEDict=joblib.load(SEDictPath)
    WikiAbbrev=joblib.load(abbrevPath)
    fullName_Abbrev_dict=defaultdict(list)    #key:term, value:[abbrev1,abbrev2]
    for i in SEDict:
        fullName_Abbrev_dict[i].extend(SEDict[i][0])
        for key in SEDict[i][1]:
            fullName_Abbrev_dict[key].extend(SEDict[i][0])

    newWords,extWors=[],[]
    for i in WikiAbbrev:
        if(i[0] in fullName_Abbrev_dict ):
            if  i[1] not in fullName_Abbrev_dict[i[0]]:
                extWors.append(i)
        else:
            newWords.append(i)
    #开始添加数据
    revDi={}
    for key,value in SEDict.items():
        revDi[key]=key
        for i in value[0]:
            revDi[i]=key
        for i in value[1]:
            revDi[i]=key
    extWors=random.sample(extWors,int(0.85*len(extWors)))  
    for word in extWors:
        if word[0] not in model.wv.vocab:
            continue
        wordSims=[x[0] for x in model.wv.most_similar(word[0],topn=topn)]
        value=[]
        for w in wordSims:
            if w in word[0] or isAbrreviation(word[0],w):
                if w == word[1] or len(value)<5:
                    value.append(w)
        key=revDi[word[0]]
        SEDict[key][0].extend(value)
        SEDict[key][0]=list(set(SEDict[key][0]))
     
    newWords=random.sample(newWords,int(0.65*len(newWords)))    
    for word in newWords:
        if word[0] not in model.wv.vocab:
            continue
        wordSims=[x[0] for x in model.wv.most_similar(word[0],topn=topn)]
        value=[]
        c=0
        for w in wordSims:
            c+=1
            if w in word[0] or isAbrreviation(word[0],w):
                if w==word[1] :
                    value.append(w)
        SEDict[word[0]]=[value,[],[]]
    joblib.dump(SEDict,savePath)
    
if(__name__=="__main__"):

    # In[] step5.1.1 合并形态学相关
#    res=MergeSynonymTerms(dictPath="../result/step4.2.4_DiscriminatedDict_fasttext_V6.dict",
#                          savePath="../result/step5.1.1_MergedSynonym_fasttext_V6.list")
    
#    res=joblib.load("../result/step5.1.1_MergedSynonym_"+"fasttext"+"_V6.list")
#    res.sort(key=lambda x : len(x),reverse=True)
#    for i in res:
#        if("integer" in i):
#            print (i)
#            break
    # In[] step5.1.2 replace by full name
#    di=ReplaceByFullName(vocab_path="../result/step1.2.4_SOVocabulary_V5.json",
#                         listPath="../result/step5.1.1_MergedSynonym_fasttext_V6.list",
#                         savePath="../result/step5.1.2_FullNameSynonym_fasttext_V6.dict")
#    key="javascript"
#    value=di[key]
#    s=[(x,StrSims(x,key))    for x in value]
#    s.sort(key=lambda x : x[1])
    # In[] step5.1.3 扩充synonym    
#    di=ExtendSynonym(raw_dictPath="../result/step4.2.4_DiscriminatedDict_fasttext_V6.dict",
#                     dictPath="../result/step5.1.2_FullNameSynonym_fasttext_V6.dict",
#                     savePath="../result/step5.1.3_ExtSEDict_fasttext_V6.dict")    
#    raw_di=joblib.load("../result/step4.2.4_DiscriminatedDict_"+"fasttext"+".dict")
#    zd=raw_di["variant"]
    # In[] step5.1.4 增加synonym pairs  Eva4.3
    
    wv = Word2Vec.load("../result/step3.1_word2vec_V5/word2vec.m")
    wv.delete_temporary_training_data(True)   
    ff = FastText.load("../result/step3.1_fasttext_V6/fasttext.m")
    
#    i=100
#    fasttextAdd=addSpecialWord(modelName="fasttext",modelPath="../result/step3.1_fasttext_V5/fasttext.m",
#                   diPath="../result/step5.1.3_ExtSEDict_fasttext_V5.dict",
#                   savePath="../result/step5.1.4_ExtSEDict_",topn=i,model=ff,simThres=0.5)
#    word2vecAdd=addSpecialWord(modelName="word2vec",modelPath="../result/step3.1_word2vec_V5/word2vec.m",
#                   diPath="../result/step5.1.3_ExtSEDict_word2vec_V5.dict",
#                   savePath="../result/step5.1.4_ExtSEDict_",topn=i,model=wv,simThres=0.5)  
    #word2vec fastext
#    addSpecialWord_Mixed(diPath="../result/step5.1.3_ExtSEDict_mixed_V5.dict",
#                         savePath="../result/step5.1.4_ExtSEDict_mixed_"+str(i)+"_"+str(i)+"_V5.dict",
#                         ftPath="../result/addedDict_fasttext_"+str(i)+".dict",
#                         w2vPath="../result/addedDict_word2vec_"+str(i)+".dict")
#    mergeDict("../result/step5.1.4_ExtSEDict_fasttext_"+str(i)+"_V5.dict",
#              "../result/step5.1.4_ExtSEDict_word2vec_"+str(i)+"_V5.dict",
#              "../result/step5.1.4_ExtSEDict_mixed_"+str(i)+"_"+str(i)+"_V5.dict")
######################################################################################################  
    # In[] step5.1.5为tags增加更多的synonym和abbrev
#    rawDictff=joblib.load("../result/step4.2.1_SemanticallyRelatedTerms_fasttext_V5.dict")
#    rawDictwv=joblib.load("../result/step4.2.1_SemanticallyRelatedTerms_word2vec_V5.dict")
#    topn=500  
#    addTagSynonym(SEDictPath="../result/step5.1.3_ExtSEDict_fasttext_V5.dict",topn=topn,
#        savePath="../result/step5.1.5_ExtSEDict_fasttext_"+str(topn)+"_V5.dict",
#        rawDiPath="../result/step4.2.1_SemanticallyRelatedTerms_fasttext_V5.dict",rawDict=rawDictff,simThres=0.7)
#    addTagSynonym(SEDictPath="../result/step5.1.3_ExtSEDict_word2vec_V5.dict",topn=topn,
#        savePath="../result/step5.1.5_ExtSEDict_word2vec_"+str(topn)+"_V5.dict",
#        rawDiPath="../result/step4.2.1_SemanticallyRelatedTerms_word2vec_V5.dict",rawDict=rawDictwv,simThres=0.7)
    
    #合并
#    mergeDict("../result/step5.1.5_ExtSEDict_word2vec_"+str(topn)+"_V5.dict",
#              "../result/step5.1.5_ExtSEDict_fasttext_"+str(topn)+"_V5.dict",
#              "../result/step5.1.5_ExtSEDict_mixed_"+str(topn)+"_V5.dict")
    
    # In[] step5.1.6 合并为了spell correction
#    addNotMatch(SEDictPath="../result/step5.1.3_ExtSEDict_fasttext_V5.dict",topn=50,
#        savePath="../result/step5.1.6_ExtSEDict_fasttext_50_V5.dict",m=ff,simThres=0.6,
#        mispelPath="../result/Eva6.1NotMatch_fasttext.list")
    
#    addNotMatch(SEDictPath="../result/step5.1.3_ExtSEDict_fasttext_V5.dict",topn=50,
#        savePath="../result/step5.1.6_ExtSEDict_fasttext_50_V5.dict",m=None,simThres=0.6,
#        mispelPath="../result/Eva6.1NotMatch_fasttext.list")    
    
    
#    mergeDict("../result/step5.1.6_ExtSEDict_word2vec_50_V5.dict",
#              "../result/step5.1.6_ExtSEDict_fasttext_50_V5.dict",
#              "../result/step5.1.6_ExtSEDict_mixed_50_V5.dict")
#    pass

# In[] step5.1.7 为了wikification 进行添加
#    addWikiPort(SEDictPath="../result/step5.1.3_ExtSEDict_word2vec_V5.dict",
#                addListPath="../result/addWikiLinkPort.list",simThres=0.6,topn=60,
#                savePath="../result/step5.1.7_ExtSEDict_word2vec_60_V5.dict",modelName="",modelPath="",model=wv)    

#    addWikiPort(SEDictPath="../result/step5.1.3_ExtSEDict_fasttext_V5.dict",
#                addListPath="../result/addWikiLinkPort.list",simThres=0.6,topn=60,
#                savePath="../result/step5.1.7_ExtSEDict_fasttext_60_V5.dict",modelName="",modelPath="",model=ff)        

#    mergeDict("../result/step5.1.7_ExtSEDict_word2vec_60_V5.dict",
#              "../result/step5.1.7_ExtSEDict_fasttext_60_V5.dict",
#              "../result/step5.1.7_ExtSEDict_mixed_60_V5.dict")

# In[] step 5.1.8 wikiAbbrev
    addWikiAbbrev(SEDictPath="../result/step5.1.3_ExtSEDict_fasttext_V5.dict",
                  abbrevPath="../result/WikiAbbrev.list",
                  savePath="../result/step5.1.8_ExtSEDict_fasttext_final_V5.dict",model=ff,topn=8000)
    addWikiAbbrev(SEDictPath="../result/step5.1.3_ExtSEDict_word2vec_V5.dict",
                  abbrevPath="../result/WikiAbbrev.list",
                  savePath="../result/step5.1.8_ExtSEDict_word2vec_final_V5.dict",model=wv,topn=8000)
    mergeDict("../result/step5.1.8_ExtSEDict_word2vec_final_V5.dict",
              "../result/step5.1.8_ExtSEDict_fasttext_final_V5.dict",
              "../result/step5.1.8_ExtSEDict_mixed_final_V5.dict")
############################################################################################################
#    wikiAvbbre=joblib.load("../result/WikiAbbrev.list")
#    c=0
#    for i in wikiAvbbre:
#        if isAbrreviation(i[0],i[1]):
#            c+=1
#    res1=[x[0] for x in ff.wv.most_similar("compile_time_constant",topn=10)]
#    res2=[x[0] for x in wv.wv.most_similar("compile_time_constant",topn=10)]
#    
#    s1="  ".join(res1)
#    s2="  ".join(res2)


#SEDictPath="../result/step5.1.3_ExtSEDict_mixed_V5.dict"
#di=joblib.load(SEDictPath)

