"""
Created on Thu May  3 16:35:45 2018

@author: benrobbins

This code reads in a series of json files, converts them into session
objects, appends them to sessions, pickles sessions, conerts those bytes
to a string and then writes it into a text file. It also reads in the text file
and prints out the name of the first eperiment to test it.
"""

from BYBLoadGrasshopperData import *
import os
import pickle

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Finds all the directories of all the JSON files in the given file and puts 
# them all in a list. This may contain some blank lists.
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
dirs = findJSONfiles(os.getcwd() + "/Publications-master/2016 Nguyen et al - "
                     + "Grasshopper DCMD/data")


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Filters out any blank lists that come from files without a json file.
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
for index in range(len(dirs)):
    if index >= len(dirs):
        pass
    elif type(dirs[index]) != str:
        dirs.pop(index)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Itterates through all of the directories, converts the files into 
# sessions, adds the attribute number to each one, and adds them into a 
# newly created sessions object.
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
iCounter = 1
sessions = sessions()
for i in dirs:
    expElement = convert_JSON_to_python(i)
    expElement.number = iCounter
    sessions.append(expElement)
    iCounter += 1

    
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Pickles the sessions object, casts the bytes to a string, and writes it 
# into a new file '2016 Nguyen et al - Grasshopper DCMD'
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
db = open('2016 Nguyen et al - Grasshopper DCMD', 'w')
s = str(pickle.dumps(sessions))
db.write(s)
db.close()

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Tests to makes sure everything worked by reading in the string, converting it
# to bytes throught the use of eval, unpickling those bytes and printing out the
# first sessions name.
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
db = open('2016 Nguyen et al - Grasshopper DCMD', 'r')
x = db.read()
l = pickle.loads(eval(x))
print(l[0].session)
