from datetime import datetime
import sys
import pandas as pd
import musicbrainzngs 
from musicbrainzngs import WebServiceError

def printUsage():
	print("Usage: python mbzmeta.py {user_id}")


try:
	user = sys.argv[1]
except IndexError as err:
	printUsage()
	sys.exit(1)
	
	
datafile = './'+user+'/'+user+'_data.tsv'

# Tell musicbrainz what your app is, and how to contact you
# (this step is required, as per the webservice access rules
# at http://wiki.musicbrainz.org/XML_Web_Service/Rate_Limiting )
musicbrainzngs.set_useragent("Mood Music Library", "0.1", "cw374@student.le.ac.uk")

# Authentication needed for certain data retrieval functions
musicbrainzngs.auth("smidge","abracadabra")

# Import data from data.tsv
data=pd.read_csv(datafile,sep='\t',header=0,usecols=["user_id","track_id","track_name","artist_id","artist_name","playcount"])

# Get all the unique track IDs in the dataset
unique_tracks = data["track_id"].unique()		

l = []

for track_id in unique_tracks:
	try:
		# Recording specific info
		recording = musicbrainzngs.get_recording_by_id(track_id,includes=["artists","releases","tags"])["recording"]
	except WebServiceError as exc:
		print("Something went wrong with the request: %s" % exc)
	else:
		try:
			title = recording["title"]
			artist_id=recording["artist-credit"][0]['artist']['id']
			artist_name=recording["artist-credit"][0]['artist']['name']
		except KeyError as err:
			print("Info is missing for this song.")
			# Move on to next track
			continue
		except IndexError as err:
			print(err)
			# Move on to next track
			continue

		try:
			release_list = recording["release-list"]
			album = release_list[0]['title']

		except KeyError as err:
			print("Could not get album info")
			album = ""
		except IndexError as err:
			print("Could not get album info")
			album = ""	
		try:
			sorted_releases = sorted(release_list,key=lambda k: k['release-event-list'][0]['date'])
			album = sorted_releases[0]['title']
			date = sorted_releases[0]['release-event-list'][0]['date']
			year=""
			try:
				date = datetime.strptime(date, '%Y-%m-%d')
				year = date.year
				if(1950 <= year < 1960):
					year = "1950s"
				elif (1960 <= year < 1970):
					year = "1960s"
				elif (1970 <= year < 1980):
					year = "1970s"
				elif (1980 <= year < 1990):
					year = "1980s"
				elif (1990 <= year < 2000):
					year = "1990s"
				elif (2000 <= year < 2020):
					year = "2000s"
				else:
					year = ""
			except ValueError as err:
				print("Date is not in YYYY-mm-dd format.")
				if ("195" in date):
					year = "1950s"
				elif ("196" in date):
					year = "1960s"
				elif ("197" in date):
					year = "1970s"
				elif ("198" in date):
					year = "1980s"
				elif ("199" in date):
					year = "1990s"
				elif ("200" in date):
					year = "2000s"
				elif ("201" in date):
					year = "2000s"
				else:
					year = ""
				
		except KeyError as err:
			print("Could not sort releases by date.")
			year = ""
		except IndexError as err:
			print(err)
			year = ""
		try:
			artist = musicbrainzngs.get_artist_by_id(artist_id,includes=["tags"])['artist']
		except WebServiceError as exc:
			print("Something went wrong with the request: %s" % exc)

		try:
			country = artist['country']
		except KeyError as err:
			print("Could not get country")
			country = ""
		
		try:
			song_tags = recording['tag-list']
			song_tags = sorted(song_tags,key=lambda k: k['count'], reverse=True)
		except KeyError as err:
			print("No song tags")
			song_tags = []
		try:
			artist_tags = artist['tag-list']
			artist_tags = sorted(artist_tags,key=lambda k: k['count'], reverse=True)
		except KeyError as err:
			print("No artist tags")
			artist_tags=[]

		try:
			genres = song_tags + artist_tags
			genres = genres[:3]
		except IndexError as err:
			print("There are less than 3 tags in total.")

		try: 
			genres = [d['name'] for d in genres]
		except KeyError as err:
			print("Could not get genres")
			genres=""
		
		l.append([track_id,title,artist_id,artist_name,country,album,year,genres])	
		
cols = ['track_id','title','artist_id','artist_name','country','album','year','genres']

df = pd.DataFrame(l,columns=cols)
df.set_index('track_id')
df.to_csv('./'+user+"/meta.tsv",sep='\t',index=False, encoding='utf-8')
