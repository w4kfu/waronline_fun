import struct
import sys
import os
import construct
import zlib
import string
import Image
import math

MYP_HEADER_SIZE = 40

MYP_Header = construct.Struct("MYP_Header",
                construct.ULInt32("signature"),             # + 0x00
                construct.ULInt32("version"),               # + 0x04
                construct.ULInt32("unk_dword_00"),          # + 0x08
                construct.ULInt64("offset_filetable"),      # + 0x0C
                construct.ULInt32("unk_dword_01"),          # + 0x14
                construct.ULInt32("nb_files"),              # + 0x18
                construct.ULInt32("unk_dword_02"),          # + 0x1C
                construct.ULInt32("unk_dword_03"),          # + 0x20
                construct.ULInt32("unk_dword_04")           # + 0x24
                )

MYP_FILETABLE_HEADER_SIZE = 12

MYP_FileTableHeader = construct.Struct("MYP_FileTableHeader",
                construct.ULInt32("nb_entry"),              # + 0x00
                construct.ULInt64("next_offset")            # + 0x04
                )

MYP_FILE_ENTRY_SIZE = 34

MYP_FileEntryHeader = construct.Struct("MYP_FileEntryHeader",
                construct.ULInt64("offset"),
                construct.ULInt32("size_header"),
                construct.ULInt32("sizez"),
                construct.ULInt32("size"),
                construct.ULInt64("name"),
                construct.ULInt32("crc"),
                construct.ULInt16("flag"),
                )

MYP_FILE_HEADER_SIZE = 64

MYP_FileHeader = construct.Struct("MYP_FileEntryHeader",
                construct.ULInt16("unk_word_00"),
                construct.ULInt8("unk_byte_00"),
                construct.ULInt16("unk_word_01"),
                construct.ULInt16("unk_word_02"),
                construct.ULInt8("unk_byte_01")
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

class StatFile:

    def __init__(self, name):
        self.name = name
        self.file_size = os.stat(sys.argv[1]).st_size
        self.fd = open(self.name, "rb")
        self.pos = 0
        self.nbread = 0
        self.range_read = list()

    def read(self, size):
        if (self.pos, self.pos + size) not in self.range_read:
            self.range_read.append((self.pos, self.pos + size))
            self.range_read = merge(self.range_read)
        self.nbread += size
        self.pos += size
        b = self.fd.read(size)
        return b

    def readat(self, size, pos):
        saved_pos = self.fd.tell()
        self.seek(pos)
        b = self.read(size)
        self.seek(saved_pos)
        return b

    def seek(self, pos, whence=0):
        self.pos = pos
        self.fd.seek(pos, whence)

    def get_remaining_bytes(self):
        return self.length - self.nbread

    def get_range_not_read(self):
        range_read = tuple(sorted(self.range_read))
        range_not_read = []
        for x, y in zip(range_read, range_read[1:]):
            if x[1] != y[0]:
                range_not_read.append((x[1], y[0] - 1))
        return range_not_read

    def output_picture(self):
        IMAGE_WIDTH = 128
        image_height = int(math.ceil(self.file_size / (IMAGE_WIDTH * 1.0)))
        image = Image.new("RGB", (IMAGE_WIDTH, image_height), "white")
        pix = image.load()
        index = 0
        l_range = self.get_range_not_read()
        for y in xrange(0, image_height):
            for x in xrange(0, IMAGE_WIDTH):
                color = 0xffff00
                for start, end in l_range:
                    if index > start and index < (end):
                        color = 0x0000ff
                        break
                pix[x, y] = color
                index += 1
                if index >= self.file_size:
                    image.convert("P").save(self.name + ".png", "PNG")
                    return
        image.convert("P").save(self.name + ".png", "PNG")
        return

class MYP:

    def __init__(self, name, hash_filename="hashes_filename.txt"):
        self.statfile = StatFile(name)
        self.hash_filename = hash_filename
        # HASH_VALUE / FILENAME
        self.hashval = {}
        self.myph = MYP_Header.parse(self.statfile.read(MYP_HEADER_SIZE))

    def load_hash(self):
        for line in open(self.hash_filename, "rb"):
            line = line.split("#")
            self.hashval[int(line[0] + line[1], 16)] = line[2]

    def is_valid_myp(self):
        if self.myph['signature'] != 0x0050594d:
            return False
        return True

    def get_nb_files(self):
        return self.myph['nb_files']

    def get_file_tables(self):
        file_tables = []
        self.statfile.seek(self.myph['offset_filetable'], 0)
        while True:
            file_table_header = MYP_FileTableHeader.parse(self.statfile.read(MYP_FILETABLE_HEADER_SIZE))
            file_table_header['foffset'] = self.statfile.pos
            file_tables.append(file_table_header)
            if file_table_header['next_offset'] == 0:
                break
            self.statfile.seek(file_table_header['next_offset'], 0)
        return file_tables

    def is_file_present(self, hashvalue):
        file_tables = self.get_file_tables()
        for file_table_header in file_tables:
            self.statfile.seek(file_table_header['foffset'])
            for i in xrange(0, file_table_header['nb_entry']):
                file_entry_header = MYP_FileEntryHeader.parse(self.statfile.read(MYP_FILE_ENTRY_SIZE))
                if file_entry_header['name'] == hashvalue:
                    return True
        return False

    def get_list_files(self):
        file_list = []
        file_tables = self.get_file_tables()
        for file_table_header in file_tables:
            self.statfile.seek(file_table_header['foffset'])
            for i in xrange(0, file_table_header['nb_entry']):
                file_entry_header = MYP_FileEntryHeader.parse(self.statfile.read(MYP_FILE_ENTRY_SIZE))
                if file_entry_header['name'] != 0:
                    file_list.append(file_entry_header)
        return file_list

    def extract_files(self, outdir="out"):
        for file_entry_header in self.get_list_files():
            self.statfile.seek(file_entry_header['offset'])
            self.statfile.read(file_entry_header['sizez'] + file_entry_header['size_header'])


    def print_myp_header(self):
        print "----- MYP HEADER -----"
        print "[+] magic            : 0x%08X (%d)" % (self.myph['signature'], self.myph['signature'])
        print "[+] version          : 0x%08X (%d)" % (self.myph['version'], self.myph['version'])
        print "[+] unk_dword_00     : 0x%08X (%d)" % (self.myph['unk_dword_00'], self.myph['unk_dword_00'])
        print "[+] offset_filetable : 0x%016lX (%d)" % (self.myph['offset_filetable'], self.myph['offset_filetable'])
        print "[+] unk_dword_01     : 0x%08X (%d)" % (self.myph['unk_dword_01'], self.myph['unk_dword_01'])
        print "[+] nb_files         : 0x%08X (%d)" % (self.myph['nb_files'], self.myph['nb_files'])
        print "[+] unk_dword_02     : 0x%08X (%d)" % (self.myph['unk_dword_02'], self.myph['unk_dword_02'])
        print "[+] unk_dword_03     : 0x%08X (%d)" % (self.myph['unk_dword_03'], self.myph['unk_dword_03'])
        print "[+] unk_dword_04     : 0x%08X (%d)" % (self.myph['unk_dword_04'], self.myph['unk_dword_04'])
        print "-" * 40

    def print_file_table_header(filetableh):
        print "----- MYP FILE TABLE HEADER -----"
        print "[+] nb_entry         : 0x%08X (%d)" % (filetableh['nb_entry'], filetableh['nb_entry'])
        print "[+] offset           : 0x%016lX (%d)" % (filetableh['offset'], filetableh['offset'])
        print "-" * 40

class Buffer:

    def __init__(self, buf):
        self.buf = buf
        self.length = len(self.buf)
        self.pos = 0
        self.nbread = 0
        self.range_read = list()

    def get_byte(self, endian="<"):
        byte = struct.unpack(endian + "B", self.buf[self.pos: self.pos + 1])[0]
        self.range_read.append((self.pos, self.pos + 1))
        self.pos += 1
        self.nbread += 1
        return byte

    def get_word(self, endian="<"):
        word = struct.unpack(endian + "H", self.buf[self.pos: self.pos + 2])[0]
        self.range_read.append((self.pos, self.pos + 2))
        self.pos += 2
        self.nbread += 2
        return word

    def get_dword(self, endian="<"):
        dword = struct.unpack(endian + "I", self.buf[self.pos: self.pos + 4])[0]
        self.range_read.append((self.pos, self.pos + 4))
        self.pos += 4
        self.nbread += 4
        return dword

    def get_qword(self, endian="<"):
        qword = struct.unpack(endian + "Q", self.buf[self.pos: self.pos + 8])[0]
        self.range_read.append((self.pos, self.pos + 8))
        self.pos += 8
        self.nbread += 8
        return qword

    def get_buffer_size(self, size):
        b = self.buf[self.pos: self.pos + size]
        self.range_read.append((self.pos, self.pos + size))
        self.pos += size
        self.nbread += size
        return b

    def get_buffer(self):
        size = self.GetDword()
        b = self.buf[self.pos:self.pos + size]
        self.range_read.append((self.pos, self.pos + size))
        self.pos += size
        self.nread += size
        return b

def handle_file_entry(myp_fd, myp_fileentry_header):
    #PrintFileEntry(myp_fileentry_header)
    if myp_fileentry_header['compressed'] == 0 and myp_fileentry_header['sizez'] > 32:
        #print "-----------"
        #print myp_fileentry_header
        myp_fd.seek(myp_fileentry_header['offset'], 0)
        if myp_fileentry_header['size_header'] != 0:
            data = myp_fd.read(myp_fileentry_header['size_header'])
            # 04 00 84 00 00 02 00 80
            #if data[7] != "\x80":
            PrintFileEntry(myp_fileentry_header)
            print hexdump(data)
        else:
            print "[-] NO SIZE HEADER!"
            PrintFileEntry(myp_fileentry_header)
            sys.exit(0)
        #myp_fd.seek(myp_fileentry_header['size_header'], 1)
        data = myp_fd.read(32)
        #print hexdump(data)
    else:
        myp_fd.seek(myp_fileentry_header['offset'], 0)
        myp_fd.seek(myp_fileentry_header['size_header'], 1)
        data = myp_fd.read(20)
        #print hexdump(data)
        #sys.exit(1)

def handle_myp(myp_fd, myp_header_data):
    #total
    print hex(myp_header_data['offset_filetable'])
    myp_fd.seek(myp_header_data['offset_filetable'], 0)
    while myp_header_data['all_nb_file'] != 0:
        filetable_header = myp_fd.read(MYP_FILETABLE_HEADER_SIZE)
        myp_filetable_header, data = depack(MYP_FILETABLE_HEADER, filetable_header, "<")
        #print hex(myp_filetable_header['offset'])
        #print myp_filetable_header
        for i in xrange(0, myp_filetable_header['nb_entry']):
            fileentry_header = myp_fd.read(MYP_FILE_ENTRY_SIZE)
            myp_fileentry_header, data = depack(MYP_FILE_ENTRY, fileentry_header, "<")
            myp_fd_saved_offset = myp_fd.tell()
            handle_file_entry(myp_fd, myp_fileentry_header)
            myp_fd.seek(myp_fd_saved_offset)
            #print myp_fileentry_header
            myp_header_data['all_nb_file'] = myp_header_data['all_nb_file'] - 1
            if myp_header_data['all_nb_file'] == 0:
                break
        myp_fd.seek(myp_filetable_header['offset'], 0)
        #raw_input('moo')

def PrintFileEntry(myp_fileentry):
    print "[+] offset      : 0x%08X" % myp_fileentry['offset']
    print "[+] size_header : 0x%08X" % myp_fileentry['size_header']
    print "[+] size        : 0x%08X" % myp_fileentry['size']
    print "[+] sizez       : 0x%08X" % myp_fileentry['sizez']
    print "[+] name        : 0x%016lX" % myp_fileentry['name']
    print "[+] crc         : 0x%08X" % myp_fileentry['crc']
    print "[+] compressed  : 0x%04X" % myp_fileentry['compressed']

def xchg_repr_hex(type):
    import ctypes
    type_id = id(type)
    as_nb = ctypes.c_uint.from_address(type_id + 0xc + (4 * (8 + 1))).value
    to_hex = ctypes.c_uint.from_address(as_nb + (4 * 22)).value
    to_dec = ctypes.c_uint.from_address(type_id + 0xc + (4 * (8))).value
    # Change type.__repr__ and type.__str__ by type.__hex__
    ctypes.c_uint.from_address(type_id + 0xc + (4 * (8))).value = to_hex  # __repr__
    ctypes.c_uint.from_address(type_id + 0xc + (4 * (8 + 6))).value = to_hex #__str__

#xchg_repr_hex(int)
#xchg_repr_hex(long)

def merge(times):
    l_new = []
    saved = list(times[0])
    for st, en in sorted([sorted(t) for t in times]):
        if st <= saved[1]:
            saved[1] = max(saved[1], en)
        else:
            l_new.append(tuple(saved))
            #yield tuple(saved)
            saved[0] = st
            saved[1] = en
    l_new.append(tuple(saved))
    return l_new
    #yield tuple(saved)

def search_extension(buf):
    if len(buf[:100].split(",")) > 10:
        #print ".csv"
        return ".csv"
    elif buf[0] == "\x42" and buf[1] == "\x49" and buf[2] == "\x4b" and buf[3] == "\x69":   # BIKi
        #print ".bik"
        return ".bik"
    elif buf[0] == "\x50" and buf[1] == "\x4B":
        #print ".zip"
        return ".zip"
    elif (buf[0] == "\xEF" and buf[1] == "\xBB" and buf[2] == "\xBF") or (buf[0] == "<" and ((buf[-2] == ">" and buf[-1] == "\x0A") or buf[-1] == ">")):
        #if (buf[0] == "<"):
        #    print hexdump(buf[-10:])
        #print ".xml"
        return ".xml"
    elif (buf[0] == "\x42" and buf[1] == "\x4d"):
        #print ".bmp"
        return ".bmp"
    elif all(c in string.printable for c in buf) == True:
        #print ".txt"
        return ".txt"
    elif (buf[0] == "\xFF" and buf[1] == "\xFE") or (buf[-3] == "\x00" and buf[-2] == "\x0a" and buf[-1] == "\x00"):#or all(c in string.printable for c, z in zip(*[iter(buf)]*2)) == True:
        #print ".unicode"
        #return ".unicode"
        return ".txt"
    else:
        return False
    return True

hashval = {}

def extract_file(myp_fd, fileentryh):
    saved_pos = myp_fd.tell()
    myp_fd.seek(fileentryh['offset'] + fileentryh['size_header'], 0)
    if fileentryh['flag'] == 1:
        buf = zlib.decompress(myp_fd.read(fileentryh['sizez']))
    elif fileentryh['flag'] == 0:
        buf = myp_fd.read(fileentryh['sizez'])
    else:
        print "[-] unknow flag"
        print fileentryh
        sys.exit(42)
    #buf = buf[:140]
    #if fileentryh['name'] == 0x3849E198A9F8A49D:
    #    sys.exit(42)
    #print fileentryh['name']
    ext = search_extension(buf)
    if ext == False:
        # [+] "data/bin/abilitycomponentexport.bin" = 4BE40EEE0832E506
        # [+] "data/bin/upgradetableexport.bin" = 62F986B75828AE17
        # [+] "data/bin/abilityexport.bin" = 4C76B1E3FE9C21EB
        # 2E39E785#C5E23305#data/gamedata/cursor_corner.tga#00000000
        # 5914CCF6#8066CBA5#data/strings/spanish/careerlines_f.txt#00000000
        # 7F6F0FDE#947B6B62#data/strings/spanish/careerlines_m.txt#00000000
        if fileentryh['name'] not in [0x4BE40EEE0832E506, 0x62F986B75828AE17, 0x4C76B1E3FE9C21EB, 0x2E39E785C5E23305, 0x5914CCF68066CBA5, 0x7F6F0FDE947B6B62]:
            print hex(fileentryh['name']).upper()
            print hexdump(buf[:100])
            open("test.bmp", "wb").write(buf)
            sys.exit(42)
    #if fileentryh['name'] == 0x3923A08ED6FCA73C:
    #    print "WUT!!"
    #    sys.exit(42)
    else:
        if fileentryh['name'] not in hashval.keys():
            print "[-] NOT FOUND in hashval", hex(fileentryh['name'])
        else:
            if not hashval[fileentryh['name']].endswith(ext):
                print "[-] WRONG EXT for %s, %s insted of %s" % (hex(fileentryh['name']), ext, hashval[fileentryh['name']])
        open("extracted/" + hex(fileentryh['name']) + ext, "wb").write(buf)
        #ext
    myp_fd.seek(saved_pos, 0)

def search_filename(hash_list):
    for root, dirs, files in os.walk("."):
        for f in files:
            fullpath = os.path.join(root, f)
            if f.endswith('.myp'):
                myp = MYP(fullpath)
                for hash in hash_list:
                    if myp.is_file_present(hash) == True:
                        print "[+] FOUND 0x%016lX inside %s" % (hash, fullpath)

def test(filename):
    for root, dirs, files in os.walk("."):
        for f in files:
            fullpath = os.path.join(root, f)
            if f.endswith('.myp'):
                myp = MYP(fullpath)
                if myp.is_file_present(0xF091BDF10149E70B) == True:
                    print "[+] FOUND 0x80074DF73BCD9C95 inside %s" % fullpath
                #print fullpath
                #print fullpath
    #for root, dirs, files in os.walk("."):
    #    for file in files:
    #        if file.endswith('.txt'):
    #            print file

def main():
    #search_filename([0x80074DF73BCD9C95, 0xF091BDF10149E70B])
    #test(sys.argv[1])
    #load_filename()
    if len(sys.argv) != 2:
        print "Usage: %s <.myp>" % (sys.argv[0])
        sys.exit(1)
    myp = MYP(sys.argv[1])
    print myp.statfile
    if myp.is_valid_myp() == False:
        print "[-] Not a valid MYP file"
        sys.exit(1)
    print "[+] nb_files : %08X (%d)" % (myp.get_nb_files(), myp.get_nb_files())
    print myp.get_file_tables()
    myp.print_myp_header()
    print myp.statfile

    print myp.is_file_present(0xF091BDF10149E70B)
    print myp.is_file_present(0x4242424242424242)
    print myp.is_file_present(0x80074DF73BCD9C95)

    l_files = myp.get_list_files()

    myp.extract_files()

    l_range = myp.statfile.get_range_not_read()

    print l_range

    for range_s, range_d in l_range:
        for file_entry_header in l_files:
            if range_s > file_entry_header['offset'] and range_s < file_entry_header['offset'] + file_entry_header['sizez'] + file_entry_header['size_header']:
                print "BUG DETECTED", (range_s, range_d)
                print file_entry_header
            if range_d > file_entry_header['offset'] and range_d < file_entry_header['offset'] + file_entry_header['sizez'] + file_entry_header['size_header']:
                print "BUG DETECTED", (range_s, range_d)
                print file_entry_header

    myp.statfile.output_picture()

    sys.exit(42)


    nb_files_read = 0
    nb_bytes_read = 0
    file_size = os.stat(sys.argv[1]).st_size
    #range_not_read = set([x for x in xrange(0, file_size)])
    range_read = list()
    pos = 0

    myp_fd = open(sys.argv[1], "rb")
    buf = myp_fd.read(MYP_HEADER_SIZE)
    nb_bytes_read += MYP_HEADER_SIZE
    range_read.append((pos, pos + MYP_HEADER_SIZE))
    #for z in xrange(pos, pos + MYP_HEADER_SIZE):
        #range_not_read.remove(z)
    pos += MYP_HEADER_SIZE
    myph = MYP_Header.parse(buf)
    if myph['signature'] != 0x0050594d:
        print "[-] Wrong signature!"
        sys.exit(1)
    print_myp_header(myph)
    myp_fd.seek(myph['offset_filetable'], 0)
    pos = myph['offset_filetable']
    #print "[+] myp_fd.tell() : %08X" % myp_fd.tell()
    while True:
        buf = myp_fd.read(MYP_FILETABLE_HEADER_SIZE)
        # filetableh = MYP_FileTableHeader.parse(buf)
        #for z in xrange(pos, pos + MYP_FILETABLE_HEADER_SIZE):
            #range_not_read.remove(z)
        range_read.append((pos, pos + MYP_FILETABLE_HEADER_SIZE))
        pos += MYP_FILETABLE_HEADER_SIZE
        nb_bytes_read += MYP_FILETABLE_HEADER_SIZE
        filetableh = MYP_FileTableHeader.parse(buf)
        print_file_table_header(filetableh)
        #saved_offset =
        #print "[+] next_off ? : %08X" % (myp_fd.tell() + filetableh['nb_entry'] * MYP_FILE_ENTRY_SIZE)
        #print "[+] offset     : %08X" % (filetableh['offset'])
        #myp_fd.seek(filetableh['offset'], 0)
        #print filetableh
        for i in xrange(0, filetableh['nb_entry']):

            buf = myp_fd.read(MYP_FILE_ENTRY_SIZE)
            #fileentryh = MYP_FileEntryHeader.parse(buf)
            nb_bytes_read += MYP_FILE_ENTRY_SIZE
            #for z in xrange(pos, pos + MYP_FILE_ENTRY_SIZE):
            #    range_not_read.remove(z)
            range_read.append((pos, pos + MYP_FILE_ENTRY_SIZE))
            pos += MYP_FILE_ENTRY_SIZE
            saved_pos = pos

            fileentryh = MYP_FileEntryHeader.parse(buf)
            if fileentryh['offset'] != 0 and fileentryh['sizez'] != 0 and fileentryh['size'] != 0:
                if fileentryh['offset'] >= 39016 and fileentryh['offset'] <= 39016 + 10:
                    print fileentryh
                extract_file(myp_fd, fileentryh)
                #if nb_files_read == 0:
                #    print hex(fileentryh['offset'])
                nb_files_read = nb_files_read + 1
                nb_bytes_read = nb_bytes_read + fileentryh['sizez'] + fileentryh['size_header']
                pos = fileentryh['offset']
                #for z in xrange(pos, pos + fileentryh['sizez'] + fileentryh['size_header']):
                    #range_not_read.remove(z)
                range_read.append((pos, pos + fileentryh['sizez'] + fileentryh['size_header']))
                pos += fileentryh['sizez'] + fileentryh['size_header']
            pos = saved_pos
            #    continue
            #print fileentryh
            #print fileentryh
        if filetableh['offset'] == 0:
            break
        myp_fd.seek(filetableh['offset'], 0)
        pos = filetableh['offset']
        print "MOO"
    print "[+] nb_files_read : %08X" % nb_files_read
    #print "[+] all_nb_file   : %08X" % myph['all_nb_file']
    print "[+] file_size     : %08X" % file_size
    print "[+] nb_bytes_read : %08X" % nb_bytes_read
    #print range_not_read
    return
    import itertools
    import operator
    print "[+] range!"
    #print range_read
    #for times in range_read:
    #range_read = list(merge(range_read))
    #range_read.sort(key=operator.itemgetter(1))
    range_read = tuple(sorted(range_read))
    range_not_read = []
    for x, y in zip(range_read, range_read[1:]):
        #print x, y
        if x[1] != y[0]:
            range_not_read.append((x[1] + 1, y[0] - 1))
    print range_not_read
    #range_read.sort()
    #print range_read
    #range_not_read = []
    #for f, t in range_read:
    #    range_not_read.append(t,
    #for k, g in itertools.groupby(enumerate(range_not_read), lambda (i,x):i-x):
    #    l = map(operator.itemgetter(1), g)
    #    myp_fd.seek(l[0], 0)
    for l in range_not_read:
        myp_fd.seek(l[0], 0)
        buf = myp_fd.read(l[-1] - l[0])
        if MYP_FILE_HEADER_SIZE > (l[-1] - l[0]):
            continue

        print hexdump(buf[:100])
        fileh = MYP_FileHeader.parse(buf)
        print fileh
        b = buf[(fileh['unk_byte_00'] + 2 + 2):]
        if len(b) == 0:
            continue
        if (b[0] == "\x78"):
            import zlib
            print hexdump(zlib.decompress(b[:100]))
        else:
            print hexdump(b[:100])

    #else:
        #PrintMYPHeader(myp_header_data)
        #handle_myp(myp_fd, myp_header_data)
    myp_fd.close()

if __name__ == "__main__":
    main()