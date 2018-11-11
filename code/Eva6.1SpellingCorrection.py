# -*- coding: utf-8 -*-
import codecs
import re
from lxml import etree
from sklearn.externals import joblib
from os.path import dirname
from collections import defaultdict
import difflib
import time
import pickle
def GetWrongSpell_Correct(modelName="word2vec"):
    SEDict=joblib.load("../result/step5.1.3_ExtSEDict_"+modelName.lower()+"_V5.dict")
    di={}
    for key,value in SEDict.items():
        for i in value[1]:
            di[i]=key
    joblib.dump(di,"../result/Eva6.1WrongToCorrect"+modelName.lower()+".dict")


def __getText(strText, reSub0, reSub1, rePlus, reSplit1):
    strText = strText.lower()
    strText = re.sub(reSub0, " ", strText)
    strText = re.sub(reSub1, " ", strText)
    # 开始处理最复杂的加号情况
    for sub in set(re.findall(rePlus, strText)):
        strText = strText.replace(sub, sub[0] + " " + sub[2])
    res = []
    for sentence in re.split(reSplit1, strText):
        t = sentence.split()
        if (len(t) > 0):
            res.extend(t)
    res.append("\n")
    return " ".join(res)


def GetOriginAndEditedQuestion():
    context = etree.iterparse("../data/PostHistory.xml", encoding="utf-8")
    previousText, data, c = None, [], 0
    fw = codecs.open("../result/Eva6.1.txt", "w", encoding="utf-8")
    reSub0 = re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")  # URL
    reSub1 = re.compile("[\[\]<>`~$\^&*=|%@(){},:\"/'\\\\]")  # replace with " "
    rePlus = re.compile("[^+]\+[^+]")
    reSplit1 = re.compile("\.[^a-z0-9]|[?!;\n\r]")
    for _, elem in context:  # 迭代每一个
        c += 1
        if (c % 100000 == 0):
            print("already pasrse record:", str(c / 10000) + "W")
        title, postHistoryTypeId = elem.get("Text"), elem.get("PostHistoryTypeId")
        elem.clear()
        if title is not None and postHistoryTypeId is not None:
            if int(postHistoryTypeId) == 1:
                previousText = title
            elif int(postHistoryTypeId) == 4:
                data.append(__getText(title, reSub0, reSub1, rePlus, reSplit1))
                data.append("\n")
                data.append(__getText(previousText, reSub0, reSub1, rePlus, reSplit1))
                data.append("\n")

        # 开始存储
        if len(data) > 50000:
            fw.writelines(data)
            data = []
    if len(data) > 0:
        fw.writelines(data)
        data = []


if (__name__ == "__main__"):
    PROJPATH=dirname(dirname(__file__))
    
    # GetOriginAndEditedQuestion()
# In[] Eva6.1.1 获取所有的相关的Id,postId,postHistoryTypeId,CreationDate并存储到本地，并排序好
#    context = etree.iterparse("../data/PostHistory.xml", encoding="utf-8")
#    c=0
#    res=[]
#    for _, elem in context:  # 迭代每一个
#        c += 1
#        if (c % 100000 == 0):
#            print("already pasrse record:", str(c / 10000) + "W")
#        Id,postId,postHistoryTypeId,creationDate = elem.get("Id"),elem.get("PostId"), elem.get("PostHistoryTypeId"),elem.get("CreationDate")
#        elem.clear()
#        if postId is not None:
#            Id,postId,postHistoryTypeId,creationDate=int(Id),int(postId),int(postHistoryTypeId),time.strptime(creationDate.split(".")[0], "%Y-%m-%dT%H:%M:%S") 
#            if postHistoryTypeId==1 or postHistoryTypeId==4:
#                res.append((Id,postId,postHistoryTypeId,creationDate))
#                   
#    res.sort(key=lambda x : (x[1],x[2],x[3]))
#    res=[(i[0],i[1]) for i in res]
#    joblib.dump(res,"../result/Eva6.1.1.list")
#    start=0
#    for i in range(0,10000):
#        print(i)
#        if start>18324520:
#            break
#        joblib.dump(res[start:start+200000],"../result/Eva6.1.1/info_"+str(i)+".list")
#        start+=200000
#    joblib.dump(res,"../result/Eva6.1.1.list")
#    with open("../result/Eva6.1.1.list","wb") as fw:
#        pickle.dump(res,fw,0)
# In[] Eva6.1.2 选取title和最后修改的title 的post
# #####################################################       
#    prePostId,preIndexStart=res[0][1],0
#    t=[]
#    for i in range(len(res)):
#        if(prePostId !=res[i][1]):
#            if i-1!=preIndexStart:               
#                t.append(res[preIndexStart])
#                t.append(res[i-1])
#            preIndexStart=i
#            prePostId =res[i][1]
#    idIndexs=[ x[0] for x in t]
#    joblib.dump(idIndexs,"../result/Eva6.1.2.list")
################################################################################
#    res=joblib.load("../result/Eva6.1.1.list")
#    idIndexs=[]
#    for i in range(len(res)-1):
#        if res[i][1]==res[i+1][1]:
#            idIndexs.append(res[i][0])
#            idIndexs.append(res[i+1][0])
#    joblib.dump(idIndexs,"../result/Eva6.1.2.list")
    #idIndexs是偶数两两对是最临近的修改记录
# In[] Eva6.1.3 获取成对的title
#    idIndexs=joblib.load("../result/Eva6.1.2.list")
#    context = etree.iterparse("../data/PostHistory.xml", encoding="utf-8")
#    c=0
#    data=[None]*len(idIndexs)
#    #建立查询字典  key:history里的ID,value应该存放的位置
#    queryDict=defaultdict(list)
#    for i in range(len(idIndexs)):
#        queryDict[idIndexs[i]].append(i)
#    for _, elem in context:  # 迭代每一个
#        c += 1
#        if (c % 100000 == 0):
#            print("already pasrse record:", str(c / 10000) + "W")
#        Id,title,postHistoryTypeId = elem.get("Id"),elem.get("Text"),elem.get("PostHistoryTypeId")
#        elem.clear()  
#        if Id is not None and title is not None and postHistoryTypeId is not None:
#            postHistoryTypeId=int(postHistoryTypeId)
#            if(postHistoryTypeId!=1 and postHistoryTypeId !=4):
#                continue
#            indexs=queryDict.get(int(Id))
#            if indexs is not None:
#                for ind in indexs:
#                    data[ind]=title+"\n"
                
    #相关处理然后存到文本文件中
#    reSub0 = re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")  # URL
#    reSub1 = re.compile("[\[\]<>`~$\^&*=|%@(){},:\"/'\\\\]")  # replace with " "
#    rePlus = re.compile("[^+]\+[^+]")
#    reSplit1 = re.compile("\.[^a-z0-9]|[?!;\n\r]")
#    newData=[None]*len(data)
#    for i in range(len(data)):
#        if i%10000==0:
#            print( i/10000,"w")
#        if(data[i] is None):
#            data[i]="None\n"
#        newData[i]=__getText(data[i], reSub0, reSub1, rePlus, reSplit1)
#    
#    with codecs.open("../result/Eva6.1.3.txt","w",encoding="utf-8") as fw:
#        fw.writelines(newData)
        
# In[] Eva6.1.4 使用集合相似度去除一些行
#    with codecs.open("../result/Eva6.1.3.txt","r",encoding="utf-8") as fr:
#        data=fr.readlines()
#    newData=[]
#    i=0
#    while True:
#        origin=set(data[2*i].split())
#        edited=set(data[2*i+1].split())
#        if  len(origin.union(edited))>0 and float(len(origin.intersection(edited))) / len(origin.union(edited)) > 0.8   :
#            newData.append(data[2*i])
#            newData.append(data[2*i+1])
#        i+=1
#        if (2*i+1) >= len(data):
#            break
#    with codecs.open("../result/Eva6.1.4.txt","w",encoding="utf-8") as fw:
#        fw.writelines(newData)
                        
            
 # In[] Eva6.1.5  
### (wrong spell, correct spell)          
#    with codecs.open("../result/Eva6.1.4.txt","r",encoding="utf-8") as fr:
#        data=fr.readlines()
#    i=0
#    pairs=[]
#    while True:
#        origin,edited=data[2*i],data[2*i+1]
#        res=list(difflib.ndiff(origin.split(),edited.split()))
#        for j in range(len(res)):
#            if(res[j][0]=="?"):
#                if j>0 and j+1<len(res) and res[j-1][0]=="-" and res[j+1][0]=="+":
#                    pairs.append (   (res[j-1][2:],res[j+1][2:])    )
#                elif j>1  and res[j-2][0]=="-" and res[j-1][0]=="+":
#                    pairs.append (   (res[j-2][2:],res[j-1][2:])    )
#        i+=1
#        if (2*i+1) >= len(data):
#            break
#In[] Eva6.1.6 过滤评率出现太少的pairs
#    newPairs=[]
#    di=defaultdict(int)
#    for i in pairs:
#        di[i[0]+"\n"+i[1]]+=1
#    for key,value in di.items():
#        if value>6:
#            t1,t2=key.split("\n")
#            newPairs.append((t1,t2))
#    joblib.dump(newPairs,"../result/Eva6.1newPairs.list")
    
#   # In[] Eva6.1.7 开始SEDict评测覆盖率
#    modelName="word2vec"  
    newPairs=joblib.load("../result/Eva6.1newPairs.list")
    
    SEDict=joblib.load("../result/step5.1.6_ExtSEDict_fasttext_50_V5.dict")
#    SEDict=joblib.load("../result/step5.1.6_ExtSEDict_word2vec_V5.dict")
#    SEDict=joblib.load("../result/step5.1.6_ExtSEDict_mixed_V5.dict")
    #第一种不太地道的做法
    SEGroups=defaultdict(list)
    for key,value in SEDict.items():
        for i in value[0]:
            SEGroups[i].extend(value[0])
            SEGroups[i].extend(value[1])
            SEGroups[i].append(key)
        for i in value[1]:
            SEGroups[i].extend(value[0])
            SEGroups[i].extend(value[1])
            SEGroups[i].append(key)
        SEGroups[key].extend(value[0])
        SEGroups[key].extend(value[1])
        SEGroups[key].append(key)    
    #开始测试
    counall,countmath=0.0,0.0
    stu=[]  
    for i in newPairs:
        flag=0
        wrongSpell,correctSpell=i
        if wrongSpell in SEGroups:
            flag=1
            counall+=1
            if correctSpell in SEGroups[wrongSpell]:
                flag=2
                countmath+=1
        if flag==1:
            stu.append(i)
#    stu=[x[0] for x in stu]
#    joblib.dump(stu,"../result/Eva6.1NotMatch_word2vec.list")
#    print("SEDict ","#CoveredMisspellings:",counall,"    Coverage:",counall/len(newPairs)
#          ,"    #AccurateCorrection:",countmath,"    Accuracy",countmath/counall)     
    


































