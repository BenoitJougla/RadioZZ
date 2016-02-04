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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from rds_encoder import rds_encoder

class qa_rds_encoder (gr_unittest.TestCase):

	def setUp (self):
		self.tb = gr.top_block ()

	def tearDown (self):
		self.tb = None

	def test_001_t (self):
		src_data = (0, 0)
		expected_result = (0xF0A1, 0xF0A1)
		src = blocks.vector_source_f (src_data)
		fxn = rds_encoder (0xF0A1, "Test", "Test")
		snk = blocks.vector_sink_f ()
		self.tb.connect (src, fxn)
		self.tb.connect (fxn, snk)
		self.tb.run ()
		result_data = snk.data ()
		self.assertFloatTuplesAlmostEqual (expected_result, result_data, 2)

	def test_002_t (self):
		rds = rds_encoder(0xF0A1, "test", "test")
		blocB = rds.createBlocB(0b0000, 0b1, 0b1, 0b00111, 0b0, 0b1, 0b0, 0b00)
		self.assertAlmostEqual(blocB, 0b0000110011101000)
		
	def test_003_t (self):
		rds = rds_encoder(0xF849, "--KCBS--", "test")
		frames = rds.preparePsnFrame()
		self.assertAlmostEqual(len(frames), 4)
		
		blocA = 0b1111100001001001
		blocB = 0b0000110010101100
		blocC = 0b1111100001001001
		blocD = 0b0010110100101101
		self.assertAlmostEqual(frames[0], blocA << (26 * 3) | blocB << (26 * 2) | blocC << 26 | blocD)
		
		blocB = 0b0000110010101001
		blocD = 0b0100101101000011
		self.assertAlmostEqual(frames[1], blocA << (26 * 3) | blocB << (26 * 2) | blocC << 26 | blocD)
		
		blocB = 0b0000110010101010
		blocD = 0b0100001001010011
		self.assertAlmostEqual(frames[2], blocA << (26 * 3) | blocB << (26 * 2) | blocC << 26 | blocD)
		
		blocB = 0b0000110010101011
		blocD = 0b0010110100101101
		self.assertAlmostEqual(frames[3], blocA << (26 * 3) | blocB << (26 * 2) | blocC << 26 | blocD)
	
	def test_004_t (self) : 
		rds = rds_encoder(0xF849, "--KCBS--", "test")
		crcA = rds.computeCRC(0b1111100001001001, 0b111111)
		crcB = rds.computeCRC(0b0000110010101100, 0b1100110)
		crcC = rds.computeCRC(0b1111100001001001, 0b1011010)
		crcD = rds.computeCRC(0b0010110100101101, 0b1101101)
		print  bin(crcA)
		print bin(crcB)
		print  bin(crcC)
		print bin(crcD)
		#self.assertEqual(len(bin(crc)), 28)
		

		

if __name__ == '__main__':
	gr_unittest.run(qa_rds_encoder, "qa_rds_encoder.xml")
