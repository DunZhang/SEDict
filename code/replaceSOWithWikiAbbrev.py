# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 17:20:40 2018

@author: Administrator
"""

import codecs
from gensim.models import Word2Vec,FastText
from gensim.models.word2vec import LineSentence
from sklearn.externals import joblib
import re
import gc
import time
import logging
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
class SOTxtIter(object):
    def __init__(self,path):
        self.times = 0
        self.path=path
        pass

    def __iter__(self):
        self.times += 1
        count = 0
        fread = codecs.open(self.path, "r", encoding="utf-8")
        for line in fread:
            count += 1
            if (count % 500000 == 0):
                logger.warning("step" + str(self.times) + ": already processe:" + str(count))
            yield line.split()
        fread.close()



if __name__=="__main__":
    # In[] 开始替换
    fr=codecs.open("c:/SE/step1.2.3_SOTrigramList_V4.txt","r",encoding="utf-8")
    fw=codecs.open("c:/SE/step1.2.3_SOTrigramList_V5.txt","w",encoding="utf-8")
    subPairs=[(re.compile(x[0]),x[1])    for x in joblib.load("../result/replacePairs_with4moreWiki.list")]
    batch_size=100000000
    pos=0
    ts=fr.read(batch_size)
    while len(ts)>0:
        print(pos/1000000,"w")
        t=len(ts)
        npos=ts.rfind("\n")
        if t==batch_size:
            ts=ts[:npos+1]

        for p in subPairs:
            ts=re.sub(p[0],p[1],ts)
        fw.write(ts)
        if t!=batch_size:
            print("t!=batch_size",t)
            break
        pos+=(npos+1)
        fr.seek(pos)
        ts=fr.read(batch_size)
    fr.close()
    fw.close()
#    del ts
#    gc.collect()
#    time.sleep(30)
    # In[] 训练
#    FastText_model = FastText(sentences=LineSentence("c:/SE/step1.2.3_SOTrigramList_V4.txt",max_sentence_length=500000000), min_count=5, 
#                              size=200, sg=1,workers=12, window=5)
#    FastText_model.save("../result/step3.1_FastText_V4/fasttext.m")
#    
    
    
    # In[] Test
#    fr=codecs.open("c:/SE/123.txt","r",encoding="utf-8")
#    s=fr.readlines(40)
    
    
    
    
    
    
    
    