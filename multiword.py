from stanfordcorenlp import StanfordCoreNLP
import logging
import json
import csv
import numpy as np


class StanfordNLP:
    def __init__(self, host='http://localhost', port=9000):
        self.nlp = StanfordCoreNLP(host, port=port,
                                   timeout=30000)  # , quiet=False, logging_level=logging.DEBUG)
        self.props = {
            'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }

    def word_tokenize(self, sentence):
        return self.nlp.word_tokenize(sentence)

    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)

    def postag(self, sentence):
        return self.nlp.pos_tag(sentence)

    def compound(self, sentence):  # extract nn pada relasi compund
        kalimat = self.nlp.word_tokenize(sentence)
        pola = self.nlp.dependency_parse(sentence)
        ress = []
        ceil = []
        for i in range(len(pola)):
            con = 'compound' in pola[i][0]
            if con:
                in1 = pola[i][2]
                in2 = pola[i][1]
                kal1 = kalimat[in1 - 1]
                kal2 = kalimat[in2 - 1]
                ceil = kal1 + ' ' + kal2
                ress.append(ceil)

        return ress

    def advmod(self, sentence):  # extract multi word adverb
        kalimat = self.nlp.word_tokenize(sentence)
        pola = self.nlp.dependency_parse(sentence)
        ress = []
        ceil = []

        for i in range(len(pola)):
            con = 'advmod' in pola[i][0]
            if con:
                in1 = pola[i][2]
                in2 = pola[i][1]
                kal1 = kalimat[in1 - 1]
                kal2 = kalimat[in2 - 1]
                ceil = kal1 + ' ' + kal2
                ress.append(ceil)

        return ress

    def negation(self, sentence):  # extract negation selain no
        kalimat = self.nlp.word_tokenize(sentence)
        pola = self.nlp.dependency_parse(sentence)
        ress = []
        ceil = []

        for i in range(len(pola)):
            con = 'neg' in pola[i][0]
            if con:
                in1 = pola[i][2]
                in2 = pola[i][1]
                if "n't" == kalimat[in1 - 1]:
                    kal1 = kalimat[in1 - 2] + kalimat[in1 - 1]  # handle n't
                else:
                    kal1 = kalimat[in1 - 2] + ' ' + \
                        kalimat[in1 - 1]  # hanle with  not
                kal2 = kalimat[in2 - 1]
                ceil = kal1 + ' ' + kal2
                ress.append(ceil)
        return ress

    def negationNO(self, sentence):  # extract negation no
        kalimat = self.nlp.word_tokenize(sentence)
        pola = self.nlp.dependency_parse(sentence)
        ress = []
        ceil = []

        for i in range(len(pola)):
            con = 'neg' in pola[i][0]
            if con:
                in1 = pola[i][2]
                in2 = pola[i][1]
                kal1 = kalimat[in1 - 1]
                kal2 = kalimat[in2 - 1]
                ceil = kal1 + ' ' + kal2
                ress.append(ceil)

        return ress

    def hypoPhrase(self, sentence):  # extract phrasa yang panjang
        kalimat = self.nlp.word_tokenize(sentence)
        pola = self.nlp.dependency_parse(sentence)
        ress = []
        ceil = []

        for i in range(len(pola)):  # untuk aux
            con = 'aux' in pola[i][0]
            if con and pola[i+1][0] == 'aux':
                in1 = pola[i][2]
                in1next = pola[i+1][2]
                kal1 = kalimat[in1 - 1]
                kal1nex = kalimat[in1next - 1]
                ceil = kal1 + ' ' + kal1nex
                ress.append(ceil)
            elif con and pola[i+1][0] == 'cop':
                in1 = pola[i+1][2]
                in2 = pola[i][1]
                kal1 = kalimat[in1-1]
                kal2 = kalimat[in2-1]
                ceil = kal1 + ' ' + kal2
                ress.append(ceil)
        if len(ress) > 1:
            ress[0:1] = [' '.join(ress)]
            ress.pop(1)

        return ress


if __name__ == '__main__':
    sNLP = StanfordNLP()
    sNLP.compound("the plot could have better story")
