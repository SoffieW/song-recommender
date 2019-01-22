import matplotlib
matplotlib.use('Agg')
import pylab
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np

colors = ['blue','green','red','yellow','orange','purple','pink']

co = 0

files = os.listdir('.')
files.sort(key=lambda x: os.path.getmtime(x))

fig, ax = plt.subplots()
ax.grid()
ax.set_axisbelow(True)
x = [0,0.007]
y = [0,0.007]
ax.set_xlim(x[0],x[1])
ax.set_ylim(y[0],y[1])
ax.plot(x,y,color='black',linewidth=0.5)
plt.title("Ridge: Actual vs Predicted")
plt.xlabel("Actual Value")
plt.ylabel("Predicted Value")

for filename in files:
	if '.tsv' in filename:
		df = pd.read_csv(filename,sep='\t',header=0,usecols=["Actual","Predicted"])
		user = filename[:11]
		df = df.rename(columns={ 'Predicted' : user })
		print(df.columns)
		ax.scatter(df["Actual"],df[user],color=colors[co],s=10)
		co=co+1

ax.legend(loc="upper left")
pylab.savefig('accuracy.png')
