import sys
import os
import numpy as np
import pandas as pd
from collections import OrderedDict
from operator import itemgetter
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.linear_model import RidgeCV
import matplotlib.pyplot as plt
from model_data import importMappedData, mbzMeta

def printUsage():
	print("Usage: python Ridge.py {user_id}")
	
	
try:
	user = sys.argv[1]
except IndexError as err:
	printUsage()
	sys.exit(1)
	
# Check folder exists for this user
found = False
files = os.listdir('../')
for filename in files:
	if user == filename:
		print("Found " + user + "'s data folder.")
		user_folder = '../'+user
		found = True
		break

if(found == False):
	print("No data folder found for this user.")
	sys.exit(1)
	

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# SET UP DATA

# Include the metadata for every song
data = mbzMeta(user,importMappedData(user_folder+'/mapped_data.tsv'))

# Rename country column to 'cntry' - because 'country' is a genre!
data = data.rename(columns={ 'country':'cntry' })

# Clean-up genres column
data['genres'] = data['genres'].apply(lambda x: x.replace("[","").replace("]","").replace("'","") )

# For joining two dataframes use track_id as key
trackids = data.index

# Convert artist_id to numerical
artistids = data["artist_id"].tolist()
artistle = LabelEncoder()
artistle.fit_transform(artistids)
artist_classes = artistle.classes_
encoded_artists = artistle.transform(artistids)
encoded_artists = pd.Series(encoded_artists)

# Convert country to numerical
countries = data["cntry"].tolist()
countryle = LabelEncoder()
countryle.fit_transform(countries)
country_classes = countryle.classes_
encoded_countries = countryle.transform(countries)
encoded_countries = pd.Series(encoded_countries)

# get dates
# Need to deal with YYYY-mm format
# For now just insert as 0 (missing)
yearList = []
years = data["year"].tolist()
for year in years:
	try:
		yearList.append(int(year))	
	except ValueError as err:
		yearList.append(0) 
yearList = pd.Series(yearList)

# Pre-process genres
# Store as elements of list
genres = data["genres"].tolist()
genreList = []
for group in genres:
	genreList.append(group.split(", "))
mlb = MultiLabelBinarizer()
mlb.fit(genreList)

# Number of unique genres
numGenres = len(mlb.classes_)
encoded_genres = mlb.transform(genreList) 

# Existence matrix to show if each genre corresponds to each track or not (0 or 1)
genreDF = pd.DataFrame(encoded_genres,columns = mlb.classes_)
genreDF['track_id'] = trackids
genreDF.set_index('track_id')

data['encoded_artist'] = encoded_artists.values
data['encoded_country'] = encoded_countries.values
data['encoded_year'] = yearList.values
data = data.merge(genreDF, on='track_id')

# Split data into training and testing sets
msk = np.random.rand(len(data)) < 0.8 # Randomise msk for selecting data
#print(msk)
train = data[msk] # Train on 0.8 of data
#print(train)
test = data[~msk] # Test on 0.2 of data

all_genres = mlb.classes_.tolist()
feature_cols = ['encoded_artist','encoded_country','encoded_year'] + all_genres

Xtrain = train[feature_cols]
Ytrain = train["normalised_pc"]

Xtest = test[feature_cols]
Ytest = test["normalised_pc"].tolist()

model = RidgeCV(alphas=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],cv=3)
model.fit(Xtrain,Ytrain)

print(model.alpha_)
print("Feature coefficients:")
coef_dict={}
for coef, feat in zip(model.coef_,feature_cols):
	coef_dict[feat] = coef

for coef in sorted(coef_dict, key=coef_dict.get, reverse=True):
	print coef, coef_dict[coef]

prediction = model.predict(Xtest)

compareDF = pd.DataFrame(columns=["Predicted","Actual"])
compareDF["Predicted"] = pd.Series(prediction)
compareDF["Actual"] = pd.Series(Ytest)

actual = compareDF["Actual"].tolist()
predicted = compareDF["Predicted"].tolist()

print(compareDF)

mae = mean_absolute_error(actual,predicted)
print("Mean absolute error:" + str(mae))

mape = mean_absolute_percentage_error(actual,predicted)
print("Mean absolute percentage error:" + str(mape))

score = model.score(Xtest,Ytest)
print("R2 score: " + str(score))

mse = mean_squared_error(actual,predicted)
print("Mean squared error: " + str(mse))

compareDF.to_csv('../results/Ridge/'+user+'_results.tsv',sep='\t',index=False)

