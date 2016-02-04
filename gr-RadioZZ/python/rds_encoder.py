#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr

class rds_encoder(gr.sync_block):
	"""
	docstring for block rds_encoder
	"""
	def __init__(self, piCode, radioName, radioText):

		self.piCode = piCode
		self.radioName = radioName
		self.radioText = radioText		
		
		gr.sync_block.__init__(self,
		name="rds_encoder",
		in_sig=[numpy.float32],
		out_sig=[numpy.float32])

	def createBlocA(self):
		return self.piCode
		
	def createBlocB(self, groupe, version, tp, pty, ta, ms, di, address):		
		blocB = groupe << 12 | version << 11 | tp << 10 | pty << 5 | ta << 4 | ms << 3 | di << 2 | address
		return blocB
		
	def preparePsnFrame(self):
		rds = []
		blocA = self.createBlocA()
		blocC = blocA
		
		psnLength = len(self.radioName)
		
		di = []
		di.append(0b1)
		di.append(0b0)
		di.append(0b0)
		di.append(0b0)
		
		index = 0
		
		for i in range(0, 4):
			# groupe 0B : transmission du psn (goupe = 0, version = 1)
			# tp (Traffic program) : oui car certains autoradio n'affichent pas le nom si ce flag n'est pas à 1
			# pty (Program type) : 00101 => education
			# TA ("Traffic Announcement"): 0
			# M/S ("Music/Speech"): musique, donc (1)
			# DI ("Decoder information"): 4 bits transmis sequentiellement avec les 4 groupes: 1000. 1 => stereo Voir page 41
			# Adresse: premier groupe (00), deuxiéme groupe (01), troisième groupe (10), quatrième groupe (11)
			blocB = self.createBlocB(0b0000, 0b1, 0b1, 0b00101, 0b0, 0b1, di[i], int(bin(i),2))
			
			firstChar = " ";
			secondChar = " ";
			
			if index < psnLength :
				firstChar = self.radioName[index]
			if index + 1 < psnLength :
				index += 1
				secondChar = self.radioName[index]
				index += 1
			
			blocD = ord(firstChar) << 8 | ord(secondChar)
			frame = blocA << (26 * 3) | blocB << (26 * 2) | blocC << 26 | blocD
			rds.append(frame)
			
		return rds

	def work(self, input_items, output_items):
		in0 = input_items[0]
		out = output_items[0]
		
		# <+signal processing here+>
		rds = self.preparePsnFrame()
		
		out[:] = self.piCode
		return len(output_items[0])
	
	def computeCRC (self, bloc, blocType):
		polynomial = 0b10110111001
		R = (bloc / polynomial)%2
		c = R + blocType
		return  bloc << 10 |(c ^ blocType) 
		
		
