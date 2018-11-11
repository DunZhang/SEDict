# -*- coding: utf-8 -*-
import re
import string
from bs4 import BeautifulSoup
import numpy as np
from sklearn.externals import joblib
from gensim.models import Word2Vec, FastText
import jellyfish
import codecs
import json
from copy import deepcopy
def filterTerms(term, stopWords_set):
    """
    对术语做一个简单的判断，返回True也不代表一定是软工术语及其同义词等
    remove some terms in Stack Overflow by some rules
    :param term:
    :param stopWords_set:
    :return:True represent it is a term, False represent it is not a SE term
    """
    #无法ascii的直接过滤
    try:
        term.encode(encoding="ascii")
    except:
        return False
    
    if len(term) == 1 and term != "r" and term != "c":
        return False
    term=term.replace("-","_")
    if(term in [".3gp","3gp",".7z",".3ds","3ds","2d", "3d","4d", "2g","3g","4g","32_bit", "64_bit","1nf","2nf","3nf","4nf"]):
        return True
    #最后一个不是.
    if term[-1]=="." or term[-1]=="_":
        return False
    if term in stopWords_set:  # remove the stop words
        return False
    # the term cannot include these punctuations
    special_list = ["@", "*", "[", "]", "=", ">", "<", "\\", "/", "|", "&", "$", "~", "^", "%", "..", "--", "__", "`",
                    "´", "’", "‘", "“","”", " ", "£","¿", "www.", ".com", "test.", "slow","'s",".org",".axd",".app",
                    ".mail",".test",".mf",".location",
                    ".system",".imageio",".io",".beginform",".futures",".mappath",".drawing",".observablearray",".conf",".table",
                    ".path",".actionlink",".settings",".log",".util",".concurrent"]
    for i in special_list:
        if i in term:
            return False
#    for spart in re.split("[._]",term):  # .分割后，里面不能有停词
#        if (spart in stopWords_set):
#            return False
        

    if (len(term) > 2):
        if (term[0] == "." and term[1].isdigit()):  # 以点数字开头的过滤掉
            return False
    # print(term)
    # 除了标点符号全是数字的过滤掉
#    t_term=deepcopy(term)
#    for c in string.punctuation:
#        t_term=t_term.replace(c,"")
#    if ( t_term.isdigit()):  
#        return False
    # remove terms whose begining is
    firstLetter_set = set(["#", "_", "+", "-"])
    if term[0] in firstLetter_set:
        return False
    # remove terms whose first character is a digit except some special cases
    if term[0].isdigit():
        return False
    if len(term) > 3 and term[0:3] == "im_":  # remove some terms such as im_guessing
        return False

    if len(re.findall(r"\d\.\d", term)) > 0:  # no version number such as "3.2.1"
        return False

    signal = False  # fail if there are no letters in the term
    for character in term:
        if character.isalpha():
            signal = True
            break
    return signal
def numberInString(term):
    for i in term:
        if i.isdigit():
            return True
    return False


# check if the number in two string are the same
def isNumberSame(term1, term2):
    # if one term has number inside, the other one should have the same number
    if numberInString(term1) or numberInString(term2):
        if re.findall(r"\d+", term1) != re.findall(r"\d+",
                                                   term2):  # if the number lists are different, they are not abbreviation relationships
            return False
    return True


# check if the letter order of two terms are the same
def checkLetterOrder(shortTerm, longTerm):
    position = 0  # record the position of letter
    matchCount = 0  # how many letters in the short term are ordered as those in long term
    # do not take "-" and "_" into consideration
    for letter in shortTerm:
        addPosition = longTerm[position:].find(letter)
        if addPosition == -1:
            break
        else:
            matchCount = matchCount + 1
        position = position + addPosition + 1

    if matchCount == len(shortTerm):
        # if the abbreviation only refer to the the first word in long term, it is not the abbreviation of the whole term such as advace --> advace_mike
        # the last position of the blank i.e., the letters in an abbreviation should lay in all components in the words
        if " " in longTerm and position < longTerm.rfind(" ") + 1 and (shortTerm[-1] != longTerm.split(" ")[-1][
            0]):  # note that the position of " " should add 1 because of the earlier program
            # print shortTerm, "," , longTerm
            return False
        else:
            return True
    else:
        return False


# check if one term is an abbreviation of the other
def isAbrreviation(longTerm, shortTerm):
    """
    判断term2是否是term1的key
    """
    try:
        longTerm.encode(encoding="ascii")
        shortTerm.encode(encoding="ascii")
    except:
        return False
    
    longTerm = longTerm.replace("-", " ")
    shortTerm = shortTerm.replace("-", " ")

    # the length of the abbreviation must be shorter than the full style at least 2 letters
    if(len(longTerm)-len(shortTerm)<2):
        return False

    # the length of the abbreviation should not be so long compared to its postential full name
    if float(len(shortTerm)) / len(longTerm) > 0.68 and not numberInString(
            shortTerm):  # the parameter is determined by observation
        return False

    if len(shortTerm) > 10:  # the short term should not be so long
        return False

    if ("++" in shortTerm) != ("++" in longTerm):  # if they both include "++" or neither do they
        return False

    if " " in shortTerm or " " in longTerm:  # if the parts of short term is part of the long term, it is not regarded as abbreviations
        if set(shortTerm.split(" ")) < set(longTerm.split(" ")):
            return False

    if longTerm[0] == "." and shortTerm[0] == "." and not longTerm.startswith(".net") and not shortTerm.startswith(
            ".net"):  # As term beginning with dot is always the file extension, it always is not the abbreviation
        return False

    if shortTerm[0] != longTerm[0]:  # two terms should have the same first letter
        return False

    if longTerm.split(" ")[0] + "s" == shortTerm:  # e.g., bolg aritcles --> blogs
        return False

    # if any letter in the short term is not contained in the long term, it is not an abbreviation
    for letter in shortTerm:
        if letter != "-" and letter != "_":
            if letter not in longTerm:
                return False
                break

    # check if number in terms are the same
    if numberInString(longTerm) or numberInString(shortTerm):
        if not isNumberSame(longTerm, shortTerm):
            return False

    # check if the letter order is the same
    try :
        if checkLetterOrder(shortTerm, longTerm):
            if shortTerm.replace(" ", "") in longTerm.replace(" ",""):  # if shortTerm in a consecutive part of long term, it is not an abbreviation
                return False
            return True
        else:
            return False
    except Exception as e:
        print ("zdd",e)
        print (longTerm,shortTerm,type(shortTerm),type(longTerm),len(shortTerm),len(longTerm))
        return False


# check if two terms are synonyms
def isSynonym(term1, term2):
    try:
        term1.encode(encoding="ascii")
        term2.encode(encoding="ascii")
    except:
        return False    
    
    
    if term1 == term2 or term1.replace(" ", "") == term2.replace(" ", ""):
        return True

    # the numbers inside them should be the same
    if not isNumberSame(term1, term2):
#        print("AA")
        return False

    if ("++" in term1) != ("++" in term2):  # if they both include "++" or neither do they    like c++
        # print term1, term2
        return False

    # there are some one-letter change which may results in different meaning such as "encode" and "decode"
    if (term1.replace(" ", "").replace("en", "de") == term2.replace(" ", "")) or (
            term1.replace(" ", "").replace("de", "en") == term2.replace(" ", "")):
        # print term1, "," ,term2
        return False

    # the first letter of two terms should be the same
    if term1[0] != term2[0]:
        return False

    if term1[0] == "." and term2[
        0] == ".":  # As term beginning with dot is always the file extension, it always is not the abbreviation
        return False
    try:
        absoluteDis = jellyfish.damerau_levenshtein_distance(term1, term2)  # absolute edit distance
    except Exception as e:
        print (e,term1,term2)
        return False
    relativeDis = 1.0-(float(absoluteDis) / max(len(term1) , len(term2)))  # relative edit distance by diving the length of two terms23
#    print(absoluteDis ,relativeDis )
    if absoluteDis < 4 and relativeDis > 0.7:  # set the absoluteDis for long term while relativeDis for short term
        return True
    else:
        return False
def StrSims(str1,str2):
    try:
        str1.encode(encoding="ascii")
        str2.encode(encoding="ascii")
    except:
        return 1
    return jellyfish.damerau_levenshtein_distance(str1, str2)/float(max(len(str1),len(str2)))

def mergeDict(di1Path="",di2Path="",newDiPath=""):
    di1=joblib.load(di1Path)
    di2=joblib.load(di2Path)
    rdi={}
    for key,value in di1.items():
        rdi[key]=key
        for i in value[0]:
            rdi[i]=key
        for i in value[1]:
            rdi[i]=key
    for key,value in di2.items():
        if key in rdi:
            di1[rdi[key]][0].extend(value[0])
            di1[rdi[key]][1].extend(value[1])
            di1[rdi[key]][2].extend(value[2])
            di1[rdi[key]][0]=list(set(di1[rdi[key]][0]))
            di1[rdi[key]][1]=list(set(di1[rdi[key]][1]))
            di1[rdi[key]][2]=list(set(di1[rdi[key]][2]))
        else:
            di1[key]=value
    joblib.dump(di1,newDiPath)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if(__name__=="__main__"):
    print (isSynonym("pip","pip3"))
    print (isSynonym("debuggig","debugging"))


