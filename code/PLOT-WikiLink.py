# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 16:04:07 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 11:42:26 2018

@author: Administrator
"""
import matplotlib.pyplot as plt





if __name__=="__main__":
    # In[] data
    # SO coverage      CP coverage
    origin=[0.7345,0.8114]
    wordnet=[0.7349,0.8114]
    porter=[0.7456,0.8199]
    sedict=[0.8077,0.8663]
    # In[] 开始画图
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim((1.5,3.5))
    ax.set_ylim((0,1.4))
    X=[2,3]
    ax.set_xticks(X)
    ax.set_xticklabels(["1","2"])
    plt.ylabel("Precision@K")
    plt.xlabel("K")
    plt.bar([i-0.3 for i in X],height=origin,width=0.2,label="No Normalization")
    plt.bar([i-0.1 for i in X],height=wordnet,width=0.2,label="WordNet Lemmatization")
    plt.bar([i+0.1 for i in X],height=porter,width=0.2,label="Porter Stemming")
    plt.bar([i+0.3 for i in X],height=sedict,width=0.2,label="SEThesaurus")
    
    # In[] 标数字
    fontsize=14
    T=1.6
    t=T
    for i in origin:
        plt.text(x=t,y=i+0.01,s=round(i,2),fontsize=fontsize)
        t+=1
    T+=0.2
    t=T
    for i in wordnet:
        plt.text(x=t,y=i+0.01,s=round(i,2),fontsize=fontsize)
        t+=1
    T+=0.2
    t=T
    for i in porter:
        plt.text(x=t,y=i+0.01,s=round(i,2),fontsize=fontsize)
        t+=1
    T+=0.2
    t=T
    for i in sedict:
        plt.text(x=t,y=i+0.01,s=round(i,2),fontsize=fontsize)
        t+=1    
    plt.legend()
    plt.savefig("E:/anchorText-zd.pdf")
    
    
