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
    
#    modelPath="../result/step3.1_word2vec_V5/word2vec.m"
#    m=Word2Vec.load(modelPath)
    term=["internet_explorer","hardware","msbuild"]
    words=[]
    for i in term:
        words.append(i)
        words.extend(wvdi[i][0:6])
    data=[]
    words[words.index("ie7")]="ie"
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
    data_plot["ie11"][0]-=0.3
    data_plot["ie10"][0]-=0.3
    data_plot["microsoft edge"][1]-=0.05
#    data_plot["ie7"][1]-=0.05
    data_plot["ie9"][0]-=0.15
    data_plot["vcbuild"][1]-=0.1
    data_plot["vcbuild"][0]+=0.13
    data_plot["vstest"][1]+=0.03
    data_plot["devenv"][0]+=0.12
    data_plot["hardware"][1]+=0.2
    data_plot["hw"][1]+=0.18
    data_plot["pmic"][1]+=0.1
    data_plot["hardward"][0]+=0.05
    data_plot["hardward"][1]-=0.05
    data_plot["harware"][1]-=0.02
    data_plot["chipset"][1]-=0.1
#开始画图
    fig = plt.figure(figsize=(10.5,10.5))
    ax = fig.add_subplot(111)
    ax.set_xlim((-0.8,1))
    ax.set_ylim((-0.8,0.9))
    for key,value in data_plot.items():            
        ax.scatter(value[0],value[1],c="w")
        ax.annotate(s=key,xy=(value[0],value[1]),fontsize=11)
    fig.savefig("E:/vectorSpace-Word2Vec.pdf")
    