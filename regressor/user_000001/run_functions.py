from functions import importData, normalisePlayCount, importNormData, mapPlayCount, numUsers
import sys

datafile = sys.argv[1]

data = importData(datafile)
normalisePlayCount(data)
data = importNormData()
mapPlayCount(data)
numUsers(data)
