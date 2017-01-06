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

# PATH
REP_ROOT = os.environ['YA_RECOGNIZE_ROOT']
TEXT_ANALYZE = REP_ROOT + '/text_analyze'

# arguments
args = sys.argv
if len(args) == 1:
    print('Please give process_type string')
    sys.exit()

# MySql connection
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

# model作成用のデータ作成 => descriptions
# とりあえず5万件で作っておいて、train用のscriptを作る
# dataの重複に気をつける
descriptions = {}
print('Start modeling...')
for i in range(1, 50000, 20):
    query = """
        SELECT items.auction_id, ptexts.description, ptexts.title
        FROM items
        LEFT JOIN processed_texts AS ptexts ON items.auction_id = ptexts.auction_id
        WHERE process_type = '{0}'
        LIMIT {1}, 20;
    """.format(args[1], i)
    cursor.execute(query)
    results = cursor.fetchall()

    if len(results) == 0:
        print('Not found data...')
        sys.exit()

    for result in results:
        print("reflect to model {0}".format(result['auction_id']))
        descriptions[result['auction_id']] = result['description'].split(' ') + result['title'].split(' ')

labeled_descriptions = models.doc2vec.LabeledListSentence(descriptions.values())
model = models.doc2vec.Doc2Vec(labeled_descriptions, min_count=0)
model.save(TEXT_ANALYZE + '/doc2vec_model/model.d2c')
