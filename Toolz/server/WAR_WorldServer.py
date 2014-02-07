import SocketServer
import struct
import time
import zlib

import WAR_TCPHandler
import WAR_Utils

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
        print WAR_Utils.hexdump(buf)
        return buf

    def handle(self):
        self.name = "WorldTCPHandler"
        self.encrypted = False
        print "WorldTCPHandler : New connection from %s : %d" % (self.client_address[0], self.client_address[1])

        while True:
            buf = self.recv_data()
            if buf == "":
                break
            if self.encrypted == True:
                buf = WAR_RC4(buf, self.RC4Key, False)
                print WAR_Utils.hexdump(buf)
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
        if opcode == 0x0F:
            self.handle_0x0F(buf)
        elif opcode == 0x04:
            self.handle_0x04(buf)
        elif opcode == 0x54:
            self.handle_0x54(buf)
        elif opcode == 0x5C:
            self.handle_0x5C(buf)
        elif opcode == 0xB8:
            self.handle_0xB8(buf)
        else:
            print "[-] UNNKOW OPCODE 0x%02X (%d)" % (opcode, opcode)
            exit(0)

    def handle_0x04(self, buf):
        print "[+] Exit"

    def handle_0x0F(self, buf):
        cipher, buf = WAR_Utils.GetByte(buf)
        unk_byte_00, buf = WAR_Utils.GetByte(buf)
        major_version, buf = WAR_Utils.GetByte(buf)
        minor_version, buf = WAR_Utils.GetByte(buf)
        revision_version, buf = WAR_Utils.GetByte(buf)
        unk_byte_01, buf = WAR_Utils.GetByte(buf)
        unk_word_00, buf = WAR_Utils.GetWord(buf)

        print "[+] cipher : %02X" % (cipher)
        print "[+] unk_byte_00 : %02X" % (unk_byte_00)
        print "[+] major_version : %02X" % (major_version)
        print "[+] minor_version : %02X" % (minor_version)
        print "[+] revision_version : %02X" % (revision_version)
        print "[+] unk_byte_01 : %02X" % (unk_byte_01)
        print "[+] unk_word_00 : %02X" % (unk_word_00)

        protocol_version, buf = WAR_Utils.GetDword(buf)
        print "[+] Protocol Version = %08X" % (protocol_version)
        session, buf = WAR_Utils.GetBufferSize(buf, 80)
        print "[+] Session = %s" % session
        buf = buf[21:]
        username, buf = WAR_Utils.GetBufferSize(buf, 21)
        print "[+] username = %s" % username
        size_xml, buf = WAR_Utils.GetWord(buf)
        print "[+] size_xml = %04X" % (size_xml)

        self.prepare_0x82(protocol_version, username)

    def prepare_0x82(self, protocol_version, username):
        """ S_CONNECTED """
        p = struct.pack(">B", 0x82)

        p += struct.pack(">B", 0x00)    # unknow
        p += struct.pack(">B", 0x00)    # unknow
        p += struct.pack(">B", 0x00)    # unknow
        p += struct.pack(">B", 0x00)    # unknow
        p += struct.pack(">I", protocol_version)
        p += WAR_Utils.MakeBBuffer(username)
        p += WAR_Utils.MakeBBuffer(WAR_TCPHandler.WorldName)
        p += struct.pack(">B", 0x00)    # NS related to arry of informations
        p = WAR_RC4(p, self.RC4Key, True)
        p = struct.pack(">H", len(p) - 1) + p
        self.send_data(p)

    def handle_0x5C(self, buf):
        print "[+] handle_0x5C"
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
        p = WAR_RC4(p, self.RC4Key, True)
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
        p = WAR_RC4(p, self.RC4Key, True)
        p = struct.pack(">H", len(p) - 1) + p
        self.send_data(p)

    def finish(self):
        print "WorldTCPHandler : Closing connection from %s : %d" % (self.client_address[0], self.client_address[1])
        return SocketServer.BaseRequestHandler.finish(self)