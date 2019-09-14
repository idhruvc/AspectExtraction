from stanfordcorenlp import StanfordCoreNLP
import logging
import json
import csv
import numpy as np
import multiword as multiword

sNLP = multiword.StanfordNLP()
tes = sNLP.compound("Nicolas cage is a very talented actor")
print(tes)
