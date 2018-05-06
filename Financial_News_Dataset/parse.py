import os
import csv
import string
import unicodedata
import sys
import re
import datetime
import json

tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                      if unicodedata.category(chr(i)).startswith('P'))


path_bloom = ("./20061020_20131126_bloomberg_news/")
path_Reuter = ("./ReutersNews106521/")
output = {}

for root, dirs, files in os.walk(path_bloom):
    for name in files:
        if name == ".DS_Store":
            continue
        fp = open(root+'/'+name, 'r')
        text = ''
        date = ''
        gotDate = False
        for line in fp:
            if line[:4] == '-- 2':
                date = line[3:13]
                gotDate = True
                if date not in output:
                    output[date] = []
                #print(date)
            if line[:2] == '20' and gotDate == False:
                date = line[:10]
                gotDate = True
                if date not in output:
                    output[date] = []
            if line[:3] != '-- ' and gotDate == True:
                text += line
        x = text.replace('\n',' ')
        if x != '':
            #print(root, name)
            output[date].append(x.translate(tbl))
            
            #if date == '2011-03-29':
            #    print(date,":", output[date])
        #print(date)
        #print(date,': ',output[date]) 
        fp.close()
        
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun' ]               
mons = ['Jan','Fed','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
for root, dirs, files in os.walk(path_Reuter):
    for name in files:
        #print(name)
        if name == ".DS_Store":
            continue
        fp = open(root+'/'+name, 'r')
        text = ''
        date = ''
        temp = root[20:]
        date = datetime.datetime.strptime(temp,'%Y%m%d').strftime('%Y-%m-%d')
        if date not in output:
            output[date] = []
        #print(root+'/'+name)
        for line in fp:
            if line[:3] != '-- ':
                text += line
        x = text.replace('\n',' ')
        if x != '':
            #print(root, name)
            output[date].append(x.translate(tbl)) 
            
            #if date == '2011-03-29':
            #    print(date,":", output[date])
        #print(date)
        #print(date,': ',output[date]) 
        fp.close()

news = open('news.txt', 'w')
for key in output:
    for item in output[key]:
        news.write(key+'\n')
        news.write(item+'\n')

news.close()
