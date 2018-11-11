# -*- coding: utf-8 -*-
"""
存储格式：
列表：[[word1,word1,...],[word3,word4,...],...]
"""
from gensim.models import Word2Vec, FastText
import codecs
import json
import networkx as nx
from sklearn.externals import joblib
import logging
from copy import deepcopy
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# import matplotlib.pyplot as plt
def GetSynonymForSingleWord(m, word, seTerms_set):
    ind = 1
    ws = [word]
    while True:
        res = m.wv.most_similar(word, topn=10)#前20最相似
        for i in res:
            if (i[1] >= 0.8 and m.wv.similarity(word, i[0]) > 0.8):
                if (i[0] not in ws):#这个单词不是已有的
                    ws.append(i[0])
        if (ind == len(ws) or len(ws) >= 30):#相似词组不能太多
            wst=deepcopy(ws)
            for i in wst:
                if(i.startwith(".")):
                    if(i[1:] in ws):
                        ws.remove(i)
            return ws
        else:
            word = ws[ind]
            ind += 1


#    return None
def Extract_Merge_Synonym_NonGraph(modelName):
    seTerms = json.load(codecs.open("../result/step2.3_SETerm.json", "r", encoding="utf-8")).keys()
    if (modelName.lower() == "fasttext"):
        m = FastText.load("../result/step3.1_FastText/step3.1_FastText.m")
    else:
        m = Word2Vec.load("../result/step3.1_skipgram/step3.1_skipgram.m")
        m.delete_temporary_training_data(True)
    synonyms = []
    while (True):
        if (len(seTerms) == 0):
            break
        word = seTerms[0]
        t = GetSynonymForSingleWord(m, word, seTerms)
        for i in t:
            if(i in seTerms):
                seTerms.remove(i)
        if(len(t)>2):#同义词至少要有3个
            synonyms.append(t)
    if (modelName.lower() == "fasttext"):
        joblib.dump(synonyms, "../result/step4.1_synonym_fasttext.list")
    else:
        joblib.dump(synonyms, "../result/step4.1_synonym_skipgram.list")
    return synonyms


#


if (__name__ == "__main__"):
    # m = FastText.load("../result/step3.1_FastText/step3.1_FastText.m")
    res = Extract_Merge_Synonym_NonGraph("fasttext")
    print(len(res))
    ins = [len(e) for e in res]
    ins.sort()
    print ins


































# def Extract_Merge_Synonym(modelName):
#     seTerms = json.load(codecs.open("../result/step2.3_SETerm.json", "r", encoding="utf-8")).keys()
#     seTerms_set = set(seTerms)
#     if (modelName.lower() == "fasttext"):
#         m = FastText.load("../result/step3.1_FastText/step3.1_FastText.m")
#     else:
#         m = Word2Vec.load("../result/step3.1_skipgram/step3.1_skipgram.m")
#         m.delete_temporary_training_data(True)
#     synonyms = []
#     G = nx.Graph()
#     for term in seTerms:
#         res = m.wv.most_similar(term, topn=20)
#         G.add_node(term)
#         for i in res:
#             if (i[1] >= 0.8 and i[0] in seTerms_set):
#                 G.add_node(i[0])
#                 G.add_edge(term, i[0])
#     for subgraph in (G.subgraph(c) for c in nx.connected_components(G)):
#         synonyms.append(list(subgraph.nodes()))
#
#     if (modelName.lower() == "fasttext"):
#         joblib.dump(synonyms, "../result/step4.1_synonym_fasttext.list")
#     else:
#         joblib.dump(synonyms, "../result/step4.1_synonym_skipgram.list")