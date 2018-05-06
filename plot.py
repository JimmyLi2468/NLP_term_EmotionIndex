import datetime
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#f1 = open("final10.txt", 'r')
#f1 = open("final20.txt", 'r')
#f1 = open("final30.txt", 'r')
#f1 = open("final35.txt", 'r')
#f1 = open("final40.txt", 'r')
#f1 = open("final45.txt", 'r')
#f1 = open("final50.txt", 'r')
#f1 = open("final55.txt", 'r')
f1 = open("final.txt", 'r')
dates = []
values = []
for line in f1:
    if line[4] == '-' and line[7] == '-':
        if line[0:4] == '2013' or line[0:4] == '2014':
            continue
        dates.append(line.split()[0])
        values.append(float(line.split()[1]))
x = [datetime.strptime(d,'%Y-%m-%d').date() for d in dates]

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.plot(x,values)
#plt.gcf().autofmt_xdate()
plt.show()


    
