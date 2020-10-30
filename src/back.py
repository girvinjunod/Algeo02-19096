# -*- coding: utf-8 -*-

import re
import string
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def web_scraping():
    # Untuk mendapatkan link berita populer
    r = requests.get('https://kompas.com/')
    soup = BeautifulSoup(r.content, 'html.parser')

    link = []
    for i in soup.find('div', {'class':'most__wrap'}).find_all('a'):
        i['href'] = i['href'] + '?page=all'
        link.append(i['href'])

    # Retrieve Paragraphs
    documents = []
    for i in link:
        r = requests.get(i)
        soup = BeautifulSoup(r.content, 'html.parser')

        sen = []
        for i in soup.find('div', {'class':'read__content'}).find_all('p'):
            sen.append(i.text)
        documents.append(' '.join(sen))

    return documents

def clean_dokumen(documents):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    documents_clean = []
    for d in documents:
        document_test = re.sub(r'[^\x00-\x7F]+', ' ', d) 
        document_test = re.sub(r'@\w+', '', document_test)
        document_test = document_test.lower() #huruf kecil semua
        document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test) 
        document_test = re.sub(r'[0-9]', '', document_test) #buang angka
        document_test = re.sub(r'\s{2,}', ' ', document_test)
        document_test = document_test.split() #split
        document_test = stemmer.stem(document_test)

        documents_clean.append(document_test)
    return documents_clean

docs = dok_bersih()