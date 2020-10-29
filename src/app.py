import re
import string
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
#import magic
import urllib.request
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'os.path.join(path,test)'
path = os.getcwdb()
app.secret_key = "Cairocoders-Ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
"""
def dok_bersih():
  # Untuk mendapatkan link berita populer
  r = requests.get('127.0.0.1:5000/Content')
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

  return documents_clean
"""
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  
@app.route('/')
def home():
  return render_template('index.html')

@app.route('/upload')
def upload_form():
  return render_template('upload.html')

@app.route('/upload/<filename>')
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
  return redirect('/')
   
if __name__ == '__main__':
  app.run(debug=True)