#[Client] packet : (0x13) F_REQUEST_CHAR_TEMPLATES  Size = 13
#|------------------------------------------------|----------------|
#|00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F |0123456789ABCDEF|
#|------------------------------------------------|----------------|
#|00 01 00 00 00 00 FF FE 00 13 00 00 00          |.............   |
#-------------------------------------------------------------------
#[Client] packet : (0x5C) F_ENCRYPTKEY  Size = 18
#|------------------------------------------------|----------------|
#|00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F |0123456789ABCDEF|
#|------------------------------------------------|----------------|
#|00 06 00 01 00 00 00 00 00 5C 00 35 01 04 08 00 |.........\.5....|
#|00 00                                           |..              |
#-------------------------------------------------------------------

import struct

FILENAME = "sniff_h00m39.txt"

PATTERN_SIZE = "Size = "

BYTE = "B"
WORD = "H"
DWORD = "I"
QWORD = "Q"

def padding(fmt):
    return "x" * (struct.calcsize(fmt) - 1) + "B"

PACKET_CLIENT_HEADER = [
        ("sequence_packet", WORD),
        ("session_id_packet", WORD),
        ("unk_word_00", WORD),
        ("unk_byte_00", BYTE),
        ("opcode_packet", BYTE),
        ]

PACKET_SERVER_HEADER = [
        ("opcode_packet", BYTE)
        ]

PACKET_F_REQUEST_CHAR_TEMPLATES = [
        ("unk_byte_00", BYTE)
        ]

PACKET_F_ENCRYPTKEY = [
        ("key_present", BYTE),
        ("unk_byte_00", BYTE),
        ("major_version", BYTE),
        ("minor_version", BYTE),
        ("revision_version", BYTE),
        ("unk_byte_01", BYTE)]

        #unk_word_00, buf = WAR_Utils.GetWord(buf)
        #unk_byte_00, buf = WAR_Utils.GetByte(buf)
        #unk_byte_01, buf = WAR_Utils.GetByte(buf)
        #unk_data_00, buf = WAR_Utils.GetBufferSize(buf, 24)
        #ns_port, buf = WAR_Utils.GetWord(buf)
        #langage, buf = WAR_Utils.GetBufferSize(buf, 6)
        #unk_dword_00, buf = WAR_Utils.GetDword(buf)
        #unk_dword_01, buf = WAR_Utils.GetDword(buf)
        #unk_dword_02, buf = WAR_Utils.GetDword(buf)

PACKET_F_PLAYER_ENTER_FULL = [
        ("unk_word_00", WORD),
        ("unk_byte_00", BYTE),
        ("unk_byte_01", BYTE),
        ("unk_data_00", BYTE * 24),
        ("ns_port", WORD),
        ("langage", BYTE * 6),
        ("unk_dword_00", DWORD),
        ("unk_dword_01", DWORD),
        ("unk_dword_01", DWORD),
]

PACKET_F_CONNECT = [
        ("unk_byte_00", BYTE),
        ("unk_byte_01", BYTE),
        ("major_version", BYTE),
        ("minor_version", BYTE),
        ("revision_version", BYTE),
        ("unk_byte_02", BYTE),
        ("unk_word_00", WORD),
        ("protocol_version", DWORD),
        ("session_id", BYTE * 101),
        ("username", BYTE * 21),
        ("size_xml", WORD)
]

PACKET_F_REQUEST_CHAR = [
        ("action", WORD),
        ("unk_byte_00", BYTE),
]

PACKET_F_PLAYER_EXIT = [
        ("session_id", WORD),
        ("unk_word_00", WORD),
]

PACKET_F_PING = [
        ("timestamp", DWORD),
        ("unk_dword_01", DWORD),
        ("unk_dword_02", DWORD),
        ("unk_word_00", WORD),
        ("unk_word_01", WORD),
        ("unk_word_02", WORD),
        ("unk_word_03", WORD),
]

PACKET_F_DELETE_NAME = [
    ("char_name", BYTE * 24),
    ("padding", padding(6 * BYTE)),
    ("user_name", BYTE * 24)
]

PACKET_F_CREATE_CHARACTER = [
    ("unk_byte_00", BYTE),
    ("unk_byte_01", BYTE),
    ("unk_byte_02", BYTE),
    ("sex", BYTE),
    ("unk_word_00", WORD),
    ("nickname_size", BYTE),
    ("unk_byte_05", BYTE),
    ("unk_byte_06", BYTE),
    ("face_attributes", BYTE * 0xF),
    ("nickname", "nickname_size"),
    ("buffer_unk_byte_05", "unk_byte_05"),
    ("unk_byte_07", BYTE),
]

PACKET_F_DUMP_ARENAS_LARGE = [
    ("unk_byte_00", BYTE),
    ("unk_byte_01", BYTE),
]

PACKET_F_OPEN_GAME = [
    ("unk_byte_00", BYTE),
    ("unk_byte_01", BYTE),
]

PACKET_F_PLAYER_STATE2 = [
    ("unk_dword_00", DWORD),
    ("unk_byte_00", BYTE),
]

PACKET_F_INTERFACE_COMMAND = [
    ("unk_byte_00", BYTE),
    ("unk_byte_01", BYTE),
    ("unk_word_00", WORD),
    ("unk_word_01", WORD),
]

PACKET_F_INIT_PLAYER = [
    ("unk_word_00", WORD),
    ("unk_word_01", WORD),
    ("unk_word_02", WORD),
    ("unk_word_03", WORD),
    ("unk_word_04", WORD),
    ("unk_word_05", WORD),
    ("unk_word_06", WORD),
    ("unk_word_07", WORD),
    ("unk_word_08", WORD),
    ("unk_dword_00", DWORD),
]

WorldOpcodesClient = [
    (0x04, "F_PLAYER_EXIT", PACKET_F_PLAYER_EXIT),
    (0x0B, "F_PING", PACKET_F_PING),
    (0x0F, "F_CONNECT", PACKET_F_CONNECT),
    (0x13, "F_REQUEST_CHAR_TEMPLATES", PACKET_F_REQUEST_CHAR_TEMPLATES),
    (0x17, "F_OPEN_GAME", PACKET_F_OPEN_GAME),
    (0x35, "F_DUMP_ARENAS_LARGE", PACKET_F_DUMP_ARENAS_LARGE),
    (0x68, "F_DELETE_NAME", PACKET_F_DELETE_NAME),
    (0xB8, "F_PLAYER_ENTER_FULL", PACKET_F_PLAYER_ENTER_FULL),
    (0x54, "F_REQUEST_CHAR", PACKET_F_REQUEST_CHAR),
    (0x5C, "F_ENCRYPTKEY", PACKET_F_ENCRYPTKEY),
    (0x62, "F_PLAYER_STATE2", PACKET_F_PLAYER_STATE2),
    (0x7C, "F_INIT_PLAYER", PACKET_F_INIT_PLAYER),
    (0x91, "F_CREATE_CHARACTER", PACKET_F_CREATE_CHARACTER),
    (0xC8, "F_INTERFACE_COMMAND", PACKET_F_INTERFACE_COMMAND)
]

#WorldOpcodesServer = [

#]

def GetWord(buf):
    word = struct.unpack(">H", buf[:2])[0]
    return (word, buf[2:])

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
                print "MOOO !!!! res_struct[value] = %d" % res_struct[value]
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

start_log = 0
moo = ""
lopcode = []
dopcode = {}.fromkeys(set(range(0, 0xFF)),0)

def decode_packet(packet_size, packet_data, is_client):
    global start_log
    global moo, lopcode
    size_data, packet_data = GetWord(packet_data)
    if is_client == True:
        if start_log == 1:
            fd = open("C:\Temp\lol.py", "w")
            fd.write(moo)
            fd.close()
            print map(hex, lopcode)
            for i, k in dopcode.items():
               if k != 0:
                print "%02X : %02X" % (i, k)
            raise "LOL"
        return
        packet_crc = packet_data[len(packet_data) - 2: len(packet_data)]
        packet_data = packet_data[:-2]
        packet_client_header, packet_data = depack(PACKET_CLIENT_HEADER, packet_data)
        print packet_client_header
        print packet_data.encode('hex')
        found = False
        for i in WorldOpcodesClient:
            if i[0] == packet_client_header['opcode_packet']:
                data_unpacked, packet_data = depack(i[2], packet_data)
                print data_unpacked
                found = True
                break
        if found == False:
            print "GTFO OPCODE UNKNOW %02X" % packet_client_header['opcode_packet']
            exit(0)
        if len(packet_data) > 0 and len(packet_data) != 256 and i[1] != 'F_PLAYER_STATE2':
            print "WTF DATA LEFT !"
            exit(0)
    else:
        #packet_server_header, packet_data = depack(PACKET_SERVER_HEADER, packet_data)
        #print packet_server_header
        if packet_data[0] == chr(0x46):
            start_log = 1
        if start_log == 1 and ord(packet_data[0]) != 0xF8 and ord(packet_data[0]) != 0xF3:
            dopcode[ord(packet_data[0])] += 1
            if ord(packet_data[0]) not in lopcode:
                lopcode.append(ord(packet_data[0]))
            #print "0x%02X" % (struct.unpack(">B", packet_data[:1]))
            print "p = \'" + packet_data.encode('hex') + "\'"
            moo += "        p = \'" + packet_data.encode('hex') + "\'.decode(\'hex\')\n        self.send_data(p)\n"

if __name__ == "__main__":
    fd = open(FILENAME, "r")
    while True:
        line = fd.readline()
        if not line:
            break
        if PATTERN_SIZE in line:
            size_packet = int(line[line.find(PATTERN_SIZE) + len(PATTERN_SIZE):])
            #print "size_packet = %08X" % size_packet
            if line.startswith("[Client]"):
                is_client = True
            else:
                is_client = False
            fd.readline() # Skip "|----------- ... "
            fd.readline() # Skip "|00 01 02 03 ... "
            fd.readline() # Skip "|----------- ... "
            remain_size = size_packet
            buf_data = ""
            for i in xrange(0, (size_packet / 16)):
                data_line = fd.readline()
                #print data_line[1:(16 * 3)].replace(" ", "")
                buf_data += data_line[1:(16 * 3)].replace(" ", "").decode('hex')
                remain_size = remain_size - 16
            if remain_size > 0:
                data_line = fd.readline()
                #print data_line[1:(remain_size * 3)].replace(" ", "")
                buf_data += data_line[1:(remain_size * 3)].replace(" ", "").decode('hex')
            #print hex(len(buf_data))
            #print buf_data
            decode_packet(size_packet, buf_data, is_client)
            #break
