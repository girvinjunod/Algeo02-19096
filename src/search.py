from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from csv import DictWriter
from pathlib import Path
import pandas as pd
import numpy as np
import os
import glob
import errno
import csv

def read_file(path_to_folder):
    kal = []
    num = 2
    fieldname = ['Word','Q']
    files = glob.glob(path_to_folder)
    for name in files:
        fieldname.append(name)
        try:
            with open(name, encoding='utf-8') as f:
                temp = f.read().splitlines()
                kal.append(temp)
        except IOError as exc: #Not sure what error this is
            if exc.errno != errno.EISDIR:
                raise
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
    qmat = [[0 for i in range (num-1)] for j in range (10000)]
    #input query & kalimat yang telah di clean
    n = [0 for i in range (num)]
    kata = []
    found = False
    # n berguna untuk menampung kalimat dokumen yang sudah di clean
    for i in range (1,num-1):
        found = False
        j = 0
        # j adalah pengatur kata berikut dalam 1 dokumen
        n = np.array(clean_document(str(kalimat[i-1])))
        #print ("panjang kalimat " + str(len(n)))
        if (i == 1):
            kata.append(str(n[j]))
            qmat[j][i] += 1
            j += 1
        else:
            while (j < len(n)):
                found = False
                k = 0
                while(k < len(kata)) and (found==False):
                    if (kata[k]==n[j]):
                        qmat[k][i] += 1
                        found = True
                    else:
                        k += 1
                #print("k adalah" + str(k))
                if (found == False):
                    kata.append(str(n[j]))
                    qmat[k][i] += 1
                j += 1
    j = 0
    q = clean_document(str(query))
    while (j < len(q)):
        k=0
        found = False
        while(k < len(kata)) and (found==False):
            if (kata[k]==q[j]):
                qmat[k][0] += 1
                found= True
            else:
                k += 1
        if (found == False):
            kata.append(str(q[j]))
            qmat[k][0] += 1
        j += 1
    return qmat, kata

def similar(qmat,num,kata):
    for i in range (1,num-1):
        j = 0
        u = 0
        uv = 0 #u.v
        v = 0
        while (j < len(kata)):
            if (qmat[j][0]!=0):
                v = v + qmat[j][i]
                u = u + qmat[j][0]
                uv += u*v
                j += 1
            else:
                j += 1
        bagi = (u**0.5)*(v**0.5)
        if (bagi != 0):
            s = uv/bagi
            score.append(s)
        else:
            score.append(int(0))
    return score

def term_table(fieldname, qmat, kata, num):
    with open("query.csv", mode='w',newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(fieldname)
        for i in range(len(kata)):
            writer.writerow([kata[i],str(qmat[i][0:num])])
"""
fieldname = ['Word','Q','D1','D2','D3','D4','D5'
    ,'D6','D7','D8','D9','D10','D11','D12','D13','D14','D15','D16','D17','D18',
    'D19','D20','D21','D22','D23','D24','D25']
"""
path = 'D:/git/Algeo02-19096/test/*.txt'
fieldnames, kalimat, num = read_file(path)
query = input("Masukkan Pencarian:")
score = []
kata = []

hmat= [["0" for i in range (num)] for j in range (10000)]
read_file(path)
hmat ,kata = query_table(query, kalimat, num)
print(similar(hmat,num,kata))
#hmat=np.insert(str(hmat), 0, kata, axis=1)
term_table(fieldnames, hmat, kata, num)

df = pd.read_csv("query.csv")
df.head() 
"""
with open('query.csv','w') as f:
    csv_writer = DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()
    #blom selesai
"""