# -*- coding: utf-8 -*-
import json
import re
import string
import jellyfish
import codecs
from sklearn.externals import joblib
from Levenshtein import distance
from SEUtils import isSynonym,isAbrreviation
# check if there are numbers in the string


#def isSpellingMistake(term,vocab_so,vocab_wiki,websterDict):
#    """
#    判断这个单词是否真实存在，那不然就是拼写错误
#    """
#    if(term.replace("-"," ").replace("_"," ") in websterDict):
#        return False
#    if(term in vocab_wiki):
#        return False
#    if(term not in vocab_so):
#        return True
#    if(vocab_so[term]<20):
#        return True
    
# find abbreviations, synonyms from semantically-related candidates
def discriminateWords(modelName="fastText"):
#    f = codecs.open("../result/step1.3_SOVocabulary.json", encoding="utf-8")
#    vocab_so = json.load(f)
#    f.close()
#    f = codecs.open("../result/step1.1_WikiVocabulary.json", encoding="utf-8")
#    vocab_wiki = json.load(f)
#    f.close()
#    websterDict=joblib.load("../result/WebsterWords.set")
    raw_dic = joblib.load("../result/step4.4.1_SynonymFullName_"+modelName.lower()+".dict")
    seperate_dic = {}  # store synonyms and abbreviation
    c=0
    for key in raw_dic:
        c+=1
        if(c%1000==0):
            print (c)
        if(raw_dic[key][0] is None):
            representWord=key
            values=raw_dic[key][1:]
        else:
            representWord=raw_dic[key][0]
            values=raw_dic[key][1:]
            values.append(key)
        representWord=representWord.replace("-"," ").replace("_"," ")
        values=[x.replace("-"," ").replace("_"," ") for x in values]
        key=key.replace("-"," ").replace("_"," ")
        seperate_dic[key] = [representWord, [], [],[]]  # 0representWord,1abbreviation, 2synonyms and the 3rest as three lists
        for term in values:
            if isSynonym(term, representWord):
                seperate_dic[key][2].append(term)
            elif isAbrreviation(representWord,term):
                seperate_dic[key][1].append(term)
            else:
                seperate_dic[key][3].append(term)
    joblib.dump(seperate_dic,"../result/FinalDict_"+modelName.lower()+".dict")
    return seperate_dic

#def 
if (__name__ == "__main__"):
#    discriminateWords()
    res=discriminateWords(modelName="fasttext")

    
    
    