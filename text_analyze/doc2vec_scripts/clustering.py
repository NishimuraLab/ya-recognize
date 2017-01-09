from gensim import models
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
import x_means as XMeans
import os
import sys
import MySQLdb
import MySQLdb.cursors

REP_ROOT = os.environ['YA_RECOGNIZE_ROOT']
TEXT_ANALYZE = REP_ROOT + '/text_analyze'
DOC2VEC_MODEL = TEXT_ANALYZE + '/doc2vec_model'

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

def fetch_similarities(label_id):
    query = "SELECT pair_label_id, degree FROM similarities WHERE label_id = {0}".format(label_id)
    cursor.execute(query)
    return cursor.fetchall()

# labels = dic
def create_similarities_matrix(labels):
    matrix = []
    matrix_append = matrix.append
    label_count = len(labels)
    for label_id, label in labels.items():
        vec = np.zeros(label_count)
        similarities = fetch_similarities(label_id)
        for similarity in similarities:
            pair_label = labels[similarities['pair_label_id']]
            _, pair_label_idx = pair_label.split('_')
            vec[int(pair_label_idx)] = similarity['degree']
        matrix_append(vec)
    return matrix

# arguments
args = sys.argv
if len(args) == 1:
    print('Please give model name want to load.')
    sys.exit()

# labelをfetch
# query = """
#     SELECT id, label FROM labels;
# """
# cursor.execute(query)
# labels = cursor.fetchall()

# keyがid, valueがlabelの辞書に整形する
labels_dic = {}
for label in labels:
    labels_dic[label['id']] = label['label']

matrix = create_similarities_matrix(labels_dic)
print(matrix[:10])
# 次元圧縮
lsa = TruncatedSVD(1000)
info_matrix = lsa.fit_transform(matrix)
print(info_matrix[:10])
# データ整形ここまで

km = KMeans
fitted_km = km.fit(matrix)
