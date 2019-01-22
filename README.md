# song-recommender
Scripts for final year university project using machine learning to recommend songs to users.

Python versions 2.7 and up can be used for running the scripts. 

## python dependencies
* numpy
* pandas
* sklearn
* matplotlib (for Python versions < 3.0, install matplotlib version < 3.0)
* tkinter
* musicbrainzngs 

## data
**data.tsv** contains the listening history of 100 users. The data consists of:
* user_id - e.g. "user_000001"
* track_id - musicbrainz track id. This id can be used to retrieve metadata about the song from musicbrainz database
* track_name
* artist_id - musicbrainz artist id. This id can be used to retrieve metadata about the artist from musicbrainz
* artist_name
* playcount - number of times the songs has been played by this user
* last_played - last datetime this song was played by user *(not currently used in ML for this project)*

### Users
There are 3 users extracted from the above dataset to try and build ML models for - user_000001, user_000002 and user_000003.  
If you want to try a different user from the dataset, please do the following:  
* Make a copy of one of the existing user's directory and name it the user_id of the user you wish to extract. Note this user must be in 'data.tsv'. 
* If there are any .tsv files in the new directory, remove them by running rm *.tsv
* run python extract.py [user_id] e.g. if your user is user_000004 you would run python extract.py user_000004. This generates a .tsv file with only data for that user e.g. user_000004_data.tsv and 500 of their top tracks. If you'd like to increase/decrease number of tracks, you can do so in the script file but if there are too many tracks, it'll take too long to retrieve metadata (in a later step)
* now run: python run_functions.py [user_id]_data.tsv 
* This performs operations on the user data file to generate normalised play count
* Run python mbzmeta.py [user_id]_data.tsv   
* This gets the metadata for each song from the musicbrainz database *Note: musicbrainzngs package needs to be installed for this*
* For 500 songs, this takes approximately 15 minutes.

