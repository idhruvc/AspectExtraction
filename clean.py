import numpy as np
import csv
import nltk
from nltk.tokenize import PunktSentenceTokenizer, word_tokenize

bag = []
with open("Data_Test.csv", 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        bag.append(''.join(line))

#a = bag[0]
# c = a.index('#') + 2
# print(a[:c-2])
kalimat = []  # kalimat bersih
fitur_tmp = []
for i in range(len(bag)):
    sent = bag[i]
    sentence_index = sent.index('#') + 2
    kal = sent[sentence_index:]
    fit = sent[:sentence_index - 2]
    kalimat.append(kal)
    fitur_tmp.append(fit)

fitur = []  # menyimpan fitur sementara
for j in range(len(fitur_tmp)):
    con = fitur_tmp[j].count(',')
    if con >= 1:
        clean = fitur_tmp[j]
        cl = clean.replace(',', ' ')
        tmp = cl.split()
        fitur.append(tmp)
    else:
        a = [fitur_tmp[j]]
        fitur.append(a)


with open("Data_Test.csv", 'w', newline='') as f:
    tulis = csv.writer(f)
    for j in range(len(kalimat)):
        tulis.writerow([kalimat[j]])


def bersih(fitur):
    clean_fitur = []
    for i in range(len(fitur)):
        temp = fitur[i]
        if len(temp) > 2:
            for u in range(len(temp)-1):
                io = temp[u]
                if '+' not in io and '-' not in io:
                    temp[u:u+2] = [' '.join(temp[u:u+2])]
                    break
            clean_fitur.append(temp)
        else:
            clean_fitur.append(temp)

    return clean_fitur


def trainFeature():
    ou = bersih(fitur)
    Feature = bersih(ou)  # koleksi fitur
    return Feature
