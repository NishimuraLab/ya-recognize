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
auction_ids = []
model = models.doc2vec.Doc2Vec(min_count=1)

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

    # if len(results) == 0:
    #     print('Not found data...')
    #     sys.exit()
    #
    sentences = []
    for result in results:
        print("reflect to model {0}".format(result['auction_id']))
        auction_ids.append(result['auction_id'])
        sentences.append(models.doc2vec.LabeledSentence(words=result['description'].split(' ') + result['title'].split(' '), tags=["{0}".format(result['auction_id'])]))
        model.scan_vocab(sentences, update=True)

model.scale_vocab()
model.finalize_vocab()

# 訓練
for i in range(0, 800, 20):
    start = i
    end = i + 20
    query = """
        SELECT auction_id, description, title FROM processed_texts WHERE auction_id IN ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}')
    """.format(auction_ids[start:end][0], auction_ids[start:end][1], auction_ids[start:end][2], auction_ids[start:end][3], auction_ids[start:end][4], auction_ids[start:end][5], auction_ids[start:end][6], auction_ids[start:end][7], auction_ids[start:end][8]
    , auction_ids[start:end][9], auction_ids[start:end][10], auction_ids[start:end][11], auction_ids[start:end][12], auction_ids[start:end][13], auction_ids[start:end][14], auction_ids[start:end][15], auction_ids[start:end][16], auction_ids[start:end][17]
    , auction_ids[start:end][18], auction_ids[start:end][19])
    print(query)
    cursor.execute(query)
    ptexts = cursor.fetchall()

    sentences = []
    for ptext in ptexts:
        sentences.append(models.doc2vec.LabeledSentence(words=ptext['description'].split(' ') + ptext['title'].split(' '), tags=["{0}".format(ptext['auction_id'])]))
    model.train(sentences)

model.save(TEXT_ANALYZE + '/doc2vec_model/model.d2c')
