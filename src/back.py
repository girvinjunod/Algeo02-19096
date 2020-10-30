# -*- coding: utf-8 -*-
import re
import string
import requests
import numpy as np
import pandas as pd
import glob
import errno
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import glob
import errno
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

path = "../test/*"
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
        document_test = re.sub(r'[^\x00-\x7F]+', ' ', str(d)) 
        document_test = re.sub(r'@\w+', '', str(document_test))
        document_test = document_test.lower() #huruf kecil semua
        document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test) 
        document_test = re.sub(r'[0-9]', '', document_test) #buang angka
        document_test = re.sub(r'\s{2,}', ' ', document_test)
        document_test = document_test.split() #split
        document_test = stemmer.stem(str(document_test))

        documents_clean.append(document_test)
    return documents_clean

def read_file(path_to_folder):
    kal = []
    num = 2
    fieldname = ['Word','Q']
    files = glob.glob(path_to_folder)
    for name in files:
        fieldname.append(name)
        try:
            with open(name,encoding='utf-8') as f:
                temp = f.read().splitlines()
                kal.append(temp)
        except IOError as exc: #Not sure what error this is
            if exc.errno != errno.EISDIR:
                raise
        num += 1
    return fieldname, kal, num

fieldname, kalimat, num = read_file(path)
kalimat = clean_dokumen(kalimat)
print(kalimat)