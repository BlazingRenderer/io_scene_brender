# 
# EXPORT BRENDER DAT
# 

# modules
from ast import Import
import os, sys, math, struct, time
import numpy
sys.path.append(os.path.dirname(__file__))

from brenderlib import *
import kaitaistruct
from brender_datafile import BrenderDatafile

# blender python modules
import bpy
import bmesh

from bpy_extras.io_utils import ExportHelper, ImportHelper
from bpy.props import StringProperty, CollectionProperty, BoolProperty, EnumProperty

# bl_info
bl_info = {
	"name": "BRender (DAT) format",
	"author": "erysdren (it/she/they)",
	"version": (0, 0, 2),
	"blender": (3, 2, 0),
	"location": "File > Export, File > Import",
	"description": "BRender model import and export",
	"warning": "",
	"doc_url": "https://github.com/BlazingRenderer/io_scene_brender",
	"support": "COMMUNITY",
	"category": "Export",
}

def menu_func_import(self, context):
	self.layout.operator(ImportBRender.bl_idname, text="BRender model (.dat)")

def menu_func_export(self, context):
	self.layout.operator(ExportBRender.bl_idname, text="BRender model (.dat)")

def register():
	bpy.utils.register_class(ExportBRender)
	bpy.utils.register_class(ImportBRender)
	bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
	bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
	bpy.utils.unregister_class(ExportBRender)
	bpy.utils.unregister_class(ImportBRender)
	bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
	bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
	register()

class ImportBRender(bpy.types.Operator, ImportHelper):
	"""Import a BRender Model (.dat) File"""
	bl_idname = "import.brender_dat"
	bl_label = "Import BRender Model"
	bl_options = {'UNDO'}

	# hidden properties
	filepath : StringProperty(name="File Path", description="Filepath used for importing the DAT file", maxlen=1024, default="", options={'HIDDEN'})
	files : CollectionProperty(type=bpy.types.OperatorFileListElement, options={'HIDDEN'})
	directory : StringProperty(maxlen=1024, default="", subtype='FILE_PATH', options={'HIDDEN'})
	filter_folder : BoolProperty(name="Filter Folders", description="", default=True, options={'HIDDEN'})
	filter_glob : StringProperty(default="*.dat;", options={'HIDDEN'})

	def execute(self, context):
		print("Reading %s..." % self.filepath)

		name = bpy.path.display_name(bpy.path.basename(self.filepath), has_ext=False, title_case=False)
		scene = bpy.context.scene

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
			object = bpy.data.objects.new(name, mesh)

			return object

		def link_object(object):
			scene.collection.objects.link(object)

		def write_material(name):
			mat = bpy.data.materials.new(name = name)
			mat.use_nodes = True
			bsdf = mat.node_tree.nodes["Principled BSDF"]

			return mat

		BrImport = BrenderDatafile.from_file(self.filepath)

		BrModels = []

		# stuff to put into the model
		BrIdentifier = ""
		BrVertices = []
		BrFaces = []
		BrMaterials = []
		BrAssignments = []
		BrUVs = []

		BrChunk = BrImport.BrDatafileChunkT
		BrVertex = BrImport.BrVertexT
		BrFace = BrImport.BrFaceT
		BrMaterial = BrImport.BrMaterialT
		BrUV = BrImport.BrUvT

		m = 0

		# determine how many models are in the file
		for BrChunk in BrImport.chunks:
			if BrChunk.type == BR_CHUNK_FILEINFO:
				if BrChunk.data.type != BR_FILE_MODELS:
					raise ImportError("Valid BRender datafile, but does not contain models!")
			if BrChunk.type == BR_CHUNK_MODEL:
				BrModels.append([])
				BrIdentifier = BrChunk.data.identifier
				BrModels[m].append([BR_CHUNK_MODEL, BrIdentifier])
			if BrChunk.type == BR_CHUNK_VERTICES:
				for BrVertex in BrChunk.data.vertices:
					BrVertices.append([BrVertex.coords[0], BrVertex.coords[1], BrVertex.coords[2]])
				BrModels[m].append([BR_CHUNK_VERTICES, BrVertices])
			if BrChunk.type == BR_CHUNK_UVS:
				for BrUV in BrChunk.data.uvs:
					BrUVs.append((BrUV.u, BrUV.v))
				BrModels[m].append([BR_CHUNK_UVS, BrUVs])
			if BrChunk.type == BR_CHUNK_FACES:
				for BrFace in BrChunk.data.faces:
					BrFaces.append([BrFace.vertex_indices[0], BrFace.vertex_indices[1], BrFace.vertex_indices[2]])
				BrModels[m].append([BR_CHUNK_FACES, BrFaces])
			if BrChunk.type == BR_CHUNK_MATERIALS:
				for BrMaterial in BrChunk.data.materials:
					mat = write_material(BrMaterial.identifier)
					BrMaterials.append(mat)
				BrModels[m].append([BR_CHUNK_MATERIALS, BrMaterials])
			if BrChunk.type == BR_CHUNK_MATERIAL_ASSIGNMENTS:
				for BrAssignment in BrChunk.data.face_materials:
					BrAssignments.append(BrAssignment)
				BrModels[m].append([BR_CHUNK_MATERIAL_ASSIGNMENTS, BrAssignments])
			if BrChunk.type == BR_FILE_TERMINATOR:
				BrIdentifier = ""
				BrVertices = []
				BrFaces = []
				BrMaterials = []
				BrAssignments = []
				BrUVs = []
				m += 1

		# calculate models
		for BrModel in BrModels:
			BrIdentifier = ""
			BrVertices = []
			BrFaces = []
			BrMaterials = []
			BrAssignments = []
			BrUVs = []

			# first pass - parse geometry
			for BrModelChunk in BrModel:
				if BrModelChunk[0] == BR_CHUNK_MODEL:
					BrIdentifier = BrModelChunk[1]
				if BrModelChunk[0] == BR_CHUNK_VERTICES:
					BrVertices = BrModelChunk[1]
				if BrModelChunk[0] == BR_CHUNK_FACES:
					BrFaces = BrModelChunk[1]

			# create mesh
			BrMesh = add_mesh(BrIdentifier, BrVertices, [], BrFaces)

			# second pass - parse UVs
			for BrModelChunk in BrModel:
				if BrModelChunk[0] == BR_CHUNK_UVS:
					BrUVs = BrModelChunk[1]

			# add UVs to mesh
			for poly in BrMesh.polygons:
				for loop_index in poly.loop_indices:
					BrMesh.uv_layers.active.data[loop_index].uv = BrUVs[BrMesh.loops[loop_index].vertex_index]

			# create object
			BrObj = add_object(BrIdentifier, BrMesh)

			# third pass - parse materials
			for BrModelChunk in BrModel:
				if BrModelChunk[0] == BR_CHUNK_MATERIALS:
					for mat in BrModelChunk[1]:
						BrObj.data.materials.append(mat)
				if BrModelChunk[0] == BR_CHUNK_MATERIAL_ASSIGNMENTS:
					for a, assignment in enumerate(BrModelChunk[1]):
						BrObj.data.polygons[a].material_index = assignment

			# link object to scene
			link_object(BrObj)

		return {"FINISHED"}

class ExportBRender(bpy.types.Operator, ExportHelper):
	"""Export a BRender Model (.dat) File"""
	bl_idname = "export.brender_dat"
	bl_label = "Export BRender Model"

	filename_ext = ".dat"
	filter_glob: StringProperty(default="*.dat", options={"HIDDEN"})

	def execute(self, context):
		print("Saving %s..." % self.properties.filepath)

		duration = time.time()

		out_model = BRenderLib(self.properties.filepath)
		out_model.OpenDataFile(BR_FILE_MODELS)

		for i, object in enumerate(context.scene.objects):
			mesh = object.to_mesh()

			# triangulate mesh
			bm = bmesh.new()
			bm.from_mesh(mesh)
			bmesh.ops.triangulate(bm, faces=bm.faces)
			bm.to_mesh(mesh)
			bm.free

			print(f"Exporting object {i}: {mesh.name}\n")

			model_id = b"\x00\x00" # flags
			model_id += mesh.name.encode("ascii") + b"\x00" # identifier

			# calculate vertex data chunk
			num_verts = len(mesh.vertices)
			vertices = struct.pack(">I", num_verts)

			for vertex in mesh.vertices:
				coords = object.matrix_world @ vertex.co
				vertices += struct.pack(">f", coords[0])
				vertices += struct.pack(">f", coords[1])
				vertices += struct.pack(">f", coords[2])

			# calculate face and UV data chunks
			num_uvs = num_verts
			uvs = struct.pack(">I", num_uvs)

			num_faces = len(mesh.polygons)
			faces = struct.pack(">I", num_faces)

			num_materials = len(mesh.materials)
			materials = struct.pack(">I", num_materials)

			for material in mesh.materials:
				materials += material.name.encode("ascii") + b"\x00"

				for node in material.node_tree.nodes:
					if node.type == "TEX_IMAGE":
						print(os.path.splitext(os.path.normpath(bpy.path.abspath(node.image.filepath, library=node.image.library)))[0] + ".pix")

			num_material_assignments = num_faces
			material_assignments = struct.pack(">I", num_material_assignments)
			material_assignments += struct.pack(">I", 2)

			# initialize temp arrays
			uv_array = [None] * num_uvs
			material_index_array = [None] * num_faces

			for poly in mesh.polygons:
				for vert_idx, loop_idx in zip(poly.vertices, poly.loop_indices):
					uv_coords = mesh.uv_layers.active.data[loop_idx].uv
					uv_array[vert_idx] = [uv_coords.x, uv_coords.y]
					# print(f"{vert_idx}: {uv_coords.x:.2f} {uv_coords.y:.2f}")
					faces += struct.pack(">H", vert_idx)

				faces += struct.pack(">H", 1) # smoothing
				faces += struct.pack(">B", 0) # flags

				material_index_array[poly.index] = poly.material_index + 1

			for mi in material_index_array:
				material_assignments += struct.pack(">H", mi)

			for u, uv in enumerate(uv_array):
				if uv == None:
					print(f"UV coord {u} is Null, for some reason.")
					uvs += struct.pack(">f", 0)
					uvs += struct.pack(">f", 0)
				else:
					uvs += struct.pack(">f", uv[0])
					uvs += struct.pack(">f", uv[1])

			out_model.WriteModel(model_id, vertices, uvs, faces, materials, material_assignments)

		out_model.CloseDataFile()

		if os.path.exists(self.properties.filepath):
			print(f"Successfully exported {os.path.split(self.properties.filepath)[1]} in {time.time() - duration:.2f} seconds")
		else:
			print(f"WARNING: Failed to export model {os.path.split(self.properties.filepath)[1]}")
		
		return {"FINISHED"}
