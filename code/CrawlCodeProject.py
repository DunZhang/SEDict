# -*- coding: utf-8 -*-
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import requests
from bs4 import BeautifulSoup
from sklearn.externals import joblib
import re
def CrawCPTag():
    baseUrl="https://www.codeproject.com/script/Content/TagList.aspx?pgnum="
    taglists=[]
    for i in range(1,25):
        print(i)
        url=baseUrl+str(i)
        response=requests.get(url)
        s=response.content.decode(encoding="utf-8")
        beau=BeautifulSoup(s,"lxml")
        res=beau.find("div",id="tag-columns")
        tags=res.find_all("a")
        taglists.extend([(x.get_text().replace("-","_").lower(),x["href"]) for x in tags])
    joblib.dump(taglists,"../result/CPTags.list")
    return taglists
def CrawCPQuestionLinks(pages):
    baseUrl="https://www.codeproject.com/script/Answers/List.aspx?tab=active&pgnum="
    qUrls=[]
    try:
        for i in pages:
            print (i)
            url=baseUrl+str(i)
            response=requests.get(url)
            s=response.content.decode(encoding="utf-8")
            beau=BeautifulSoup(s,"lxml")	
            s1=beau.find("table",attrs={"class":"question-list"})
            s2=s1.find_all("h3")
            qUrls.extend([x.find("a").attrs["href"]  for x in s2]      )  
        joblib.dump(qUrls,"../result/CPQuesionsLinks_"+str(pages[0])+"_"+str(pages[-1])+".list")
    except Exception as e:
        print (e)
        print ("error",pages[0],pages[-1])
        return None
    
    return None

def GetCPTagTimes(url):
    response=requests.get(url)
    content=response.content.decode(encoding="utf-8")
    soup=BeautifulSoup(content,"lxml")	            
    table_qa=soup.find("table",attrs={"class":"qa-list"})
    table_question=table_qa.find("table",attrs={"class":"question-list"})
    #0条记录的情况
    if(table_question is None):
        return 0
    div=soup.find_all("div",attrs={"class":"indicator"})
    #只有一页的情况
    if(len(div)==0):
        return len(table_question.find_all("tr"))/2 
    return int(div[-1].get_text().split("of")[-1].replace(",",""))*20-10
#print GetCPTagTimes("https://www.codeproject.com/script/Answers/List.aspx?tab=active&tags=4480")    
if (__name__ == '__main__'):
    # In[] crawl CP Tags
#    res=CrawCPTag()
#    res=joblib.load("../result/CPTags.list")
    # In[] Crawl CP QuestionLinks 共有16621页
#    baseUrl="https://www.codeproject.com/script/Answers/List.aspx?tab=active&pgnum="
#    qUrls=[]
#    i=1
#    while(True):
#        try:
#            print i
#            url=baseUrl+str(i)
#            response=requests.get(url)
#            s=response.content.decode(encoding="utf-8")
#            beau=BeautifulSoup(s,"lxml")	
#            s1=beau.find("table",attrs={"class":"question-list"})
#            s2=s1.find_all("h3")
#            qUrls.extend([x.find("a").attrs["href"]  for x in s2]      )
#            if(i>10):
#                break
#        except:
#            continue
#        i+=1
# In[] Crawl CP Tags with Frequency
#    baseUrl="https://www.codeproject.com"
#    CPTags=joblib.load("../result/CPTags.list")
#    res=[]
#    
#    while(len(CPTags)>0):
#        print(len(res),len(CPTags))
#        tag=CPTags.pop()
#        try:
#            t=GetCPTagTimes(baseUrl+tag[1])
#        except Exception,e:
#            CPTags.insert(0,tag)
#            print (e)
#            print (baseUrl+tag[1])
#            continue
#        tag=list(tag)
#        tag.append(t)
#        res.append(tag)
#        if(len(res)>2000):
#            break
        
        
#    joblib.dump(res,"../result/CPTags.list")
    
#    i=1
#    taglists=[]
#    for i in range(1,25):
#        print(i)
#        url=baseUrl+str(i)
#        response=requests.get(url)
#        s=response.content.decode(encoding="utf-8")
#        beau=BeautifulSoup(s,"lxml")
#        res=beau.find("div",id="tag-columns")
#        tags=res.find_all("a")
#        taglists.extend(([x.get_text().replace("-","_").lower(),x["href"]) for x in tags])
#    taglists=list(set(taglists))
##        
        
        
#    response=requests.get("https://www.codeproject.com/Questions/1234899/How-to-learn-machine-learning-Road-map")
#    s=response.content.decode(encoding="utf-8")
#    beau=BeautifulSoup(s,"lxml")	
#    res1=beau.find_all("div",attrs={"class":"t"})    
#    
#    for i in res1:
#        print i.find("a").get_text().lower().replace(" ","_").replace(".","_").replace("-","_")
#        
        
#    beau=BeautifulSoup("<div>this is my code: <p>this a  a href <a href=www> javascripts <\a></p></div>","lxml")        
    reSub1 = re.compile("d(\+)")    
    ss= re.search(reSub1,"c++d+as")
    ss.group()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        