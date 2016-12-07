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
from datetime import datetime

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
cursor.execute(u'SELECT count(id) FROM items;')
cnt = cursor.fetchone()['count(id)']

descriptions = {}

# model作成用のデータ作成 => descriptions
for i in range(1, 1000, 20):
    query = u"SELECT auction_id, title, non_tagged_description FROM items LIMIT {0}, 20;".format(i)
    cursor.execute(query)
    results = cursor.fetchall()

    for result in results:
        descriptions[result['auction_id']] = result['non_tagged_description'].split(' ')

labeled_descriptions = models.doc2vec.LabeledListSentence(descriptions.values())
model = models.doc2vec.Doc2Vec(labeled_descriptions, min_count=0)
model.save('./doc2vec_model/model.d2c')
