''' Extract data from data.tsv into a smaller dataset for testing '''
import numpy as np
import pandas as pd
import sys
import os
import csv
import random


def printUsage():
	print("Usage: python extract.py {user_id} {number_of_tracks}")
	
	
# p_tracks: The percentage of tracks to keep
# p_users: The percentage of users to keep
def dropFew(p_tracks, p_users):
	df=pd.read_csv('../data/data.tsv',sep='\t',header=0,usecols=["user_id","track_id","track_name","artist_id","artist_name","playcount"])
	num_rows = df.shape[0]
	print('Number of rows of original:' + str(num_rows))

    # First, drop tracks that haven't been played many times 
    # Group by track_id
	grouped_df = df.groupby(['track_id']).size().reset_index(name='counts')
	# Sort by most commonly occurring tracks desc
	sorted_df = grouped_df.sort_values(by=['counts'],ascending=False)
	num_tracks = sorted_df.shape[0]
	print('Number of unique tracks:' + str(num_tracks))

	# Select N tracks in sorted_df
	N = int(num_tracks*p_tracks)
	print("Number of tracks in subset dataset: " + str(N))
	most_common_tracks = sorted_df['track_id'].iloc[:N]
	smaller_df = df.loc[df['track_id'].isin(most_common_tracks)]

	# Then, drop users that have only played to a few songs

    # Group by user_id
	grouped_df2 = smaller_df.groupby(['user_id']).size().reset_index(name='counts')
    # Sort by most commonly occurring users desc
	sorted_df2 = grouped_df2.sort_values(by=['counts'],ascending=False)
    
	num_users = sorted_df2.shape[0]
	print('Number of unique users:' + str(num_users))

    # Select the first N users in sorted_df
    # Here we specify to select 20% of original number of users 
	N = int(num_users*p_users) 
	print("Number of users in subset dataset: " + str(N))
	most_common_users = sorted_df2['user_id'].iloc[:N]
	even_smaller_df = smaller_df.loc[df['user_id'].isin(most_common_users)]
	os.mkdir('./droppedSubset/')
	even_smaller_df.to_csv('./droppedSubset/data.tsv',sep='\t',index=False)


def randomSubset(nUsers,nTracks):
	df=pd.read_csv('../data/data.tsv',sep='\t',header=0,usecols=["user_id","track_id","track_name","artist_id","artist_name","playcount"])
	num_rows = df.shape[0]	
	print('Number of rows of original:' + str(num_rows))

    # Keep only the specified number nUsers of users
	allUsers = df['user_id'].unique().tolist()
	numUsers = str(len(allUsers))
	print("Number of users is " + numUsers)

	removeNusers = int(numUsers) - int(nUsers)

	for x in xrange(removeNusers):
		randomUser = random.choice(allUsers)
		allUsers.remove(randomUser)
	
	print("The " + str(len(allUsers)) + " users that have been selected:")
	print(allUsers)
    
    # Contains only the rows corresponding to users in the subset list
	df = df.loc[df['user_id'].isin(allUsers)] 

    # Now reduce number of tracks in dataset to nTracks
	allTracks = df['track_id'].unique().tolist()
	numTracks = str(len(allTracks))  
	print("Total number of tracks for the selected " + str(nUsers) + " users: " + numTracks)
    
	removeNtracks = int(numTracks)-int(nTracks)

	for x in xrange(removeNtracks):
		randomTrack = random.choice(allTracks)
		allTracks.remove(randomTrack)

	print("The " + str(len(allTracks)) + " tracks that have been selected:")
	print(allTracks)

	df = df.loc[df['track_id'].isin(allTracks)]

	print(df.head())
	os.mkdir('./randomSubset/')
	df.to_csv('./randomSubset/data.tsv',sep='\t',index=False)


# Get data for one user to be used in classification using song features
# user : the user id of user to collect data
# nSongs : number of songs to keep (get the top n songs for this user)
def userSubset(user, nSongs):
	df=pd.read_csv('../data/data.tsv',sep='\t',header=0,usecols=["user_id","track_id","track_name","artist_id","artist_name","playcount"])
	userData = df.loc[df['user_id'] == user].sort_values(by=['playcount'],ascending=False)[:nSongs]
	os.mkdir('./'+user)
	userData.to_csv('./'+user+'/'+user+'_data.tsv',sep='\t',index=False)
	return userData
	
	
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
#	normalised_data.to_csv('normalised_data.tsv',sep='\t',index=False)
	
	
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
#	mapped_data.to_csv('mapped_data.tsv',sep='\t',index=False)

'''
Creates a new directory for the user specified
and generates mapped_data.tsv for this user
adding columns normalised_pc and like
'''
try:
	user = sys.argv[1]
	numTracks = int(sys.argv[2])
except IndexError as err:
	printUsage()
	sys.exit(1)
	

userData = userSubset(user,numTracks)
normalisedUserData = normalisePlayCountUser(user,userData)
mappedUserData = mapPlayCountUser(user,normalisedUserData)
mappedUserData.to_csv('./'+user+'/mapped_data.tsv',sep='\t',index=False)
