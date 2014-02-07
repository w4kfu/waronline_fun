import SocketServer
import struct
import time
import zlib
import threading

import WAR_TCPHandler
import WAR_Utils

class WorldTCPHandler(WAR_TCPHandler.TCPHandler):

    def recv_data(self):
        buf = self.request.recv(2)
        print "[+] Receiving data (%s) from %s : %d" % (self.name, self.client_address[0], self.client_address[1])
        buf_len = len(buf)
        print "[+] len(buf) = %d (0x%08X)" % (buf_len, buf_len)
        if buf_len == 0:
            return ""
        print WAR_Utils.hexdump(buf)
        len_packet = struct.unpack(">H", buf)[0]
        print "[+] Receiving data (%s) from %s : %d" % (self.name, self.client_address[0], self.client_address[1])
        buf = self.request.recv(len_packet + 8 + 2)
        buf_len = len(buf)
        print "[+] len(buf) = %d (0x%08X)" % (buf_len, buf_len)
        if buf_len == 0:
            return ""
        if self.encrypted == True:
            buf = WAR_Utils.WAR_RC4(buf, self.RC4Key, False)
        print WAR_Utils.hexdump(buf)
        return buf

    def handle(self):
        self.OpcodesTableRecv = [
            (0x00, "UNKNOWN", self.handle_unknown), (0x01, "UNKNOWN", self.handle_unknown),
            (0x02, "UNKNOWN", self.handle_unknown), (0x03, "UNKNOWN", self.handle_unknown),
            (0x04, "UNKNOWN", self.handle_unknown), (0x05, "UNKNOWN", self.handle_unknown),
            (0x06, "UNKNOWN", self.handle_unknown), (0x07, "UNKNOWN", self.handle_unknown),
            (0x08, "UNKNOWN", self.handle_unknown), (0x09, "UNKNOWN", self.handle_unknown),
            (0x0A, "UNKNOWN", self.handle_unknown), (0x0B, "UNKNOWN", self.handle_unknown),
            (0x0C, "UNKNOWN", self.handle_unknown), (0x0D, "UNKNOWN", self.handle_unknown),
            (0x0E, "UNKNOWN", self.handle_unknown), (0x0F, "UNKNOWN", self.handle_0x0F),
            (0x10, "UNKNOWN", self.handle_unknown), (0x11, "UNKNOWN", self.handle_unknown),
            (0x12, "UNKNOWN", self.handle_unknown), (0x13, "UNKNOWN", self.handle_unknown),
            (0x14, "UNKNOWN", self.handle_unknown), (0x15, "UNKNOWN", self.handle_unknown),
            (0x16, "UNKNOWN", self.handle_unknown), (0x17, "UNKNOWN", self.handle_unknown),
            (0x18, "UNKNOWN", self.handle_unknown), (0x19, "UNKNOWN", self.handle_unknown),
            (0x1A, "UNKNOWN", self.handle_unknown), (0x1B, "UNKNOWN", self.handle_unknown),
            (0x1C, "UNKNOWN", self.handle_unknown), (0x1D, "UNKNOWN", self.handle_unknown),
            (0x1E, "UNKNOWN", self.handle_unknown), (0x1F, "UNKNOWN", self.handle_unknown),
            (0x20, "UNKNOWN", self.handle_unknown), (0x21, "UNKNOWN", self.handle_unknown),
            (0x22, "UNKNOWN", self.handle_unknown), (0x23, "UNKNOWN", self.handle_unknown),
            (0x24, "UNKNOWN", self.handle_unknown), (0x25, "UNKNOWN", self.handle_unknown),
            (0x26, "UNKNOWN", self.handle_unknown), (0x27, "UNKNOWN", self.handle_unknown),
            (0x28, "UNKNOWN", self.handle_unknown), (0x29, "UNKNOWN", self.handle_unknown),
            (0x2A, "UNKNOWN", self.handle_unknown), (0x2B, "UNKNOWN", self.handle_unknown),
            (0x2C, "UNKNOWN", self.handle_unknown), (0x2D, "UNKNOWN", self.handle_unknown),
            (0x2E, "UNKNOWN", self.handle_unknown), (0x2F, "UNKNOWN", self.handle_unknown),
            (0x30, "UNKNOWN", self.handle_unknown), (0x31, "UNKNOWN", self.handle_unknown),
            (0x32, "UNKNOWN", self.handle_unknown), (0x33, "UNKNOWN", self.handle_unknown),
            (0x34, "UNKNOWN", self.handle_unknown), (0x35, "UNKNOWN", self.handle_unknown),
            (0x36, "UNKNOWN", self.handle_unknown), (0x37, "UNKNOWN", self.handle_unknown),
            (0x38, "UNKNOWN", self.handle_unknown), (0x39, "UNKNOWN", self.handle_unknown),
            (0x3A, "UNKNOWN", self.handle_unknown), (0x3B, "UNKNOWN", self.handle_unknown),
            (0x3C, "UNKNOWN", self.handle_unknown), (0x3D, "UNKNOWN", self.handle_unknown),
            (0x3E, "UNKNOWN", self.handle_unknown), (0x3F, "UNKNOWN", self.handle_unknown),
            (0x40, "UNKNOWN", self.handle_unknown), (0x41, "UNKNOWN", self.handle_unknown),
            (0x42, "UNKNOWN", self.handle_unknown), (0x43, "UNKNOWN", self.handle_unknown),
            (0x44, "UNKNOWN", self.handle_unknown), (0x45, "UNKNOWN", self.handle_unknown),
            (0x46, "UNKNOWN", self.handle_unknown), (0x47, "UNKNOWN", self.handle_unknown),
            (0x48, "UNKNOWN", self.handle_unknown), (0x49, "UNKNOWN", self.handle_unknown),
            (0x4A, "UNKNOWN", self.handle_unknown), (0x4B, "UNKNOWN", self.handle_unknown),
            (0x4C, "UNKNOWN", self.handle_unknown), (0x4D, "UNKNOWN", self.handle_unknown),
            (0x4E, "UNKNOWN", self.handle_unknown), (0x4F, "UNKNOWN", self.handle_unknown),
            (0x50, "UNKNOWN", self.handle_unknown), (0x51, "UNKNOWN", self.handle_unknown),
            (0x52, "UNKNOWN", self.handle_unknown), (0x53, "UNKNOWN", self.handle_unknown),
            (0x54, "UNKNOWN", self.handle_unknown), (0x55, "UNKNOWN", self.handle_unknown),
            (0x56, "UNKNOWN", self.handle_unknown), (0x57, "UNKNOWN", self.handle_unknown),
            (0x58, "UNKNOWN", self.handle_unknown), (0x59, "UNKNOWN", self.handle_unknown),
            (0x5A, "UNKNOWN", self.handle_unknown), (0x5B, "UNKNOWN", self.handle_unknown),
            (0x5C, "handle_0x5C", self.handle_0x5C), (0x5D, "UNKNOWN", self.handle_unknown),
            (0x5E, "UNKNOWN", self.handle_unknown), (0x5F, "UNKNOWN", self.handle_unknown),
            (0x60, "UNKNOWN", self.handle_unknown), (0x61, "UNKNOWN", self.handle_unknown),
            (0x62, "UNKNOWN", self.handle_unknown), (0x63, "UNKNOWN", self.handle_unknown),
            (0x64, "UNKNOWN", self.handle_unknown), (0x65, "UNKNOWN", self.handle_unknown),
            (0x66, "UNKNOWN", self.handle_unknown), (0x67, "UNKNOWN", self.handle_unknown),
            (0x68, "UNKNOWN", self.handle_unknown), (0x69, "UNKNOWN", self.handle_unknown),
            (0x6A, "UNKNOWN", self.handle_unknown), (0x6B, "UNKNOWN", self.handle_unknown),
            (0x6C, "UNKNOWN", self.handle_unknown), (0x6D, "UNKNOWN", self.handle_unknown),
            (0x6E, "UNKNOWN", self.handle_unknown), (0x6F, "UNKNOWN", self.handle_unknown),
            (0x70, "UNKNOWN", self.handle_unknown), (0x71, "UNKNOWN", self.handle_unknown),
            (0x72, "UNKNOWN", self.handle_unknown), (0x73, "UNKNOWN", self.handle_unknown),
            (0x74, "UNKNOWN", self.handle_unknown), (0x75, "UNKNOWN", self.handle_unknown),
            (0x76, "UNKNOWN", self.handle_unknown), (0x77, "UNKNOWN", self.handle_unknown),
            (0x78, "UNKNOWN", self.handle_unknown), (0x79, "UNKNOWN", self.handle_unknown),
            (0x7A, "UNKNOWN", self.handle_unknown), (0x7B, "UNKNOWN", self.handle_unknown),
            (0x7C, "UNKNOWN", self.handle_unknown), (0x7D, "UNKNOWN", self.handle_unknown),
            (0x7E, "UNKNOWN", self.handle_unknown), (0x7F, "UNKNOWN", self.handle_unknown),
            (0x80, "UNKNOWN", self.handle_unknown), (0x81, "UNKNOWN", self.handle_unknown),
            (0x82, "UNKNOWN", self.handle_unknown), (0x83, "UNKNOWN", self.handle_unknown),
            (0x84, "UNKNOWN", self.handle_unknown), (0x85, "UNKNOWN", self.handle_unknown),
            (0x86, "UNKNOWN", self.handle_unknown), (0x87, "UNKNOWN", self.handle_unknown),
            (0x88, "UNKNOWN", self.handle_unknown), (0x89, "UNKNOWN", self.handle_unknown),
            (0x8A, "UNKNOWN", self.handle_unknown), (0x8B, "UNKNOWN", self.handle_unknown),
            (0x8C, "UNKNOWN", self.handle_unknown), (0x8D, "UNKNOWN", self.handle_unknown),
            (0x8E, "UNKNOWN", self.handle_unknown), (0x8F, "UNKNOWN", self.handle_unknown),
            (0x90, "UNKNOWN", self.handle_unknown), (0x91, "UNKNOWN", self.handle_unknown),
            (0x92, "UNKNOWN", self.handle_unknown), (0x93, "UNKNOWN", self.handle_unknown),
            (0x94, "UNKNOWN", self.handle_unknown), (0x95, "UNKNOWN", self.handle_unknown),
            (0x96, "UNKNOWN", self.handle_unknown), (0x97, "UNKNOWN", self.handle_unknown),
            (0x98, "UNKNOWN", self.handle_unknown), (0x99, "UNKNOWN", self.handle_unknown),
            (0x9A, "UNKNOWN", self.handle_unknown), (0x9B, "UNKNOWN", self.handle_unknown),
            (0x9C, "UNKNOWN", self.handle_unknown), (0x9D, "UNKNOWN", self.handle_unknown),
            (0x9E, "UNKNOWN", self.handle_unknown), (0x9F, "UNKNOWN", self.handle_unknown),
            (0xA0, "UNKNOWN", self.handle_unknown), (0xA1, "UNKNOWN", self.handle_unknown),
            (0xA2, "UNKNOWN", self.handle_unknown), (0xA3, "UNKNOWN", self.handle_unknown),
            (0xA4, "UNKNOWN", self.handle_unknown), (0xA5, "UNKNOWN", self.handle_unknown),
            (0xA6, "UNKNOWN", self.handle_unknown), (0xA7, "UNKNOWN", self.handle_unknown),
            (0xA8, "UNKNOWN", self.handle_unknown), (0xA9, "UNKNOWN", self.handle_unknown),
            (0xAA, "UNKNOWN", self.handle_unknown), (0xAB, "UNKNOWN", self.handle_unknown),
            (0xAC, "UNKNOWN", self.handle_unknown), (0xAD, "UNKNOWN", self.handle_unknown),
            (0xAE, "UNKNOWN", self.handle_unknown), (0xAF, "UNKNOWN", self.handle_unknown),
            (0xB0, "UNKNOWN", self.handle_unknown), (0xB1, "UNKNOWN", self.handle_unknown),
            (0xB2, "UNKNOWN", self.handle_unknown), (0xB3, "UNKNOWN", self.handle_unknown),
            (0xB4, "UNKNOWN", self.handle_unknown), (0xB5, "UNKNOWN", self.handle_unknown),
            (0xB6, "UNKNOWN", self.handle_unknown), (0xB7, "UNKNOWN", self.handle_unknown),
            (0xB8, "UNKNOWN", self.handle_unknown), (0xB9, "UNKNOWN", self.handle_unknown),
            (0xBA, "UNKNOWN", self.handle_unknown), (0xBB, "UNKNOWN", self.handle_unknown),
            (0xBC, "UNKNOWN", self.handle_unknown), (0xBD, "UNKNOWN", self.handle_unknown),
            (0xBE, "UNKNOWN", self.handle_unknown), (0xBF, "UNKNOWN", self.handle_unknown),
            (0xC0, "UNKNOWN", self.handle_unknown), (0xC1, "UNKNOWN", self.handle_unknown),
            (0xC2, "UNKNOWN", self.handle_unknown), (0xC3, "UNKNOWN", self.handle_unknown),
            (0xC4, "UNKNOWN", self.handle_unknown), (0xC5, "UNKNOWN", self.handle_unknown),
            (0xC6, "UNKNOWN", self.handle_unknown), (0xC7, "UNKNOWN", self.handle_unknown),
            (0xC8, "UNKNOWN", self.handle_unknown), (0xC9, "UNKNOWN", self.handle_unknown),
            (0xCA, "UNKNOWN", self.handle_unknown), (0xCB, "UNKNOWN", self.handle_unknown),
            (0xCC, "UNKNOWN", self.handle_unknown), (0xCD, "UNKNOWN", self.handle_unknown),
            (0xCE, "UNKNOWN", self.handle_unknown), (0xCF, "UNKNOWN", self.handle_unknown),
            (0xD0, "UNKNOWN", self.handle_unknown), (0xD1, "UNKNOWN", self.handle_unknown),
            (0xD2, "UNKNOWN", self.handle_unknown), (0xD3, "UNKNOWN", self.handle_unknown),
            (0xD4, "UNKNOWN", self.handle_unknown), (0xD5, "UNKNOWN", self.handle_unknown),
            (0xD6, "UNKNOWN", self.handle_unknown), (0xD7, "UNKNOWN", self.handle_unknown),
            (0xD8, "UNKNOWN", self.handle_unknown), (0xD9, "UNKNOWN", self.handle_unknown),
            (0xDA, "UNKNOWN", self.handle_unknown), (0xDB, "UNKNOWN", self.handle_unknown),
            (0xDC, "UNKNOWN", self.handle_unknown), (0xDD, "UNKNOWN", self.handle_unknown),
            (0xDE, "UNKNOWN", self.handle_unknown), (0xDF, "UNKNOWN", self.handle_unknown),
            (0xE0, "UNKNOWN", self.handle_unknown), (0xE1, "UNKNOWN", self.handle_unknown),
            (0xE2, "UNKNOWN", self.handle_unknown), (0xE3, "UNKNOWN", self.handle_unknown),
            (0xE4, "UNKNOWN", self.handle_unknown), (0xE5, "UNKNOWN", self.handle_unknown),
            (0xE6, "UNKNOWN", self.handle_unknown), (0xE7, "UNKNOWN", self.handle_unknown),
            (0xE8, "UNKNOWN", self.handle_unknown), (0xE9, "UNKNOWN", self.handle_unknown),
            (0xEA, "UNKNOWN", self.handle_unknown), (0xEB, "UNKNOWN", self.handle_unknown),
            (0xEC, "UNKNOWN", self.handle_unknown), (0xED, "UNKNOWN", self.handle_unknown),
            (0xEE, "UNKNOWN", self.handle_unknown), (0xEF, "UNKNOWN", self.handle_unknown),
            (0xF0, "UNKNOWN", self.handle_unknown), (0xF1, "UNKNOWN", self.handle_unknown),
            (0xF2, "UNKNOWN", self.handle_unknown), (0xF3, "UNKNOWN", self.handle_unknown),
            (0xF4, "UNKNOWN", self.handle_unknown), (0xF5, "UNKNOWN", self.handle_unknown),
            (0xF6, "UNKNOWN", self.handle_unknown), (0xF7, "UNKNOWN", self.handle_unknown),
            (0xF8, "UNKNOWN", self.handle_unknown), (0xF9, "UNKNOWN", self.handle_unknown),
            (0xFA, "UNKNOWN", self.handle_unknown), (0xFB, "UNKNOWN", self.handle_unknown),
            (0xFC, "UNKNOWN", self.handle_unknown), (0xFD, "UNKNOWN", self.handle_unknown),
            (0xFE, "UNKNOWN", self.handle_unknown), (0xFF, "UNKNOWN", self.handle_unknown),
        ]
        self.name = "WorldTCPHandler"
        self.encrypted = False
        print "WorldTCPHandler : New connection from %s : %d" % (self.client_address[0], self.client_address[1])

        while True:
            buf = self.recv_data()
            if buf == "":
                break
            sequence_packet, buf = WAR_Utils.GetWord(buf)
            session_id_packet, buf = WAR_Utils.GetWord(buf)
            unk_word_00, buf = WAR_Utils.GetWord(buf)
            unk_byte_00, buf = WAR_Utils.GetByte(buf)
            opcode_packet, buf = WAR_Utils.GetByte(buf)
            print "[+] Sequence packet : %04X" % (sequence_packet)
            print "[+] Session ID packet : %04X" % (session_id_packet)
            print "[+] unk_word_00 : %04X" % (unk_word_00)
            print "[+] unk_byte_00 : %02X" % (unk_byte_00)
            print "[+] Opcode packet : %02X" % (opcode_packet)
            self.handle_opcode(opcode_packet, buf)

    def handle_opcode(self, opcode, buf):
        if opcode <= len(self.OpcodesTableRecv):
            entry_opcode = self.OpcodesTableRecv[opcode]
            print "[+] Calling opcode 0x%02X : %s" % (entry_opcode[0], entry_opcode[1])
            entry_opcode[2](buf)
        else:
            print "[-] OPCODE LARGER THAN OpcodesTableRecv size : (%02X) %d " % (opcode, opcode)
            exit(0)
        #if opcode == 0x0F:
            #self.handle_0x0F(buf)
        #elif opcode == 0x04:
            #self.handle_0x04(buf)
        #elif opcode == 0x54:
            #self.handle_0x54(buf)
        #elif opcode == 0x5C:
            #self.handle_0x5C(buf)
        #elif opcode == 0xB8:
            #self.handle_0xB8(buf)
        #else:
            #print "[-] UNNKOW OPCODE 0x%02X (%d)" % (opcode, opcode)
            #exit(0)

    def handle_unknown(self, buf):
        print "[-] EXIT !"
        exit(0)

    def handle_0x04(self, buf):
        print "[+] Exit"

    def handle_0x0F(self, buf):
        unk_byte_00, buf = WAR_Utils.GetByte(buf)
        unk_byte_01, buf = WAR_Utils.GetByte(buf)
        major_version, buf = WAR_Utils.GetByte(buf)
        minor_version, buf = WAR_Utils.GetByte(buf)
        revision_version, buf = WAR_Utils.GetByte(buf)
        unk_byte_02, buf = WAR_Utils.GetByte(buf)
        unk_word_00, buf = WAR_Utils.GetWord(buf)

        print "[+] unk_byte_00 : %02X" % (unk_byte_00)
        print "[+] unk_byte_01 : %02X" % (unk_byte_01)
        print "[+] major_version : %02X" % (major_version)
        print "[+] minor_version : %02X" % (minor_version)
        print "[+] revision_version : %02X" % (revision_version)
        print "[+] unk_byte_02 : %02X" % (unk_byte_02)
        print "[+] unk_word_00 : %02X" % (unk_word_00)

        protocol_version, buf = WAR_Utils.GetDword(buf)
        print "[+] Protocol Version = %08X" % (protocol_version)
        session, buf = WAR_Utils.GetBufferSize(buf, 101)
        print "[+] Session = %s" % session
        username, buf = WAR_Utils.GetBufferSize(buf, 21)
        print "[+] username = %s" % username
        size_xml, buf = WAR_Utils.GetWord(buf)
        print "[+] size_xml = %04X" % (size_xml)

        self.prepare_0x82(protocol_version, username)

    def prepare_0x82(self, protocol_version, username):
        """ S_CONNECTED """
        p = struct.pack(">B", 0x82)
        p += struct.pack(">B", 0x00)    # UNK_BYTE_00
        p += struct.pack(">B", 0x00)    # UNK_BYTE_01
        p += struct.pack(">B", 0x00)    # UNK_BYTE_02
        p += struct.pack(">B", 0x00)    # UNK_BYTE_03
        p += struct.pack(">I", protocol_version)
        p += struct.pack(">B", WAR_TCPHandler.WorldID)    # SERVER_ID
        p += struct.pack(">B", 0x00)    # UNK_BYTE_04
        p += struct.pack(">B", 0x00)    # UNK_BYTE_05
        p += struct.pack(">B", 0x00)    # UNK_BYTE_06
        p += struct.pack(">B", 0x00)    # TRANSFER_FLAG
        p += WAR_Utils.MakeBBuffer(username)    # USERNAME
        p += WAR_Utils.MakeBBuffer(WAR_TCPHandler.WorldName)    # SERVER_NAME
        p += struct.pack(">B", 0x00)    # NS related to arry of informations
        p = WAR_Utils.WAR_RC4(p, self.RC4Key, True)
        p = struct.pack(">H", len(p) - 1) + p
        self.send_data(p)

    def handle_0x5C(self, buf):
        key_present, buf = WAR_Utils.GetByte(buf)
        unk_byte_00, buf = WAR_Utils.GetByte(buf)
        major_version, buf = WAR_Utils.GetByte(buf)
        minor_version, buf = WAR_Utils.GetByte(buf)
        revision_version, buf = WAR_Utils.GetByte(buf)
        unk_byte_01, buf = WAR_Utils.GetByte(buf)
        print "[+] key_present : %02X" % (key_present)
        print "[+] unk_byte_00 : %02X" % (unk_byte_00)
        print "[+] major_version : %02X" % (major_version)
        print "[+] minor_version : %02X" % (minor_version)
        print "[+] revision_version : %02X" % (revision_version)
        print "[+] unk_byte_01 : %02X" % (unk_byte_01)
        if key_present == 0:
            # ask for a key
            self.prepare_0x8A()
        else:
            # read the key
            key = buf[0 : 256]
            print "[+] Key (len(key) = %08X) :" % (len(key))
            print WAR_Utils.hexdump(key)
            self.encrypted = True
            self.RC4Key = key

    def prepare_0x8A(self):
        p = struct.pack(">B", 0x8A)
        p += struct.pack(">B", 0x01)
        p = struct.pack(">H", len(p) - 1) + p
        self.send_data(p)

    def handle_0xB8(self, buf):

        self.prepare_0x80()

    def prepare_0x56(self):
        p = struct.pack(">B", 0x56)
        p += struct.pack(">H", 0x1)
        p = WAR_Utils.WAR_RC4(p, self.RC4Key, True)
        p = struct.pack(">H", len(p) - 1) + p
        self.send_data(p)

    def handle_0x54(self, buf):
        action, buf = WAR_Utils.GetWord(buf)
        print "[+] Action = %04X" % (action)
        if action == 0x2D58:
            self.prepare_0x56()


    def prepare_0x80(self):
        p = struct.pack(">B", 0x80)
        p += struct.pack(">H", 0x42)    # unknow
        p = WAR_Utils.WAR_RC4(p, self.RC4Key, True)
        p = struct.pack(">H", len(p) - 1) + p
        self.send_data(p)

    def finish(self):
        print "WorldTCPHandler : Closing connection from %s : %d" % (self.client_address[0], self.client_address[1])
        return SocketServer.BaseRequestHandler.finish(self)

if __name__ == "__main__":

    WorldServer = WAR_TCPHandler.ThreadedTCPServer((WAR_TCPHandler.WorldHost, WAR_TCPHandler.WorldPort), WorldTCPHandler)
    WorldServer.allow_reuse_address = True
    WorldServerThr = threading.Thread(target=WorldServer.serve_forever)
    WorldServerThr.daemon = True
    WorldServerThr.start()
    print "[+] WorldServer started on \"%s\" : %d" % (WAR_TCPHandler.WorldHost, WAR_TCPHandler.WorldPort)

    raw_input('Press enter to stop servers.\n')
    WorldServerThr._Thread__stop()