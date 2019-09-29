from stanfordcorenlp import StanfordCoreNLP
import logging
import json
import csv
import numpy as np
import multiword as multiword
import clean
"""
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,sentiment" -port 9000 -timeout 30000
"""

sNLP = multiword.StanfordNLP()
camera_feature = clean.fitur_kamera()


bag = []
with open("Dataset.csv", 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        bag.append(''.join(line))

hasil = []

par = sNLP.HasilDependencyPath(
    "although canon's batteries are proprietary , they last a really long time , recharge fairly quickly in the camera , plus if you want 'more power', you can even find a knockoff charger and spare batteries right here on amazon")
print(par)
"""
for i in range(len(bag)):
    parse = sNLP.HasilDependencyPath(bag[i])
    if parse == None:
        parse = ''
    hasil.append(parse)
    
f = open('Aspect Extraction.csv', 'w')
for item in hasil:
    for i in range(len(item)):
        if i == 0:
            f.write(str(item[i]))
        else:
            f.write(',' + str(item[i]))
    f.write('\n')
f.close()
"""
