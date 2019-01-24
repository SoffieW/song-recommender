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

## Users
There are 3 users extracted from the above dataset to try and build ML models for - user_000001, user_000002 and user_000003.  
If you want to try a different user from the dataset, please do the following:  
* run ```python extract.py {user_id} {number_of_songs}```
* where user_id is the user id of the user you wish to extract (must be in data/data.tsv)
* and number_of_songs is the max number of songs to keep (these are the user's top songs)
* A directory will be created for the user, with the user_id being the name of the new directory. In there you will now find 'mapped_data.tsv'

## Analysis
The 3 analysis scripts are:
* songsPerCountry.py
* songsPerGenre.py
* songsPerYear.py

You can run them from the regressor/ directory e.g.
```python songsPerCountry.py user_000001``` will run the script for user_000001    

## Machine Learning Scripts
The three algorithms being investigated are Ridge Regressor, Decision Tree Regressor and Nearest Neighbours Regressor.   

The scripts for the ML models are in regressor/models   

To run the Ridge Regressor script:    
```python Ridge.py {user_id}``` 
The feature coefficients are printed in descending order 

To run Decision Tree Regressor script:  
```python DTR.py {user_id}```  
The feature importances are printed in descending order

To run K Nearest Neighbours script:   
```python KNN.py {user_id}```  

Please ensure you run the scripts within the 'models' directory.   

Running each script builds a model using the specified algorithm from the sklearn library. Cross validation is performed and the estimator with the best parameters is selected as the optimal model; this is then used on the test set to produce predictions which are evaluated using R2, MAE, MSE statistical tests.   

A .tsv file will be generated in results/[algorithm_name]/ directory for the user, which contains Actual and Predicted run times.  

In the 'results' directory, run ```python accuracy_scatter.py {algorithm_name}``` to generate a .png to display results of actual vs predicted values for that algorithm. The graph generated shows all the user's results and will be in the directory for that model in 'results'. 



