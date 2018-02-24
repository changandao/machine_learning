#import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression as LR

from sklearn.metrics import roc_auc_score as AUC

#%% download nltk stopwords
# import nltk
# ntlk.download('stopwords')

# load stopwords
stops = set(stopwords.words('english'))

# function for preprocessing the data
def review_prepro(data, remove_stopwords=False):
    # remove HTML tags
    review_text = BeautifulSoup(data, 'lxml').get_text()
    # remove non-letters and numbers
    letters_only = re.sub( '[^a-zA-Z]',
                          ' ',
                          review_text )
    # make all characters lower case and split the documents into single wirds
    words = letters_only.lower().split()
    
    if remove_stopwords:
        # remove stop words
        meaningful_words = [ w for w in words if not w in stops ]
        # return concatenated single string
        return ' '.join(meaningful_words)
    else:
        # or don't and concatenate to single string
        return ' '.join(words)

# load data as pandas dataframe
train = pd.read_csv('labeledTrainData.tsv', 
                    header=0,
                    delimiter="\t", 
                    quoting=3 )

test = pd.read_csv('labeledTestData.tsv', 
                   header=0,
                   delimiter="\t",
                   quoting=3 )

print('Cleaning reviews. This may take some time...')
print('You can also import the cleaned data (see code line 85)')


# preprocess train and test data
num_reviews = train['review'].size

clean_train_reviews = []
for i in xrange(num_reviews):
    if (i+1)%1000 == 0:
        print('Review {} of {}\n'.format(i+1, num_reviews))
    clean_train_reviews.append(review_prepro(train['review'][i]))
    
num_test_reviews = test['review'].size

clean_test_reviews = []
for i in xrange(num_test_reviews):
    if (i+1)%1000 == 0:
        print('Review {} of {}\n'.format(i+1, num_test_reviews))
    clean_test_reviews.append(review_prepro(test['review'][i]))
    
#%% export data using pickle
export = False
if export:
    print('Saving cleaned data...')
    import pickle
    
    with open('clean_train', 'wb') as fp:
        pickle.dump(clean_train_reviews, fp)
        
    with open('clean_test', 'wb') as fp:
        pickle.dump(clean_test_reviews, fp)

# load 
load = False
if load:
    print('Loading cleaned data...')
    import pickle
    with open ('clean_train', 'rb') as fp:
        clean_train_reviews = pickle.load(fp)
    with open ('clean_test', 'rb') as fp:
        clean_test_reviews = pickle.load(fp)
    

#%% create BoW
# Documentation:
# http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
vectorizer = CountVectorizer(analyzer = 'word',
                             tokenizer = None,
                             preprocessor = None,
                             stop_words = stops,
                             max_features = 5000)

# fit the vectorizer and return transformed reviews
vectorizer.fit(clean_train_reviews)
train_data_features = vectorizer.transform(clean_train_reviews)
# convert to numpy array
train_data_features = train_data_features.toarray()

#%% build logistic regression classifier
# Documentation:
# http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
# initiate classifier
model = LR()
# fit classifier to training data
model.fit( train_data_features, train['sentiment'] )

# create BoW representation of test data
test_data_features = vectorizer.transform(clean_test_reviews)
test_data_features = test_data_features.toarray()

# predict test labels
# column 1 of p: probability that class is 1
p = model.predict_proba( test_data_features )

# compute and print AUC score
auc = AUC( test['sentiment'].values, p[:,1] )

print('AUC using LR: {}'.format(auc))

#%%
# initialize TF-IDF vectorizer
# Documentation:
# http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
tfidfvectorizer = TfidfVectorizer( analyzer = 'word',
                                  tokenizer = None,
                                  preprocessor = None,
                                  stop_words = None,
                                  max_features = 5000,     # more features = better accuracy
                                  ngram_range = ( 1, 1 ),  # tri (1, 2) for bigrams
                                  sublinear_tf = True )    # sublinear term frequency 1 + log(tf)

# fit and transform
tfidf_train_x = tfidfvectorizer.fit_transform( clean_train_reviews )
tfidf_test_x = tfidfvectorizer.transform( clean_test_reviews )

# train LR classifier using TF-IDF features
model_tfidf = LR()
model_tfidf.fit( tfidf_train_x, train['sentiment'] )

p_tfidf = model_tfidf.predict_proba(tfidf_test_x)

# compute and print AUC score
auc_tfidf = AUC(test['sentiment'].values, p_tfidf[:,1])
print('AUC using LR and TFIDF: {}'.format(auc_tfidf))

#%% bonus: show ROC (receiver operator characteristic) AUC curve
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

fpr, tpr, thresholds = roc_curve(test['sentiment'].values, p_tfidf[:,1])

plt.figure()
lw = 2
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % auc_tfidf)
plt.axis('scaled')
plt.plot([0, 1], [0, 1], color='navy', lw=1, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()
