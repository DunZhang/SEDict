# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 13:07:54 2018

@author: Administrator
"""
from xml import sax
from multiprocessing import Queue, Value, Process
from DBUtils.PooledDB import PooledDB
import time
import codecs
import re
from bs4 import BeautifulSoup
import MySQLdb
import random


def readSOXML(g_DataQueue, g_FinishRead, filePath):
    """
    :param g_DataQueue: 存储数据的队列，将被存到数据库
    :param g_FinishRead:是否读取完xml，0是没有读完，1是读完
    :param filePath:xml文件地址
    :return:无
    """
    handler = soXmlHandler(g_DataQueue=g_DataQueue, g_FinishRead=g_FinishRead)
    parser = sax.make_parser()
    parser.setContentHandler(handler)
    parser.parse(filePath)


class soXmlHandler(sax.ContentHandler):
    def __init__(self, g_DataQueue, g_FinishRead):
        self.attrs = []
        self.batchSize = 1000  # 一次存储的记录个数
        self.flag = False  # 判断是否可以提取标签里的attrs
        self.g_DataQueue, self.g_FinishRead = g_DataQueue, g_FinishRead  # 存储的数据和是否读取完的标志位
        self.count = 0  # 读取的记录数
        self.numPosType = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def getStandardText(self, attrs):
        Id, PostTypeId, AcceptedAnswerId, CreationDate, Score, ViewCount, Body, \
        LastEditDate, LastActivityDate, Title, Tags, AnswerCount, CommentCount, ParentId = \
            attrs.get("Id"), attrs.get("PostTypeId"), attrs.get("AcceptedAnswerId"), attrs.get(
                "CreationDate"), attrs.get("Score"), attrs.get("ViewCount"), \
            attrs.get("Body"), attrs.get("LastEditDate"), attrs.get("LastActivityDate"), attrs.get("Title"), attrs.get(
                "Tags"), attrs.get("AnswerCount"), \
            attrs.get("CommentCount"), attrs.get("ParentId")
        if (CreationDate is not None):
            CreationDate = str(CreationDate).split("T")[0]
        if (LastEditDate is not None):
            LastEditDate = str(LastEditDate).split("T")[0]
        if (LastActivityDate is not None):
            LastActivityDate = str(LastActivityDate).split("T")[0]
        try:
            soup = BeautifulSoup(Body, "lxml")
            for pre in soup.find_all("pre"):
                if (len(pre.find_all("code")) > 0):
                    pre.decompose()
            Body = soup.get_text()  # .encode("utf-8")#.replace("\n",".").replace("\r",".")
        except Exception as e:
            print("get html text has wrong:", e)
            print(attrs.get("Body"))
            print(Body)
        # Body=re.sub("\?[.]+","?",Body)
        # Body = re.sub("![.]+", "!", Body)
        # Body = re.sub("[.]+", ".", Body)
        # Body = re.sub(":[.]+", ":", Body)
        # Body = re.sub(";[.]+", ";", Body)

        ###记录一些信息
        self.numPosType[int(PostTypeId)] += 1
        return (Id, PostTypeId, AcceptedAnswerId, CreationDate, Score, ViewCount, Body, \
                LastEditDate, LastActivityDate, Title, Tags, AnswerCount, CommentCount, ParentId)

    def getBatchData(self):
        """
        处理attrs里的数据来获取可以直接插入数据库的数据
        :return:标准化处理过后的数据
        """
        datas = []
        for i in self.attrs:
            datas.append(self.getStandardText(i))
        return datas

    def startDocument(self):
        print('XML开始解析中...')

    # 元素开始事件处理
    def startElement(self, name, attrs):
        #        print(name)
        if (self.flag):  # 开始处理
            self.attrs.append(attrs)
            if (len(self.attrs) >= self.batchSize):  # 可以开始处理了
                self.g_DataQueue.put(self.getBatchData())#放到公共队列中
                self.attrs = []
        else:
            self.flag = True

    def characters(self, content):
        pass

    def endElement(self, name):
        pass

    def endDocument(self):
        if (len(self.attrs) > 0):  # 把剩下的数据放到队列中处理掉
            self.g_DataQueue.put(self.getBatchData())
            self.attrs = []
        self.g_FinishRead.value = 1  # 读取结束，设置标志位
        print("postType:", self.numPosType)
        print("totalCount", self.count)
        print('XML文档解析结束!')


def saveToDataBase(g_DataQueue, g_FinishRead):
    """
    取数据往数据库里存储
    :param g_DataQueue:数据队列
    :param g_FinishRead:另一个进程是否完成读取xml
    :return:无
    """
    pool = PooledDB(MySQLdb, 6, host='localhost', user='root', passwd='123456', db='so', port=3306,
                    charset='utf8mb4')  # 6为连接池里的最少连接数
    count = 0
    while (g_FinishRead.value == 0 or (not g_DataQueue.empty())):
        data = g_DataQueue.get()
        count += 1000
        if (count % 50000 == 0):
            print("have store:", count)
        # 插入数据库的操作
        conn = pool.connection()
        curs = conn.cursor()
        insert_sql = "replace into sodata(Id,PostTypeId,AcceptedAnswerId,CreationDate,Score,ViewCount,Body,LastEditDate,LastActivityDate,Title,Tags,AnswerCount,CommentCount,ParentId) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            curs.executemany(insert_sql, data)
            conn.commit()
        except Exception as e:
            print("write wrong:", e)
            for ii in data[0]:
                print(ii)
            conn.rollback()

        curs.close()
        conn.close()
        del data
    pool.close()


if __name__ == '__main__':
#    g_DataQueue = Queue(1000)  # 一次最多只有1000组数据放到内存中
#    g_FinishRead = Value("I", 0)
#    readProc = Process(target=readSOXML, args=(g_DataQueue, g_FinishRead, "../data/Posts.xml"))
#    writeProc=Process(target=saveToDataBase,args=(g_DataQueue,g_FinishRead))
#    readProc.start()
#    writeProc.start()
#    readProc.join()
#    writeProc.join()
#    print("done!!!!!!!!!!!!!!")
##############################################################################
    reSub1 = re.compile("[(){},:\"/'\\\\]")  # replace with " "
    reSplit1 = re.compile("\.[^a-z0-9]|[?!;]")
#    reSplit1 = re.compile("\.[^a-z0-9]|[?!;]")
    s="5!!!!2"
#    print re.sub(reSplit1," ",s)   
    print re.split(reSplit1,s)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    