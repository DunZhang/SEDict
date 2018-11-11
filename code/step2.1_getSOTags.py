 #-*- coding: utf-8 -*-
"""
从SO数据库获取Tags
数据格式：["Tag","TagTimes", "SOTimes", "WikiTimes", "StartDate", "EndDate", "Duration"]
"""

import pickle
import codecs
from collections import defaultdict
from sklearn.externals import joblib
import json
import pandas as pd
import gc

from datetime import date
from lxml import etree
import logging
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)
    
def getSOTagsByTags():
    res=[]
    context = etree.iterparse("../data/Tags.xml",encoding="utf-8")
    for _ , elem in context:
        tagName,count=elem.get("TagName"),elem.get("Count")
        if(tagName is not None):
            tagName=tagName.replace("-","_").lower()
            res.append((tagName,int(count)))
        elem.clear()
    di=dict(res)
    joblib.dump(di,"../result/step2.1_SOTags_Eva.dict")
    pd.DataFrame(res,columns=["Tag","Count"]).to_csv("../result/step2.1_SOTags_Eva.csv",encoding="utf-8",index=False)
if (__name__ == "__main__"):
    getSOTagsByTags()
#    di=dict(res)
    
    
    
    
    
    
    
    
    
    
    