import matplotlib.pyplot as plt 
import pandas as pd
import sys
from functions import importMappedData, trackMeta, mbzMeta, getUsers
from collections import OrderedDict, Counter
from operator import itemgetter


user = sys.argv[1]
data = importMappedData()
userData = getUsers()
userInfo = userData[userData["user_id"]==user]

gender = ""
age = 0
country = ""

try:
	gender = userInfo['gender'].values[0]
	age = userInfo['age'].values[0]
	country = userInfo['country'].values[0]
except IndexError as err:
	pass

print(user)
print("gender: " + gender)
print("age: " + str(age))
print("country: " + country)

# Create a DF with data relevant to the specified user
userPlays = pd.DataFrame(data[data["user_id"]==user],columns=["user_id","track_id","track_name","artist_id","artist_name","playcount","normalised_pc","like"])
if userPlays.empty:
	print(user + " does not exist! ")
	sys.exit(1)
# Sort by playcount 
sortedPlays = userPlays.sort_values(by='normalised_pc',ascending=False)	
num = 1
print (user + "'s listened to tracks in order of preference desc:") 
for index,row in sortedPlays.iterrows():
	track_name, artist_name = trackMeta(sortedPlays,row['track_id'])
	print (str(num) + " " + track_name + " by " + artist_name)
	num = num+1

print(sortedPlays)

songData = mbzMeta(sortedPlays)

# Clean-up genres column
songData['genres'] = songData['genres'].apply(lambda x: x.replace("[","").replace("]","").replace("'","") )

genres = songData["genres"].tolist()
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

topGenres = dict(od.items()[:10])
		
labels = topGenres.keys()
attribute = topGenres.values()

print(labels)
print(attribute)

# Deal with unicode encoding
labels = [x.decode('utf-8') for x in labels]

frequency = attribute
 
# Generate the y positions. Later, replace them with labels
y_pos = range(len(labels))

# Configure plot settings
plt.title("Frequency of Songs Per Genre (For the Top 10 Genres)")
plt.xlabel("Genre")
plt.ylabel("Number of Songs")
plt.bar(y_pos,frequency)
plt.xticks(y_pos,labels)
plt.xticks(rotation=70)
plt.show()
