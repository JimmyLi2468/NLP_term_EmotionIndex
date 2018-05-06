import csv
import string
import unicodedata
import sys
import re

tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                      if unicodedata.category(chr(i)).startswith('P'))

pos = open('pos_review.csv','w+')
neg = open('neg_review.csv','w+')
with open("yelp_review.csv",'r') as f:
    reader = csv.reader(f, delimiter = ',')
    for i,line in enumerate(reader):
        #print(line)
        #line[3]  line[5]
        if line[3] == '5':
            x = line[5].replace('\n',' ')
            #print(re.sub('['+string.punctuation+']','', x))
            pos.write(x.translate(tbl))
            pos.write('\n')
        if line[3] == '1':
            y = line[5].replace('\n',' ')
            #print(re.sub('['+string.punctuation+']','', x))
            neg.write(y.translate(tbl))
            #neg.write(line[5].translate(tbl))
            neg.write('\n')


pos.close()
neg.close()


