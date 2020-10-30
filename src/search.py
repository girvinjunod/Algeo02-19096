from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from csv import DictWriter
from pathlib import Path
import numpy as np
import os
import glob
import errno

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
    # n berguna untuk menampung kalimat dokumen yang sudah di clean
    for i in range (1,num-1):
        found = False
        j = 0
        # j adalah pengatur kata berikut dalam 1 dokumen
        n = np.array(clean_document(str(kalimat[i-1])))
        print(np.array(clean_document(str(kalimat[i-1]))))
        print(len(n))
        #print ("panjang kalimat " + str(len(n)))
        while (j < len(n)):
            if (i == 1) and (j==0):
                kata.append(str(n[j]))
                qmat[j][i] += 1
            else:
                k = 0
                while(k < len(kata)) and (found==False):
                    if (kata[k]==n[j]):
                        qmat[k][i] += 1
                        found= True
                    else:
                        k += 1
                if (found == False):
                    kata.append(str(n[j]))
                    qmat[k][i] += 1
            j += 1
    
    q = clean_document(str(query))
    while (j < len(q)):
        k=0
        while(k < len(kata)) and (found==False):
            if (kata[k]==n[k]):
                qmat[k][1] += 1
                found= True
            else:
                k += 1
        if (found == False):
            kata.append(str(n[j]))
            qmat[k][1] += 1
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
                u = u + qmat[j][i]
                uv += qmat[j][0]*qmat[j][i]
                j += 1
            else:
                j += 1
        bagi = (u**0.5)*(v**0.5)
        print(bagi)
        s = float(uv/bagi)
        score.append[s]
    return score

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
print(hmat[0:50])
print(kata)
print(similar(hmat,num,kata))

"""
with open('query.csv','w') as f:
    csv_writer = DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()
    #blom selesai
"""