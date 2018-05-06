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

posdata = []
posfile = open('positive-data.csv','r')
posreader = csv.reader(posfile,delimiter=',')
for word in posreader:
    posdata.append(word[0])

negdata = []
negfile = open('negative-data.csv','r')
negreader = csv.reader(negfile,delimiter=',')
for word in negreader:
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
    #print(negcutoff)
 
    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    #print(trainfeats)
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    
    classifierName = 'SVM'
    classifier = SklearnClassifier(LinearSVC(),sparse=False).train(trainfeats)
    #classifier.train(trainfeats)
        
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    #print(testfeats)
    for i, (feats, label) in enumerate(testfeats):
        #print(feats,'---',label)
        refsets[label].add(i)
        observed = classifier.classify(feats)
        #print(observed)
        testsets[observed].add(i)
        #print(testsets)
 
    accuracy = nltk.classify.util.accuracy(classifier, testfeats)
    pos_precision = nltk.precision(refsets['pos'], testsets['pos'])
    pos_recall = nltk.recall(refsets['pos'], testsets['pos'])
    pos_fmeasure = nltk.f_measure(refsets['pos'], testsets['pos'])
    neg_precision = nltk.precision(refsets['neg'], testsets['neg'])
    neg_recall = nltk.recall(refsets['neg'], testsets['neg'])
    neg_fmeasure =  nltk.f_measure(refsets['neg'], testsets['neg'])
    
    print ('')
    print ('---------------------------------------')
    print ('SINGLE FOLD RESULT ' + '(' + classifierName + ')')
    print ('---------------------------------------')
    print ('accuracy:', accuracy)
    print ('precision', (pos_precision + neg_precision) / 2)
    print ('recall', (pos_recall + neg_recall) / 2)
    print ('f-measure', (pos_fmeasure + neg_fmeasure) / 2    )
            
    #classifier.show_most_informative_features()
    
    print ('')
    
    ## CROSS VALIDATION
    
    trainfeats = negfeats + posfeats    
    
    # SHUFFLE TRAIN SET
    # As in cross validation, the test chunk might have only negative or only positive data    
    random.shuffle(trainfeats)    
    n = 5 # 5-fold cross-validation    
    
        
    subset_size = int(len(trainfeats) / n)
    accuracy = []
    pos_precision = []
    pos_recall = []
    neg_precision = []
    neg_recall = []
    pos_fmeasure = []
    neg_fmeasure = []
    cv_count = 1
    for i in range(n):        
        testing_this_round = trainfeats[i*subset_size:][:subset_size]
        training_this_round = trainfeats[:i*subset_size] + trainfeats[(i+1)*subset_size:]
        
        classifierName = 'SVM'
        classifier = SklearnClassifier(LinearSVC(), sparse=False)
        classifier.train(training_this_round)
                
        refsets = collections.defaultdict(set)
        testsets = collections.defaultdict(set)
        for i, (feats, label) in enumerate(testing_this_round):
            refsets[label].add(i)
            observed = classifier.classify(feats)
            testsets[observed].add(i)
        
        cv_accuracy = nltk.classify.util.accuracy(classifier, testing_this_round)
        cv_pos_precision = nltk.precision(refsets['pos'], testsets['pos'])
        cv_pos_recall = nltk.recall(refsets['pos'], testsets['pos'])
        cv_pos_fmeasure = nltk.f_measure(refsets['pos'], testsets['pos'])
        cv_neg_precision = nltk.precision(refsets['neg'], testsets['neg'])
        cv_neg_recall = nltk.recall(refsets['neg'], testsets['neg'])
        cv_neg_fmeasure =  nltk.f_measure(refsets['neg'], testsets['neg'])
                
        accuracy.append(cv_accuracy)
        pos_precision.append(cv_pos_precision)
        pos_recall.append(cv_pos_recall)
        neg_precision.append(cv_neg_precision)
        neg_recall.append(cv_neg_recall)
        pos_fmeasure.append(cv_pos_fmeasure)
        neg_fmeasure.append(cv_neg_fmeasure)
        
        cv_count += 1
            
    print ('---------------------------------------')
    print ('N-FOLD CROSS VALIDATION RESULT ' + '(' + classifierName + ')')
    print ('---------------------------------------')
    print ('accuracy:', sum(accuracy) / n)
    print ('precision', (sum(pos_precision)/n + sum(neg_precision)/n) / 2)
    print ('recall', (sum(pos_recall)/n + sum(neg_recall)/n) / 2)
    print ('f-measure', (sum(pos_fmeasure)/n + sum(neg_fmeasure)/n) / 2)
    print ('')
    
        
#evaluate_classifier(word_feats)
evaluate_classifier(stopword_filtered_word_feats)
#evaluate_classifier(bigram_word_feats)    
#evaluate_classifier(bigram_word_feats_stopwords)


#classifier =
