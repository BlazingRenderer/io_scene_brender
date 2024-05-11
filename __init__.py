#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports
import os, sys, struct
import bpy, bmesh
import brender as Br
from bpy_extras.io_utils import ExportHelper, ImportHelper
from bpy.props import StringProperty, CollectionProperty, BoolProperty, EnumProperty

# bl_info
bl_info = {
	"name": "BRender (DAT) format",
	"author": "erysdren (it/she/they)",
	"version": (1, 0, 0),
	"blender": (4, 1, 0),
	"location": "File > Export, File > Import",
	"description": "BRender model import and export",
	"warning": "",
	"doc_url": "https://github.com/BlazingRenderer/io_scene_brender",
	"support": "COMMUNITY",
	"category": "Export",
}

#
# useful functions
#

def add_mesh(name, vertices, edges, polys):
	mesh = bpy.data.meshes.new(name)
	mesh.from_pydata(vertices, edges, polys)
	mesh.vertex_colors.new()
	mesh.uv_layers.new()
	mesh.update()
	return mesh

def add_object(name, mesh):
	obj = bpy.data.objects.new(name, mesh)
	return obj

def link_object(obj):
	scene.collection.objects.link(obj)

def write_material(name):
	mat = bpy.data.materials.new(name)
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes["Principled BSDF"]
	return mat

#
# register, unregister, etc
#

def menu_func_import(self, context):
	self.layout.operator(ImportBRender.bl_idname, text="BRender Model (.dat)")

def menu_func_export(self, context):
	self.layout.operator(ExportBRender.bl_idname, text="BRender Model (.dat)")

def register():
	bpy.utils.register_class(ExportBRender)
	bpy.utils.register_class(ImportBRender)
	bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
	bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

	# decide brender lib name
	if os.name == "nt":
		lib = "libbrender.dll"
	else:
		lib = "libbrender.so"

	# make path absolute
	lib = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + lib

	# init brender
	Br.Begin(lib)

def unregister():
	bpy.utils.unregister_class(ExportBRender)
	bpy.utils.unregister_class(ImportBRender)
	bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
	bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

	# close brender
	Br.End()

if __name__ == "__main__":
	register()

#
# main import class
#

class ImportBRender(bpy.types.Operator, ImportHelper):
	"""Import a BRender Model (.dat) File"""
	bl_idname = "import.brender_dat"
	bl_label = "Import BRender Model (.dat)"
	bl_options = {'UNDO'}

	# hidden properties
	filepath : StringProperty(name="File Path", description="Filepath used for importing the DAT file", maxlen=1024, default="", options={'HIDDEN'})
	files : CollectionProperty(type=bpy.types.OperatorFileListElement, options={'HIDDEN'})
	directory : StringProperty(maxlen=1024, default="", subtype='FILE_PATH', options={'HIDDEN'})
	filter_folder : BoolProperty(name="Filter Folders", description="", default=True, options={'HIDDEN'})
	filter_glob : StringProperty(default="*.dat;*.DAT", options={'HIDDEN'})

	def execute(self, context):

		print(f"importing {self.filepath}")

		mdl = Br.ModelLoad(self.filepath)
		if mdl == None:
			print(f"failed to import {self.filepath}")
		else:
			print(f"successfully imported {self.filepath}")
			Br.ModelFree(mdl)

		return {"FINISHED"}

#
# main export class
#

class ExportBRender(bpy.types.Operator, ExportHelper):
	"""Export a BRender Model (.dat) File"""
	bl_idname = "export.brender_dat"
	bl_label = "Export BRender Model (.dat)"

	filename_ext = ".dat"
	filter_glob: StringProperty(default="*.dat", options={"HIDDEN"})

	def execute(self, context):
		return {"FINISHED"}
