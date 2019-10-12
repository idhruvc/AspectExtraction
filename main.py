from stanfordcorenlp import StanfordCoreNLP
import logging
import json
import csv
import numpy as np
import multiword as multiword
# import clean

"""
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,sentiment" -port 9000 -timeout 30000
"""

sNLP = multiword.StanfordNLP()

# Run Program
"""
par = sNLP.allTableOne("the reason i rated it a four is because of that darn diopter adjustment dial its very small and hard to turn so you can't get an accurate adjustment ( for those of you who don't know what a diopter adjustment is , it is to adjust the focus of the viewfinder to your eyesight  )")
print("Output Replace" + str(par))
"""
bag = []
with open("Data_Test.csv", 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        bag.append(''.join(line))

hasil = []

for k in range(len(bag)):
    AE = sNLP.allTableOne(bag[k])
    hasil.append(AE)

# print(hasil[23])
# print(len(hasil[23]))

aspect = []
temp = []
# print(hasil)
for i in range(len(hasil)):
    if hasil[i] != None:
        pjg = len(hasil[i])
        for x in range(pjg):
            lent = len(hasil[i][x])
            if lent == 2:
                h0 = hasil[i][x][0]
                h1 = hasil[i][x][1]
                a = sNLP.postag(h0)
                b = sNLP.postag(h1)

                posA = a[0][1]
                posB = b[0][1]
                if posA == 'NN' or posA == 'NNS':
                    temp.append(a[0][0])
                if posB == 'NN' or posB == 'NNS':
                    if len(b) > 1:
                        h = b[0][0]
                        h += ' '+b[1][0]
                        temp.append(h)
                    if len(b) == 1:
                        temp.append(b[0][0])
                # temp.append(g)
            elif lent == 3:
                h0 = hasil[i][x][0]
                h1 = hasil[i][x][1]
                h2 = hasil[i][x][2]
                a = sNLP.postag(h0)
                b = sNLP.postag(h1)
                c = sNLP.postag(h2)

                posA = a[0][1]
                posB = b[0][1]
                posC = c[0][1]
                if posA == 'NN' or posA == 'NNS':
                    temp.append(a[0][0])
                if posB == 'NN' or posB == 'NNS':
                    if len(b) > 1:
                        h = b[0][0]
                        h += ' '+b[1][0]
                        temp.append(h)
                    if len(b) == 1:
                        temp.append(b[0][0])
                if posC == 'NN' or posB == 'NNS':
                    if len(c) > 1:
                        h = c[0][0]
                        h += ' '+c[1][0]
                        temp.append(h)
                    if len(c) == 1:
                        temp.append(c[0][0])
                # print(a, b, c)
                # temp.append(g)
        aspect.append(temp)
        temp = []
    else:
        temp = ['']
        aspect.append(temp)
        temp = []

"""
realAspect = []
# print(len(realAspect))
for x in range(len(aspect)):
    term = aspect[x]
    cocok = False
    for j in range(len(realAspect)):
        if term == realAspect[j]:
            cocok = True
            break
        elif term != realAspect[j]:
            cocok = False
    if cocok == False:
        realAspect.append(term)
print(realAspect)

for i in range(len(bag)):
    parse = sNLP.HasilDependencyPath(bag[i])
    if parse == None:
        parse = ''
    hasil.append(parse)
"""
f = open('Aspect Extraction Test.csv', 'w')
for item in aspect:
    for i in range(len(item)):
        if i == 0:
            f.write(str(item[i]))
        else:
            f.write(',' + str(item[i]))
    f.write('\n')
f.close()
