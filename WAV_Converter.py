#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 16:44:28 2018

@author: benrobbins
"""
from BYBLoadContinuousData import *
import os
import pickle

#Gets the experinment names, direcetories, subjects, and proticals of each wav file
dirs = findWAVfiles(os.getcwd() + '/Human Experiments/Movement Mind Reader')

#Iterate through dirs, converts each tuple into a session, and appends it into a list
sessions = [] 
for i in range(len(dirs)):
    for index in range(len(dirs[i])):
        for tup in range(len(dirs[i][index])):
            if dirs[i][index][tup][2] != '00':
                sessions.append(convert_to_session(dirs[i][index][tup][1], dirs[i][index][tup][3], dirs[i][index][tup][2], dirs[i][index][tup][0], comment = ''))

#P02 
#S02
sessions[5].comment = ("The actual recording began after 01234")
sessions[1].comment = ("The actual recording began after 12305")
sessions[3].comment = ("The actual recording began after 40232(Faulty)")
sessions[4].comment = ("The actual recording began after 40132")
sessions[2].comment = ("The actual recording began after 01234")
sessions[0].comment = ("The actual recording began after 12304")

#P03
#S02
sessions[10].comment = ("The actual recording began after 012345")
sessions[11].comment = ("The actual recording began after 021345")
sessions[6].comment = ("The actual recording began after 031425")
sessions[8].comment = ("The actual recording began after 031425")
sessions[9].comment = ("The actual recording began after 012345")
sessions[7].comment = ("The actual recording began after 031425")

#S03
sessions[16].comment = ("The actual recording began after 012345 (Extra relax in the end)")
sessions[12].comment = ("The actual recording began after 021345")
sessions[13].comment = ("The actual recording began after 031425 (Skipped relax between 0 and 3)")
sessions[15].comment = ("The actual recording began after 031425")
sessions[14].comment = ("The actual recording began after 012345")
sessions[17].comment = ("The actual recording began after 021435")

#S01
sessions[20].comment = ("The actual recording began after 012345") 
sessions[21].comment = ("The actual recording began after 021345")
sessions[23].comment = ("The actual recording began after 031425")
sessions[19].comment = ("The actual recording began after 031425")
sessions[22].comment = ("The actual recording began after 012345")
sessions[18].comment = ("The actual recording began after 031425") 

#P01
#S05
sessions[25].comment = ("The actual recording began after 031425") 
sessions[26].comment = ("The actual recording began after 031425") 
sessions[28].comment = ("The actual recording began after 031425") 
sessions[27].comment = ("The actual recording began after 031425") 
sessions[24].comment = ("The actual recording began after 031425")
  
#S04
sessions[29].comment = ("The actual recording began after 01432") 
sessions[33].comment = ("The actual recording began after 14320") 
sessions[32].comment = ("The actual recording began after 40213") 
sessions[31].comment = ("The actual recording began after 40213") 
sessions[30].comment = ("The actual recording began after 14320") 

#S06
sessions[38].comment = ("The actual recording began after 01432") 
sessions[36].comment = ("The actual recording began after 14320") 
sessions[34].comment = ("The actual recording began after 40123") 
sessions[35].comment = ("The actual recording began after 40213") 
sessions[37].comment = ("The actual recording began after 01432") 
sessions[39].comment = ("The actual recording began after 14320") 

#S07
sessions[41].comment = ("The actual recording began after 01432") 
sessions[45].comment = ("The actual recording began after 14320") 
sessions[44].comment = ("The actual recording began after 40123") 
sessions[42].comment = ("The actual recording began after 40213") 
sessions[43].comment = ("The actual recording began after 01432") 
sessions[40].comment = ("The actual recording began after 14320") 

#Pickles the list of sessions, casts the bytes as a string, and writes it to a file.
db = open('Movement Mind Reader 2018', 'w')
s = str(pickle.dumps(sessions))
db.write(s)
db.close()

x = sessions[0].EEG.data[2]

print('done')