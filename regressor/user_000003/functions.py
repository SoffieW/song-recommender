import pandas as pd
import csv
from collections import Counter


# Import lastfm data that was transformed to include playcount aggregated by user,track
def importData(filename):
    	data=pd.read_csv(filename,sep='\t',header=0,usecols=["user_id","track_id","track_name","artist_id","artist_name","playcount"])
	return data


# Import tsv file containing per user play stats including normalised playcount (normalised_pc)
def importNormData():
	data = pd.read_csv('normalised_data.tsv',sep='\t',header=0,usecols=["user_id","track_id","track_name","artist_id","artist_name","playcount","normalised_pc"])
	return data

# Import tsv file containing per user play stats including like column
def importMappedData():
	data = pd.read_csv('mapped_data.tsv',sep='\t',header=0,usecols=["user_id","track_id","track_name","artist_id","artist_name","normalised_pc","like"])
	return data

def importMetaData():
	data = pd.read_csv('meta.tsv',sep='\t',header=0,usecols=["track_id","title","artist_id","artist_name", "country", "album","year","genres"])
	return data
	

'''
Normalise the playcount for every song the specified user has listened to
Adds an extra column "normalised_pc" holding this value
normalised_pc = playcount/totalPlaycount
'''
def normalisePlayCountUser(user, data):
    userData = data.loc[data['user_id'] == user]	
    totalPlayCount = userData['playcount'].sum()
    userData["normalised_pc"] = userData['playcount'].apply(lambda x: float(x)/float(totalPlayCount))
    return userData


def normalisePlayCount(data):
	# Transform data DF so it has extra column 'normalised_pc'
	normalised_data = pd.DataFrame()
	unique_users = data["user_id"].unique()
	for user in unique_users:
		new_df = normalisePlayCountUser(user,data)
		normalised_data = normalised_data.append(new_df)
	# Write out to normalised_data
	normalised_data.to_csv('normalised_data.tsv',sep='\t',index=False)

'''
Assign a value 0 or 1 to each track played by the user
If playcount is above avg then = 1
Otherwise = 0
1 indicates user likes the track a lot, 0 indicates not that bothered.
'''
def mapPlayCountUser(user,data):
	userData = data.loc[data['user_id'] == user]	
	totalPC = userData['playcount'].sum()
	numRows = len(userData)
	avg = float(totalPC)/float(numRows)
   	userData["like"] = userData['playcount'].apply(lambda x: 1 if x>avg else 0)
	return userData


def mapPlayCount(data):
	# Transform data DF so it has extra column 'like'
	mapped_data = pd.DataFrame()
	unique_users = data["user_id"].unique()
	for user in unique_users:
		new_df = mapPlayCountUser(user,data)
		mapped_data = mapped_data.append(new_df)
	# Write out to mapped_data
	print(mapped_data)
	mapped_data.to_csv('mapped_data.tsv',sep='\t',index=False)

def numUsers(data):
	unique_users = data["user_id"].unique()
	print("Number of unique users in dataset is: " + str(len(unique_users)))


# Get user profile data for just those users in data.tsv
def getUsers():
	df = importData('data.tsv') # random subset	
        users = df['user_id'].unique().tolist()
	l = []
	with open ('../../data/users.tsv') as f:
		reader = csv.DictReader(f, delimiter='\t')
		for row in reader:
			if row['user_id'] in users:
				user_id = row['user_id']
				gender = row['gender']
				age = row['age']
				country = row['country']		
				l.append([user_id,gender,age,country])
	cols = ['user_id','gender','age','country']
	user_df = pd.DataFrame(l,columns=cols)
	return user_df


# Return an array of all the unique track IDs
def trackIds(data):
	unique_tracks = data["track_id"].unique()		
	print("There are " + str(len(unique_tracks)) + " unique tracks")
	return unique_tracks


def trackMeta(data,track_id):
	track_name = data.loc[data['track_id'] == track_id,'track_name'].iloc[0]
	artist_name = data.loc[data['track_id'] == track_id,'artist_name'].iloc[0]
	return track_name, artist_name


def faveSongs(data,user,n):
	# Create a DF with data relevant to the specified user
	userPlays = pd.DataFrame(data[data["user_id"]==user],columns=["user_id","track_id","track_name","artist_id","artist_name","playcount","normalised_pc"])
	if userPlays.empty:
		print(user + " does not exist! ")
		return
	# Sort by playcount 
	sortedPlays = userPlays.sort_values(by='normalised_pc',ascending=False)[:n]	
	num = 1
	print (user + " 's top " + str(n) + " favourite tracks:") 
	for index,row in sortedPlays.iterrows():
		track_name, artist_name = trackMeta(userPlays,row['track_id'])
		print (str(num) + " " + track_name + " by " + artist_name)
		num = num+1
	return sortedPlays


def rankSongs(data,user):
	# Create a DF with data relevant to the specified user
	userPlays = pd.DataFrame(data[data["user_id"]==user],columns=["user_id","track_id","track_name","artist_id","artist_name","playcount","normalised_pc"])
	if userPlays.empty:
		print(user + " does not exist! ")
		return
	# Sort by playcount 
	sortedPlays = userPlays.sort_values(by='normalised_pc',ascending=False)	
	'''
	num = 1
	print ("All of " + user + "'s played tracks sorted by pc desc:") 
	for index,row in sortedPlays.iterrows():
		track_name, artist_name = trackMeta(userPlays,row['track_id'])
		print (str(num) + " " + track_name + " by " + artist_name)
		num = num+1
	'''
	return sortedPlays


def mbzMeta(data):
	ids = data["track_id"].unique().tolist()	
	l = []
	# For every track ID, get its metadata
	filename = 'meta.tsv'
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

def genreCount(data):
	genres = data["genres"].tolist()
	genres = [g.replace("[","").replace("]","").replace("'","") for g in genres]
	print(Counter(genres))

