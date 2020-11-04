import re
import string
import requests
import numpy as np
import pandas as pd
from csv import DictWriter
import csv
from bs4 import BeautifulSoup
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.stem.porter import PorterStemmer
import os
import glob
import errno
#import magic
import urllib.request
 
app = Flask(__name__)
 
UPLOAD_FOLDER = '../test'
path = '../test/*'
app.secret_key = "Cairocoders-Ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def read_file(path_to_folder):
    kal = []
    num = 2
    fieldname = ['Word','Query']
    files = glob.glob(path_to_folder)
    for name in files:
        fieldname.append(name)
        if (name.endswith('.txt')):
            try:
                with open(name, encoding='utf-8') as f:
                    temp = f.read().splitlines()
                    kal.append(temp)
            except IOError as exc: #Not sure what error this is
                if exc.errno != errno.EISDIR:
                    raise
        num += 1
    return fieldname, kal, num

def read_first(path_to_folder):
    kal = []
    nama = path_to_folder
    try:
        with open(nama, encoding='utf-8') as f:
            temp = f.readline()
            kal.append(temp)
    except IOError as exc: #Not sure what error this is
        if exc.errno != errno.EISDIR:
            raise
    return kal[0]

def clean_document(example_sent):
    stop_words = set(stopwords.words('english'))
    porter = PorterStemmer()
    word_tokens = word_tokenize(example_sent) #dibuat ke token
    word_tokens = [porter.stem(w) for w in word_tokens] #distem menggunakan porterstemmer dri nltk
    word_tokens = [w.lower() for w in word_tokens] #dibuat ke huruf kecil semua
    punc = str.maketrans('', '', string.punctuation)
    word_tokens = [w.translate(punc) for w in word_tokens] #menghilangkan punctuations
    word_tokens = [w for w in word_tokens if w.isalpha()] #filter jadi alphabet aja
    words = [w for w in word_tokens if not w in stop_words] #filter stopwords
    return words

def query_table (query, kalimat, num):
    qmat = [[0 for i in range (num-1)] for j in range (10000)]
    #input query & kalimat yang telah di clean
    kata = []
    found = False
    # n berguna untuk menampung kalimat dokumen yang sudah di clean
    for i in range (1,num-1):
        found = False
        j = 0
        # j adalah pengatur kata berikut dalam 1 dokumen
        n = np.array(clean_document(str(kalimat[i-1])))
        #print ("panjang kalimat " + str(len(n)))
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
    score = []
    for i in range (1,num-1):
        j = 0
        u = 0
        uv = 0 #u.v
        v = 0
        while (j < len(kata)):
            v += (qmat[j][i])**2
            if (qmat[j][0]!=0):
                u += (qmat[j][0])**2
                uv += qmat[j][0]*qmat[j][i]
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
            row=[]
            row += [kata[i]]
            for j in range (num-1):
                row += [str(qmat[i][j])]
            writer.writerow(row)

def read_web():
    # Untuk mendapatkan link berita populer
    r = requests.get('http://bola.kompas.com/')
    soup = BeautifulSoup(r.content, 'html.parser')
    link = []
    fieldname = ['Word', 'Query']
    for i in soup.find('div', {'class':'most__wrap'}).find_all('a'):
        i['href'] = i['href'] + '?page=all'
        link.append(i['href'])
        fieldname.append(i['href'])

    # Retrieve Paragraphs
    documents = []
    
    num = 2
    for i in link:
        r = requests.get(i)
        soup = BeautifulSoup(r.content, 'html.parser')

        sen = []
        for i in soup.find('div', {'class':'read__content'}).find_all('p'):
            sen.append(i.text)
        documents.append(' '.join(sen))
        num += 1

    # Clean Paragraphs
    documents_clean = []
    for d in documents:
        document_test = re.sub(r'[^\x00-\x7F]+', ' ', d)
        document_test = re.sub(r'@\w+', '', document_test)
        document_test = document_test.lower()
        document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
        document_test = re.sub(r'[0-9]', '', document_test)
        document_test = re.sub(r'\s{2,}', ' ', document_test)
        documents_clean.append(document_test)
    

    return fieldname, documents_clean, num

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def menu_utama():
    return render_template("menu_utama.html")

@app.route("/data/about_us")
def about_us():
    return render_template("aboutus.html")

@app.route('/local',methods=["POST", "GET"])
def home():
    if (request.method == "POST"):
	    result = request.form["nm"]
	    return redirect(url_for("result", res=result))
    else:
	    return render_template("index.html")

@app.route('/web',methods=["POST", "GET"])
def webhome():
    if (request.method == "POST"):
	    result = request.form["nm"]
	    return redirect(url_for("webresult", res=result))
    else:
	    return render_template("webindex.html")

@app.route("/websearch/<res>")
def webresult(res):
    fieldnames, kalimat, num = read_web()
    hmat ,kata = query_table(res, kalimat, num)
    score = similar(hmat,num,kata)
    frek = {}
    judul_tabel=['Word','Query']
    for i in range (2,num):
        base=os.path.basename(fieldnames[i])
        a = os.path.splitext(base)
        judul_tabel.append((a)[0])
    for i in range (2,num):
        frek[(fieldnames[i])] = score[i-2]
    frek = sorted(frek.items(), key = lambda x:(x[1], x[0]), reverse=True)
    keys = []
    judul = []
    read = []
    for key in frek:
        keys.append(key)
    for i in range (0,num-2):
        base=os.path.basename(keys[i][0])
        a = os.path.splitext(base)
        judul.append((a)[0])
        read.append(kalimat[i][0:150])
    term_table(judul_tabel, hmat, kata, num)
    return render_template('webresult.html', Text=res, file=keys, judul = judul, kal = read, num = num-2)

@app.route('/upload')
def upload_form():
    return render_template('upload.html')

@app.route("/search/<res>")
def result(res):
    fieldnames, kalimat, num = read_file(path)
    hmat ,kata = query_table(res, kalimat, num)
    score = similar(hmat,num,kata)
    frek = {}
    judul_tabel=['Word','Query']
    for i in range (2,num):
        base=os.path.basename(fieldnames[i])
        a = os.path.splitext(base)
        judul_tabel.append((a)[0])
    for i in range (2,num):
        frek[(fieldnames[i])] = score[i-2]
    frek = sorted(frek.items(), key = lambda x:(x[1], x[0]), reverse=True)
    keys = []
    judul = []
    read = []
    for key in frek:
        keys.append(key)
    for i in range (0,num-2):
        base=os.path.basename(keys[i][0])
        a = os.path.splitext(base)
        judul.append((a)[0])
        read.append(read_first(str(keys[i][0])))
    term_table(judul_tabel, hmat, kata, num)
    return render_template('result.html', Text=res, file=keys, judul = judul, kal = read, num = num-2)

@app.route('/table')
def table():
    df = pd.read_csv("query.csv")
    return render_template('termtable.html', data=df.to_html())
    
@app.route('/test/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('File(s) successfully uploaded')
    return redirect('/local')

if __name__ == '__main__':
  app.run(debug=True)