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

from brender.vector import *
from brender.material import *

# vertex
class vertex(Structure):
	_fields_ = [
		("p", vector3),
		("map", vector2),
		("index", c_ubyte),
		("red", c_ubyte),
		("grn", c_ubyte),
		("blu", c_ubyte),
		("_pad0", c_ushort),
		("n", vector3)
	]

# face
class face(Structure):
	_fields_ = [
		("vertices", c_ushort),
		("smoothing", c_ushort),
		("material", POINTER(material)),
		("index", c_ubyte),
		("red", c_ubyte),
		("grn", c_ubyte),
		("blu", c_ubyte),
		("flags", c_ubyte),
		("_pad0", c_ubyte),
		("_pad1", c_uint),
		("n", vector3),
		("d", c_float)
	]

# model
class model(Structure):
	_fields_ = [
		("_reserved", c_void_p),
		("identifier", c_char_p),
		("vertices", POINTER(vertex)),
		("faces", POINTER(face)),
		("nvertices", c_ushort),
		("nfaces", c_ushort),
		("pivot", vector3),
		("flags", c_ushort),
		("custom", c_void_p),
		("user", c_void_p),
		("crease_angle", c_float),
		("radius", c_float),
		("bounds", bounds3),
		("prepared", c_void_p),
		("stored", c_void_p),
		("nprimitive_lists", c_ushort),
		("primitive_list", c_void_p)
	]
