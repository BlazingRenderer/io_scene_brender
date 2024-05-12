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
from brender.matrix import *
from brender.pixelmap import *
from brender.model import *
from brender.material import *
from brender.error import *

__author__ = "erysdren"
__version__ = "0.1.0"

####################################################
#
# private
#
####################################################

__BrLib = None

####################################################
#
# utilities
#
####################################################

def CSTR(s): return c_char_p(s.encode('ascii'))

####################################################
#
# startup/shutdown
#
####################################################

def Begin(libname="brender"):
	global __BrLib
	if __BrLib != None:
		return
	__BrLib = CDLL(libname)
	__BrLib.BrV1dbBeginWrapper()

	# set default findfailed hooks
	__BrLib.BrMapFindHook(__BrLib.BrMapFindFailedLoad)
	__BrLib.BrTableFindHook(__BrLib.BrTableFindFailedLoad)
	__BrLib.BrModelFindHook(__BrLib.BrModelFindFailedLoad)
	__BrLib.BrMaterialFindHook(__BrLib.BrMaterialFindFailedLoad)


def End():
	global __BrLib
	if __BrLib == None:
		return
	__BrLib.BrV1dbEndWrapper()
	__BrLib = None

####################################################
#
# misc
#
####################################################

# get error string
def StrError(error):
	__BrLib.BrStrError.argtypes = [c_uint]
	__BrLib.BrStrError.restype = c_char_p
	return __BrLib.BrStrError(error)

####################################################
#
# pixelmaps
#
####################################################

# allocate
def PixelmapAllocate(pm_type, width, height, pixels, flags):
	__BrLib.BrPixelmapAllocate.argtypes = [c_ubyte, c_int, c_int, c_void_p, c_int]
	__BrLib.BrPixelmapAllocate.restype = POINTER(pixelmap)
	if type(pixels) == "bytes":
		pixels = create_string_buffer(pixels, len(pixels))
	return __BrLib.BrPixelmapAllocate(pm_type, width, height, pixels, flags)

# free
def PixelmapFree(pm):
	__BrLib.BrPixelmapFree.argtypes = [POINTER(pixelmap)]
	__BrLib.BrPixelmapFree(pm)

# save
def PixelmapSave(filename, pm):
	__BrLib.BrPixelmapSave.argtypes = [c_char_p, POINTER(pixelmap)]
	__BrLib.BrPixelmapSave.restype = c_uint
	return __BrLib.BrPixelmapSave(CSTR(filename), pm)

# load
def PixelmapLoad(filename):
	__BrLib.BrPixelmapLoad.argtypes = [c_char_p]
	__BrLib.BrPixelmapLoad.restype = POINTER(pixelmap)
	return __BrLib.BrPixelmapLoad(CSTR(filename))

####################################################
#
# models
#
####################################################

# allocate
def ModelAllocate(name, nvertices, nfaces):
	__BrLib.BrModelAllocate.argtypes = [c_char_p, c_int, c_int]
	__BrLib.BrModelAllocate.restype = POINTER(model)
	return __BrLib.BrModelAllocate(CSTR(name), nvertices, nfaces)

# free
def ModelFree(m):
	__BrLib.BrModelFree.argtypes = [POINTER(model)]
	__BrLib.BrModelFree(m)

# save
def ModelSave(filename, m):
	__BrLib.BrModelSave.argtypes = [c_char_p, POINTER(model)]
	__BrLib.BrModelSave.restype = c_uint
	return __BrLib.BrModelSave(CSTR(filename), m)

# load
def ModelLoad(filename):
	__BrLib.BrModelLoad.argtypes = [c_char_p]
	__BrLib.BrModelLoad.restype = POINTER(model)
	return __BrLib.BrModelLoad(CSTR(filename))

####################################################
#
# materials
#
####################################################

# allocate
def MaterialAllocate(name):
	__BrLib.BrMaterialAllocate.argtypes = [c_char_p]
	__BrLib.BrMaterialAllocate.restype = POINTER(material)
	return __BrLib.BrMaterialAllocate(CSTR(name))

# free
def MaterialFree(m):
	__BrLib.BrMaterialFree.argtypes = [POINTER(material)]
	__BrLib.BrMaterialFree(m)

# save
def MaterialSave(filename, m):
	__BrLib.BrMaterialSave.argtypes = [c_char_p, POINTER(material)]
	__BrLib.BrMaterialSave.restype = c_uint
	return __BrLib.BrMaterialSave(CSTR(filename), m)

# load
def MaterialLoad(filename):
	__BrLib.BrMaterialLoad.argtypes = [c_char_p]
	__BrLib.BrMaterialLoad.restype = POINTER(material)
	return __BrLib.BrMaterialLoad(CSTR(filename))
