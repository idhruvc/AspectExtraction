from stanfordcorenlp import StanfordCoreNLP
import logging
import json
import csv
import numpy as np


class StanfordNLP:
    def __init__(self, host='http://localhost', port=9000):
        # , quiet=False, logging_level=logging.DEBUG)
        self.nlp = StanfordCoreNLP(host, port=port, timeout=30000)
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
        print(kalimat)
        print(pola)
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

    def adjectivalModifier(self, sentence):  # extract multi word adverb
        kalimat = self.nlp.word_tokenize(sentence)
        pola = self.nlp.dependency_parse(sentence)
        print(kalimat)
        print(pola)
        ress = []
        ceil = []

        for i in range(len(pola)):
            con = 'amod' in pola[i][0]
            if con:
                in1 = pola[i][2]
                in2 = pola[i][1]
                kal1 = kalimat[in1 - 1]
                kal2 = kalimat[in2 - 1]
                ceil = kal1 + ' ' + kal2
                ress.append(ceil)

        return ress

    def directObject(self, sentence):  # extract multi word adverb
        kalimat = self.nlp.word_tokenize(sentence)
        pola = self.nlp.dependency_parse(sentence)
        polas = self.nlp.pos_tag(sentence)
        print(kalimat)
        print(pola)
        print(polas)
        ress = []
        ceil = []
        new = []

        for i in range(len(pola)):
            con = 'nsubj' in pola[i][0]
            j = i + 1
            if con:
                if polas[pola[i][2] - 1][1] == 'NN':
                    new.append(pola[i][2])
                elif polas[pola[i][1] - 1][1] == 'NN':
                    new.append(pola[i][1])
                for j in range(len(pola)):
                    con2 = 'dobj' in pola[j][0]
                    if con2:
                        if (polas[pola[j][2] - 1][1] == 'VBD' or polas[pola[j][2] - 1][1] == 'JJ'):
                            new.append(pola[j][2])
                        if (polas[pola[j][1] - 1][1] == 'VBD' or polas[pola[j][1] - 1][1] == 'JJ'):
                            new.append(pola[j][1])
                        new = sorted(set(new))
                        if len(new) == 3:
                            kal1 = kalimat[new[0] - 1]
                            kal2 = kalimat[new[1] - 1]
                            kal3 = kalimat[new[2] - 1]
                            ceil = kal1 + ' ' + kal2 + ' ' + kal3
                            ress.append(ceil)

        return ress

    def adjectivalComplement(self, sentence):  # extract multi word adverb
        kalimat = self.nlp.word_tokenize(sentence)
        pola = self.nlp.dependency_parse(sentence)
        print(kalimat)
        print(pola)
        ress = []
        ceil = []
        new = []

        for i in range(len(pola)):
            con = 'nsubj' in pola[i][0]
            j = i + 1
            if con:
                new.append(pola[i][2])
                for j in range(len(pola)):
                    con2 = 'xcomp' in pola[j][0]
                    if con2:
                        new.append(pola[j][2])
                        new.append(pola[j][1])
                        new = sorted(set(new))
                        kal1 = kalimat[new[0] - 1]
                        kal2 = kalimat[new[1] - 1]
                        kal3 = kalimat[new[2] - 1]
                        ceil = kal1 + ' ' + kal2 + ' ' + kal3
                        ress.append(ceil)

        return ress

    def complementVerb(self, sentence):  # extract multi word adverb
        kalimat = self.nlp.word_tokenize(sentence)
        pola = self.nlp.dependency_parse(sentence)
        polas = self.nlp.pos_tag(sentence)
        print(kalimat)
        print(pola)
        ress = []
        ceil = []
        new = []

        for i in range(len(pola)):
            con = 'nsubj' in pola[i][0]
            j = i + 1
            if con:
                if polas[pola[i][2] - 1][1] == 'NN':
                    new.append(pola[i][2])
                elif polas[pola[i][1] - 1][1] == 'NN':
                    new.append(pola[i][1])
                for j in range(len(pola)):
                    con2 = 'cop' in pola[j][0]
                    if con2:
                        if (polas[pola[j][2] - 1][1] == 'VBD' or polas[pola[j][2] - 1][1] == 'JJ'):
                            new.append(pola[j][2])
                        if (polas[pola[j][1] - 1][1] == 'VBD' or polas[pola[j][1] - 1][1] == 'JJ'):
                            new.append(pola[j][1])
                        new = sorted(set(new))
                        kal1 = kalimat[new[0] - 1]
                        kal2 = kalimat[new[1] - 1]
                        kal3 = kalimat[new[2] - 1]
                        ceil = kal1 + ' ' + kal2 + ' ' + kal3
                        ress.append(ceil)

        return ress

    def adverbialModifier(self, sentence):  # extract multi word adverb
        kalimat = self.nlp.word_tokenize(sentence)
        pola = self.nlp.dependency_parse(sentence)
        polas = self.nlp.pos_tag(sentence)
        print(kalimat)
        print(pola)
        print(polas)
        ress = []
        ceil = []
        new = []

        for i in range(len(pola)):
            con = 'nsubjpass' in pola[i][0]
            j = i + 1
            if con:
                if polas[pola[i][2] - 1][1] == 'NN':
                    new.append(pola[i][2])
                elif polas[pola[i][1] - 1][1] == 'NN':
                    new.append(pola[i][1])
                for j in range(len(pola)):
                    con2 = 'advmod' in pola[j][0]
                    if con2:
                        if (polas[pola[j][2] - 1][1] == 'VBN' or polas[pola[j][2] - 1][1] == 'RB'):
                            new.append(pola[j][2])
                        if (polas[pola[j][1] - 1][1] == 'VBN' or polas[pola[j][1] - 1][1] == 'RB'):
                            new.append(pola[j][1])
                        new = sorted(set(new))

                        print(new)
                        if len(new) == 3:
                            kal1 = kalimat[new[0] - 1]
                            kal2 = kalimat[new[1] - 1]
                            kal3 = kalimat[new[2] - 1]
                            ceil = kal1 + ' ' + kal2 + ' ' + kal3
                            ress.append(ceil)

        return ress

if __name__ == '__main__':
    sNLP = StanfordNLP()
    sNLP.compound("the plot could have better story")
