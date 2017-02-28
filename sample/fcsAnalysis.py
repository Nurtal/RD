"""
Function for the 
analys of fcs files

using FlowCytometryTools 0.45 package



Notes:

Channel i.e parameters

Forward scatter (FS machin)
 => not interesting (include only B cells)
 => have to exlude all SS* channel and all FS* channel + Time channel
"""

import FlowCytometryTools
from FlowCytometryTools import FCMeasurement

import numpy as np

from trashlib import *







def ExludeUndesirableChannel(fcsFileName):
	"""
	[A VERIFIER]
	fcsData is numpy array
	"""

	# Delete non desirable channel in data
	sample = FCMeasurement(ID='Test Sample', datafile=fcsFileName)
	data = sample.data.values
	listOfParameters = []
	for name in sample.channel_names:
		listOfParameters.append(str(name))

	cmpt = 0
	listOfIndexToDelete = []
	for channel in listOfParameters:
		channelInArray = channel.split("-")
		if len(channelInArray) > 1:
			listOfIndexToDelete.append(cmpt)
		cmpt = cmpt + 1

	data = np.delete(data, listOfIndexToDelete, 0)

	return data





datafile = "DATA/FCS/export_Panel_5_32141759_A_CD19_subset.fcs"
datafileB = "DATA/FCS/export_Panel_5_32152203_B_CD19_subset.fcs"
sample = FCMeasurement(ID='Test Sample', datafile=datafile)

#print sample.channels
#print sample.data.values

#data = sample.data.values
#quickClustering(data, 4, "fcsCluster.png")
#quickPCA(data, listOfParameters, "2d", "pcaFCS.jpg") # manque le parametre y



