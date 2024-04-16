# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class BrenderDatafile(KaitaiStruct):
    """This is a generic container format used by the BRender rendering engine created by
    Argonaut Technologies. Internally, it's known as a "datafile".
    It can contain models, pixelmaps, and actors.
    
    It was also used by Carmageddon, and possibly Carmageddon 2.
    Other BRender engine games may also make use of it.
    I haven't checked many of them.
    
    Origin of this file: https://github.com/erysdren/Formats
    
    .. seealso::
       fw/formats.h
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.chunks = []
        i = 0
        while not self._io.is_eof():
            self.chunks.append(BrenderDatafile.BrDatafileChunkT(self._io, self, self._root))
            i += 1


    class BrVertexIndexT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_vertices = self._io.read_u4be()
            self.vertices = []
            for i in range(self.num_vertices):
                self.vertices.append(BrenderDatafile.BrVertexT(self._io, self, self._root))



    class BrPixelmapNewT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.bitmap_type = self._io.read_bits_int_be(8)
            self._io.align_to_byte()
            self.row_bytes = self._io.read_u2be()
            self.width = self._io.read_u2be()
            self.height = self._io.read_u2be()
            self.origin_x = self._io.read_u2be()
            self.origin_y = self._io.read_u2be()
            self.mip_offset = self._io.read_u2be()
            self.identifier = (self._io.read_bytes_term(0, False, True, True)).decode(u"ascii")


    class BrFaceIndexT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_faces = self._io.read_u4be()
            self.faces = []
            for i in range(self.num_faces):
                self.faces.append(BrenderDatafile.BrFaceT(self._io, self, self._root))



    class BrDatafileChunkT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._io.read_u4be()
            if self.type < 65536:
                self.len_data = self._io.read_u4be()

            _on = self.type
            if _on == 61:
                self.data = BrenderDatafile.BrPixelmapNewT(self._io, self, self._root)
            elif _on == 0:
                self.data = BrenderDatafile.BrTerminatorT(self._io, self, self._root)
            elif _on == 24:
                self.data = BrenderDatafile.BrUvIndexT(self._io, self, self._root)
            elif _on == 35:
                self.data = BrenderDatafile.BrActorT(self._io, self, self._root)
            elif _on == 3:
                self.data = BrenderDatafile.BrPixelmapT(self._io, self, self._root)
            elif _on == 33:
                self.data = BrenderDatafile.BrPixelsT(self._io, self, self._root)
            elif _on == 23:
                self.data = BrenderDatafile.BrVertexIndexT(self._io, self, self._root)
            elif _on == 53:
                self.data = BrenderDatafile.BrFaceIndexT(self._io, self, self._root)
            elif _on == 36:
                self.data = BrenderDatafile.BrActorModelT(self._io, self, self._root)
            elif _on == 18:
                self.data = BrenderDatafile.BrFileIndexT(self._io, self, self._root)
            elif _on == 26:
                self.data = BrenderDatafile.BrFaceMaterialIndexT(self._io, self, self._root)
            elif _on == 54:
                self.data = BrenderDatafile.BrModelT(self._io, self, self._root)
            elif _on == 22:
                self.data = BrenderDatafile.BrMaterialIndexT(self._io, self, self._root)
            else:
                self.data = BrenderDatafile.BrUnknownT(self._io, self, self._root)


    class BrMaterialIndexT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_materials = self._io.read_u4be()
            self.materials = []
            for i in range(self.num_materials):
                self.materials.append(BrenderDatafile.BrMaterialT(self._io, self, self._root))



    class BrUnknownT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes(self._parent.len_data)


    class BrFaceT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.vertex_indices = []
            for i in range(3):
                self.vertex_indices.append(self._io.read_u2be())

            self.smoothing = self._io.read_u2be()
            self.flags = self._io.read_u1()


    class BrPixelmapT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.bitmap_type = self._io.read_bits_int_be(8)
            self._io.align_to_byte()
            self.row_bytes = self._io.read_u2be()
            self.width = self._io.read_u2be()
            self.height = self._io.read_u2be()
            self.origin_x = self._io.read_u2be()
            self.origin_y = self._io.read_u2be()
            self.identifier = (self._io.read_bytes_term(0, False, True, True)).decode(u"ascii")


    class BrFileIndexT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = self._io.read_u4be()
            self.version = self._io.read_u4be()


    class BrUvT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.u = self._io.read_f4be()
            self.v = self._io.read_f4be()


    class BrPixelsT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_pixels = self._io.read_u4be()
            self.len_pixel = self._io.read_u4be()
            if self.len_pixel == 1:
                self.data_paletted = []
                for i in range((self.len_pixel * self.num_pixels)):
                    self.data_paletted.append(self._io.read_u1())


            if self.len_pixel == 2:
                self.data_depth = []
                for i in range((self.len_pixel * self.num_pixels) // 2):
                    self.data_depth.append(self._io.read_u2be())


            if self.len_pixel == 3:
                self.data_rgb = []
                for i in range((self.len_pixel * self.num_pixels) // 3):
                    self.data_rgb.append(BrenderDatafile.RgbT(self._io, self, self._root))


            if self.len_pixel == 4:
                self.data_argb = []
                for i in range((self.len_pixel * self.num_pixels) // 4):
                    self.data_argb.append(BrenderDatafile.ArgbT(self._io, self, self._root))




    class BrActorModelT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.identifier = (self._io.read_bytes_term(0, False, True, True)).decode(u"ascii")


    class ArgbT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.a = self._io.read_u1()
            self.r = self._io.read_u1()
            self.g = self._io.read_u1()
            self.b = self._io.read_u1()


    class BrVertexT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.coords = []
            for i in range(3):
                self.coords.append(self._io.read_f4be())



    class BrActorT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.actor_type = self._io.read_u1()
            self.render_style = self._io.read_u1()
            self.identifier = (self._io.read_bytes_term(0, False, True, True)).decode(u"ascii")


    class BrFaceMaterialIndexT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_face_materials = self._io.read_u4be()
            self.len_face_material = self._io.read_u4be()
            self.face_materials = []
            for i in range(self.num_face_materials):
                self.face_materials.append(self._io.read_u2be())



    class BrMaterialT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.identifier = (self._io.read_bytes_term(0, False, True, True)).decode(u"ascii")


    class BrModelT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.flags = self._io.read_u2be()
            self.identifier = (self._io.read_bytes_term(0, False, True, True)).decode(u"ascii")


    class BrUvIndexT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_uvs = self._io.read_u4be()
            self.uvs = []
            for i in range(self.num_uvs):
                self.uvs.append(BrenderDatafile.BrUvT(self._io, self, self._root))



    class RgbT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.r = self._io.read_u1()
            self.g = self._io.read_u1()
            self.b = self._io.read_u1()


    class BrTerminatorT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass



