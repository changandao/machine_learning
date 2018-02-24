#coding = utf-8

import pandas as pd
from bs4 import BeautifulSoup
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression as LR
from sklearn.metrics import roc_auc_score as AUC

#print(stopwords.words('english'))

train = pd.read_csv('labeledTrainData.tsv', header=0, delimiter='\t', quoting=3)
test = pd.read_csv('labeledTestData.tsv', header=0, delimiter='\t', quoting=3)

stops = set(stopwords.words('english'))

def review_prepro(rawstring, remove_stopwords = True):
	sentence = BeautifulSoup(rawstring, 'lxml').get_text()
	pattern = '[^a-zA-Z]'
	letters_only = re.sub(pattern, ' ', sentence)
	lower_case = letters_only.lower()
	words = lower_case.split()
	if remove_stopwords:
		# remove stop words
		meaningful_words = [w for w in words if not w in stops]
		# return concatenated single string
		return ' '.join(meaningful_words)
	else:
		# or don't and concatenate to single string
		return ' '.join(words)
	#words = ''.join(words)
	#return words

def retuneDatalist(origindf):
	datalength = len(origindf)
	clean_reviews = []
	for i in range(datalength):
		newwords = review_prepro(origindf['review'][i])
		clean_reviews.append(newwords)
	return clean_reviews

clean_trian_reviews = retuneDatalist(train)
clean_test_reviews = retuneDatalist(test)

vectorizer = CountVectorizer(analyzer = 'word', tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000)
train_data_features = vectorizer.fit_transform(clean_trian_reviews)
train_data_features = train_data_features.toarray()

test_data_featiures = vectorizer.transform(clean_test_reviews)
test_data_featiures = test_data_featiures.toarray()

model = LR()
model.fit(train_data_features, train['sentiment'])

p = model.predict_proba(test_data_featiures)[:,1]
output = pd.DataFrame(data= {'id': test['id'], 'sentiment': p})

auc = AUC(test['sentiment'].values, p)
print(auc)