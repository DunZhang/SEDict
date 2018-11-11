# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from bs4 import BeautifulSoup
from sklearn.externals import joblib
from lxml import etree
def getAnchor(content):
    res=[]
    soup = BeautifulSoup(content, "lxml")
    for e in soup.find_all("a"):
        anchorText=e.get_text().lower()
        if( anchorText.startswith("http:")):#Remove URL
            continue
        anchorTexts=anchorText.split(',')
        res.extend(anchorTexts)
    return res
if (__name__=="__main__"):
    anchorSet=[]
    iterSOXml = etree.iterparse("../data/Posts.xml",encoding="utf-8",tag="row")
    cou=0
    for _,elem in iterSOXml:
        cou+=1
        if(cou%50000==0):
            print(cou)
        content=elem.get("Body")
        if(content is not None):
            anchorSet.extend(getAnchor(content))
        elem.clear()

    print("become set")
    anchorSet=set(anchorSet)
    print("start save anchor set")
    joblib.dump(anchorSet,"../result/step2.2_SOAnchor.set")
    print("numer of anchor :",len(anchorSet))
