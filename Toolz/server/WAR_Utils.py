import struct
import zlib
from binascii import hexlify
import colorama

###
#
###
class WarError(Exception):
    pass

LOG_LEVEL = 3

###
#
###
def LogInfo(buf, level = 1):
    colorama.init()
    if LOG_LEVEL >= level and level == 1:
        print colorama.Fore.GREEN + str(buf) + colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL
        return
    if LOG_LEVEL >= level and level == 2:
        print colorama.Fore.CYAN+ str(buf)+ colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL
        return
    if LOG_LEVEL >= level and level == 3:
        print colorama.Fore.MAGENTA  + str(buf) + colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL
        return
    else:
        #print buf
        return

###
#
###
def WAR_RC4(data, key, encrypt = True):
    j = 0
    i = 0
    out_first_half = []
    out_second_half = []
    half_len = (len(data) / 2)
    S = []
    for val in key:
        S.append(ord(val))
    for char in data[half_len:]:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i] , S[j] = S[j] , S[i]
        c = ord(char) ^ S[(S[i] + S[j]) % 256]
        out_second_half.append(chr(c))
        if encrypt == True:
            j = (j + ord(char)) % 256
        else:
            j = (j + c) % 256
    for char in data[:half_len]:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i] , S[j] = S[j] , S[i]
        c = ord(char) ^ S[(S[i] + S[j]) % 256]
        out_first_half.append(chr(c))
        if encrypt == True:
            j = (j + ord(char)) % 256
        else:
            j = (j + c) % 256
    return ''.join(out_first_half) + ''.join(out_second_half)

###
#
###
BYTE = "B"
WORD = "H"
DWORD = "I"
QWORD = "Q"

def padding(fmt):
    return "x" * (struct.calcsize(fmt) - 1) + "B"

def extract_str(str, data, endianness):
    struct_str = endianness + str
    unpack = struct.unpack(struct_str, data[:struct.calcsize(struct_str)])
    if len(unpack) == 1:
        i, = unpack
        return (i, data[struct.calcsize(struct_str):])
    return (list(unpack), data[struct.calcsize(struct_str):])

def depack(descr, data, endiannes = ">"):
    res_struct = dict()
    for field, value in iter(descr):
        if isinstance(value, basestring):
            if value in res_struct.keys():
                lfield, data = extract_str("B" * res_struct[value], data, endiannes)
                res_struct.update({field : lfield})
            else:
                lfield, data = extract_str(value, data, endiannes)
                res_struct.update({field : lfield})
            continue
        if isinstance(value, list):
            lfield, data = depack(value, data, endiannes)
            res_struct.update({field : lfield})
            continue
        if isinstance(value, tuple):
            res = []
            for descr in value:
                result, data = depack(descr, data, endiannes)
                res.append(result)
            res_struct.update({field : res})
            continue
        raise DescriptionError("Unhandled type for field : " + field)
    return (res_struct, data)

###
#
###
def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines).rstrip('\n')

###
#
###
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