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

# vector2
class vector2(Structure):
	_fields_ = [("x", c_float), ("y", c_float)]

# vector3
class vector3(Structure):
	_fields_ = [("x", c_float), ("y", c_float), ("z", c_float)]

# vector4
class vector4(Structure):
	_fields_ = [("x", c_float), ("y", c_float), ("z", c_float), ("w", c_float)]

# bounds2
class bounds2(Structure):
	_fields_ = [("min", vector2), ("max", vector2)]

# bounds3
class bounds3(Structure):
	_fields_ = [("min", vector3), ("max", vector3)]

# bounds4
class bounds4(Structure):
	_fields_ = [("min", vector4), ("max", vector4)]

