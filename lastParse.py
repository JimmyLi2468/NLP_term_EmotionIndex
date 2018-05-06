import collections

fp = open("result.txt", 'r')
norm = {}
#output = collections.OrderedDict(sorted(d.items()))
ifdate = False
date = ''
for line in fp:
    if ifdate == False:
        date = line.strip('\n')
        if date not in norm:
            norm[date] = 0.0
        ifdate = True
        print(date)
    else:
        pos = int(line.split(',')[0])
        neg = int(line.split(',')[1])
        total = pos+neg
        norm[date] = pos/total*18.75 - neg/total*2.5
        print(norm[date])
        ifdate = False

output = collections.OrderedDict(sorted(norm.items()))
fd = open("final.txt", 'w')
pre = 1350
for k, v in output.items():
    pre += v
    fd.write(k+'\t'+str(pre)+'\n')
