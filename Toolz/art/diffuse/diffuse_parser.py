import struct
import sys
import os
import construct

DIFFUSE_SIGNATURE   = 0x464C6469        # 'idLF' / 'FLdi'
DIFFUSE_VERSION     = 0x01

DIFFUSE_HEADER_SIZE = 0x18
MIPMAP_DATA_SIZE    = 0x0C

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
                construct.ULInt16("mipmap_width_max"),      # + 0x10
                construct.ULInt16("mipmap_height_max"),     # + 0x12
                construct.ULInt32("num_mipmaps"),           # + 0x14
                               )
                               
MIPMAP_Data = construct.Struct("MIPMAP_Data",
                construct.ULInt32("offset"),                # + 0x00
                construct.ULInt16("width"),                 # + 0x04
                construct.ULInt16("height"),                # + 0x06
                construct.ULInt32("unk_dword_00"),          # + 0x08
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
    print "  +0x10 mipmap_width_max : 0x%04X" % geom_header['mipmap_width_max']
    print "  +0x12 mipmap_height_max: 0x%04X" % geom_header['mipmap_height_max']
    print "  +0x14 num_mipmaps      : 0x%08X" % geom_header['num_mipmaps']
    print "-" * 20

def print_mipmap_data(mipmap_data):
    print "[+] MIPMAP_DATA"
    print "  +0x00 offset           : 0x%08X" % mipmap_data['offset']
    print "  +0x04 width            : 0x%04X" % mipmap_data['width']
    print "  +0x06 height           : 0x%04X" % mipmap_data['height']
    print "  +0x08 unk_dword_00     : 0x%08X" % mipmap_data['unk_dword_00']
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
    for i in xrange(0, diffuse.header['num_mipmaps']):
        mipmap_data = MIPMAP_Data.parse(diffuse.buf.GetBufferSize(MIPMAP_DATA_SIZE))
        saved_pos = diffuse.buf.pos
        print_mipmap_data(mipmap_data)
        if mipmap_data['offset'] != 0:
            diffuse.buf.pos = diffuse.buf.pos - 0x0C + mipmap_data['offset']
            buf = diffuse.buf.GetBufferSize(mipmap_data['width'] * mipmap_data['height'] / 2)
            print hexdump(buf[:0x10])
            decoded = pythonDecodeDXT1(buf)
            data = []
            for d in decoded:
                print len(d)
                data.append(d)
            data = ''.join(data)
            print len(data)
            import Image
            img = Image.new('RGB', (mipmap_data['height'], mipmap_data['width']), "black")
            img.fromstring(data)
            img.save("test_%d.png" % i, "PNG")
        print "-" * 20
  
        diffuse.buf.pos = saved_pos
    
# Python-only DXT1 decoder; this is slow!
# Better to use _dxt1.decodeDXT1 if you can
# (it's used automatically if available by DdsImageFile)
def pythonDecodeDXT1(data):
    # input: one "row" of data (i.e. will produce 4*width pixels)
    blocks = len(data) / 8  # number of blocks in row
    out = ['', '', '', '']  # row accumulators

    for xb in xrange(blocks):
        # Decode next 8-byte block.        
        c0, c1, bits = struct.unpack('<HHI', data[xb*8:xb*8+8])

        # color 0, packed 5-6-5
        b0 = (c0 & 0x1f) << 3
        g0 = ((c0 >> 5) & 0x3f) << 2
        r0 = ((c0 >> 11) & 0x1f) << 3
        
        # color 1, packed 5-6-5
        b1 = (c1 & 0x1f) << 3
        g1 = ((c1 >> 5) & 0x3f) << 2
        r1 = ((c1 >> 11) & 0x1f) << 3

        # Decode this block into 4x4 pixels
        # Accumulate the results onto our 4 row accumulators
        for yo in xrange(4):
            for xo in xrange(4):
                # get next control op and generate a pixel
                
                control = bits & 3
                bits = bits >> 2
                if control == 0:
                    out[yo] += chr(r0) + chr(g0) + chr(b0)
                elif control == 1:
                    out[yo] += chr(r1) + chr(g1) + chr(b1)
                elif control == 2:                                
                    if c0 > c1:
                        out[yo] += chr((2 * r0 + r1 + 1) / 3) + chr((2 * g0 + g1 + 1) / 3) + chr((2 * b0 + b1 + 1) / 3)
                    else:
                        out[yo] += chr((r0 + r1) / 2) + chr((g0 + g1) / 2) + chr((b0 + b1) / 2)
                elif control == 3:
                    if c0 > c1:
                        out[yo] += chr((2 * r1 + r0 + 1) / 3) + chr((2 * g1 + g0 + 1) / 3) + chr((2 * b1 + b0 + 1) / 3)
                    else:
                        out[yo] += '\0\0\0'

    # All done.
    return tuple(out)

if __name__ == "__main__":
    main()