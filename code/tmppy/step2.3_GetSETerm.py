# -*- coding: utf-8 -*-
"""
获取软工术语
存储格式：字典形式，key=term，value=(Frequency,isSOTag,isAnchor,inWiki,Ratio)
"""
import codecs
import json
import operator
import re
import string
import pandas as pd
from sklearn.externals import joblib


def countTotalFreq(input_dic):
    count = 0
    for term in input_dic:
        if input_dic[term] > 1:  # do not count term appearing only once as it is highly likely to be noise
            count += input_dic[term]
    return count


#
def filterTerms(term, stopWords_set):
    """

    还有很多东西需要改进：
    带有.的单词 .net
    所有格的
    全是数字

    remove some terms in Stack Overflow by some rules
    :param term:
    :param stopWords_set:
    :return:True represent it is a term, False represent it is not a SE term
    """
    # remove single-letter words
    table = string.maketrans("", "")
    if len(term) == 1 and term != "r" and term != "c":
        return False
    #最后一个不是.
    if(term[-1]=="."):
        return False
    # the term cannot include these punctuations
    special_list = ["@", "*", "[", "]", "=", ">", "<", "\\", "/", "|", "&", "$", "~", "^", "%", "..", "--", "__", "`",
                    "´".decode("utf-8"), "’".decode("utf-8"), "‘".decode("utf-8"), "“".decode("utf-8"),
                    "”".decode("utf-8"), " ".decode("utf-8"), "£".decode("utf-8"),
                    "¿".decode("utf-8"), "www.", ".txt", ".com", "test.", "slow"]
    for i in special_list:
        if i in term:
            return False
    for spart in term.split("."):  # .分割后，里面不能有停词
        if (spart in stopWords_set):
            return False
    if (len(term) > 2):
        if (term[0] == "." and term[1].isdigit()):  # 以点数字开头的过滤掉
            return False
    # print(term)
    try:
        if (str(term).translate(table, string.punctuation).isdigit()):  # 除了标点符号全是数字的过滤掉
            return False
    except:
        return False
    # remove terms whose begining is
    firstLetter_set = set(["#", "_", "+", "-"])
    if term[0] in firstLetter_set:
        return False
    # remove terms whose first character is a digit except some special cases
    twoLetters_set = set(["2d", "3d", "32", "64"])
    if term[0].isdigit():
        if (len(term) > 1):
            if (term[0:2] not in twoLetters_set):
                return False
    if len(term) > 3 and term[0:3] == "im_":  # remove some terms such as im_guessing
        return False

    if term in stopWords_set:  # remove the stop words
        return False
    if term.find(".") > 0:
        if term.split(".")[-1] in stopWords_set:
            return False
    elif "_" in term:
        for item in term.split("_"):  # stop words cannot be part of the phrases
            if item in stopWords_set:
                return False

    if len(re.findall(r"\d\.\d", term)) > 0:  # no version number such as "3.2.1"
        return False

    signal = False  # fail if there are no letters in the term
    for character in term:
        if character.isalpha():
            signal = True
            break
    return signal


def extractTerm():
    f = codecs.open("../result/step1.3_SOVocabulary.json", encoding="utf-8")
    vocab_so = json.load(f)
    f.close()
    f = codecs.open("../result/step1.1_WikiVocabulary.json", encoding="utf-8")
    vocab_wiki = json.load(f)
    f.close()
    count_so = countTotalFreq(vocab_so)
    count_wiki = countTotalFreq(vocab_wiki)
    vocab_so = sorted(vocab_so.items(), key=operator.itemgetter(1), reverse=True)  # rank all words from highFreq to low
    print("vocab_so length:", len(vocab_so))
    # load frequnt anchor text in Stack overflow
    anchor_set = joblib.load("../result/step2.2_SOAnchor.set")
    # load all tags in Stack Overflow
    tag_set = joblib.load("../result/step2.1_SOTagsSet.set")
    # load all stop words
    stopWords_set = joblib.load("../result/stopWords.set")
    term_dic = {}
    for item in vocab_so:
        isTerm, value = False, [0, "N", "N", "Y", "inf"]
        if len(term_dic) > 100000 or item[1] < 200:  # the word frequency should not be lower than 500
            break
        if filterTerms(item[0], stopWords_set):  # pass if not be filtered
            if item[0] in tag_set:  # pass if it is one of Stack overflow tags
                isTerm = True
                value[1] = "Y"
            if item[0] in anchor_set:
                isTerm = True
                value[2] = "Y"
            if item[0] not in vocab_wiki:  # pass if it does not appear in wikipedia
                isTerm = True
                value[3] = "N"
            else:
                score = count_wiki / float(count_so) * item[1] / vocab_wiki[item[0]]
                value[4] = score
                if score > 10:  # pass if its score is high enough
                    isTerm = True
        # the term is SE term, store it
        #加强判断
        if (isTerm):
            value[0] = item[1]
            term_dic[item[0]] = tuple(value)
    #以点开头的，去掉点后若在字典中就存在，就删除它
#    keys=term_dic.keys()
#    for k in keys:
#        if(k.startswith(".")):
#            if(k[1:] in term_dic.keys()):
#                term_dic.pop(k)
    fwrite = codecs.open("../result/step2.3_SETerm.json", "w", encoding="utf-8")
    fwrite.write(json.dumps(term_dic))
    fwrite.close()
def toCSV():
    di=json.load(codecs.open("../result/step2.3_SETerm.json", "r", encoding="utf-8"))
    res=[]
    for key in di:
        t=[key]
        t.extend(di[key])
        res.append(t)
    res=pd.DataFrame(res,columns=("SETerm","Frequency","isSOTag","isAnchor","inWiki","Ratio"))
    res.to_csv("../result/SETerm.csv",index=False)
if (__name__ == "__main__"):
    # extractTerm()
    toCSV()

