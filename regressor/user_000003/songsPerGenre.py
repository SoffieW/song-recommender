from collections import OrderedDict, Counter
from operator import itemgetter
from functions import importMappedData, mbzMeta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re


# Set up data
allData = importMappedData()
# Get metadata for every song
data = mbzMeta(allData)

# Clean-up genres column
data['genres'] = data['genres'].apply(lambda x: x.replace("[","").replace("]","").replace("'","") )

genres = data["genres"].tolist()
genreList = []
for group in genres:
	genreList.append(group.split(", "))

d = {}
for item in genreList:
	for genre in item:
		if genre in d:
			d[genre] = d[genre] + 1
		else:
			d[genre] = 1

try:
	del d['']
except KeyError:
	pass

od = OrderedDict(sorted(d.items(), key=itemgetter(1), reverse=True))

topGenres = OrderedDict(od.items()[:10])
		
labels = topGenres.keys()
attribute = topGenres.values()

print(labels)
print(attribute)

# Deal with unicode encoding
labels = [x.decode('utf-8').replace('/','/\n') for x in labels]

# So the labels fit within display legend
def formatLabel(l):
	if len(l) > 10:
		l = l.split()
		if len(l) == 4:
			l = l[0] + ' ' + l[1] + '\n' + l[2] + ' '+ l[3]
		if len(l) == 3:
			l = l[0] + '\n' + l[1] + ' ' + l[2] 
		if len(l) == 2:
			l = l[0] + '\n' + l[1] 
	return l

#labels = [formatLabel(l) for l in labels]

frequency = attribute
 
fig,ax = plt.subplots()
y_pos = np.arange(len(labels))
ax.barh(y_pos, frequency,align='center',color='purple')
ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_xlabel('Number of Songs')
ax.set_ylabel('Genre')
ax.set_title("Songs Per Genre")
plt.gcf().subplots_adjust(left=0.25)
plt.show()	

'''
# Configure plot settings
plt.xlabel("Genre")
plt.ylabel("Number of Songs")
plt.bar(y_pos,frequency)
plt.xticks(y_pos,labels)
plt.xticks(rotation=70)
plt.gcf().subplots_adjust(bottom=0.25)
plt.show()
'''
