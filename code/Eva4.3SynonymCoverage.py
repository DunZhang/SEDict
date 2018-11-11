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
    numSynonymTerms,numGroups=0,0
    SOSynonymPairs = joblib.load("../result/SOSynonymPairs1.list")
    TSEGroups=defaultdict(list)
    for key,value in SEDict.items():
        if len(value[0])>0 or len(value[1])>0:
            numGroups+=1
        numSynonymTerms+=(1+len(value[0])+len(value[1]))
        for i in value[0]:
            TSEGroups[i].extend(value[0])
            TSEGroups[i].extend(value[1])
            TSEGroups[i].append(key)
            TSEGroups[i]=list(set(TSEGroups[i]))
        for i in value[1]:
            TSEGroups[i].extend(value[0])
            TSEGroups[i].extend(value[1])
            TSEGroups[i].append(key) 
            TSEGroups[i]=list(set(TSEGroups[i]))
        TSEGroups[key].extend(value[0])
        TSEGroups[key].extend(value[1])
        TSEGroups[key].append(key)
        TSEGroups[key]=list(set(TSEGroups[key]))
    SEGroups={}
    for key,value in TSEGroups.items():
        if len(value)>1:
            SEGroups[key]=value
    print("synonym groups",numGroups)
    print("synonym terms",numSynonymTerms)
    allNo,notMatch = [],[]
    countall, countmatch = 0, 0
    for i in SOSynonymPairs:
        flag = 0
        master, synonym = i
        if (master.replace(".", "").replace("_", "") == synonym.replace(".", "").replace("_", "")):
            if (master in TSEGroups or synonym in TSEGroups or master.replace(".", "").replace("_", "") in TSEGroups):
                flag=2
                countall += 1
                countmatch += 1
        else:
            if synonym in SEGroups:
                flag = 1
                countall += 1
                if master in SEGroups[synonym]:
                    flag=2
                    countmatch += 1
        if flag==0 :
            allNo.append((master, synonym))
        elif flag==1:
            notMatch.append((master, synonym))
#    return stu
    print("SEDict synonym match", countall)
    print("coverage",countall/len(SOSynonymPairs))
    print("SEDict synonym and tag match", countmatch)
    print("accuracy",countmatch/countall)
    print("\n\n")
    # Word Net   ----------------------------------------------
    countall, countmatch = 0, 0
    for i in SOSynonymPairs:
        master, synonym = i
        synets= wn.synsets(synonym)
        if (len(synets) > 0 ):
            countall += 1
            flag = True
            for synet in synets:
                if (master in synet.lemma_names()):
                    countmatch += 1
                    flag = False
                    break
    print("wordnet synonym match", countall)
    print("wordnet synonym and tag match", countmatch)

    return  allNo,notMatch 


if (__name__ == "__main__"):
#    modelName = "fastText"
#    main(modelName="mixed")
#    SEDictPath="../result/step5.1.4_ExtSEDict_fasttext_900_V5.dict"
#    res=main(SEDictPath="../result/step5.1.4_ExtSEDict_fasttext_100_V5.dict")
#    res=main(SEDictPath="../result/step5.1.4_ExtSEDict_word2vec_100_V5.dict")
    res=main(SEDictPath="../result/step5.1.4_ExtSEDict_mixed_100_100_V5.dict")
    
#    res=main(SEDictPath="../result/step5.1.3_ExtSEDict_fasttext_V5.dict")
#    res=main(SEDictPath="../result/step5.1.3_ExtSEDict_word2vec_V5.dict")
#    res=main(SEDictPath="../result/step5.1.3_ExtSEDict_mixed_V5.dict")
#    main(modelName="word2vec")
    ###################################################################
#    SOSynonymPairs = joblib.load("../result/SOSynonymPairs.list")
#    res=[]
#    for i in SOSynonymPairs:
#        res.append(i[0]+"\t"+i[1]+"\n")
#    with codecs.open("../result/SOSynonymPairs1.txt","w",encoding="utf-8") as fw:
#        fw.writelines(res)
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

    
    
    
    
    