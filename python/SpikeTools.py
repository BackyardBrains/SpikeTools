#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 13:50:41 2018

@author: benrobbins

This is a module contains functions to help facilitate the creation of graphs.
Particularly Rasters and PETHs for the Grasshopper data.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import gridspec

def plotPETH(session, events,numPointsToSmooth = 3,
             binSize = .03, timerange = [-1, 1], makeplot = 1, 
             barColor = ['r', 'b', 'g', 'y'], linewidth = 1, ylim = None):
    """
    Plots a histogram of a PETH
    Parameters
    ----------
    session: experiment session
    events: A string or an array-like object of strings that represent the 
            attribute(s) in the session that should be used to 
            identify when the impacts occured.
    numPointsToSmooth: The number of bins that each value should be smoothed 
                       over. Defult is 3.
    binSize: The size of each bar along the x-axis in secounds. Defult is 
             .03 secound.
    timerange: An array-like object containing two integers, which represent
               the range you want to search for spikes in each trial relative
               to the each event. The event timestamp is 0. Defult is [-1,1].
               Meassured is secounds.
    makeplot: If 1 this will generate graph. If 0 it won't. 1 is defult. 
    barColor: An array-like object containing strings that represent colors
              for the line graph. Defult is is ['r'(red),'b'(blue),
              'g'(green),'y'(yellow)].
    linewidth: Line width for the line graph. Defult is one.
    ylim: If set, will be the top frequency of the graph. Else, it will go to
          the defult limit for the data set by matplotlib.hist().
    Returns
    -------
    out: A list of lists or a 3d list, each innermost list representing a trial
         and full of all the spikes that were within the range of impact with 
         the next layer of list(s) representing one element in events.
    """
   
#     """
#     This is a calculation for the 95% confidence interval of a spike. It 
#     assumes that the spike train is a Possison train. It was taken from 
#     Abeles M. Quantification, smoothing, and confidence limits for single-units
#     histograms. Journal of Nueroscience Methodes.
#     """
#     """
#     frequency = 1/np.mean(np.diff(spiketimes))
#     c = frequency * binSizenumEvents
#     
#     if (c >= 30):
#         lowerConfidanceLimit = c - 2.58 * (c ** .5)
#         higherConfidenceLimit = c + 2.58 * (c ** .5)
#         
#     else:
#         lowerConfidanceLimit = -1
#         higherConfidenceLimit = 1
#         
#         s = 0
#         
#         for aa in range(51):
#             pp = math.exp(-c) * power(c, aa)
#             
#         fact = math.factorial(aa)
#         pp /= fact
#         s += pp
#         
#         if lowerConfidanceLimit == -1 and s >= 0.05:
#             lowerConfidanceLimit = aa - 1
#             
#         if higherConfidenceLimit == -1 and s >= .95:
#             higherConfidenceLimit = aa 
#             
#         higherConfidenceLimit = higherConfidenceLimit / binSize / numEvents
#         lowerConfidanceLimit = lowerConfidanceLimit / binSize / numEvents
#         
#         out.ci.high = higherConfidenceLimit
#         out.ci.low = lowerConfidanceLimit
#         out.m = frequency
#         """    
    
    try:
        allS = []
        out = []
        for i in range(len(events)):
            singleListOfEvents = eval("session.timestamps." + events[i])
            trials = session.trials
            sS = []
            o =[]
            
            for time in singleListOfEvents:
                for index in range(len(trials)):
                    s = []
                    
                    if abs(trials[index].timeOfImpact - (time - (index * 45000))) < .00001:
                        for spike in trials[index].spikeTimestamps:            
                            if (spike - (time - (index * 45000))) >= (timerange[0]- (numPointsToSmooth - 1)//2 * binSize)  and ((spike - (time - (index * 45000))) <= (timerange[1]+ (numPointsToSmooth - 1)//2 * binSize) ):
                                    s.append(spike - (time - (index * 45000)))
                       
                        
                        o.append(s)
                        sS += s
            out.append(o)
            allS.append(sS)    
            
            
        bins = abs(np.diff(timerange)[0])/ binSize
        if (bins % 1) != 0:
            bins = int(bins) + 1  
        else:
            bins = int(bins)
            
        if makeplot:
            fig = plt.figure()
            ax1 = fig.add_subplot(1,1,1)
            values = []
            times = []
            
            for i in range(len(events)):
                value, time, throughAway = ax1.hist(allS[i], bins = bins, 
                                                range=timerange)
                value = list(value)
                value.append(value[-1])
                values.append(value)
                times.append(time)
                ax1.clear()
                
            for i in range(len(events)):
                times[i] = times[i][(numPointsToSmooth - (numPointsToSmooth - 1)//2 - 1):(len(times[i]) - (numPointsToSmooth - 1)//2)]
                ax1.plot(times[i], smooth(values[i], numPointsToSmooth), drawstyle = 'steps-post', 
                         color = barColor[i], linewidth = linewidth)
            
            ax1.set_ylim(bottom = 0)
            if (ylim != None):
                ax1.set_ylim(top = ylim * (binSize * len(eval('session.timestamps.' + events[0]))))    
            bottomLim, topLim = ax1.get_ylim()
            top = topLim
            topLim = topLim/(binSize * len(eval('session.timestamps.' + events[0])))
            labels = []
            locs = []
            for i in range(5):
                labels.append('%d' % (bottomLim + (((topLim - bottomLim)/4) * i)))
                locs.append(bottomLim + (((top - bottomLim)/4) * i))
            
            plt.yticks(locs, labels)
            plt.ylabel('Firing Rate (Hz)')
            
            plt.title(session.session)
            plt.xlabel('Time (Secounds with impact at 0)')

    except:
        singleListOfEvents = eval("session.timestamps." + events)
        trials = session.trials
        
        for time in singleListOfEvents:
            for index in range(len(trials)):
                s = []
                
                if abs(trials[index].timeOfImpact - (time - (index * 45000))) < .00001:
                    for spike in trials[index].spikeTimestamps:            
                        if (spike - (time - (index * 45000))) >= (timerange[0]- (numPointsToSmooth - 1)//2 * binSize)  and ((spike - (time - (index * 45000))) <= (timerange[1]+ (numPointsToSmooth - 1)//2 * binSize) ):
                                s.append(spike - (time - (index * 45000)))
                   
                    
                    out.append(s)
                    allS += s 
            
        bins = abs(np.diff(timerange)[0])/ binSize
        if (bins % 1) != 0:
            bins = int(bins) + 1  
        else:
            bins = int(bins)  
        
        if makeplot:
            gs = gridspec.GridSpec(2, 1, height_ratios=[1, 3]) 
            ax1 = plt.subplot(gs[0])
            value, time, throughAway = ax1.hist(smooth(allS, numPointsToSmooth), bins = bins, color = 'k', range=timerange)  
            value = list(value)
            value.append(value[-1])
            ax1.clear()
            
            ax1.bar(range(len(value)), value, color = 'k', width = 1)
            
            if (ylim != None):
                ax1.set_ylim(top = ylim * (binSize * len(eval('session.timestamps.' + events))))   
            bottomLim, topLim = ax1.get_ylim()
            top = topLim
            bottomLim = bottomLim/(binSize * len(eval('session.timestamps.' + events)))
            topLim = topLim/(binSize * len(eval('session.timestamps.' + events)))
            labels = []
            locs = []
            for i in range(5):
                labels.append('%d' % (bottomLim + (((topLim - bottomLim)/4) * i)))
                locs.append(bottomLim + (((top - bottomLim)/4) * i))
            
            plt.yticks(locs, labels)
            plt.ylabel('Firing Rate (Hz)')
            
            plt.title(session.session)
    
    return out
    
def plotRaster(session, event, makeplot = 1, timerange = [-1,1]):
    """
    Creates a raster plot.
    Parameters
    ----------
    session : A session object
    event: A string that represents the attribute in the session that the 
           function should use to identify when the impacts occured.
    makeplot: If 1 then a plot will be generated, if 0 then no plot will be 
              generated. Defult is 1.
    timerange: An array-like object containing two integers, which represent
               the range you want to search for spikes in each trial relative
               to the each event. The event timestamp is 0. Defult is [-1,1].
    
    Returns
    -------
    ax : an axis containing the raster plot
    """
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    allS = []
    out = []
        
    singleListOfEvents = eval("session.timestamps." + event)
    trials = session.trials
    
    for time in singleListOfEvents:
        for index in range(len(trials)):
            s = []
            
            if abs(trials[index].timeOfImpact - (time - (index * 45000))) < .00001:
                for spike in trials[index].spikeTimestamps:            
                    if (spike - (time - (index * 45000))) >= timerange[0] and (spike - (time - (index * 45000))) <= timerange[1]:
                            s.append(spike - (time - (index * 45000)))
               
                
                out.append(s)
                allS += s 
    
    if makeplot:
        raster(out)
        plt.xlabel('Time (Secounds with impact at 0)')
        plt.ylabel('Trial')
        plt.subplots_adjust(hspace = 0.05)
        fig.show()  
    
    return ax

def raster(event_times_list, **kwargs): #pulled from the internet
    """
    Creates a raster plot
    Parameters
    ----------
    event_times_list : iterable
                       a list of event time iterables
    color : string
            color of vlines
    Returns
    -------
    ax : an axis containing the raster plot
    """
    ax = plt.gca()
    for ith, trial in enumerate(event_times_list):
        plt.vlines(trial, ith + .5, ith + 1.3)
    plt.ylim(.5, len(event_times_list) + .5)
    ax.invert_yaxis()
    return ax

def smooth(mylist, smoothInt):
    """
    Mimics the smooth method in matlab
    Parameters
    ----------
    mylist: A list of numbers to be smoothed
    smoothInt: The span of the moving average to span. It must be odd.
    
    Returns
    -------
    newlist: A list of the smoothed out floats.
    """
    newlist = []
    for i in range((smoothInt - (smoothInt - 1)//2 - 1),(len(mylist) - (smoothInt - 1)//2)):
        runningSum = 0
        for index in range(smoothInt):
            runningSum += mylist[index +  (i - (((smoothInt - 1)//2)))]
        k = runningSum / smoothInt    
        newlist.append(k) 
    return newlist
