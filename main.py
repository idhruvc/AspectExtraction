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
tes1 = sNLP.adjectivalModifier("The Movie had an excellent storyline!")
print('test Adjectival Modifier :' + str(tes1))
tes2 = sNLP.directObject("the story got stale")
print('test DirectObject' + str(tes2))
tes3 = sNLP.adjectivalComplement("The music does sound great")
print('test AdjectivalComplement' + str(tes3))
tes4 = sNLP.complementVerb("The action music used in the movie wasn't too good")
print('test ComplementVerb' + str(tes4))
tes5 = sNLP.adverbialModifier("the storyline is well written")
print('test adverbialModifier' + str(tes5))
# print(tes1)
# print(tes2)
