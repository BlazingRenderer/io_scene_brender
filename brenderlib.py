#
# Imports
#

import sys, getopt, os
import struct, numpy

#
# BRender file constants
#

# file types (for reading)
BR_FILE_VERSION = 2
BR_FILE_MODELS = 64206
BR_FILE_PIXELMAPS = 2
BR_FILE_TERMINATOR = 0

# file types (for writing)
BR_FILE_VERSION_B = b"\x00\x00\x00\x02"
BR_FILE_MODELS_B = b"\x00\x00\xFA\xCE"
BR_FILE_PIXELMAPS_B = b"\x00\x00\x00\x02"
BR_FILE_TERMINATOR_B = b"\x00\x00\x00\x00"

# top-level chunk types
BR_CHUNK_PIXELMAP = 3
BR_CHUNK_FILEINFO = 18
BR_CHUNK_PIXELDATA = 33
BR_CHUNK_MODEL = 54

# model subchunk types
BR_CHUNK_VERTICES = 23
BR_CHUNK_MATERIALS = 22
BR_CHUNK_UVS = 24
BR_CHUNK_MATERIAL_ASSIGNMENTS = 26
BR_CHUNK_FACES = 53

# bitmap types
BR_PIXELMAP_8BIT = 3
BR_PIXELMAP_ARGB = 7

#
# BRenderLib class
#

class BRenderLib:

	#
	# initialization
	#

	def __init__(self, outpath):
		self.outpath = outpath

	#
	# file I/O operations
	#

	# open file and write header chunk
	def OpenDataFile(self, filetype):
		self.file = open(self.outpath, "wb")
		self.WriteChunk(BR_CHUNK_FILEINFO, filetype)

	# close file when done
	def CloseDataFile(self):
		self.file.close()

	#
	# writing data to file
	#

	# writing chunks to file
	def WriteChunk(self, identifier, data):
		self.file.write(struct.pack(">i", identifier))
		self.file.write(struct.pack(">i", len(data)))
		self.file.write(struct.pack(">" + "B" * len(data), *data))

	def WriteTerminator(self):
		self.file.write(struct.pack(">" + "B" * len(BR_FILE_TERMINATOR_B), *BR_FILE_TERMINATOR_B))

	# write model
	def WriteModel(self, identifier, vertices, uvs, faces, materials, material_assignments):
		self.WriteChunk(BR_CHUNK_MODEL, identifier)
		self.WriteChunk(BR_CHUNK_VERTICES, vertices)
		self.WriteChunk(BR_CHUNK_UVS, uvs)
		self.WriteChunk(BR_CHUNK_FACES, faces)
		self.WriteChunk(BR_CHUNK_MATERIALS, materials)
		self.WriteChunk(BR_CHUNK_MATERIAL_ASSIGNMENTS, material_assignments)
		self.WriteTerminator()
