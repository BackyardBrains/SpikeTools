# SpikeTools
Software tools for reading, manipulating, and analyzing neural data.  These tools are for both timestamp spikes and continuous data (EEG, EMG).

Inorder to use BYBLoadGrasshopperData.py one must import it and call the function convert_JSON_to_python passing the directory of the folder containing the proper json files as the perameter. The function will return a sessions object which inherits from and operates like a list.

BYBSpikes contains functions to help plot raster and PETH graphs. The instructions  on how to use them are in the doc string.

JSON_Converter uses the BYBLoadGrasshopper library and reads in from a specific data set of json files, compiles them into a sessions object, and stores it in a text file. It also reads in the text file and prints out some data from the sessions object inorder to test that the process worked.

To use BYBLoadContinuousData you must have your folders arraged such that there is a folder that is named after the eperiment. This folder contains folders that represent the protocal used a naming convention (i.e. 'P00', 'P01', 'P02', ect.) and these folders contain folders representing the subject (i.e. 'S00'). Those folders contain the wanted .wav files and thier corrisponding .txt files. Inorder to use the library one must  call findWAVfiles passing the directory of the outer most folder as the parameter. You then iterate through the result to create and pass the info as the parameters for convert_to_session and append them to a list. The result is a list of session objects. One can add comments manualy to individual session objects if desired. WAV_Converter is an example of this.

graphingContinousData contains functions to help plot continuous data, event triggered averages, spetrograms, event trigared average spetrograms, and spetrums. The instructions  on how to use them are in the doc string.

Inorder to use processMothData one must call recording passing a list of the directories of the desired recordings as the first parameter and a list of the stimulus ids of the stimuluses that you want to look at.

wavfile_read.py was taken from another gitHub. link: https://github.com/scipy/scipy/blob/v0.14.0/scipy/io/wavfile.py#L116
Module to read / write wav files using numpy arrays

spikerecorder.py is written in Python 3 and it will read, parse and display data from BackyardBrains' serial devices (like Muscle, Neuron and Plant SpikerShield and Muscle and Plant SpikerBox)
