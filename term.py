import nltk
#nltk.download('stopwords')
import sklearn
import collections
import csv
from sklearn import cross_validation
from sklearn.svm import LinearSVC, SVC
import random
from nltk.classify import SklearnClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
import json
import os

posdata = []
posfile = open('pos_data.csv','r')
#posfile = open('positive-data.csv','r')
posreader = csv.reader(posfile,delimiter=',')
for word in posreader:
    #print(len(posdata))
    posdata.append(word[0])

negdata = []
negfile = open('neg_data.csv','r')
#negfile = open('negative-data.csv','r')
negreader = csv.reader(negfile,delimiter=',')
for word in negreader:
    #print(len(negdata))
    negdata.append(word[0])

def word_split(data):
    tmp = []
    for word in data:
        word_filter = [i.lower() for i in word.split()]
        tmp.append(word_filter)
    return tmp

def word_split_sentiment(data):
    temp = []
    for( word, sentiment ) in data:
        word_filter = [i.lower() for i in word.split()]
        temp.append((word_filter, sentiment))
    return temp

def wordfeats(words):
    return dict([(word,True) for word in words])

stopset = set(stopwords.words('english'))

def stopword_filtered_word_feats(words):
    return dict([(word, True) for word in words if word not in stopset])

def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    try:bigrams = bigram_finder.nbest(score_fn, n)
    except: bigrams = []
    """
    print words
    for ngram in itertools.chain(words, bigrams):
        if ngram not in stopset:
            print ngram
    exit()
    """
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

def bigram_word_feats_stopwords(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    """
    print words
    for ngram in itertools.chain(words, bigrams):
        if ngram not in stopset:
            print ngram
    exit()
    """
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams) if ngram not in stopset])

# Calculating Precision, Recall & F-measure
def evaluate_classifier(featx):
    
    negfeats = [(featx(f), 'neg') for f in word_split(negdata)]
    posfeats = [(featx(f), 'pos') for f in word_split(posdata)]

    negcutoff = int(len(negfeats)*3/4)
    poscutoff = int(len(posfeats)*3/4)
 
    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    #testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    
    classifierName = 'SVM'
    classifier = SklearnClassifier(LinearSVC(),sparse=False).train(trainfeats)
    
    newsdata  = {}
    '''
    news_path = "./xa/"
    out_ = open('result.txt', 'w')

    for root, dirs, files, in os.walk(news_path):
        for name in files:
            if name == ".DS_Store":
                continue
            fp = open(root+'/'+name, 'r')
            #print(name)
            date = ''
            text = []
            gotDate = False
            #print(root+'/'+name)
            for line in fp:
                if gotDate == False:
                    date = line.replace('\n','')
                    gotDate = True
                    if date not in newsdata:
                        newsdata[date] = [0,0]
                else:
                    if len(line.strip()) == 0:
                        gotDate = False
                        continue
                    text.append(line)
                    #print(text)
                    newsfeat = [(featx(f), date) for f in word_split(text)]
                    del text[:]
                    observed = classifier.classify(newsfeat[0][0])
                    if observed == 'neg':
                        newsdata[date][1] += 1
                        #print('------------------------------ '+ 'neg')
                    else:
                        newsdata[date][0] += 1
                        #print('------------------------------ '+ 'pos')
                        #print(root+'/'+name+': '+ 'pos')

                    gotDate = False
            fp.close()
    for date in newsdata:
        #print(date+': '+str(newsdata[date][0])+', '+str(newsdata[date][1]))
        out_.write(date+'\n'+str(newsdata[date][0])+', '+str(newsdata[date][1])+'\n')
    out_.close() 
    '''
    out_ = open('TEST_result.txt', 'w')

    fp = open('test_half_half.txt', 'r')
    #print(name)
    date = ''
    text = []
    gotDate = False
    #print(root+'/'+name)
    for line in fp:
        if gotDate == False:
            date = line.replace('\n','')
            gotDate = True
            if date not in newsdata:
                newsdata[date] = [0,0]
        else:
            if len(line.strip()) == 0:
                gotDate = False
                continue
            text.append(line)
            print(text)
            newsfeat = [(featx(f), date) for f in word_split(text)]
            del text[:]
            observed = classifier.classify(newsfeat[0][0])
            if observed == 'neg':
                newsdata[date][1] += 1
                print('------------------------------ '+ 'neg')
            else:
                newsdata[date][0] += 1
                print('------------------------------ '+ 'pos')
                #print(root+'/'+name+': '+ 'pos')

            gotDate = False
    fp.close()
    for date in newsdata:
        #print(date+': '+str(newsdata[date][0])+', '+str(newsdata[date][1]))
        out_.write(date+'\n'+str(newsdata[date][0])+', '+str(newsdata[date][1])+'\n')
    out_.close() 

            
#evaluate_classifier(word_feats)
evaluate_classifier(stopword_filtered_word_feats)
#evaluate_classifier(bigram_word_feats)    
#evaluate_classifier(bigram_word_feats_stopwords)


#classifier =
