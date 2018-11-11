# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 20:02:03 2018

@author: Administrator
"""

import requests
from bs4 import BeautifulSoup
from sklearn.externals import joblib
from nltk.corpus import wordnet as wn
s=list(wn.synsets('dog'))   







"""
(mast tag,synonym)
"""
if(__name__=="__main__"):
    res=[]
    for i in range(1,43):
        print (i)
        url="https://stackoverflow.com/tags/synonyms?page="+str(i)+"&tab=newest&filter=all"
        response=requests.get(url)
        s=response.content.decode(encoding="utf-8")
        beau=BeautifulSoup(s,"lxml")
        
    
        s1=beau.find("table",id="synonyms-table").find_all("tr")[1:]
        for j in s1:
            t=j.find_all("a")
            res.append(  (t[0].get_text().replace("-","_").replace(" ","_").lower(),t[1].get_text().replace("-","_").replace(" ","_").lower()) )
        
    joblib.dump(res,"../result/SOSynonymPairs.list")   
        
#        words=[x.get_text() for x in s]    
#        for j in xrange(0,len(words),3):
#            res.append(  (words[j].replace("-","_").replace(" ","_").lower(),words[j+1].replace("-","_").replace(" ","_").lower()) )
















