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

REP_ROOT = os.environ['YA_RECOGNIZE_ROOT']
TEXT_ANALYZE = REP_ROOT + '/text_analyze'

conn = MySQLdb.connect(
    host="localhost",
    user=os.environ['YAHOO_AUCTION_DB_USERNAME'],
    passwd=os.environ['YAHOO_AUCTION_DB_PASSWORD'],
    db=os.environ['YAHOO_AUCTION_DB_NAME'],
    charset = "utf8",
    use_unicode=True,
    cursorclass=MySQLdb.cursors.DictCursor
)
cursor = conn.cursor()

loaded_model = models.doc2vec.Doc2Vec.load(TEXT_ANALYZE + '/doc2vec_model/model.d2c')
similarities = loaded_model.docvecs.most_similar(args[1], topn=100)
print("auction_id: {0}の類似度ランキング↓".format(args[1]))

query = """
    SELECT title, description, seller_id, auction_item_url FROM items where auction_id = '{0}';
""".format(args[1])
cursor.execute(query)
item = cursor.fetchone()
print("auction_id: {0}".format(args[1]))
print("  title: {0}".format(item['title']))
print("  seller_id: {0}".format(item['seller_id']))
print("  auction_item_url: {0}".format(item['auction_item_url']))
print('-----------------------------------------------------------------')

for aid, degree in similarities:
    query = """
        SELECT title, description, seller_id, auction_item_url FROM items where auction_id = '{0}';
    """.format(aid)
    cursor.execute(query)
    _item = cursor.fetchone()
    print("auction_id: {0}".format(aid))
    print("  auction_item_url: {0}".format(_item['auction_item_url']))
    print("  degree: {0}".format(degree))
    print("  title: {0}".format(_item['title']))
    print("  same seller?: {0}".format(item['seller_id'] == _item['seller_id']))
