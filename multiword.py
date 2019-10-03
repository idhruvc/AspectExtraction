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
                # ress.append(kal2)

        return ress

    def advmod(self, sentence):  # extract multi word adverb
        kalimat = self.nlp.word_tokenize(sentence)
        pola = self.nlp.dependency_parse(sentence)
        ress = []
        #ceil = []

        for i in range(len(pola)):
            con = 'advmod' in pola[i][0]
            if con:
                in1 = pola[i][2]
                in2 = pola[i][1]
                kal1 = kalimat[in1 - 1]
                kal2 = kalimat[in2 - 1]
                ceil = kal1 + ' ' + kal2
                ress.append(ceil)
                # ress.append(kal2)
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
                # ress.append(kal2)
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
                # ress.append(kal2)

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

    def adjectivalModifier(self, sentence):  # extract multi word adverb aman
        kalimat = self.nlp.word_tokenize(sentence)
        pola = self.nlp.dependency_parse(sentence)
        ress = []
        ceil = []
        fin = []

        for i in range(len(pola)):
            con = 'amod' in pola[i][0]
            if con:
                in1 = pola[i][2]
                in2 = pola[i][1]
                kal1 = kalimat[in1 - 1]
                kal2 = kalimat[in2 - 1]
                ress.append(kal1)
                ress.append(kal2)
                fin.append(ress)  # pembaruan mulai dari sini
                ress = []
        return fin

    def directObject(self, sentence):  # extract multi word adverb belum aman.
        kalimat = self.nlp.word_tokenize(sentence)
        pola = self.nlp.dependency_parse(sentence)
        polas = self.nlp.pos_tag(sentence)
        ress = []
        ceil = []
        new = []
        fin = []

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
                            ress.append(kal1)
                            ress.append(kal2)
                            ress.append(kal3)
                            fin.append(ress)  # pembaruan mulai dari sini
                            ress = []

        return fin

    def adjectivalComplement(self, sentence):  # extract multi word adverb
        kalimat = self.nlp.word_tokenize(sentence)
        pola = self.nlp.dependency_parse(sentence)
        ress = []
        ceil = []
        new = []
        fin = []

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
                        ress.append(kal1)
                        ress.append(kal2)
                        ress.append(kal3)
                        fin.append(ress)  # pembaruan mulai dari sini
                        ress = []

        return fin

    def complementVerb(self, sentence):  # extract multi word adverb
        kalimat = self.nlp.word_tokenize(sentence)
        pola = self.nlp.dependency_parse(sentence)
        polas = self.nlp.pos_tag(sentence)
        ress = []
        ceil = []
        new = []
        fin = []

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

                        if len(new) == 3:
                            kal1 = kalimat[new[0] - 1]
                            kal2 = kalimat[new[1] - 1]
                            kal3 = kalimat[new[2] - 1]
                            ress.append(kal1)
                            ress.append(kal2)
                            ress.append(kal3)
                            fin.append(ress)  # pembaruan mulai dari sini
                            ress = []

        return fin

    def adverbialModifier(self, sentence):  # extract multi word adverb
        kalimat = self.nlp.word_tokenize(sentence)
        pola = self.nlp.dependency_parse(sentence)
        polas = self.nlp.pos_tag(sentence)
        ress = []
        ceil = []
        new = []
        fin = []

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

                        if len(new) == 3:
                            kal1 = kalimat[new[0] - 1]
                            kal2 = kalimat[new[1] - 1]
                            kal3 = kalimat[new[2] - 1]
                            ress.append(kal1)
                            ress.append(kal2)
                            ress.append(kal3)
                            fin.append(ress)  # pembaruan mulai dari sini
                            ress = []

        return fin

    def removeDupli2D(self, list):
        result = []
        for x in list:
            if x not in result:
                result.append(x)
        return result

    def allTableOne(self, sentence):
        if len(self.adjectivalModifier(sentence)) > 0 or len(self.directObject(sentence)) > 0 or len(self.adjectivalComplement(sentence)) > 0 or len(self.complementVerb(sentence)) > 0 or len(self.adverbialModifier(sentence)) > 0:
            all = []
            # Function Table 1
            admod = self.adjectivalModifier(sentence)
            dirob = self.directObject(sentence)
            adjcom = self.adjectivalComplement(sentence)
            comverb = self.complementVerb(sentence)
            adverb = self.adverbialModifier(sentence)
            # Function Table 2
            #print("~~~ Sebelum dilakukan proses replace data ~~~")
            compound = self.compound(sentence)
            #print("Compound Noun:" + str(compound))
            advmod = self.advmod(sentence)
            #print("Adverbial Modifier :" + str(advmod))
            negation = self.negation(sentence)
            #print("Simple Negation :" + str(negation))
            negationNo = self.negationNO(sentence)
            #print("Negation Through :" + str(negationNo))
            hypoPhrase = self.hypoPhrase(sentence)
            #print("HypoPhrase :" + str(hypoPhrase))
            all.extend(admod)
            all.extend(dirob)
            all.extend(adjcom)
            all.extend(comverb)
            all.extend(adverb)
            total = all
            total = self.removeDupli2D(total)
           # print("Satuan Function :" + str(total))
            new = []
            new.append(compound)
            new.append(advmod)
            new.append(negation)
            new.append(negationNo)
            new.append(hypoPhrase)
            for i in range(len(total)):
                for j in range(len(total[i])):
                    for x in new:
                        for y in x:
                            if total[i][j] in y:
                                total[i][j] = y
                                break
            for i in compound:
                for j in total:
                    if i in total:
                        temp_index = total.index(i)
                        total[temp_index:temp_index + 1] = compound
            for i in range(len(negation)):
                temp_word = negation[i].replace(negationNo[i], "")
                if (temp_word in total):
                    temp_index = total.index(temp_word)
                    total[temp_index] = negation[i]
            for i in advmod:
                if i in total:
                    temp_index = total.index(i)
                    total[temp_index:temp_index + 1] = advmod
            return total


if __name__ == '__main__':
    sNLP = StanfordNLP()
    #b = sNLP.dependency_parse("the plot could have been better")
