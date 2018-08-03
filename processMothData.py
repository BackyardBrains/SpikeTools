#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 09:56:15 2018

@author: benrobbins
"""
import wavfile_read
import matplotlib.pyplot as plt
import csv
import numpy as np

class stimulus:
    """
    Organisational class that will be filled in processMothData.
    """
    def __init__(self, name, iD):
        self.name = name
        self.id = iD
        self.rawSignal = []
        self.timestamps = []
        self.peak = []
        self.baseline = []
        self.lightBaseline = []
        
class recording:
    """
    Organisational class that will be filled in recordings.
    """
    def __init__(self):
        self.mins = []
        self.session = []
        self.metadata = {}
        self.aveMin = []
        self.std = []
    

def processMothData (nameOfFile):
    """
    Converts the directory of a .wav file, with the .txt file in the same folder 
    with the the same directory except the for there is a -events.txt insted of 
    .wav at the end, into a stimulus object.
    
    Parameters
    ----------
    nameOfFile: String representing a directory.
    
    Returns
    ----------
    parameters: Dictionary containing information about the sessions.
    allEvents: List of stimulus objects.
    """
    #define constants
    baseLevelInterval = [2.0, 4.0]
    numberOfSecondsToProcess = 17
    
    #load signal file
    fullNameOfTheWav = nameOfFile + '.wav'
    fs, mothSignal = wavfile_read.read(fullNameOfTheWav)

    #create metadata
    parameters = {}
    parameters['fileName'] = nameOfFile
    parameters['sampleRate'] = fs
    parameters['numberOfSecondsToProcess'] = numberOfSecondsToProcess
    parameters['baseLevelInterval'] = baseLevelInterval
    parameters['sex'] = fullNameOfTheWav.split('/')[-3][0]
    parameters['fullWAV'] = mothSignal

    fin = open(nameOfFile + '-events.txt')
    mothEvents = [[],[]]
    reader = csv.reader(fin)
    for line in reader:
        if not '#' in line[0]:
            num, flt = line
            mothEvents[0].append(int(num))
            mothEvents[1].append(float(flt.strip()))
            
    numberOfEvents= len(mothEvents[0])
    
    #Adding the different event catigories
    allEvents =[]
    allEvents += [stimulus('Blow', 0)]
    allEvents += [stimulus('Fan start', 1)]
    allEvents += [stimulus('Control', 2)]
    allEvents += ['blank']
    allEvents += [stimulus('Hand', 4)]
    allEvents += [stimulus('Mineral oil', 5)]
    allEvents += [stimulus('Linalool', 6)]
    allEvents += [stimulus('Bombykol', 7)]
    allEvents += ['blank']
    allEvents += [stimulus('Fan off', 9)]
    
    for i in range(numberOfEvents):
        allEvents[mothEvents[0][i]].timestamps.append(mothEvents[1][i])
        allEvents[mothEvents[0][i]].baseline.append(np.average(np.transpose(mothSignal[int(mothEvents[1][i] * fs) 
              + int(baseLevelInterval[0] * fs):int(mothEvents[1][i] * fs) + int(baseLevelInterval[1] * fs)])[0]))
        allEvents[mothEvents[0][i]].lightBaseline.append(np.average(np.transpose(mothSignal[int(mothEvents[1][i] * fs) 
              + int(baseLevelInterval[0] * fs):int(mothEvents[1][i] * fs) + int(baseLevelInterval[1] * fs)])[1]))
        allEvents[mothEvents[0][i]].peak.append(np.transpose(mothSignal[int(mothEvents[1][i] * fs) 
            + int(baseLevelInterval[0] * fs):int(mothEvents[1][i] * fs) + int(baseLevelInterval[1] * fs)]).max())
        allEvents[mothEvents[0][i]].rawSignal.append(mothSignal[int(mothEvents[1][i] * fs) 
            + int(baseLevelInterval[1] * fs):int(mothEvents[1][i] * fs) + int(numberOfSecondsToProcess * fs)])
                
    return parameters, allEvents

def plotStimulus(stimulus, fs, fullWAV):
    """
    Plots the stimulus EAG and light minus an 'baseLevel' with filter, 1.5 
    secounds before the light first breaks the 75% of its max and 5.5 after. The
    'baseLevel' is the average value of two seound before the program starts
    checking for the max.
    
    Parameters
    ----------
    stimulus: stimulus object.
    fs: Frequency
    rawIndex: What trail of the stimulus you want to graph.
    
    Returns
    ----------
    mins: list of mini
    """
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(fullWAV)
    for time in stimulus.timestamps:
        ax.plot([int(time * fs), int(time * fs)], [-10000, 10000], color = 'r')
    
    mins = []
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    duration = []
    y = []

    
    for rawIndex in range(len(stimulus.timestamps)):
        
        
        maxLight = np.array(list(map(list, zip(*stimulus.rawSignal[rawIndex])))[1]).max()
        ind, = np.where((list(map(list, zip(*stimulus.rawSignal[rawIndex])))[1] -  stimulus.lightBaseline[rawIndex] >= .75 * (maxLight - stimulus.lightBaseline[rawIndex])))
        start = ind[0]
                       
        if int(start - 1.5 * fs) > 0:
            duration.append(int((stimulus.timestamps[rawIndex] + 4) * fs) + int(start - 1.5 * fs))
            duration.append(int((stimulus.timestamps[rawIndex] + 4) * fs) + int(start + 5.5 * fs))
            ax1.plot((np.array(list(map(list, zip(*stimulus.rawSignal[rawIndex])))[0][int(start - 1.5 * fs):int(start + 5.5 * fs)]) - stimulus.baseline[rawIndex]), color = 'c')
            mins.append((np.array(list(map(list, zip(*stimulus.rawSignal[rawIndex])))[0][int(start - 1.5 * fs):int(start + 1.5 * fs)]) - stimulus.baseline[rawIndex]).min())
            y.append(np.where(abs((np.array(list(map(list, zip(*stimulus.rawSignal[rawIndex])))[0][int(start - 1.5 * fs):int(start + 1.5 * fs)]) - stimulus.baseline[rawIndex]) - mins[-1]) < .0001)[0][0])
                   
            if rawIndex == 0:
                aveLine = np.array(list(map(list, zip(*stimulus.rawSignal[rawIndex])))[0][int(start - 1.5 * fs):int(start + 5.5 * fs)]) - stimulus.baseline[rawIndex]
            else:
                aveLine += (np.array(list(map(list, zip(*stimulus.rawSignal[rawIndex])))[0][int(start - 1.5 * fs):int(start + 5.5 * fs)]) - stimulus.baseline[rawIndex])
        else:
            duration.append((int(stimulus.timestamps[rawIndex] + 4) * fs))
            duration.append((int(stimulus.timestamps[rawIndex] + 4) * fs) + 35000)
            ax1.plot((np.array(list(map(list, zip(*stimulus.rawSignal[rawIndex])))[0][0:35000]) - stimulus.baseline[rawIndex]), color = 'c')
            mins.append((np.array(list(map(list, zip(*stimulus.rawSignal[rawIndex])))[0][0:15000] - stimulus.baseline[rawIndex]).min()))
            y.append(np.where(((np.array(list(map(list, zip(*stimulus.rawSignal[rawIndex])))[0][0:15000] - stimulus.baseline[rawIndex]).min()) - mins[-1]) < .0001)[0][0])
            aveLine += (np.array(list(map(list, zip(*stimulus.rawSignal[rawIndex])))[0][0:35000]) - stimulus.baseline[rawIndex])

    aveLine = aveLine / len(stimulus.timestamps)
    ax1.plot(aveLine, color = 'k')
    
    for index in range(len(y)):
        ax1.plot(y, mins,  'ro')
        
    for index in range(len(duration)//2): 
        ax.plot(duration[index * 2:index * 2 + 2], [5000,5000] , color = 'g')
     
    bottomLim, topLim = ax1.get_xlim()
    labels = []
    locs = []
    whitespace = 0 - bottomLim
    for i in range(5):
        labels.append(7/4 * i)
        locs.append((bottomLim + whitespace) + ((((topLim - whitespace)- (bottomLim + whitespace))/4) * i))
        
    plt.xticks(locs, labels)
    plt.xlabel('Secounds')
# =============================================================================
#     fig = plt.figure()
#     ax2 = fig.add_subplot(1,1,1)
#     rawIndex = 8
#     maxLight = np.array(list(map(list, zip(*stimulus.rawSignal[rawIndex])))[1]).max()
#     ax2.plot((np.array(list(map(list, zip(*stimulus.rawSignal[rawIndex])))[1]) - stimulus.baseline[rawIndex]))
#     ax2.plot([duration[16] - int((stimulus.timestamps[rawIndex] + 4) * fs),duration[17] - int((stimulus.timestamps[rawIndex] + 4) * fs)],[2000,2000])
#     ax2.plot([.75 * (maxLight - stimulus.baseline[rawIndex]),.75 * (maxLight - stimulus.baseline[rawIndex])], [2000,2000], color = 'g')
# =============================================================================
    
    return mins

    
def recordings(dirs, stimuli):
    """
    Turns a list of directories of .wav files into a list of recordings.
    
    Parameters
    ----------
    dirs: list of directories
    stimuli: list of the stimuli ids that you want to get info on
    
    Returns
    ----------
    re: list of recordings
    """
    re = []
    for directory in dirs:
        record = recording()
        record.metadata, record.session = processMothData(directory)
        for sitmulus in stimuli:
            mins = plotStimulus(record.session[sitmulus], record.metadata['sampleRate'], record.metadata['fullWAV'])
            record.mins += [mins]
            record.aveMin += [sum(mins) / len(mins)]
            record.std += [np.std(mins)]


        re += [record]
        
    return re