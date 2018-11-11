# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 20:23:13 2018

@author: Administrator
"""
from sklearn.decomposition import PCA
from gensim.models import Word2Vec,FastText
import numpy as np
from sklearn.externals import joblib
import matplotlib.pyplot as plt
if __name__=="__main__":
#    ffdi=joblib.load("../result/step4.2.3_SemanticallyRelatedTermsFiltered_fasttext_V5.dict")
#    wvdi=joblib.load("../result/step4.2.3_SemanticallyRelatedTermsFiltered_word2vec_V5.dict")
    
#    modelPath="../result/step3.1_fasttext_V5/fasttext.m"
#    m=FastText.load(modelPath)
    term=["internet_explorer","hardware","msbuild"]
    words=[]
    for i in term:
        words.append(i)
        words.extend(ffdi[i][0:6])
    data=[]
    for i in words:
        data.append(list(m.wv[i]))
    data=np.vstack(data)


    #开始降维
    pca=PCA(n_components=2)
    data_pca=pca.fit_transform(data)

#生成坐标
    data_plot={}
    for i in range(len(data_pca)): 
        data_plot[words[i].replace("_"," ")]=[data_pca[i,0],data_pca[i,1]]
    data_plot["internet explorer6"][1]=2.0
    data_plot["internet explorer7"][1]=2.2
    data_plot["internet explorer8"][1]=1.8
    data_plot["internet explorer9"][1]=1.6
    data_plot["internet explorers"][1]=1.4
    data_plot["internet explorere"][1]-=1.2
    data_plot["msbuil"][0]-=1.3
    data_plot["msbuild"][0]-=1
    data_plot["msbuild"][1]-=0.1
    data_plot["msbuild12"][0]-=1
    data_plot["msbuild14"][0]-=1
    data_plot["msbuild15"][0]-=1
    data_plot["msbuild4"][0]-=2.5
    data_plot["msbuilds"][0]-=2
    data_plot["hardware drivers"][1]+=0.1
    data_plot["ihardware"][1]+=0.5
    data_plot["hardwares"][0]+=0.8
    data_plot["non hardware"][1]+=0.25

#开始画图
    fig = plt.figure(figsize=(10.5,10.5))
    ax = fig.add_subplot(111)
    ax.set_xlim((-2.5,3.5))
    ax.set_ylim((-3,3))
    for key,value in data_plot.items():            
        ax.scatter(value[0],value[1],c="w")
        ax.annotate(s=key,xy=(value[0],value[1]),fontsize=11)
    fig.savefig("E:/vectorSpace-FastText.pdf")
    