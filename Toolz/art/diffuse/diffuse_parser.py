import struct
import sys
import os
import construct

DIFFUSE_SIGNATURE   = 0x464C6469        # 'idLF' / 'FLdi'
DIFFUSE_VERSION     = 0x01

DIFFUSE_HEADER_SIZE = 0x18

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines).rstrip('\n')

DIFFUSE_Header = construct.Struct("DIFFUSE_Header",
                construct.ULInt32("signature"),             # + 0x00
                construct.ULInt32("version"),               # + 0x04
                construct.ULInt32("file_size"),             # + 0x08
                construct.ULInt32("unk_dword_00"),          # + 0x0C
                construct.ULInt16("unk_word_00"),           # + 0x10
                construct.ULInt16("unk_word_01"),           # + 0x12
                construct.ULInt32("unk_dword_01"),          # + 0x14
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
        
class Diffuse:

    def __init__(self, filename):
        self.file_size = os.stat(filename).st_size
        self.buf = Buffer(open(filename, "rb").read())
        self.header = DIFFUSE_Header.parse(self.buf.GetBufferSize(DIFFUSE_HEADER_SIZE))
        #self.header = DIFFUSE_Header.parse(self.buf.GetBufferSize(0x1C))
            
    def is_valid_diffuse(self):
        if self.header['signature'] != DIFFUSE_SIGNATURE:
            print "[-] Wrong DIFFUSE_SIGNATURE : %08X" % self.header['signature']
            return False
        if self.header['version'] != DIFFUSE_VERSION:
            print "[-] Wrong DIFFUSE_VERSION : %08X" % self.header['version']
            return False
        if self.header['file_size'] != self.file_size:
            print "[-] Wrong file_size : %08X != %08X" % (self.header['file_size'], self.file_size)
            return False
        return True

def print_diffuse_header(geom_header):
    print "[+] DIFFUSE_HEADER"
    print "  +0x00 signature        : 0x%08X" % geom_header['signature']
    print "  +0x04 version          : 0x%08X" % geom_header['version']
    print "  +0x08 file_size        : 0x%08X" % geom_header['file_size']
    print "  +0x0C unk_dword_00     : 0x%08X" % geom_header['unk_dword_00']
    print "  +0x10 unk_word_00      : 0x%04X" % geom_header['unk_word_00']
    print "  +0x12 unk_word_01      : 0x%04X" % geom_header['unk_word_01']
    print "  +0x14 unk_dword_01     : 0x%08X" % geom_header['unk_dword_01']
    print "-" * 20

# 0x0B * 0x0C    
    
def main():
    if len(sys.argv) != 2:
        print "Usage: %s <.diffuse>" % (sys.argv[0])
        sys.exit(1)
    diffuse = Diffuse(sys.argv[1])
    if diffuse.is_valid_diffuse() == False:
        sys.exit(1)
    print_diffuse_header(diffuse.header)
    for i in xrange(0, diffuse.header['unk_dword_01']):
        buf = diffuse.buf.GetBufferSize(0x4 + 0x2 + 0x2 + 0x4)
        saved_pos = diffuse.buf.pos
        print hexdump(buf)
        offset = struct.unpack("<I", buf[0:4])[0]
        print "[+] saved_pos : 0x%08X" % saved_pos
        print "[+] offset    : 0x%08X" % offset
        print "[+] com_offset: 0x%08X" % (((i + 2) * 0x0C) + offset)
        if offset != 0:
            #diffuse.buf.pos = diffuse.buf.pos - 0x0C + offset
            diffuse.buf.pos = (((i + 2) * 0x0C) + offset)
            print hexdump(diffuse.buf.GetBufferSize(0x10))
        print "-" * 20
  
        diffuse.buf.pos = saved_pos
    #print hexdump(diffuse.buf.buf[diffuse.buf.pos:])
    
if __name__ == "__main__":
    main()
