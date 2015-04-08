import struct
import sys
import os
import construct

GEOM_SIGNATURE      = 0x464c7367
GEOM_VERSION        = 0x04

GEOM_HEADER_SIZE    = 40
MESH_SIZE           = 0x20
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

MESH_Header = construct.Struct("MESH_Header",
                construct.ULInt16("unk_word_00"),           # + 0x00
                construct.ULInt16("unk_nb_00"),             # + 0x02
                construct.ULInt32("unk_off_00"),            # + 0x04
                construct.ULInt32("unk_nb_01"),             # + 0x08
                construct.ULInt32("unk_off_01"),            # + 0x0C
                construct.ULInt32("unk_dword_04"),          # + 0x10
                construct.ULInt32("unk_dword_05"),          # + 0x14
                construct.ULInt32("unk_dword_06"),          # + 0x18
                construct.ULInt32("unk_dword_07"),          # + 0x1C
                               )

VERTEX_Header = construct.Struct("VERTEX_Header",
                construct.LFloat32("unk_float_00"),         # + 0x00
                construct.LFloat32("unk_float_01"),         # + 0x04
                construct.LFloat32("unk_float_02"),         # + 0x08
                construct.LFloat32("unk_float_03"),         # + 0x0C
                construct.LFloat32("unk_float_04"),         # + 0x10
                construct.LFloat32("unk_float_05"),         # + 0x14
                construct.LFloat32("unk_float_06"),         # + 0x18
                construct.LFloat32("unk_float_07"),         # + 0x1C
                #construct.LFloat32("unk_float_08"),         # + 0x20
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
    print "[+] signature        : 0x%08X" % geom_header['signature']
    print "[+] version          : 0x%08X" % geom_header['version']
    print "[+] file_size        : 0x%08X" % geom_header['file_size']
    print "[+] unk_dword_00     : 0x%08X" % geom_header['unk_dword_00']
    print "[+] nb_bones         : 0x%08X" % geom_header['nb_bones']
    print "[+] offset_bones     : 0x%08X" % geom_header['offset_bones']
    print "[+] nb_meshes        : 0x%08X" % geom_header['nb_meshes']
    print "[+] offset_meshes    : 0x%08X" % geom_header['offset_meshes']
    print "-" * 20

def print_mesh_header(mesh_header):
    print "[+] unk_word_00      : 0x%04X" % mesh_header['unk_word_00']
    print "[+] unk_nb_00        : 0x%04X" % mesh_header['unk_nb_00']
    print "[+] unk_off_00       : 0x%08X" % mesh_header['unk_off_00']
    print "[+] unk_nb_01        : 0x%08X" % mesh_header['unk_nb_01']
    print "[+] unk_off_01       : 0x%08X" % mesh_header['unk_off_01']
    print "[+] unk_dword_04     : 0x%08X" % mesh_header['unk_dword_04']
    print "[+] unk_dword_05     : 0x%08X" % mesh_header['unk_dword_05']
    print "[+] unk_dword_06     : 0x%08X" % mesh_header['unk_dword_06']
    print "[+] unk_dword_07     : 0x%08X" % mesh_header['unk_dword_07']
    print "[+] unk_off_00 + unk_nb_00 * 0x20 : 0x%08X" % (mesh_header['unk_off_00']  + mesh_header['unk_nb_00'] * 0x20)
    print "-" * 20

def print_vertex_header(vertex_header):
    print "[+] unk_float_00     : %f" % vertex_header['unk_float_00']
    print "[+] unk_float_01     : %f" % vertex_header['unk_float_01']
    print "[+] unk_float_02     : %f" % vertex_header['unk_float_02']
    print "[+] unk_float_03     : %f" % vertex_header['unk_float_03']
    print "[+] unk_float_04     : %f" % vertex_header['unk_float_04']
    print "[+] unk_float_05     : %f" % vertex_header['unk_float_05']
    print "[+] unk_float_06     : %f" % vertex_header['unk_float_06']
    print "[+] unk_float_07     : %f" % vertex_header['unk_float_07']
    print "v %f %f %f" % (vertex_header['unk_float_00'], vertex_header['unk_float_02'], vertex_header['unk_float_01'])
    print "-" * 20

def main():
    fd_out = open("test.obj", "wb")
    fd_out.write("o test.001\n")
    if len(sys.argv) != 2:
        print "Usage: %s <.geom>" % (sys.argv[0])
        sys.exit(1)
    file_size = os.stat(sys.argv[1]).st_size
    buf = Buffer(open(sys.argv[1], "rb").read())
    header_buf = buf.GetBufferSize(GEOM_HEADER_SIZE)
    geom_header = GEOM_Header.parse(header_buf)
    #signature = buf.GetDword()
    print_geom_header(geom_header)
    if geom_header['signature'] != GEOM_SIGNATURE:
        print "[-] Wrong GEOM_SIGNATURE : %08X" % geom_header['signature']
        sys.exit(42)
    if geom_header['version'] != GEOM_VERSION:
        print "[-] Wrong GEOM_VERSION : %08X" % geom_header['version']
        sys.exit(42)
    if geom_header['file_size'] != file_size:
        print "[-] Wrong file_size : %08X != %08X" % (geom_header['file_size'], file_size)
        sys.exit(42)
    print "[+] offset_bones + nb_bones * 0x6C : 0x%08X" % (geom_header['offset_bones'] + geom_header['nb_bones'] * 0x6C)
    buf.pos = geom_header['offset_bones']
    for i in xrange(geom_header['nb_bones']):
        print "[+] actual offset    : 0x%08X" % buf.pos
        header_buf = buf.GetBufferSize(BONES_SIZE)
        print "-" * 20
        
    buf.pos = geom_header['offset_meshes']
    for i in xrange(geom_header['nb_meshes']):
        print "[+] actual offset    : 0x%08X" % buf.pos
        header_buf = buf.GetBufferSize(MESH_SIZE)
        mesh_header = MESH_Header.parse(header_buf)
        print_mesh_header(mesh_header)
        saved_pos = buf.pos
        buf.pos = buf.pos - MESH_SIZE + mesh_header['unk_off_00']
        for j in xrange(mesh_header['unk_nb_00']):
            header_buf = buf.GetBufferSize(0x20)
            print hexdump(header_buf)
            vertex_header = VERTEX_Header.parse(header_buf)
            print_vertex_header(vertex_header)
            fd_out.write("v %f %f %f\n" % (vertex_header['unk_float_00'], vertex_header['unk_float_01'], vertex_header['unk_float_02']))
            #fd_out.write("vn %f %f %f\n" % (vertex_header['unk_float_03'], vertex_header['unk_float_04'], vertex_header['unk_float_05']))
        buf.pos = saved_pos

        save_pos = buf.pos
        buf.pos = saved_pos - MESH_SIZE + mesh_header['unk_off_01']
        for j in xrange(mesh_header['unk_nb_01']):
            buff = buf.GetBufferSize(0x6)
            w1, w2, w3 = struct.unpack("<HHH", buff)
            print "[+] w1 : 0x%04X ; w2 : 0x%04X ; w3 : 0x%04X" % (w1, w2, w3)
            #fd_out.write("l %d %d\n" % (w1 + 1, w2 + 1))
            #fd_out.write("l %d %d\n" % (w2 + 1, w3 + 1))
            #fd_out.write("l %d %d\n" % (w1 + 1, w3 + 1))
            fd_out.write("f %d %d %d\n" % (w1 + 1, w2 + 1, w3 + 1))
        buf.pos = saved_pos
        
        
    #print hex(signature)
    fd_out.close()

if __name__ == "__main__":
    main()
