#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports
import os, sys, struct
import bpy, bmesh
from bpy_extras.io_utils import ExportHelper, ImportHelper
from bpy.props import StringProperty, CollectionProperty, BoolProperty, EnumProperty

# for brender import
sys.path.append(os.path.dirname(__file__))
import brender as Br

# bl_info
bl_info = {
	"name": "BRender (DAT) format",
	"author": "erysdren (it/she/they)",
	"version": (0, 1, 0),
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
	bpy.context.scene.collection.objects.link(obj)

def add_material(name):
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
	print("io_scene_brender: BRender successfully initialized.")

def unregister():
	bpy.utils.unregister_class(ExportBRender)
	bpy.utils.unregister_class(ImportBRender)
	bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
	bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

	# close brender
	Br.End()
	print("io_scene_brender: BRender successfully shutdown.")

if __name__ == "__main__":
	register()

#
# main import class
#

class ImportBRender(bpy.types.Operator, ImportHelper):
	"""Import a BRender Model (.dat) File"""
	bl_idname = "import.brender_dat"
	bl_label = "Import BRender Model (.dat)"
	bl_options = {"UNDO"}

	# hidden properties
	filepath : StringProperty(name="File Path", description="Filepath used for importing the DAT file", maxlen=1024, default="", options={"HIDDEN"})
	files : CollectionProperty(type=bpy.types.OperatorFileListElement, options={"HIDDEN"})
	directory : StringProperty(maxlen=1024, default="", subtype="FILE_PATH", options={"HIDDEN"})
	filter_folder : BoolProperty(name="Filter Folders", description="", default=True, options={"HIDDEN"})
	filter_glob : StringProperty(default="*.dat;*.DAT", options={"HIDDEN"})

	def execute(self, context):

		# load with BRender
		model = Br.ModelLoad(self.filepath)
		if model == None:
			print(f"io_scene_brender: Failed to load \"{self.filepath}\"")
			return {"CANCELLED"}

		print(f"io_scene_brender: Successfully loaded \"{self.filepath}\"")

		# setup arrays
		vertices = []
		faces = []
		uvs = []
		edges = []
		assignments = []

		# start parsing model data
		identifier = model.contents.identifier.decode("ascii")

		# reel in vertices and uvs
		for i in range(0, model.contents.nvertices):
			vertices.append([model.contents.vertices[i].p.x, model.contents.vertices[i].p.y, model.contents.vertices[i].p.z])
			uvs.append([model.contents.vertices[i].map.x, model.contents.vertices[i].map.y])

		# reel in faces and materials
		for i in range(0, model.contents.nfaces):
			faces.append([model.contents.faces[i].vertices[0],
				 model.contents.faces[i].vertices[1],
				 model.contents.faces[i].vertices[2]])

		# create mesh
		mesh = add_mesh(identifier, vertices, edges, faces)

		# add uvs to mesh
		for poly in mesh.polygons:
			for loop_index in poly.loop_indices:
				mesh.uv_layers.active.data[loop_index].uv = uvs[mesh.loops[loop_index].vertex_index]

		# create object
		obj = add_object(identifier, mesh)

		# add material assignments to object

		# link object
		link_object(obj)

		# free model
		Br.ModelFree(model)

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

		# each object in the scene is a discrete model in the datafile
		for i, obj in enumerate(context.scene.objects):
			mesh = obj.to_mesh()

			# triangulate mesh
			bm = bmesh.new()
			bm.from_mesh(mesh)
			bmesh.ops.triangulate(bm, faces=bm.faces)
			bm.to_mesh(mesh)
			bm.free

			# allocate brender model
			model = Br.ModelAllocate(mesh.name, len(mesh.vertices), len(mesh.polygons))

			uv_array = [None] * len(mesh.vertices)

			# write in faces and fetch uvs
			for p, poly in enumerate(mesh.polygons):
				i = 0
				for vert_idx, loop_idx in zip(poly.vertices, poly.loop_indices):

					# save uv coords
					uv_coords = mesh.uv_layers.active.data[loop_idx].uv
					uv_array[vert_idx] = [uv_coords.x, uv_coords.y]

					# add vertex idx
					model.contents.faces[p].vertices[i] = vert_idx
					i += 1

			# write in vertices
			for v, vert in enumerate(mesh.vertices):
				coords = obj.matrix_world @ vert.co
				model.contents.vertices[v].p.x = coords[0]
				model.contents.vertices[v].p.y = coords[1]
				model.contents.vertices[v].p.z = coords[2]
				model.contents.vertices[v].map.x = uv_array[v][0]
				model.contents.vertices[v].map.y = uv_array[v][1]

			# save model to disk
			Br.ModelSave(self.filepath, model)

			# free model
			Br.ModelFree(model)

		return {"FINISHED"}
