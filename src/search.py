from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from csv import DictWriter
import numpy as np
import os 
"""
fieldname = ['Word','Q','D1','D2','D3','D4','D5'
    ,'D6','D7','D8','D9','D10','D11','D12','D13','D14','D15','D16','D17','D18',
    'D19','D20','D21','D22','D23','D24','D25']
"""
example_sent = "This is a sample sentence, showing off the stop words filtration."
path_to_folder = "./test"
fieldname = ['Word','Q']
def read_file(path_to_folder):
    kal = []
    num = 0
    for i in os.listdir(path_to_folder): 
        if i.endswith('.txt'): 
            fieldname.append(i)
            f = open(i,'r')
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

fieldnames, kalimat = read_file(path_to_folder)

def query_table (kalimat, num):
    n = [" " for k in range (2,num)]
    qmat = [[" " for j in range (10000)] for i in range (num)]
    for i in range (num):
        n = clean_document(kalimat[i])
        for j in range (n):
            while n[j]!=" ":
                if (qmat[j][0] == n[j]):
                    a = int(qmat[j][i])
                    a += 1
                    qmat[j][i] = str(a)
                else:
                    j += 1
    return qmat



    
with open('query.csv','w') as f:
    csv_writer = DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()
    #blom selesai
q = input("Masukkan Pencarian:")