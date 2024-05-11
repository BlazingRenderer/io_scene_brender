#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
MIT License

Copyright (c) 1992-1998 Argonaut Technologies Limited
Copyright (c) 2014-2024 Zane van Iperen, erysdren

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from ctypes import *

# pixelmap types
PMT_INDEX_1 = c_ubyte(0)
PMT_INDEX_2 = c_ubyte(1)
PMT_INDEX_4 = c_ubyte(2)
PMT_INDEX_8 = c_ubyte(3)
PMT_RGB_555 = c_ubyte(4)
PMT_RGB_565 = c_ubyte(5)
PMT_RGB_888 = c_ubyte(6)
PMT_RGBX_888 = c_ubyte(7)
PMT_RGBA_8888 = c_ubyte(8)
PMT_YUYV_8888 = c_ubyte(9)
PMT_YUV_888 = c_ubyte(10)
PMT_DEPTH_16 = c_ubyte(11)
PMT_DEPTH_32 = c_ubyte(12)
PMT_ALPHA_8 = c_ubyte(13)
PMT_INDEXA_88 = c_ubyte(14)
PMT_NORMAL_INDEX_8 = c_ubyte(15)
PMT_NORMAL_XYZ = c_ubyte(16)
PMT_BGR_555 = c_ubyte(17)
PMT_RGBA_4444 = c_ubyte(18)
PMT_RBG_bab = c_ubyte(19)
PMT_RBG_1aba = c_ubyte(20)
PMT_RGB_332 = c_ubyte(21)
PMT_DEPTH_8 = c_ubyte(22)
PMT_ARGB_8888 = c_ubyte(23)
PMT_ALPHA_4 = c_ubyte(24)
PMT_INDEXA_44 = c_ubyte(25)
PMT_DEPTH_15 = c_ubyte(26)
PMT_DEPTH_31 = c_ubyte(27)
PMT_DEPTH_FP16 = c_ubyte(28)
PMT_DEPTH_FP15 = c_ubyte(29)
PMT_RGBA_5551 = c_ubyte(30)
PMT_ARGB_1555 = c_ubyte(31)
PMT_ARGB_4444 = c_ubyte(32)
PMT_RGBA_8888_ARR = c_ubyte(33)
PMT_MAX = c_ubyte(34)
PMT_AINDEX_44 = PMT_INDEXA_44
PMT_AINDEX_88 = PMT_INDEXA_88

# pixelmap allocation flags
PMAF_NORMAL = c_int(0x0000)
PMAF_INVERTED = c_int(0x0001)
PMAF_NO_PIXELS = c_int(0x0002)

# colour range
class colour_range(Structure):
	_fields_ = [("low", c_uint), ("high", c_uint)]

# pixelmap
class pixelmap(Structure):
	pass
pixelmap._fields_ = [
		("_reserved", c_void_p),
		("identifier", c_char_p),
		("pixels", c_void_p),
		("map", POINTER(pixelmap)),
		("src_key", colour_range),
		("dst_key", colour_range),
		("key", c_uint),
		("row_bytes", c_short),
		("mip_offset", c_short),
		("type", c_ubyte),
		("copy_function", c_ushort),
		("flags", c_ushort),
		("base_x", c_ushort),
		("base_y", c_ushort),
		("width", c_ushort),
		("height", c_ushort),
		("origin_x", c_short),
		("origin_y", c_short),
		("user", c_void_p),
		("stored", c_void_p)
	]
