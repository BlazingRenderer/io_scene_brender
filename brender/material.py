#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
MIT License

Copyright (c) 1992-1998 Argonaut Technologies Limited
Copyright (c) 2014-2025 Zane van Iperen, erysdren

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

from brender.matrix import *
from brender.pixelmap import *

# material
class material(Structure):
	_fields_ = [
		("_reserved", c_void_p),
		("identifier", c_char_p),
		("colour", c_uint),
		("opacity", c_ubyte),
		("ka", c_float),
		("kd", c_float),
		("ks", c_float),
		("power", c_float),
		("flags", c_uint),
		("map_transform", matrix23),
		("mode", c_ushort),
		("index_base", c_ubyte),
		("index_range", c_ubyte),
		("colour_map", POINTER(pixelmap)),
		("screendoor", POINTER(pixelmap)),
		("index_shade", POINTER(pixelmap)),
		("index_blend", POINTER(pixelmap)),
		("index_fog", POINTER(pixelmap)),
		("extra_surf", c_void_p),
		("extra_prim", c_void_p),
		("fog_min", c_float),
		("fog_max", c_float),
		("fog_colour", c_uint),
		("subdivide_tolerance", c_int),
		("depth_bias", c_float),
		("user", c_void_p),
		("stored", c_void_p)
	]
