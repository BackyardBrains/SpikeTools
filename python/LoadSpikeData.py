#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 13:50:41 2018

@author: benrobbins

This is a module created for converting a specific set of JSON files into
eperiment objects for easy access and high workability.
"""

import pandas as pd
import json
import os
import numpy as np

class timestamps:
    def __init__(self):
        """
        A class purely for organisation. This is used by the session class 
        to group together all of the timestamps.
        """
        
        self.allSpike = []
        self.spike = []
        self.impact = []
        self.angleValues = []
        self.angleTimestamps = []
        
        self.impactS06 = []
        self.impactS08 = []
        self.impactV02 = []
        self.impactV04 = []
        self.impactV06 = []
        self.impactV08 = []
        self.impactV10 = []
        
        self.impactS06V02 = []
        self.impactS06V04 = []
        self.impactS06V06 = []
        self.impactS06V08 = []
        self.impactS06V10 = []
        
        self.impactS08V02 = []
        self.impactS08V04 = []
        self.impactS08V06 = []
        self.impactS08V08 = []
        self.impactS08V10 = []

class session:
    """
    This is ment to repressent each experimental session (JSON file). A  
    collection of sessions is an experiment. A session consists of multiple 
    trials.  This class provides two instantiation functions, one creates 
    default values and one that takes in a JSON object and uses it to fill
    class attributes.
    """
    def __init__(self):
        self.jsonVersion = 1
        self.session = ''
        self.timstamps = timestamps()
        self.subject = ''
        self.sampleRate = 1
        self.comment = ''
        self.velocities = []
        self.distance = 1
        self.sizes = []
        self.timestamps.spike = []
        self.timestamps.impact = []
        self.timestamps.angleValues = []
        self.timestamps.angleTimestamps = []
        self.trials = []
        self.targetColor = ''
       
        
        

    def __init__(self, j):
        try:
            self.jsonVersion = int(j['jsonversion'])
        except:   
            self.jsonVersion = 1
            
        self.timestamps = timestamps()
        self.session = j["name"]
        self.subject = self.session[0:3]
        self.sampleRate = 44100
        self.comment = j["comment"]
        self.velocities = j['velocities']
        self.distance = j['distance']
        self.sizes = j['sizes']
        
        targetVelocities = []
        targetSizes = []
        
        self.trials = []
        if self.jsonVersion == 3:
            self.targetColor = j['color']
        elif self.jsonVersion > 3:
            self.targetColor = {}
            
        for iTrial in range(len(j['trials'])):
            s = trial(j['trials'][iTrial])
            self.timestamps.spike.append([i + 45000 * iTrial for i in j['trials'][iTrial]
                                          ['spikeTimestamps']])
            tempAngles = [180/ np.pi * i for i in (j['trials'][iTrial]['angles'])]
            tempAngleTimestamps = (pd.Series(j['trials'][iTrial]['timestamps']) 
                                       - j['trials'][iTrial]['timeOfImpact']).tolist()
            if self.jsonVersion == 1:
                tempAngles = []
                for i in range(len(tempAngleTimestamps)):
                    if tempAngleTimestamps[i] > 0:
                        tempAngles.append(tempAngleTimestamps[i] * 2)    
            tempAngleTimestamps = (pd.Series(j['trials'][iTrial]['timestamps']) + iTrial * 45000).tolist()
            self.timestamps.angleValues.append(tempAngles)
            self.timestamps.angleTimestamps.append(tempAngleTimestamps)
            self.timestamps.impact.append((pd.Series(j['trials'][iTrial]['timeOfImpact']) + iTrial * 45000).tolist()[0])
            
            targetVelocities.append(j['trials'][iTrial]['velocity'])
            targetSizes.append(j['trials'][iTrial]['size'])
            
            self.trials.append(s)
            
        self.timestamps.allSpike = []
        if self.jsonVersion >= 5:
            self.timestamps.allSpike = j["allSpikeTimestamps"]
        
        targetSizes = np.array(targetSizes)
        targetVelocities = np.array(targetVelocities)

        self.timestamps.impactS06 = [self.timestamps.impact[i] for i in np.where(targetSizes == .06)[0].tolist()]
        self.timestamps.impactS08 = [self.timestamps.impact[i] for i in np.where(targetSizes == .08)[0].tolist()]
        self.timestamps.impactV02 = [self.timestamps.impact[i] for i in np.where(targetVelocities == -2)[0].tolist()]
        self.timestamps.impactV04 = [self.timestamps.impact[i] for i in np.where(targetVelocities == -4)[0].tolist()]
        self.timestamps.impactV06 = [self.timestamps.impact[i] for i in np.where(targetVelocities == -6)[0].tolist()]
        self.timestamps.impactV08 = [self.timestamps.impact[i] for i in np.where(targetVelocities == -8)[0].tolist()]
        self.timestamps.impactV10 = [self.timestamps.impact[i] for i in np.where(targetVelocities == -10)[0].tolist()]

        self.timestamps.impactS06.sort()
        self.timestamps.impactS08.sort()
        self.timestamps.impactV02.sort()
        self.timestamps.impactV04.sort()
        self.timestamps.impactV06.sort()
        self.timestamps.impactV08.sort()
        self.timestamps.impactV10.sort()
        
        self.timestamps.impactS06V02 = intersectEventTimes(self.timestamps.impactS06 , self.timestamps.impactV02)
        self.timestamps.impactS06V04 = intersectEventTimes(self.timestamps.impactS06 , self.timestamps.impactV04)
        self.timestamps.impactS06V06 = intersectEventTimes(self.timestamps.impactS06 , self.timestamps.impactV06)
        self.timestamps.impactS06V08 = intersectEventTimes(self.timestamps.impactS06 , self.timestamps.impactV08)
        self.timestamps.impactS06V10 = intersectEventTimes(self.timestamps.impactS06 , self.timestamps.impactV10)
        
        self.timestamps.impactS08V02 = intersectEventTimes(self.timestamps.impactS08 , self.timestamps.impactV02)
        self.timestamps.impactS08V04 = intersectEventTimes(self.timestamps.impactS08 , self.timestamps.impactV04)
        self.timestamps.impactS08V06 = intersectEventTimes(self.timestamps.impactS08 , self.timestamps.impactV06)
        self.timestamps.impactS08V08 = intersectEventTimes(self.timestamps.impactS08 , self.timestamps.impactV08)
        self.timestamps.impactS08V10 = intersectEventTimes(self.timestamps.impactS08 , self.timestamps.impactV10)
        
       
class trial:
    """
    Represents a single trial in the experiment's attribute 'trials'. It takes
    in one element from the list of trials in a JSON object and instantiates 
    its attributes based on said element. It is also contains no methodes other
    than __init__, but rather is used just for organisation.
    """
    def __init__ (self, trial):
        self.targetColor = '000000'
        self.angles = trial['angles']
        self.distance = trial['distance']
        self.timestamps = trial['timestamps']
        self.timeOfImpact = trial['timeOfImpact']
        self.spikeTimestamps = trial['spikeTimestamps']
        self.targetSize = trial['size']
        self.targetVelocity = trial['velocity']
        self.filename = trial['filename']
        
def convert_JSON_to_python(direct):
    """
    A simple funtion that takes in a string that is a directory to a JSON file
    and returns a JSON object. It makes use of the json module to accomplish
    this.
    """
    fin = open(direct, 'r')
    result = json.loads(fin.read())
    return session(result)
    

def findJSONfiles(dirname):
    """
    findJSONfiles is a function that looks for all json files in the given 
    files and in all the sub files. It takes in a string that is a directory of
    a file. It returns a list of directories of the json files with some 
    elements being blank lists that will later have to be removed.
    """
    re = []
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)
        
        if os.path.isfile(path):
            if '.json' in path:
                return path
            
        else:
            re.append(findJSONfiles(path))
    return re
    
class sessions(list):
    """
    A list of sessions that compose an experiment. 
    """
    def sortby(self,sortType):
        """
        Sorts the selected result by sortType and returns a new sorted 
        sessions object.
        """
        if sortType == 'session':    
            self.sort(key = lambda x: x.session)
        elif sortType == 'jsonVersion':    
            self.sort(key = lambda x: x.jsonVersion)
        elif sortType == 'velocities':    
            self.sort(key = lambda x: x.velocities)
        elif sortType == 'distances':    
            self.sort(key = lambda x: x.distances)
            
    def select(self , selectQuery, selectParam):
        """
        Select allows you to choose a subset of sessions from an
        experiment based on the following selectQuery:
            session = Session Name
            subject = Subject Name
            jsonVersion = Version of data collected
            velocities = List of all velocities in session
            distance = Distance
        """
        re = []
        if selectQuery == 'subject':
            for i in self:
                if i.subject == selectParam:
                    re.append(i)
        elif selectQuery == 'session':    
            for i in self:
                if i.session == selectParam:
                    re.append(i)
        elif selectQuery == 'jsonVersion':    
            for i in self:
                if i.jsonVersion == selectParam:
                    re.append(i)
        elif selectQuery == 'velocities':    
            for i in self:
                if i.velocities == selectParam:
                    re.append(i)
        elif selectQuery == 'distance':    
            for i in self:
                if i.distance == selectParam:
                    re.append(i)
                    
        return re  


def intersectEventTimes(list1, list2):
    """
    Parameters
    ----------
    list1: A list floats.
    list2: A list floats.
    
    Returns
    -------
    newList: A list of the floats the lists have in common.
    """
    newList = []
    for i in list1:
        for n in list2:
            if abs(i - n) < .000001:
                newList.append(i)
    return newList
                