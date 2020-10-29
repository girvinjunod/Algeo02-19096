from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
#import magic
import urllib.request
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'D:/git/Algeo02-19096/test'
 
app.secret_key = "Cairocoders-Ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  
@app.route('/')
def home():
  return render_template('index.html')

@app.route('/upload')
def upload_form():
  return render_template('upload.html')

@app.route('/content') 
def content(): 
  with open('../test/apple.txt', 'r') as f:
    content = f.read()
    return render_template('content.html', text=content) 

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