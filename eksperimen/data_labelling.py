import os
from textblob import TextBlob
import pandas as pd

path = '../dataset/clean/review-2023-02-07.csv'

result = pd.read_csv(path)

review = result["review"].to_list()

data = {}
data['review'] = review
sentiments = []

test = 1

for dataHasil in review:
    hasilReview = TextBlob(dataHasil)

    test = test+1
    print(test)

    try:
        hasilReview = hasilReview.translate(from_lang="id", to="en")
    except Exception as e:
        print(e)

    if hasilReview.sentiment.polarity > 0.0:
        sentiments.append("positif")
    elif hasilReview.sentiment.polarity == 0.0:
        sentiments.append("netral")
    else:
        sentiments.append("negatif")


    # print(sentiments)

data["sentiments"] = sentiments

df = pd.DataFrame(data)
df.to_csv("./dataset3.csv")