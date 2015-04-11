import struct
import sys
import os
import construct

GEOM_SIGNATURE      = 0x464c7367        # 'gsLF' / 'FLsg'
GEOM_VERSION        = 0x04

GEOM_HEADER_SIZE    = 0x20
MESH_DATA_SIZE      = 0x20
VERTEX_DATA_SIZE    = 0x20
TRIANGLES_DATA_SIZE = 0x06
BONES_SIZE          = 0x6C

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines).rstrip('\n')

GEOM_Header = construct.Struct("GEOM_Header",
                construct.ULInt32("signature"),             # + 0x00
                construct.ULInt32("version"),               # + 0x04
                construct.ULInt32("file_size"),             # + 0x08
                construct.ULInt32("unk_dword_00"),          # + 0x0C
                construct.ULInt32("nb_bones"),              # + 0x10
                construct.ULInt32("offset_bones"),          # + 0x14
                construct.ULInt32("nb_meshes"),             # + 0x18
                construct.ULInt32("offset_meshes"),         # + 0x1C
                               )

MESH_Data = construct.Struct("MESH_Data",
                construct.ULInt16("unk_word_00"),           # + 0x00
                construct.ULInt16("nb_vertices"),           # + 0x02
                construct.ULInt32("offset_vertices"),       # + 0x04
                construct.ULInt32("nb_triangles"),          # + 0x08
                construct.ULInt32("offset_triangles"),      # + 0x0C
                construct.ULInt32("unk_dword_00"),          # + 0x10
                construct.ULInt32("unk_dword_01"),          # + 0x14
                construct.ULInt32("unk_dword_02"),          # + 0x18
                construct.ULInt32("unk_dword_03"),          # + 0x1C
                               )

VERTEX_Data = construct.Struct("VERTEX_Data",
                construct.LFloat32("position_x"),           # + 0x00
                construct.LFloat32("position_y"),           # + 0x04
                construct.LFloat32("position_z"),           # + 0x08
                construct.LFloat32("normal_x"),             # + 0x0C
                construct.LFloat32("normal_y"),             # + 0x10
                construct.LFloat32("normal_z"),             # + 0x14
                construct.LFloat32("texture_u"),            # + 0x18
                construct.LFloat32("texture_v"),            # + 0x1C
                               )
              
TRIANGLES_Data = construct.Struct("TRIANGLES_Data",
                    construct.Array(3, construct.ULInt16("vertex_indice"))
                    )
              
BONES_Data = construct.Struct("BONES_Data",
                construct.ULInt32("offset_name"),           # + 0x00
                construct.ULInt32("unk_dword_01"),          # + 0x04
                construct.ULInt32("unk_dword_02"),          # + 0x08
                construct.ULInt32("unk_dword_03"),          # + 0x0C
                construct.ULInt32("unk_dword_04"),          # + 0x10
                construct.ULInt32("unk_dword_05"),          # + 0x14
                construct.ULInt32("unk_dword_06"),          # + 0x18
                construct.ULInt32("unk_dword_07"),          # + 0x1C
                construct.ULInt32("unk_dword_08"),          # + 0x20
                construct.ULInt32("unk_dword_09"),          # + 0x24
                construct.ULInt32("unk_dword_0A"),          # + 0x28
                construct.ULInt32("unk_dword_0B"),          # + 0x2C
                construct.ULInt32("unk_dword_0C"),          # + 0x30
                construct.ULInt32("unk_dword_0D"),          # + 0x34
                construct.ULInt32("unk_dword_0E"),          # + 0x38
                construct.ULInt32("unk_dword_0F"),          # + 0x3C
                construct.ULInt32("unk_dword_10"),          # + 0x40
                construct.ULInt32("unk_dword_11"),          # + 0x44
                construct.ULInt32("unk_dword_12"),          # + 0x48
                construct.ULInt32("unk_dword_13"),          # + 0x4C
                construct.ULInt32("unk_dword_14"),          # + 0x50
                construct.ULInt32("unk_dword_15"),          # + 0x54
                construct.ULInt32("unk_dword_16"),          # + 0x58
                construct.ULInt32("unk_dword_17"),          # + 0x5C
                construct.ULInt32("unk_dword_18"),          # + 0x60
                construct.ULInt32("unk_dword_19"),          # + 0x64
                construct.ULInt32("unk_dword_1A"),          # + 0x68
                )

class Buffer:

    def __init__(self, buf):
        self.buf = buf
        self.length = len(self.buf)
        self.pos = 0

    def GetByte(self):
        byte = struct.unpack("<B", self.buf[self.pos: self.pos + 1])[0]
        self.pos += 1
        return byte

    def GetWord(self, endian = "<"):
        word = struct.unpack(endian + "H", self.buf[self.pos: self.pos + 2])[0]
        self.pos += 2
        return word

    def GetDword(self, endian = "<"):
        dword = struct.unpack(endian + "I", self.buf[self.pos: self.pos + 4])[0]
        self.pos += 4
        return dword

    def GetBufferSize(self, size):
        buf = self.buf[self.pos: self.pos + size]
        self.pos += size
        return buf
        
class Geom:

    def __init__(self, filename):
        self.file_size = os.stat(filename).st_size
        self.buf = Buffer(open(filename, "rb").read())
        self.header = GEOM_Header.parse(self.buf.GetBufferSize(GEOM_HEADER_SIZE))
            
    def is_valid_geom(self):
        if self.header['signature'] != GEOM_SIGNATURE:
            print "[-] Wrong GEOM_SIGNATURE : %08X" % self.header['signature']
            return False
        if self.header['version'] != GEOM_VERSION:
            print "[-] Wrong GEOM_VERSION : %08X" % self.header['version']
            return False
        if self.header['file_size'] != self.file_size:
            print "[-] Wrong file_size : %08X != %08X" % (self.header['file_size'], self.file_size)
            return False
        return True
        
    def get_bones(self):
        bones = []
        self.buf.pos = self.header['offset_bones']
        for i in xrange(self.header['nb_bones']):
            bones.append(BONES_Data.parse(self.buf.GetBufferSize(BONES_SIZE)))
        return bones
            
    def get_meshes(self):
        meshes = []
        self.buf.pos = self.header['offset_meshes']
        for i in xrange(self.header['nb_meshes']):
            mesh_data = MESH_Data.parse(self.buf.GetBufferSize(MESH_DATA_SIZE))
            vertices = []
            triangles = []
            saved_pos = self.buf.pos
            
            self.buf.pos = self.header['offset_meshes'] + mesh_data['offset_vertices'] + i * MESH_DATA_SIZE
            for j in xrange(mesh_data['nb_vertices']):
                vertices.append(VERTEX_Data.parse(self.buf.GetBufferSize(VERTEX_DATA_SIZE)))
            self.buf.pos = self.header['offset_meshes'] + mesh_data['offset_triangles'] + i * MESH_DATA_SIZE
            for j in xrange(mesh_data['nb_triangles']):
                triangles.append(TRIANGLES_Data.parse((self.buf.GetBufferSize(TRIANGLES_DATA_SIZE))))
            self.buf.pos = saved_pos
            mesh_data['vertices'] = vertices
            mesh_data['triangles'] = triangles
            meshes.append(mesh_data)
        return meshes

def print_geom_header(geom_header):
    print "[+] GEOM_HEADER"
    print "  +0x00 signature        : 0x%08X" % geom_header['signature']
    print "  +0x04 version          : 0x%08X" % geom_header['version']
    print "  +0x08 file_size        : 0x%08X" % geom_header['file_size']
    print "  +0x0C unk_dword_00     : 0x%08X" % geom_header['unk_dword_00']
    print "  +0x10 nb_bones         : 0x%08X" % geom_header['nb_bones']
    print "  +0x14 offset_bones     : 0x%08X" % geom_header['offset_bones']
    print "  +0x18 nb_meshes        : 0x%08X" % geom_header['nb_meshes']
    print "  +0x1C offset_meshes    : 0x%08X" % geom_header['offset_meshes']
    print "-" * 20

def print_mesh_data(mesh_data):
    print "[+] MESH_DATA"
    print "  +0x00 unk_word_00      : 0x%04X" % mesh_data['unk_word_00']
    print "  +0x02 nb_vertices      : 0x%04X" % mesh_data['nb_vertices']
    print "  +0x04 offset_vertices  : 0x%08X" % mesh_data['offset_vertices']
    print "  +0x08 nb_triangles     : 0x%08X" % mesh_data['nb_triangles']
    print "  +0x0C offset_triangles : 0x%08X" % mesh_data['offset_triangles']
    print "  +0x10 unk_dword_00     : 0x%08X" % mesh_data['unk_dword_00']
    print "  +0x14 unk_dword_01     : 0x%08X" % mesh_data['unk_dword_01']
    print "  +0x18 unk_dword_02     : 0x%08X" % mesh_data['unk_dword_02']
    print "  +0x1C unk_dword_03     : 0x%08X" % mesh_data['unk_dword_03']
    print "-" * 20

def print_vertex_data(vertex_data):
    print "[+] VERTEX_DATA"
    print "  +0x00 position_x       : %f" % vertex_data['position_x']
    print "  +0x04 position_y       : %f" % vertex_data['position_y']
    print "  +0x08 position_z       : %f" % vertex_data['position_z']
    print "  +0x0C normal_x         : %f" % vertex_data['normal_x']
    print "  +0x10 normal_y         : %f" % vertex_data['normal_y']
    print "  +0x14 normal_z         : %f" % vertex_data['normal_z']
    print "  +0x18 texture_u        : %f" % vertex_data['texture_u']
    print "  +0x1C texture_v        : %f" % vertex_data['texture_v']
    print "-" * 20
    
def print_bones_data(bones_data):
    print "[+] BONES_DATA"
    print "  +0x00 offset_name      : 0x%08X" % bones_data['offset_name']
    print "  +0x04 unk_dword_01     : 0x%08X" % bones_data['unk_dword_01']
    print "  +0x08 unk_dword_02     : 0x%08X" % bones_data['unk_dword_02']
    print "  +0x0C unk_dword_03     : 0x%08X" % bones_data['unk_dword_03']
    print "  +0x10 unk_dword_04     : 0x%08X" % bones_data['unk_dword_04']
    print "  +0x14 unk_dword_05     : 0x%08X" % bones_data['unk_dword_05']
    print "  +0x18 unk_dword_06     : 0x%08X" % bones_data['unk_dword_06']
    print "  +0x1C unk_dword_07     : 0x%08X" % bones_data['unk_dword_07']
    print "  +0x20 unk_dword_08     : 0x%08X" % bones_data['unk_dword_08']
    print "  +0x24 unk_dword_09     : 0x%08X" % bones_data['unk_dword_09']
    print "  +0x28 unk_dword_0A     : 0x%08X" % bones_data['unk_dword_0A']
    print "  +0x2C unk_dword_0B     : 0x%08X" % bones_data['unk_dword_0B']
    print "  +0x30 unk_dword_0C     : 0x%08X" % bones_data['unk_dword_0C']
    print "  +0x34 unk_dword_0D     : 0x%08X" % bones_data['unk_dword_0D']
    print "  +0x38 unk_dword_0E     : 0x%08X" % bones_data['unk_dword_0E']
    print "  +0x3C unk_dword_0F     : 0x%08X" % bones_data['unk_dword_0F']
    print "  +0x40 unk_dword_10     : 0x%08X" % bones_data['unk_dword_10']
    print "  +0x44 unk_dword_11     : 0x%08X" % bones_data['unk_dword_11']
    print "  +0x48 unk_dword_12     : 0x%08X" % bones_data['unk_dword_12']
    print "  +0x4C unk_dword_13     : 0x%08X" % bones_data['unk_dword_13']
    print "  +0x50 unk_dword_14     : 0x%08X" % bones_data['unk_dword_14']
    print "  +0x54 unk_dword_15     : 0x%08X" % bones_data['unk_dword_15']
    print "  +0x58 unk_dword_16     : 0x%08X" % bones_data['unk_dword_16']
    print "  +0x5C unk_dword_17     : 0x%08X" % bones_data['unk_dword_17']
    print "  +0x60 unk_dword_18     : 0x%08X" % bones_data['unk_dword_18']
    print "  +0x64 unk_dword_19     : 0x%08X" % bones_data['unk_dword_19']
    print "  +0x68 unk_dword_1A     : 0x%08X" % bones_data['unk_dword_1A']
    print "-" * 20