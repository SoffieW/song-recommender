import pandas as pd
import csv
from collections import Counter


# Import tsv file containing per user play stats including like column
def importMappedData(filename):
	data = pd.read_csv(filename,sep='\t',header=0,usecols=["user_id","track_id","track_name","artist_id","artist_name","normalised_pc","like"])
	return data


def mbzMeta(filename,data):
	print("FNAME:"+filename)
	ids = data["track_id"].unique().tolist()	
	l = []
	with open (filename) as f:
		reader = csv.DictReader(f, delimiter='\t')
		for row in reader:
			if row['track_id'] in ids:
				track_id = row['track_id']
				title = row['title']
				artist_id = row['artist_id']
				artist_name = row['artist_name']
				country = row['country']
				album = row['album']
				year = row['year']
				genres = row['genres']	
				normalised_pc = data.loc[data['track_id']==track_id,'normalised_pc'].iloc[0]
				like = data.loc[data['track_id']==track_id,'like'].iloc[0]
				l.append([track_id,title,artist_id,artist_name,country,album,year,genres,normalised_pc,like])

	cols = ['track_id','title','artist_id','artist_name','country','album','year','genres','normalised_pc','like']
	df = pd.DataFrame(l,columns=cols)
	# sort by playcount desc
	df = df.sort_values(by='normalised_pc',ascending=False)	
	df = df.drop_duplicates(subset='track_id',keep='first')
	df = df.set_index('track_id')
	return df
