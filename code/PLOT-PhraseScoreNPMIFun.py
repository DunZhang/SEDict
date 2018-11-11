# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 11:00:20 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

# In[]数据部分
coverage_20=[0.96682,0.48193,0.3080,0.1483]
coverage_40=[0.96682,0.426575,0.2524,0.1208]
coverage_60=[0.96682,0.4000,0.23114,0.11]
coverage_100=[0.96682,0.3900,0.2256,0.100]




X=[1,2,3,4]
# In[]画图部分

fig,ax=plt.subplots()
ax.set_xticks(X)   
ax.set_xticklabels(["1","2","3","4 and more"])     
#plt.ylim(0.5,0.9)
plt.xlim((0.5,4.5))
#o . + v ^ < >  s x
plt.bar([i-0.3 for i in X],height=coverage_20,width=0.2,color="g",label="threshold=0.6")
plt.bar([i-0.1 for i in X],height=coverage_40,width=0.2,color="b",label="threshold=0.7")
plt.bar([i+0.1 for i in X],height=coverage_60,width=0.2,color="r",label="threshold=0.8")
plt.bar([i+0.3 for i in X],height=coverage_100,width=0.2,color="y",label="threshold=0.9")
#标数字
t=0.62
for i in coverage_20:
    plt.text(x=t,y=i+0.01,s=round(i,2),fontsize=6)
    t+=1
t=0.82
for i in coverage_40:
    plt.text(x=t,y=i+0.01,s=round(i,2),fontsize=6)
    t+=1
t=1.02
for i in coverage_60:
    plt.text(x=t,y=i+0.01,s=round(i,2),fontsize=6)
    t+=1
t=1.22
for i in coverage_100:
    plt.text(x=t,y=i+0.01,s=round(i,2),fontsize=6)
    t+=1
plt.xlabel("Word number in one tag")
plt.ylabel("Coverage")

#plt.title("testSet = ")
plt.legend()#添加图例标注
#
plt.savefig("tagCoverage-npmi.pdf")

