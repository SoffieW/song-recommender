''' Extract data from data.tsv into a smaller dataset for testing '''
import numpy as np
import pandas as pd
import sys
import csv
import random
from functions import importData

# p_tracks: The percentage of tracks to keep
# p_users: The percentage of users to keep
def dropFew(p_tracks, p_users):
    df = importData('../../data/data.tsv')
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
    even_smaller_df.to_csv('data.tsv',sep='\t',index=False)


def randomSubset(nUsers,nTracks):
    df = importData('../../data/data.tsv')
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
    df.to_csv('data.tsv',sep='\t',index=False)


# Get data for one user to be used in classification using song features
# user : the user id of user to collect data
# nSongs : number of songs to keep (get the top n songs for this user)
def userSubset(user, nSongs):
    df = importData('../../data/data.tsv')
    userData = df.loc[df['user_id'] == user].sort_values(by=['playcount'],ascending=False)[:nSongs]
    userData.to_csv(user+'_data.tsv',sep='\t',index=False)

user = sys.argv[1]
userSubset(user,500)
