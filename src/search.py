from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from csv import DictWriter

with open('query.csv','w') as f:
    csv_writer = DictWriter(f, fieldnames=['Word','Q','D1','D2','D3','D4','D5'
    ,'D6','D7','D8','D9','D10','D11','D12','D13','D14','D15','D16','D17','D18',
    'D19','D20','D21','D22','D23','D24','D25'])
    csv_writer.writeheader()
    #blom selesai
q = input("Masukkan Pencarian:")

example_sent = "This is a sample sentence, showing off the stop words filtration."

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
    return a, b

dok_asli, dok_hitung = [],[]
dok_asli, dok_hitung = clean_document(example_sent)
q_asli, q_hitung = [],[]
q_asli, q_hitung = clean_document(example_sent)

