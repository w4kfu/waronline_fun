import struct
import sys
import os
import construct

GEOM_SIGNATURE      = 0x464c7367
GEOM_VERSION        = 0x04

GEOM_HEADER_SIZE    = 0x20
MESH_DATA_SIZE      = 0x20
VERTEX_DATA_SIZE    = 0x20

BONES_SIZE          = 0x6C

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

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines).rstrip('\n')

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

def is_valid_geom(geom_header, file_size):
    if geom_header['signature'] != GEOM_SIGNATURE:
        print "[-] Wrong GEOM_SIGNATURE : %08X" % geom_header['signature']
        return False
    if geom_header['version'] != GEOM_VERSION:
        print "[-] Wrong GEOM_VERSION : %08X" % geom_header['version']
        return False
    if geom_header['file_size'] != file_size:
        print "[-] Wrong file_size : %08X != %08X" % (geom_header['file_size'], file_size)
        return False
    return True
    
def main():
    search_specific_geom()
    fd_out = open("test.obj", "wb")
    if len(sys.argv) != 2:
        print "Usage: %s <.geom>" % (sys.argv[0])
        sys.exit(1)
    file_size = os.stat(sys.argv[1]).st_size
    geom_buf = Buffer(open(sys.argv[1], "rb").read())
    geom_header = GEOM_Header.parse(geom_buf.GetBufferSize(GEOM_HEADER_SIZE))
    if is_valid_geom(geom_header, file_size) == False:
        sys.exit(1)
    print_geom_header(geom_header)

    #print "[+] offset_bones + nb_bones * 0x6C : 0x%08X" % (geom_header['offset_bones'] + geom_header['nb_bones'] * 0x6C)
    # TODO BONES !
    geom_buf.pos = geom_header['offset_bones']
    for i in xrange(geom_header['nb_bones']):
        #print "[+] actual offset    : 0x%08X" % buf.pos
        buf = geom_buf.GetBufferSize(BONES_SIZE)
        #print "-" * 20

    nb_vertices = 0
    geom_buf.pos = geom_header['offset_meshes']
    for i in xrange(geom_header['nb_meshes']):
        fd_out.write("o test.%d\n" % i)
        mesh_data = MESH_Data.parse(geom_buf.GetBufferSize(0x20))
        print_mesh_data(mesh_data)
        saved_pos = geom_buf.pos
        geom_buf.pos = geom_header['offset_meshes'] + mesh_data['offset_vertices'] + i * 0x20
        for j in xrange(mesh_data['nb_vertices']):
            vertex_data = VERTEX_Data.parse(geom_buf.GetBufferSize(VERTEX_DATA_SIZE))
            print_vertex_data(vertex_data)
            fd_out.write("v %f %f %f\n" % (vertex_data['position_x'], vertex_data['position_y'], vertex_data['position_z']))
            #fd_out.write("vn %f %f %f\n" % (vertex_data['normal_x'], vertex_data['normal_y'], vertex_data['normal_z']))
        geom_buf.pos = geom_header['offset_meshes'] + mesh_data['offset_triangles'] + i * 0x20
        for j in xrange(mesh_data['nb_triangles']):
            buff = geom_buf.GetBufferSize(0x6)
            w1, w2, w3 = struct.unpack("<HHH", buff)
            fd_out.write("f %d %d %d\n" % (w1 + 1 + nb_vertices, w2 + 1 + nb_vertices, w3 + 1 + nb_vertices))
        geom_buf.pos = saved_pos
        nb_vertices += mesh_data['nb_vertices']
    fd_out.close()

if __name__ == "__main__":
    main()
