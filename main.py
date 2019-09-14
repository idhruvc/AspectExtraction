from stanfordcorenlp import StanfordCoreNLP
import logging
import json
import csv
import numpy as np
import multiword as multiword

sNLP = multiword.StanfordNLP()
# tes = sNLP.compound("canon powershot g3 i recently purchased the canon powershot g3 and am extremely satisfied with the purchase  ")
# tes1 = sNLP.advmod("canon powershot g3 i recently purchased the canon powershot g3 and am extremely satisfied with the purchase  ")
# tes2 = sNLP.negation("canon powershot g3 i recently purchased the canon powershot g3 and am extremely satisfied with the purchase  ")
tes3 = sNLP.dobj("i'd highly recommend this camera for anyone who is looking for excellent quality pictures and a combination of ease of use and the flexibility to get advanced with many options to adjust if you like")
print('tes3:' + str(tes3))
tes4 = sNLP.admof("the storyline is well written")
print('tes4' + str(tes4))
# print(tes1)
# print(tes2)
