from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from csv import DictWriter
from pathlib import Path
import numpy as np
import os 

def read_file(path_to_folder):
    kal = []
    num = 0
    fieldname = ['Word','Q']
    for i in os.listdir(path_to_folder): 
        if i.endswith('.txt'): 
            fieldname.append(i)
            f = open(i)
            a = f.read()
            kal.append(a)
            f.close()
            num += 1
    return fieldname, kal, num

def clean_document(example_sent):
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(example_sent) 
    filter = [w for w in word_tokens if not w in stop_words] 
    filter = [] 
    for w in word_tokens: 
        if w not in stop_words: 
            filter.append(w) 
    a = word_tokens #kata asli
    b = filter #kata setelah difilter
    return b

def query_table (query, kalimat, num):
    #input query & kalimat yang telah di clean
    n = ["0" for k in range (num)]
    found = False
    foundq = False
    qmat = [["0" for j in range (10000)] for i in range (num)]
    for i in range (2,num):
        j = 0
        n = clean_document(kalimat[i])
        while ((j < n) and (found == False)):
            while ((n[j]!="0") and (found == False)):
                if (qmat[j][0] == n[j]):
                    a = int(qmat[j][i])
                    a += 1
                    qmat[j][i] = str(a)
                    found = True
                else:
                    j += 1
            if (found == False):
                q[j][0] = n[j]
                d = int(qmat[j][i])
                d += 1
                qmat[j][i] = str(d)
                found = True
    
    for l in range(len(query)):
        p = 0
        while ((qmat[p][0]!="0") and (foundq == False)):
            if (qmat[p][0] == query[l]):
                a = int(qmat[l][1])
                a += 1
                qmat[p][1] = str(a)
                foundq = True
            else:
                p +=1
        if (foundq == False):
            qmat[p][0] = query[l]
            d = int(qmat[p][1])
            d += 1
            qmat[p][1] = str(a)
            foundq = True
    return qmat

def similar(qmat,num):
    for i in range (2,num):
        j = 0
        u = 0
        uv = 0 #u.v 
        v = 0
        while (qmat[j][0]!="0"):
            if (qmat[j][1]!="0"):
                v = v + qmat[j][i]
                u = u + qmat[j][i]
                uv = uv + qmat[j][1]*qmat[j][i]
                j += 1
            else:
                j += 1
        bagi = (u**0.5)*(v**0.5)
        s = float(uv/bagi)
        score.append[s]
    return score

"""
fieldname = ['Word','Q','D1','D2','D3','D4','D5'
    ,'D6','D7','D8','D9','D10','D11','D12','D13','D14','D15','D16','D17','D18',
    'D19','D20','D21','D22','D23','D24','D25']
"""
example_sent = "This is a sample sentence, showing off the stop words filtration."
path = '/../test/'
fieldnames, kalimat, num = read_file(path)
query = input("Masukkan Pencarian:")
q = clean_document(query)
print(q)
print(len(q))
score = []

read_file(path)
hmat = [["0" for i in range (num)] for j in range (10000)]
hmat = query_table(q, kalimat, num)
print(similar(hmat,num))

"""
with open('query.csv','w') as f:
    csv_writer = DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()
    #blom selesai
"""