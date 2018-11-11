# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 17:08:15 2018

@author: Administrator
"""

import codecs

if __name__=="__main__":
    
    
    fr=codecs.open("C:/SE/step1.2.3_SOTrigramList_V5.txt","r",encoding="utf-8")
    
    datas=[]
    batch=0
    c=0
    for line in fr:
        c += 1
        if (c % 500000 == 0):
            print(str(c / 10000) + "w")
        datas.append(line)
        if len(datas)>16409000 and batch<10:
            print(batch)
            fw=codecs.open("C:/SE/step1.2.3_SOTrigramList_V5_Part/"+"step1.2.3_SOTrigramList_V5_"+str(batch)+".txt","w",encoding="utf-8")
            fw.writelines(datas)
            fw.close()
            del datas
            datas=[]
            batch+=1
    if len(datas)>0:
        fw=codecs.open("C:/SE/step1.2.3_SOTrigramList_V5_Part/"+"step1.2.3_SOTrigramList_V5_"+str(batch)+".txt","w",encoding="utf-8")
        fw.writelines(datas)
        fw.close()    
    fr.close()
