# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 15:54:25 2018

@author: Administrator
"""

import requests
from bs4 import BeautifulSoup
from sklearn.externals import joblib




if __name__=="__main__":
    # In[] Crawl https://www.tutorialspoint.com/basics_of_computer_science/basics_of_computer_science_abbreviations.htm
#    response=requests.get("https://www.tutorialspoint.com/basics_of_computer_science/basics_of_computer_science_abbreviations.htm")
#    content=response.content.decode(encoding="utf-8")
#    soup=BeautifulSoup(content,"lxml")	  
#    table=soup.find("table",attrs={"class":"table table-bordered"})     
#    trs=table.find_all("tr")
#    res=[]
#    for i in trs:
#        t=i.find_all("td")
#        if len(t)!=2:
#            continue
#        fullName,abbrev=t[1].get_text(),t[0].get_text()
#        fullName,abbrev=fullName.lower().strip().replace(" ","_").replace("-","_"),abbrev.lower().strip().replace(" ","_").replace("-","_")
#        res.append(( fullName,abbrev))
#    joblib.dump(res,"../result/tutorialspointAbbrev.list")


    # In[] Crawl https://www.tutsraja.com/2018/07/a-to-z-computer-abbreviations-for-competitive-exams.html
    response=requests.get("https://www.tutsraja.com/2018/07/a-to-z-computer-abbreviations-for-competitive-exams.html")
    content=response.content.decode(encoding="utf-8")
    soup=BeautifulSoup(content,"lxml")	  
    table=soup.find("table",attrs={"class":"table table-bordered table-hover"})  
    trs=table.find_all("tr",attrs={"class":"white"})
    res=[]
    for i in trs:
        t=i.find_all("td")
        if len(t)!=3:
            continue
        fullName,abbrev=t[2].get_text(),t[1].get_text()
        fullName,abbrev=fullName.lower().strip().replace(" ","_").replace("-","_"),abbrev.lower().strip().replace(" ","_").replace("-","_")
        res.append(( fullName,abbrev))
    joblib.dump(res,"../result/tutsrajaAbbrev.list")
