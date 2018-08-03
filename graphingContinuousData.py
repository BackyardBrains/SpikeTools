#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 10:25:37 2018

@author: benrobbins
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import spectrogram


def plotContinuousData(oSession, channel = 0, timerange = 0):
    """
    Plots a time vs voltage of a session object.
    Parameters
    ----------
    oSession: session object
    channel: List of channels you want to graph. Defult is all channels are graphed.
    timerange: List with two values, the start time of the graph and the end
               time of the graph.
    """

    if not timerange:
        timerange = [0,len(oSession.EEG.data[0])/ oSession.EEG.FS]
    if not channel:
        channel = [i for i in range(len(oSession.EEG.data))]
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    base = 0
    locs = []
    labels = []

    temp = []
    for i in range(len(oSession.EEG.data)):
        temp.append(oSession.EEG.data[i][timerange[0] * oSession.EEG.FS:int(timerange[1] * oSession.EEG.FS + 1)])
    oSession.EEG.data = np.array(temp, np.int32)
    
    for i in range(len(channel)):
        ax1.plot(oSession.EEG.data[channel[i]] + base)
        locs.append(base)
        labels.append(str(channel[i] + 1))
        if channel[i] != len(oSession.EEG.data) - 1:
            base += (oSession.EEG.data[channel[i]].max() + 10 - oSession.EEG.data[channel[i + 1]].min())

    plt.yticks(locs, labels)
    plt.ylabel('Channels')
    
    bottomLim, topLim = ax1.get_xlim()
    labels = []
    locs = []
    whitespace = 0 - bottomLim
    for i in range(5):
        labels.append((timerange[0] + (((timerange[1] - timerange[0])/4) * i)))
        locs.append((bottomLim + whitespace) + ((((topLim - whitespace)- (bottomLim + whitespace))/4) * i))
        
    plt.xticks(locs, labels)
    plt.xlabel('Secounds since the start')

def plotEventTriggeredAverage(oSession, event = '', channels = 0, timerange = [-1, 3]):
    """
    Plots an average time vs voltage of a session object for an event.
    Parameters
    ----------
    oSession: session object
    event: string represents an event in the session object
    channel: List of channels you want to graph. Defult is all channels are graphed.
    timerange: List with two values, the start time of the graph and the end
               time of the graph.
    """

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    base = 0
    locs = []
    labels = []
    
    if not channels:
        channels = [i for i in range(len(oSession.EEG.data))]
    
    data = np.zeros((len(oSession.EEG.data), (timerange[1] - timerange[0]) * oSession.EEG.FS))
    for singleEvent in eval('oSession.' + event):
        for i in range(len(data)):
            data[i] += oSession.EEG.data[i][(singleEvent + timerange[0]) * oSession.EEG.FS:(singleEvent + timerange[1]) * oSession.EEG.FS + 1]
    data = data/len(eval('oSession.' + event))
    
    for i in channels:
        ax1.plot(data[i] + base)
        locs.append(base)
        labels.append(str(i + 1))
        if i != len(data) - 1:
            base += (data[i].max() + 10 - data[i + 1].min())

    plt.yticks(locs, labels)
    plt.ylabel('Channels')
    
    bottomLim, topLim = ax1.get_xlim()
    labels = []
    locs = []
    whitespace = 0 - bottomLim
    for i in range(5):
        labels.append((timerange[0] + (((timerange[1] - timerange[0])/4) * i)))
        locs.append((bottomLim + whitespace) + ((((topLim - whitespace)- (bottomLim + whitespace))/4) * i))
        
    plt.xticks(locs, labels)
    plt.xlabel('Secounds (Event is at 0)')

def plotContinuousSpectrogram(oSession, channel = 0, timerange = 0):
    """
    Plots a time vs frequency vs power spectogram of a session object.
    Parameters
    ----------
    oSession: session object
    channel: List of channels you want to graph. Defult is all channels are graphed.
    timerange: List with two values, the start time of the graph and the end
               time of the graph.
    """

    if not timerange:
        timerange = [0,len(oSession.EEG.data[0])/ oSession.EEG.FS]
    if not channel:
        channel = [i for i in range(len(oSession.EEG.data))]
        
    temp = []
    for i in range(len(oSession.EEG.data)):
        temp.append(oSession.EEG.data[i][timerange[0] * oSession.EEG.FS:int(timerange[1] * oSession.EEG.FS + 1)])
    data = np.array(temp, np.int32)
        
    for i in channel:
        f, t, Sxx = spectrogram(data[i], fs = oSession.EEG.FS, nfft = 2500)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.pcolormesh(t,f,Sxx)
        
        plt.title('Channel ' + str(i +1))
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [S]')
        
        ax.set_ylim(0,40)
        
        


def plotEventTriggeredSpetrogram( oSession, event = '', channel = 0, timerange = [-1,3]):
    """
    Plots a time vs frequency vs power spectogram of a session object.
    Parameters
    ----------
    oSession: session object
    event: string represents an event in the session object
    channel: List of channels you want to graph. Defult is all channels are graphed.
    timerange: List with two values, the start time of the graph and the end
               time of the graph.
    """

    if not timerange:
        timerange = [0,len(oSession.EEG.data[0])/ oSession.EEG.FS]
    if not channel:
        channel = [i for i in range(len(oSession.EEG.data))]
        
    data = np.zeros((len(oSession.EEG.data), (timerange[1] - timerange[0]) * oSession.EEG.FS))
    for singleEvent in eval('oSession.' + event):
        for i in range(len(data)):
            data[i] += oSession.EEG.data[i][(singleEvent + timerange[0]) * oSession.EEG.FS:(singleEvent + timerange[1]) * oSession.EEG.FS + 1]
    data = data/len(eval('oSession.' + event))
        
    for i in channel:
        f, t, Sxx = spectrogram(data[i], fs = oSession.EEG.FS, scaling = 'spectrum', nfft = 2500)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.pcolormesh(t,f,Sxx)
        
        plt.title('Channel ' + str(i +1))
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [S]')
        
        ax.set_ylim(0,40)

def plotContinuousSpetrum(oSession, channel = 0, timerange = 0):
    """
    Plots a frequency vs power Spetrum of a session object.
    Parameters
    ----------
    oSession: session object
    channel: List of channels you want to graph. Defult is all channels are graphed.
    timerange: List with two values, the start time of the graph and the end
               time of the graph.
    """

    if not timerange:
        timerange = [0,len(oSession.EEG.data[0])/ oSession.EEG.FS]
    if not channel:
        channel = [i for i in range(len(oSession.EEG.data))]
        
    temp = []
    for i in range(len(oSession.EEG.data)):
        temp.append(oSession.EEG.data[i][timerange[0] * oSession.EEG.FS:int(timerange[1] * oSession.EEG.FS + 1)])
    data = np.array(temp, np.int32)
    
    for i in channel:
        f, t, Sxx = spectrogram(data[i], fs = oSession.EEG.FS, nfft = 2500)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        
        newData = []
        for freq in Sxx:
            newData += [freq.sum()/len(freq)]
        
        ax.bar(range(len(newData)), newData, color = 'k', width = 1)
        
        plt.title('Channel ' + str(i +1))
        plt.ylabel('Power')
        plt.xlabel('Frequency[Hz]')
        
        ax.set_xlim(0,200)
