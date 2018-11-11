# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 15:36:25 2018

@author: Administrator
"""
# (mast tag,synonym)
from sklearn.externals import joblib
import json
import codecs
from nltk.corpus import wordnet as wn
from SEUtils import isSynonym,isAbrreviation
from gensim.models import Word2Vec,FastText
from collections import defaultdict
def main(SEDictPath=""):
    print(SEDictPath)
    SEDict = joblib.load(SEDictPath)

    SOSynonymPairs = joblib.load("../result/SOSynonymPairs1.list")
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
    synonymSEGroups = []
#    for key, value in SEDict.items():
#        if  len(value[0]) > 0 or len(value[1]) > 0:
#            t = [key]
#            t.extend(value[0])
#            t.extend(value[1])
#            synonymSEGroups.append(t)
    # SE Dict
    allNo,notMatch = [],[]
    countall, countmatch = 0, 0
    c = 0
    for i in SOSynonymPairs:
#        c += 1
#        if (c % 200 == 0):
#            print(c)
        flag = 0
        master, synonym = i
        if (master.replace(".", "").replace("_", "") == synonym.replace(".", "").replace("_", "")):
            for i in synonymSEGroups:
                flag=2
                if (master in i or synonym in i or master.replace(".", "").replace("_", "") in i):
                    countall += 1
                    countmatch += 1
                    break
        else:
            for i in synonymSEGroups:
                if (synonym in i):
                    flag = 1
                    countall += 1
                    if (master in i):
                        flag=2
                        countmatch += 1
                    break
        if flag==0 :
            allNo.append((master, synonym))
        elif flag==1:
            notMatch.append((master, synonym))
#    return stu
    print("SEDict synonym match", countall)
    print("coverage",countall/len(SOSynonymPairs))
    print("SEDict synonym and tag match", countmatch)
    print("accuracy",countmatch/countall)
    # Word Net   ----------------------------------------------
#    countall, countmatch = 0, 0
#    for i in SOSynonymPairs:
#        master, synonym = i
#        synets= wn.synsets(synonym)
#        if (len(synets) > 0 ):
#            countall += 1
#            flag = True
#            for synet in synets:
#                if (master in synet.lemma_names()):
#                    countmatch += 1
#                    flag = False
#                    break
#    print("wordnet synonym match", countall)
#    print("wordnet synonym and tag match", countmatch)

    return  allNo,notMatch 


if (__name__ == "__main__"):
#    modelName = "fastText"
#    main(modelName="mixed")
    res=main(SEDictPath="../result/step5.1.3_ExtSEDict_fasttext_V5.dict")
    res=main(SEDictPath="../result/step5.1.3_ExtSEDict_word2vec_V5.dict")
    res=main(SEDictPath="../result/step5.1.3_ExtSEDict_mixed_V5.dict")
    
#    main(SEDictPath="../result/step5.1.4_ExtSEDict_fasttext_500_V5.dict")
#    main(SEDictPath="../result/step5.1.4_ExtSEDict_word2vec_800_V5.dict")
#    main(SEDictPath="../result/step5.1.4_ExtSEDict_mixed_800_800_V5.dict")
#    main(modelName="word2vec")
    ###################################################################
#    SOSynonymPairs = joblib.load("../result/SOSynonymPairs.list")
#    MergedSynonym = joblib.load("../result/step5.1.1_MergedSynonym_" + modelName.lower() + "_V5.list")
#    SETerms = joblib.load("../result/step4.1.3_SETerm_V5.list")
#    SEDict = joblib.load("../result/step5.1.3_ExtSEDict_" + modelName.lower() + "_V5.dict")
#    f = codecs.open("../result/step1.2.4_SOVocabulary_V5.json", encoding="utf-8")
#    vocab_so = json.load(f)
#    f.close()
#    c=[]
#    for i in SOSynonymPairs:
#        if i[1] in m.wv.vocab:
#            c.append(1)
#        if i[0] in vocab_so and vocab_so[i[0]]>100:
#            c+=1
#        if i[1] in vocab_so and vocab_so[i[1]]>100:
#            c+=1
#        c.append(m.wv.similarity(i[0],i[1]))
#    fasttext=FastText.load("../result/step3.1_FastText_V5/fasttext.m")
#    word2vec = Word2Vec.load("../result/step3.1_word2vec_V5/word2vec.m")
#    word2vec.delete_temporary_training_data(True) 
#    newPairs=[]
#    for i in SOSynonymPairs:
#        if i[0] not in  word2vec.wv.vocab :
#            continue
#        newPairs.append(i)
#    joblib.dump(newPairs,"../result/SOSynonymPairs1.list")
#    
#    resAllNo=[]
#    for i in allNo:
#        if i[1] in word2vec.wv.vocab and i[0] in word2vec.wv.vocab:
#            resAllNo.append((i[0],i[1],fasttext.wv.similarity(i[0],i[1]),word2vec.wv.similarity(i[0],i[1])))
#    resAllNo.sort(key=lambda x: x[2])
#    resNotMatch=[]
#    for i in notMatch:
#        if i[1] in word2vec.wv.vocab and i[0] in word2vec.wv.vocab:
#            resNotMatch.append((i[0],i[1],fasttext.wv.similarity(i[0],i[1]),word2vec.wv.similarity(i[0],i[1])))
#    resNotMatch.sort(key=lambda x: x[2])
    

#    fullNameDict=joblib.load("../result/step5.1.2_FullNameSynonym_fasttext_V5.dict")
##    res=[]
##    for i in SOSynonymPairs:
##        if isSynonym(i[0],i[1]):
##            res.append(i)
#    
#    "graphics" in SETerms
#    for i in MergedSynonym:
#        if "internal" in i:
#            print (i)
#    print(m.wv.similarity("internal","internals"))
#    print(m.wv.most_similar("figures",topn=20))
#    for key,value in fullNameDict.items():
#        if "" in value:
#            print(key,value)
#            break
#   "chars" in m.wv.vocab 
    
    
    
    
    