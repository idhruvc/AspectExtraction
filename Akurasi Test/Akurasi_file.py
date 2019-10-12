import csv

bag = []
with open("Aspect Extraction.csv", 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        bag.append(line)
# print(bag[596])

realAspect = []
tampung = []
# print(len(realAspect))
for x in range(len(bag)):
    pjg = len(bag[x])
    for t in range(pjg):
        cocok = False
        term = bag[x][t]
        for j in range(len(tampung)):
            if term == tampung[j]:
                cocok = True
                break
            elif term != tampung[j]:
                cocok = False
        if cocok == False:
            tampung.append(term)
    realAspect.append(tampung)
    tampung = []

"""
f = open('Akurasi Test File.csv', 'w')
for item in realAspect:
    for i in range(len(item)):
        if i == 0:
            f.write(str(item[i]))
        else:
            f.write(',' + str(item[i]))
    f.write('\n')
f.close()
"""
