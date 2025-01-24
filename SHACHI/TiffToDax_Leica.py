#!/usr/bin/env python
"""
Convert a mess of tiff files into a single dax file.

Original code: Hazen 09/14, storm_analysis/sa_utilities/tiffs_to_dax.py, Copyright (c) 2014 Zhuang Lab, Harvard University

Modified by Taihei Fujimori to adapt the program to tiff images obtained using LAS X software (Leica)
"""

# -- import packages -- #
import glob
import numpy
import sys
import os

import datawriter # copied from storm_analysis.sa_library
import datareader # copied from storm_analysis.sa_library

class TiffToDax():
	def __init__(self,
	             sourceDIR = False, destDIR = False, hybnum = False, FOVnum = False, bOverwrite = False):
		# -- directories -- #
		self.sourceDIR = sourceDIR
		self.destDIR = destDIR
		self.bOverwrite = bOverwrite

		# --  detect number of positions and hyb rounds -- #
		self.hybnum = range(1,hybnum+1)
		self.FOV = range(1,FOVnum+1)

	# --  export data as dax -- #
	def export(self):
		print('start export')
		for hyb in self.hybnum:
			tmpDIR = self.destDIR+'hyb'+str(hyb)+'/'
			if not os.path.isdir(tmpDIR):
				os.makedirs(tmpDIR)
			for fov in range(0,len(self.FOV)):
				argout = tmpDIR+'ConvZscan_'+"%03d" % (fov+1) +'.dax'

				if os.path.isfile(argout) & (self.bOverwrite == 0):
					print(argout+' exists. Export failed.')
				else:
					# # --- Naming rule in Acquisition panel
					# argfov = 'Position'+"%03d" % self.FOV[fov]
					# arghyb = 't'+"%02d" % (hyb-1)

					# --- Naming rule in Navagator mode
					argfov = 'Position '+"%01d" % self.FOV[fov]
					arghyb = 't'+"%04d" % (hyb-1)
					argTS = 'TileScan '+"%01d" % hyb + '/'

					dax_file = datawriter.DaxWriter(argout)
					# in the order of modification time 20210330 Taihei Fujimori
					tiff_files = sorted(glob.glbo(self.sourceDIR+argfov+"--"+arghyb+"*.tif"),key=os.path.getmtime)
					# not time-lapse 20240327 Taihei Fujimori
					# tiff_files = sorted(glob.glob(self.sourceDIR+argTS+argfov+"--"+"*.tif"),key=os.path.getmtime)

					if (len(tiff_files) == 0):
						print("No tiff files found : '" + argfov+"--"+arghyb + "'")
						# print("No tiff files found : '" + argfov+"--" + "'")
					else:
						znum = int(len(tiff_files)/2)
						for idx in range(0,znum):
							print(tiff_files[idx]) # cy5 channel
							data = datareader.TifReader(tiff_files[idx]).loadAFrame(0)
							dax_file.addFrame(data)
							print(tiff_files[idx+znum]) # cy3 channel
							data = datareader.TifReader(tiff_files[idx+znum]).loadAFrame(0)
							dax_file.addFrame(data)
						dax_file.close()


