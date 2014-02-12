import struct

BYTE = "B"
WORD = "H"
DWORD = "I"
QWORD = "Q"

MYP_HEADER_SIZE = 36

MYP_HEADER = [
    ("magic", DWORD),
    ("version", DWORD),
    ("unk_dword_00", DWORD),
    ("offset_filetable", QWORD),
    ("nb_file", DWORD),
    ("all_nb_file", DWORD),
    ("nb_filetable", DWORD),
    ("nb_filetable2", DWORD),
    ]

MYP_FILETABLE_HEADER_SIZE = 12

MYP_FILETABLE_HEADER = [
    ("nb_entry", DWORD),
    ("offset", QWORD),
    ]

MYP_FILE_ENTRY_SIZE = 34

MYP_FILE_ENTRY = [
    ("offset", QWORD),
    ("size_header", DWORD),
    ("cmp_size", DWORD),
    ("ucmp_size", DWORD),
    ("name", QWORD),
    ("crc", DWORD),
    ("compressed", WORD)
    ]

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines).rstrip('\n')

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

def handle_file_entry(myp_fd, myp_fileentry_header):
    if myp_fileentry_header['compressed'] == 0 and myp_fileentry_header['ucmp_size'] > 32:
        print "-----------"
        print myp_fileentry_header
        myp_fd.seek(myp_fileentry_header['offset'], 0)
        myp_fd.seek(myp_fileentry_header['size_header'], 1)
        data = myp_fd.read(32)
        print hexdump(data)

def handle_myp(myp_fd, myp_header_data):
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

if __name__ == "__main__":
    myp_fd = open("data.myp", "rb")
    myp_header = myp_fd.read(MYP_HEADER_SIZE)
    myp_header_data, data = depack(MYP_HEADER, myp_header, "<")
    if myp_header_data['magic'] != 0x0050594d:
        print "[-] Wrong magic!"
    else:
        print myp_header_data
        handle_myp(myp_fd, myp_header_data)
    myp_fd.close()
