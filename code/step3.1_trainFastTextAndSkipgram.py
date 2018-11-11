# -*- coding: utf-8 -*-
import codecs
import logging
from gensim.models.word2vec import LineSentence
from gensim.models import Word2Vec,FastText

# logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.WARNING)
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


if (__name__ == "__main__"):
#     skipgram_model = Word2Vec(sentences=LineSentence("C:/SE/step1.2.3_SOTrigramList_V5.txt",max_sentence_length=100000000),
#                               min_count=5, size=200, sg=1, workers=8, window=5)
#     skipgram_model.delete_temporary_training_data(True)
#     skipgram_model.save("../result/step3.1_word2vec_V5/word2vec.m")


#    line sentece 版本
#    ls=LineSentence("C:/SE/step1.2.3_SOTrigramList_V5.txt",max_sentence_length=100000000)
#    FastText_model = FastText(sentences=ls , min_count=5, size=200, sg=1,
#                    workers=8, window=5)
#    FastText_model.save("../result/step3.1_FastText_V5/fasttext.m")
    
    # In[]分批训练
    basePath="C:/SE/step1.2.3_SOTrigramList_V5_Part/step1.2.3_SOTrigramList_V5_"
    for i in [5,6,7,8,9,10]:
        print(i)
        word2vec_model = Word2Vec(sentences=LineSentence(basePath+str(i)+".txt") , min_count=3, size=200, sg=1,
                        workers=8, window=5)
        word2vec_model.delete_temporary_training_data(True)
        word2vec_model.save("../result/step3.1_word2vec_Part_V5/word2vec_"+str(i)+".m")    
#        FastText_model = FastText(sentences=LineSentence(basePath+str(i)+".txt") , min_count=5, size=200, sg=1,
#                        workers=8, window=5)
#        FastText_model.save("../result/step3.1_FastText_Part_V5/fasttext_"+str(i)+".m")    
    
    # In[]分批训练
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
