# coding: utf-8
from gensim import models
import numpy as np
from numpy import random
random.seed(555)
# from scipy.cluster.vq import vq, kmeans, whiten
# from sklearn.decomposition import TruncatedSVD
# from collections import defaultdict
# from separatewords import MecabTokenize  # 目的に合わせた形態素解析器を呼びだして下さい
import MySQLdb
import MySQLdb.cursors
import os
import sys
from datetime import datetime

args = sys.argv
if len(args) == 1:
    print('Please give auction_id')
    sys.exit()

REP_ROOT = os.environ['YA_RECOGNIZE_ROOT']
TEXT_ANALYZE = REP_ROOT + '/text_analyze'

loaded_model = models.doc2vec.Doc2Vec.load(TEXT_ANALYZE + '/doc2vec_model/model.d2c')

print(loaded_model.docvecs.most_similar(args[1]))
