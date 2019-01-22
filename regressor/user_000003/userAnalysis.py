import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd

filename = '../data/users.tsv'

data=pd.read_csv(filename,sep='\t',header=0,usecols=["user_id","gender","age","country"])

### AGE DEMOGRAPHIC ###
def age(data):
	allAges = data["age"].tolist()
	allAges = [x for x in allAges if str(x) != 'nan']

	# Female ages
	fAges = data.loc[data['gender']=='f','age'].tolist()
	fAges = [x for x in fAges if str(x) != 'nan']

	# Male ages
	mAges = data.loc[data['gender']=='m','age'].tolist()
	mAges = [x for x in mAges if str(x) != 'nan']

	plotThis = [allAges,fAges,mAges]

	fig,ax = plt.subplots()
	ax.boxplot(plotThis)
	ax.set_xticklabels(["All","Female","Male"])
	ax.set_title('Age Demographic')
	plt.show()

### GENDER ###
def gender(data):
	counts = data['gender'].value_counts(dropna=False)
	print(counts)
	labels = ["Male","Female","Unspecified"]
	fig,ax = plt.subplots()
	ax.pie(counts,labels=labels,autopct="%1.1f%%")
	ax.set_title('Gender Demographic')
	plt.show()	

### COUNTRY ###
def country(data):
	counts = data['country'].value_counts(dropna=False)
	greater = counts[counts >= 10]
	less = counts[counts<10]
	less = less.sum()	
	less = pd.Series(less,index=['Other'])
	counts = pd.concat([greater,less])
	counts = counts.sort_values(ascending=False)
	print(counts)
	labels = counts.index
	labels = ["Unspecified" if str(x)=='nan' else x for x in labels]
	fig,ax = plt.subplots()
	y_pos = np.arange(len(labels))
	ax.barh(y_pos, counts.values,align='center',color='yellow')
	ax.set_yticks(y_pos)
	ax.set_yticklabels(labels)
	
	# Set percentage labels
	totals = []
	for i in ax.patches:
		totals.append(i.get_width())
	total = sum(totals)
	for i in ax.patches:
		ax.text(i.get_width()+.3, i.get_y()+.38, \
			str(round((i.get_width()/total)*100,2))+'%',fontsize=10)
	ax.invert_yaxis()
	ax.set_xlabel('Number of Users')
	ax.set_ylabel('Country')
	ax.set_title('Proportions of Registered Users per Country')
	plt.gcf().subplots_adjust(left=0.25)
	plt.show()	

age(data)
