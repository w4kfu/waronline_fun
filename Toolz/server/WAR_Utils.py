import struct
import zlib
from binascii import hexlify

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines)

def MakeBBuffer(buf):
    p = struct.pack(">B", len(buf))
    p += buf
    return p

def MakeBuffer(buf):
    p = struct.pack(">H", len(buf))
    p += buf + "\x00"
    return p

def MakeUnkBuffer(buf):
    p = struct.pack(">B", len(buf))
    p += buf
    return p

def GetByte(buf):
    byte = struct.unpack(">B", buf[:1])[0]
    return (byte, buf[1:])

def GetWord(buf):
    word = struct.unpack(">H", buf[:2])[0]
    return (word, buf[2:])

def GetDword(buf):
    dword = struct.unpack(">I", buf[:4])[0]
    return (dword, buf[4:])

def GetQword(buf):
    qword = struct.unpack(">Q", buf[:8])[0]
    return (qword, buf[8:])

def GetBufferSize(buf, size):
    buffer = buf[:(size)]
    return (buffer, buf[(size):])

def GetBuffer(buf):
    size, buf = GetWord(buf)
    buffer = buf[:(size + 1)]
    return (size, buffer, buf[(size + 1):])