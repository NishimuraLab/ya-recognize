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

REP_ROOT = os.environ['YA_RECOGNIZE_ROOT']
TEXT_ANALYZE = REP_ROOT + '/text_analyze'

loaded_model = models.doc2vec.Doc2Vec.load(TEXT_ANALYZE + '/doc2vec_model/model.d2c')
tarray = "商品 説明 Office 2016 WIN amp MAC 5 PC モバイル 5 台 永続 使用 版 Microsoft 社 認証 済み アカウント 永続 使用 版 Microsoft Office 2016 認証 済み アカウント X 1 Windows PC Mac インストール 5 台 iPhone iPad タブレット 等 インストール 5 台 合計 10 台 インストール 可能 対応 OS Windows 7 Windows8 Windows8 1 Windows10 対応 OS Mac OS X 10 10 以降 推奨 34 bit 64 bit 両方 対応 日本語版 対応 ご 入金 確認 後 アカウント ID パスワード お知らせ いたし サインイン 説明書 付き 発送 方法 送料 無料 入金 方法 Yahoo! かんたん 決済 Yahoo! マネー 預金 払い クレジットカード 決済 インターネットバンキング 銀行 振込 振込 先 ジャパンネット銀行 コンビニ 支払い ".split(' ')

print(loaded_model.most_similar_labels(tarray))
