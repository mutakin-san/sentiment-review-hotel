import pandas as pd
# import plotly.express as px


data = pd.read_csv('./eksperimen/dataset_labeled.csv')

# Melihat Nama Kolom
print("Daftar Kolom Yang tersedia")
print(data.columns)
print()

# Menghitung variable kategorik pada kolom sentiments 
print("Jumlah Feature")
print(data.sentiments.value_counts())
print()

# Check Missing Values
print("Data Missing")
print(data.isnull().sum())
print()

# fig = px.histogram(data, x="review", title='Number of review')
# fig.show()


import re
from nltk.tokenize import WordPunctTokenizer

tok = WordPunctTokenizer()
pat1 = r'@[A-Za-z0-9_]+' #menghilangkat username jika twitter
pat2 = r'https?://[^ ]+' #menghilangkan situs website
combined_pat = r'|'.join((pat1, pat2)) #join pat1 dan pat 2
www_pat = r'www.[^ ]+' #menhilangkan situs website


f = open('stopwords_id.txt', "r", newline='')
stopwords = f.readlines()
words = []
for word in stopwords:
    words.append(word.replace('\n', ''))
stopwords_id = set(words)


def proses_teks(teks):
    teks_bersih= re.sub("[^a-zA-Z0-9]", " ",(re.sub(www_pat, '', re.sub(combined_pat, '', teks)).lower()))
    teks_bersih= ' '.join([word for word in teks_bersih.split() if word not in stopwords_id])
    return (" ".join([x for x in tok.tokenize(teks_bersih) if len(x) > 1])).strip()



reviews = []
for teks in data.review:
    reviews.append(proses_teks(teks))

data.review = reviews

print(data.head())
print()


# Memisahkan data train dan data test

from sklearn.model_selection import train_test_split

x = data.review
y = data.sentiments

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.1, random_state=225)

print('Banyak data x_train :', len(x_train))
print('Banyak data x_test :', len(x_test))
print('Banyak data y_train :', len(y_train))
print('Banyak data y_test :', len(y_test))

print()


from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer, HashingVectorizer
cvec = CountVectorizer()
tvec = TfidfVectorizer()
hvec = HashingVectorizer()


from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC


clf1 = RandomForestClassifier()
clf2 = LogisticRegression()
clf3 = BernoulliNB()
clf4 = SVC()

from sklearn.pipeline import Pipeline
model= Pipeline([('vectorizer',tvec)
                 ,('classifier',clf4)])

model.fit(x_train,y_train)
hasil=model.predict(x_test)
print("Hasil Prediksi : ", hasil)


from sklearn.metrics import accuracy_score,confusion_matrix

print("Evaluasi")
print(confusion_matrix(hasil,y_test))
print(accuracy_score(hasil, y_test))
print()




# Menyimpan file model
import pickle
pickle_out = open("sentiment_model.pkl", "wb")
pickle.dump(model, pickle_out)
pickle_out.close()

