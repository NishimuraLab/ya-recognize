FROM ubuntu:trusty

RUN apt-get update && apt-get -y upgrade && apt-get install -y git make gcc wget unzip
RUN git clone https://github.com/dav/word2vec.git && cd /word2vec/src/ && make word2vec word2phrase distance word-analogy compute-accuracy
