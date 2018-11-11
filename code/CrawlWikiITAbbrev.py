# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 14:16:04 2018

@author: Administrator
"""
import requests
from bs4 import BeautifulSoup
from sklearn.externals import joblib


#(original word, abbrevation)
if(__name__=="__main__"):
    url="https://en.wikipedia.org/wiki/List_of_computing_and_IT_abbreviations"
    response=requests.get(url)
    s=response.content.decode(encoding="utf-8")
    beau=BeautifulSoup(s,"lxml")    
    s=beau.find_all("div",attrs={"class":"div-col columns column-width"})
    print(len(s))
    lis=[]
    for i in s:
        for j in i.find_all("li"):
            t=j.find_all("a")
            if len(t)!=1:
                continue
            abbrev=t[0].get_text()
            t[0].decompose()
            origin=j.get_text()[1:]
            lis.append( (origin.replace(" ","_").replace("-","_").lower(),abbrev.replace(" ","_").replace("-","_").lower())  )
                
                
#    lis.append( ("knowledge_machine","km")   )
#    lis.append( ("angel","ngl")   )
    joblib.dump(lis,"../result/WikiAbbrev.list")    
    