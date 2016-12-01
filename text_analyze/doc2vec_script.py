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

# descriptions = {}
#
# for i in range(1, cnt, 20):
#     query = u"SELECT auction_id, title, non_tagged_description FROM items LIMIT {0}, 20;".format(i)
#     cursor.execute(query)
#     results = cursor.fetchall()
#
#     for result in results:
#         descriptions[result['auction_id']] = result['non_tagged_description'].split(' ')
#
# arranged_descriptions = models.doc2vec.LabeledListSentence(descriptions.values())
# model = models.doc2vec.Doc2Vec(arranged_descriptions, min_count=0)
# print(model)
# print(model.labels)
# print(descriptions.keys())
# model.save('./doc2vec_model/model.d2c')

loaded_model = models.doc2vec.Doc2Vec.load('./doc2vec_model/model.d2c')

print(loaded_model.most_similar_labels('SENT_0'))
print(loaded_model.most_similar_words('windows'))
