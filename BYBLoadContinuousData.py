#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 11:10:20 2018

@author: benrobbins
A module to help convert over continuous data into session objects.
"""
import numpy as np
import os
import wavfile_read

class timestamps:
    """
    A class purely for organisation. This is used by the session class 
    to group together all of the timestamps.
    """
    def __init__(self):
        """
        A instantiation that creates all of the attributes with defult, meaningless values.
        """
        self.events = np.array([])
        self.relax_on = np.array([])
        self.relax_off = np.array([])
        
class EEG:
    def __init__(self):
        """
        A instantiation that creates all of the attributes with defult, meaningless values.
        """
        self.location = np.array([])
        self.time = np.array([])
        self.FS = 0
        self.data = np.array([])

class session:
    """
    Repressents a single session of one of the movement mind reader project.
    """
    def __init__(self):
        """
        A instantiation that creates all of the attributes with defult, meaningless values.
        """
        self.experiment = ''
        self.protocal = 0
        self.subject = 0
        self.EEG = EEG()
        self.timestamps = timestamps()
        self.comment = ''
        self.date = ''
        
        
    def __init__ (self, info):
        """
        An instantion of session with meaningful values. 
        Parameters
        ----------
        Info = a dictionary of almost all the attributs needed.
        """
        self.timestamps = timestamps()
        self.subject = info['subject']
        self.experiment = info["experiment"]
        self.protocal = info['protocal']
        self.date = info['date']
        
        self.filename = info['filename']
        
        self.EEG = EEG()
        self.EEG.data = info['data']
        self.EEG.location = info['locations']
        self.EEG.FS = info['EEGsamplingrate']
        self.EEG.time = info['time']
            
        self.timestamps.events = info['events']
        self.comment = info['comment']
        
def convert_to_session(experiment, subject, protocal, wave, comment = ''):
    """
    Creates a dictionary for creating a session object.
    Parameters
    ----------
    experiment = str of the name of the experiment
    subject = str that represents a subject(i.e. 'S02')
    protocal = str that represents a protocal(i.e. 'P01')
    wave = str that is the directory to a wave file
    comment = str that will be a comment in the session object that will be returned
    Retrurns
    ----------
    session = a session object
    """
    info = {}
    info['experiment'] = experiment
    info['subject'] = subject[-2:]
    info['protocal'] = protocal[-2:]
    info['comment'] = comment
    info['filename'] = wave.split('/')[-1]
    
    info['EEGsamplingrate'],info['data'] = wavfile_read.read(wave)
    
    info['time'] = np.linspace(0, len(info['data']/info['EEGsamplingrate']), len(info['data']))
    
    #Flips dementions
    temp1 = []
    for i in range(len(info['data'][0])):
        temp2= []
        for index in range(len(info['data'])):
            temp2 += [info['data'][index][i]]
        temp1.append(temp2)
    info['data'] = np.array(temp1, dtype = np.int32)
    info['date'] = wave.split('/')[-1].split('_')[2]
    info['locations'] = ['F4-C4','F3-C3','C4-Fz','C3-Fz']
        
    newdir = wave[0:len(wave) - 4] + '-events.txt'
    fin = open(newdir)
    temp = [[],[],[],[],[],[],[], [], [], [], []]
    for i in (fin.readlines()[2:]):
        if ',' in i:
            action, value = tuple(i.split(','))
            value = float(value.strip())
            action = int(action)
            temp[action].append(value)
        info['events'] = temp
        
    return session(info)

def findWAVfiles(dirname, firstCall = 1, experiment = '', protocal = 0, subject = 0):
    """
    findWAVfiles is a function that looks for all wav files in the given 
    file and in all the sub files. 
    Parameter
    ---------
    dirname = str of the directory of the file you want to search
    firstCall = int used internally for recursion. Don't use.
    experiment = str repressenting name of the experiment. Determined
                 internally and passed on through recursion.
    protocal = int repressing the protical. Determined internally. Don't change
    subject = int repressing the subject. Determined internally. Don't change.
    Returns
    ---------
    re = a series of lists, one for each layer the walk delves into.The last 
         list contains a tuple with the dirrectory, experiment, protical, and
         subject in that order.
    """
    re = []
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)
        
        if os.path.isfile(path):
            if '.wav' in path:
                re.append((path, experiment, protocal, subject))
            
        else:
            if firstCall:
                re = findWAVfiles(dirname, firstCall = 0, experiment = dirname.split('/')[-1])
            else:
                if 'P' in path.split('/')[-1].split('.')[0] and len(path.split('/')[-1].split('.')[0]) == 3:
                    re.append(findWAVfiles(path, firstCall = 0, experiment = experiment, protocal = path.split('/')[-1].split('.')[0][1:]))
                else:
                    if 'S' in path.split('/')[-1].split('.')[0] and len(path.split('/')[-1].split('.')[0]) == 3:
                        re.append(findWAVfiles(path, firstCall = 0, experiment = experiment, protocal = protocal, subject = path.split('/')[-1].split('.')[0][1:]))
                    else:
                        re.append(findWAVfiles(path, firstCall = 0, experiment = experiment, protocal = protocal, subject = subject))
    return re

