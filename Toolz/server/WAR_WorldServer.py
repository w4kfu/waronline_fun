import SocketServer
import struct
import time
import zlib
import threading
import thread
import construct

import WAR_TCPHandler
import WAR_Utils
from WAR_WorldStruct import *

class WorldTCPHandler(WAR_TCPHandler.TCPHandler):
    """ """

    def recv_data(self):
        buf = self.request.recv(2)
        WAR_Utils.LogInfo("[+] Receiving data (%s) from %s : %d" % (self.name, self.client_address[0], self.client_address[1]), 3)
        buf_len = len(buf)
        if buf_len == 0:
            raise WAR_Utils.WarError("Received packet length NULL")
        len_packet, buf = WAR_Utils.GetWord(buf)
        buf = self.request.recv(len_packet + SIZE_PACKET_CLIENT_HEADER + 2) # + 2 : CRC [WORD]
        buf_len = len(buf)
        WAR_Utils.LogInfo("[+] len(buf) = %d (0x%08X)" % (buf_len, buf_len), 3)
        if buf_len == 0:
            raise WAR_Utils.WarError("Received packet data of length 0")
        if self.encrypted == True:
            buf = WAR_Utils.WAR_RC4(buf, self.RC4Key, False)
        WAR_Utils.LogInfo(WAR_Utils.hexdump(buf), 3)
        return buf

    def send_data(self, buf):
        WAR_Utils.LogInfo("[+] Sending data (%s) to %s : %d" % (self.name, self.client_address[0], self.client_address[1]), 3)
        WAR_Utils.LogInfo("[+] len(buf) = %d (0x%08X)" % (len(buf), len(buf)), 3)
        WAR_Utils.LogInfo(WAR_Utils.hexdump(buf) + "\n", 3)
        if self.encrypted == True:
            buf = WAR_Utils.WAR_RC4(buf, self.RC4Key, True)
        buf = struct.pack(">H", len(buf) - 1) + buf
        self.request.send(buf)

    def handle_recv_data(self):
        while True:
            packet_data = self.recv_data()
            if packet_data == "":
                break
            self.handle_packet_client_header(packet_data)

    def handle_packet_client_header(self, packet_data):
        packet_crc = packet_data[len(packet_data) - 2: len(packet_data)]
        packet_data = packet_data[:-2]
        #packet_client_header, packet_data = WAR_Utils.depack(PACKET_CLIENT_HEADER, packet_data)
        packet_client_header = PacketClientHeader.parse(packet_data)
        packet_data = packet_data[SIZE_PACKET_CLIENT_HEADER:]
        # TODO PRETTRY PRINT THIS SHIT
        WAR_Utils.LogInfo(packet_client_header, 3)
        if packet_client_header['opcode'] <= len(self.OpcodesTableRecv):
            entry_opcode = self.OpcodesTableRecv[packet_client_header['opcode']]
            WAR_Utils.LogInfo("[+] Opcode \"%s\" (0x%02X ; %d)" % (entry_opcode[1], entry_opcode[0], entry_opcode[0]), 1)
            entry_opcode[2](entry_opcode, packet_client_header, packet_data)
                # Now make the answer if it exists
                #if answer_opcode != None:
                    #for i in self.WorldSent:
                        #if answer_opcode == i[0]:
                            #i[2](i, packet_client_header, unpacked_data)
        else:
            raise WAR_Utils.WarError("OPCODE LARGER THAN OpcodesTableRecv size : %d (0x%02X)" % (packet_client_header['opcode'], packet_client_header['opcode']))

    ### CHARACTER RELATED

    def premaidcharacter(self):
        p = CHARACTER.build(construct.Container(nickname = "Skarsnik",
            last_name = "",
            level = 0x01,
            career = 0x1A,
            realm = 0x02,
            gender = 0x00,
            unk_word_00 = 0x0E00,           # model?
            zone = 100,                     # /!\ Field on little endian Norsca: 100
            unk_data_00 = [0] * 0x0C,
            ))

        #unk_data_00 = [0] * 0x14,
        #    remaining_lockout_time = 0,
        #    unk_byte_00 = 0,
        #    unk_byte_01 = 0,
        #    max_characters = 0x10,
        #    gameplay_rule_set_type = 0,
        #    last_switched_to_realm = 0,
        #    num_paid_name_changes_available = 0,
        #    unk_word_00 = 0,
        #    ))
        #
        #construct.String("nickname", 0x30),                         # + 0x00
        #construct.UBInt8("level"),                                  # + 0x30
        #construct.UBInt8("career"),                                 # + 0x31
        #construct.UBInt8("realm"),                                  # + 0x32
        #construct.UBInt8("gender"),                                 # + 0x33
        #construct.UBInt16("unk_word_00"),                           # + 0x34
        #construct.UBInt16("zone"),                                  # + 0x36
        #construct.Array(0x0C, construct.ULInt8("unk_data_00")),     # + 0x38


        #p = "NICKNAME"
        #p += "\x00" * (48 - len(p))
        #p += struct.pack(">B", 1)                # +0x030 : LEVEL
        #p += struct.pack(">B", 0x1A)             # +0x031 : CAREER
        #p += struct.pack(">B", 0x2)              # +0x032 : REALM : ORDER = 1 ; DESTRU = 2
        #p += struct.pack(">B", 0x0)              # +0x033 : GENDER
        #p += struct.pack(">H", 0x0E00)           # +0x034 : UNK_WORD_00 // CRASH :(
        #p += struct.pack("<H", 0x0006)           # +0x036 : ZONE
        #
        #p += "\x00" * 12                         # +0x038 : UNK_DATA

        for i in xrange(0, 16):
            p += struct.pack("<H", 0x0000)            # +0x044 : ??
            p += struct.pack("<H", 0x0000)            # +0x046 : ??     # IGNORED ?
            p += struct.pack("<H", 0x0000)            # +0x048 : ??
            p += struct.pack("<H", 0x0000)            # +0x04A : ??

        for i in xrange(0, 5):
            p += struct.pack("<H", 0x0000)            # +0x0C4 : ??
            p += struct.pack("<H", 0x0000)            # +0x0C6 : ??     # IGNORED ?
            p += struct.pack("<B", 0x0000)            # +0x0C8 : ??
            p += struct.pack("<B", 0x0000)            # +0x0C9 : ??
            p += struct.pack("<H", 0x0000)            # +0x0CA : ??     # IGNORED ?


        # data/gamedata/initchars.csv => 0xAA39137EF4905FA6

        #p += '4604000000'.decode('hex')               # + 0xEC : Array[5]
        #p += '0000000000'.decode('hex')                # + 0xEC : Array[5]
        p += struct.pack("<I", 0x0446)
        for i in xrange(0, 5 - 1):
            p += struct.pack("<I", 4809)

        p += struct.pack("<B", 0x00)                    # + 0x100
        p += struct.pack("<B", 0x00)                    # + 0x101
        p += struct.pack("<B", 0x00)                    # + 0x102
        p += struct.pack("<B", 0x03)                    # + 0x103   RACE ?

        # + 0xF1 : ??
        # + 0x100: BYTE
        # + 0x101: BYTE

        #p += '000000000000000000000000000000ff000003000000000000000000'.decode('hex')
        p += "\x00" * (0x11C - len(p))
        return p

    def makepacketcharacters(self):
        NB_PREMAID = 1
        p = ""
        for i in xrange(0, NB_PREMAID):
            p += self.premaidcharacter()
        for i in xrange(0, 0x14 - NB_PREMAID):
            p += "\x00" * 0x11C
        return p

    ### ALL RESPONSE

    def response(self, opcode, packet_client_header, packet_client, packet_data):
        for i in self.WorldSent:
            if opcode == i[0]:
                WAR_Utils.LogInfo("[+] Response Opcode \"%s\" (0x%02X ; %d)" % (i[1], i[0], i[0]), 1)
                i[2](i, packet_client_header, packet_client, packet_data)
                break

    def reponse_0x0C(self, opcode_entry, packet_client_header, packet_client, packet_data):
        p = struct.pack(">B", opcode_entry[0])
        p += struct.pack(">B", 0x00)
        self.send_data(p)

    def response_0x13(self, opcode_entry, packet_client_header, packet_client, packet_data):
        p = struct.pack(">B", opcode_entry[0])
        p += struct.pack(">I", 0x00)        # NB AVAILABLETEMPLATES_NAMES
        p += struct.pack(">I", 0x00)        # NB AvailableTemplates_Classes
        p += struct.pack(">I", 0x00)        # NB AvailableTemplates_Races
        p += struct.pack(">I", 0x00)        # NB AvailableTemplates_Genders
        self.send_data(p)

    def response_F_WORLD_ENTER(self, opcode_entry, packet_client_header, packet_client, packet_data):
        """
            Response of packet F_DUMP_ARENAS_LARGE (0x35).
        """
        p = struct.pack(">B", opcode_entry[0])
        #p += struct.pack(">B", 0x06)    # UNK_BYTE_00
        #p += struct.pack(">B", 0x08)    # UNK_BYTE_01
        #p += struct.pack(">B", 0x00)    # UNK_BYTE_00
        #p += struct.pack(">B", 0x00)    # UNK_BYTE_01
        #p += struct.pack(">B", 0x00)    # UNK_BYTE_02
        #p += struct.pack(">B", 0x00)    # UNK_BYTE_03
        #p += struct.pack(">I", 0x00)    # UNK_DWORD_00
        #p += struct.pack(">I", 0x00)    # UNK_DWORD_01
        #p += struct.pack(">I", 0x00)    # UNK_DWORD_02
        #p += struct.pack(">I", 0x00)    # UNK_DWORD_03
        #p += struct.pack(">H", 0x00)    # UNK_WORD_00
        #
        #p += struct.pack(">H", 13337)
        #p += struct.pack(">H", 13337)
        #p += "0.0.0.0"
        self.send_data(p)

    def response_F_REQUEST_CHAR_RESPONSE(self, opcode_entry, packet_client_header, packet_client, packet_data):
        p = struct.pack(">B", opcode_entry[0])
        p += PACKET_F_REQUEST_CHAR_RESPONSE.build(construct.Container(unk_data_00 = [0] * 0x14,
            remaining_lockout_time = 0,
            unk_byte_00 = 0,
            unk_byte_01 = 0,
            max_characters = 0x10,
            gameplay_rule_set_type = 0,
            last_switched_to_realm = 0,
            num_paid_name_changes_available = 0,
            unk_word_00 = 0,
            ))
        p += self.makepacketcharacters()
        self.send_data(p)

    def response_0x56(self, opcode_entry, packet_client_header, packet_client, packet_data):
        p = struct.pack(">B", opcode_entry[0])
        p += struct.pack(">H", 0x00)      # TODO !?
        self.send_data(p)

    def response_0x58(self, opcode_entry, packet_client_header, packet_client, packet_data):
        p = struct.pack(">B", opcode_entry[0])
        self.send_data(p)

    def response_0x59(self, opcode_entry, packet_client_header, packet_client, packet_data):
        p = struct.pack(">B", opcode_entry[0])
        p += "\x00" * 24
        p += "DISPLAYED MESSAGE"
        self.send_data(p)

    def response_0x62(self, opcode_entry, packet_client_header, packet_client, packet_data):
        p = struct.pack(">B", opcode_entry[0])
        p += packet_data
        p += struct.pack(">B", 0x00)
        self.send_data(p)

    def response_0x6A(self, opcode_entry, packet_client_header, packet_client, packet_data):
        p = struct.pack(">B", opcode_entry[0])
        p += "\x00" * 0x31
        p += struct.pack(">B", 0x00)    # VALID_NAME : 0 OK
        self.send_data(p)

    def response_S_PID_ASSIGN(self, opcode_entry, packet_client_header, packet_client, packet_data):
        p = struct.pack(">B", opcode_entry[0])
        p += PACKET_S_PID_ASSIGN.build(construct.Container(session_id = 0x1300))
        self.send_data(p)

    def response_S_PONG(self, opcode_entry, packet_client_header, packet_client, packet_data):
        """
            response sent when packet F_PING has been received.
            Packet handling is done in the basick block at 0x004C403B.
            Answer have to reuse the timestamp sent by the client, and put a QWORD of the
            actual timestamp and increment the sequence number
        """
        p = struct.pack(">B", opcode_entry[0])
        p += PACKET_S_PONG.build(construct.Container(client_timestamp = packet_client['timestamp'],
            timestamp = time.time(),
            sequence = packet_client_header['sequence'] + 1,
            unk_dword_00 = 0x00
            ))
        self.send_data(p)

    def response_S_CONNECTED(self, opcode_entry, packet_client_header, packet_client, packet_data):
        """
            Reponse sent after receiving F_CONNECT packet.
            Packet handling is done in WAR.exe by:
                - 0x004C88F9: username and server_name are PascalString, protocol
                is normaly equal to 0xEB8DB21.
        """
        p = struct.pack(">B", opcode_entry[0])
        p += PACKET_S_CONNECTED.build(construct.Container(unk_byte_00 = 0,
            unk_byte_01 = 0,
            unk_byte_02 = 0,
            unk_byte_03 = 0,
            protocol_version = packet_client['protocol_version'],
            server_id = WAR_TCPHandler.WorldID,
            unk_byte_04 = 0,
            unk_byte_05 = 0,
            unk_byte_06 = 0,
            transfer_flag = 0,
            username = packet_client['username'],
            server_name = WAR_TCPHandler.WorldName,
            unk_byte_07 = 0                             # NS related to array of informations
            ))


        #p = struct.pack(">B", opcode_entry[0])
        #p += struct.pack(">B", 0x00)    # UNK_BYTE_00
        #p += struct.pack(">B", 0x00)    # UNK_BYTE_01
        #p += struct.pack(">B", 0x00)    # UNK_BYTE_02
        #p += struct.pack(">B", 0x00)    # UNK_BYTE_03
        #p += struct.pack(">I", packet_client['protocol_version'])
        #p += struct.pack(">B", WAR_TCPHandler.WorldID)    # SERVER_ID
        #p += struct.pack(">B", 0x00)    # UNK_BYTE_04
        #p += struct.pack(">B", 0x00)    # UNK_BYTE_05
        #p += struct.pack(">B", 0x00)    # UNK_BYTE_06
        #p += struct.pack(">B", 0x00)    # TRANSFER_FLAG
        ##p += WAR_Utils.MakeBBuffer(''.join(map(chr, packet_client['username'])))    # USERNAME
        #print packet_client['username']
        #p += WAR_Utils.MakeBBuffer(packet_client['username'])    # USERNAME
        #p += WAR_Utils.MakeBBuffer(WAR_TCPHandler.WorldName)    # SERVER_NAME
        #p += struct.pack(">B", 0x00)    # NS related to arry of informations
        self.send_data(p)

    def response_0x83(self, opcode_entry, packet_client_header, packet_client, packet_data):
        p = struct.pack(">B", opcode_entry[0])
        p += struct.pack(">B", 0x00)
        self.send_data(p)

    def response_S_GAME_OPENED(self, opcode_entry, packet_client_header, packet_client, packet_data):
        """
            Opcode handled by basic block at 0x004C40F7
        """
        p = struct.pack(">B", opcode_entry[0])
        #p += struct.pack(">B", 0x00)
        self.send_data(p)

    def response_F_RECEIVE_ENCRYPTKEY(self, opcode_entry, packet_client_header, packet_client, packet_data):
        """
            Response sent when packet F_ENCRYPTKEY received with key_present is NULL.
            Packet handler check if (WORD)field_0x1CC is not null, and packet is handled in WAR.exe by:
            - 0x004C8883: if send_key is not null, RC4 will be generated and sent with packet F_ENCRYPTKEY
        """
        p = struct.pack(">B", opcode_entry[0])
        p += PACKET_F_RECEIVE_ENCRYPTKEY.build(construct.Container(send_key = 0x01))
        self.send_data(p)

    def response_0xD6(self, opcode_entry, packet_client_header, packet_client, packet_data):
        p = struct.pack(">B", opcode_entry[0])
        p += struct.pack(">I", time.time())
        p += struct.pack(">I", 0)           # TODO CHECK
        self.send_data(p)

    def response_0xDA(self, opcode_entry, packet_client_header, packet_client, packet_data):
        p = struct.pack(">B", opcode_entry[0])
        p += struct.pack(">H", 0x0000)
        p += struct.pack(">H", packet_client['ABILITY_ID'])
        p += struct.pack(">H", 0x4242)      # OBJECT_ID ?
        p += struct.pack(">H", packet_client['ABILITY_ID'])
        p += "\x00\x00\x01\x01\x00\x00\x03\xE8\x01\x00\x00\x00"
        self.send_data(p)


        time.sleep(2)

        #p = "\xD7\x01\x01\x00\x00\x42\x42\x01\x00\x6A\x07\x0A\x37\x00\x81\x02\x01\x00\xA4\x01\x00"
        #self.send_data(p)

        #p = struct.pack(">B", opcode_entry[0])
        #p += struct.pack(">H", 0x4242)
        #p += struct.pack(">H", packet_client['ABILITY_ID'])
        #p += struct.pack(">H", 0x4242)      # OBJECT_ID ?
        #p += struct.pack(">H", packet_client['ABILITY_ID'])
        #p += "\x22\x73\x06\x01\x00\x00\x01\xE6\x00\x00\x00"
        #self.send_data(p)


        #p = struct.pack(">B", opcode_entry[0])
        #p += struct.pack(">H", 0x4242)
        #p += struct.pack(">H", packet_client['ABILITY_ID'])
        #p += struct.pack(">H", 0x4242)      # OBJECT_ID ?
        #p += struct.pack(">H", packet_client['ABILITY_ID'])
        #p += "\x22\x73\x02\x01\x00\x00\x00\x00\x01\x00\x00\x00"
        #self.send_data(p)

        #p = "\xB3\x42\x42\x42\x42\x07\x6A\x00\x00\x07\xA0\x00\xCE\x00"
        #self.send_data(p)
        #p = "\xDA\x92\xC3\x07\x6A\x92\xC3\x05\x2E\x22\x73\x06\x01\x00\x00\x01\xE6\x00\x00\x00"
        #self.send_data(p)

        #p = "\x51\x04\xB2\x00\x00\x00\x00"
        #self.send_data(p)

        #p = "\x09\x07\x26\x62\x2C\x6C\x3A\x16\x08\x64\x00\x64\x00\x00\x00\x00\x00\x16\x00"


    def response_F_PLAYER_WEALTH(self, opcode_entry, packet_client_header, packet_client, packet_data):
        """
            Send GameData.Player.money
            Packet handling is done at basic block 0x004C3BB8.
            Size packet is 0x00000008.
        """
        p = struct.pack(">B", opcode_entry[0])
        p += PACKET_F_PLAYER_WEALTH.build(construct.Container(unk_dword_00 = 0,
            player_money = 0x1337))
        self.send_data(p)

    def response_F_MAX_VELOCITY(self, opcode_entry, packet_client_header, packet_client, packet_data):
        """
            Velocity * 0.0099999998
            Packet handling is done:
                - 0x4DCF59
            Size packet is 0x00000002.
        """
        p = struct.pack(">B", opcode_entry[0])
        p += PACKET_F_MAX_VELOCITY.build(construct.Container(velocity = 0))
        self.send_data(p)

    def response_F_PLAYER_RANK_UPDATE(self, opcode_entry, packet_client_header, packet_client, packet_data):
        """
            F_PLAYER_RANK_UPDATE (0xF4)
            Packet handling is done:
                - 0x4DD5E4
            Size Packet is 0x00000004
        """
        p = struct.pack(">B", opcode_entry[0])
        p += PACKET_F_PLAYER_RANK_UPDATE.build(construct.Container(unk_byte_00 = 0,
            unk_byte_01 = 0,
            object_id = 0))
        self.send_data(p)

    def response_F_PLAYER_EXPERIENCE(self, opcode_entry, packet_client_header, packet_client, packet_data):
        """
            F_PLAYER_EXPERIENCE (0x39)
            Packet handling is done:
                - 0x4DD006
            Size Packet is 0x0000000D (?)
        """
        p = struct.pack(">B", opcode_entry[0])
        p += PACKET_F_PLAYER_EXPERIENCE.build(construct.Container(current_xp = 0x02,
            next_lvl_xp = 0x200,
            rested_xp = 0x100,
            level = 0x01))
        self.send_data(p)

    def response_F_PLAYER_RENOWN(self, opcode_entry, packet_client_header, packet_client, packet_data):
        """
            F_PLAYER_RENOWN (0x4E)
            Packet handling is done:
                - 0x4DD10F
            Size Packet is 0x00000009 (?)
        """
        p = struct.pack(">B", opcode_entry[0])
        p += PACKET_F_PLAYER_RENOWN.build(construct.Container(current_xp = 0x01,
            next_lvl_xp = 0x8,
            rank = 0x02))
        self.send_data(p)

    def response_F_PLAYER_HEALTH(self, opcode_entry, packet_client_header, packet_client, packet_data):
        """
            F_PLAYER_HEALTH (0x05)
            Packet handling is done:
                - 0x4DBBB0
            Size packet is 0x00000010 (?)

        """
        p = struct.pack(">B", opcode_entry[0])
        p += PACKET_F_PLAYER_HEALTH.build(construct.Container(hit_points_current = 0x0226,
            hit_points_max = 0x0226,
            action_points_current = 0x0064,
            action_points_max = 0x0064,
            unk_word_00 = 0x0000,
            unk_word_01 = 0x0000))
        self.send_data(p)

    def response_0xEA(self, opcode_entry, packet_client_header, packet_client, packet_data):
        p = struct.pack(">B", opcode_entry[0])
        p += struct.pack(">B", 0x00)        # TODO
        self.send_data(p)

    def response_F_PLAYER_INIT_COMPLETE(self, opcode_entry, packet_client_header, packet_client, packet_data):
        """
            F_PLAYER_INIT_COMPLETE (0xEF)
            Packet handling is done:
                - 0x4DCFDD
            Size packet is 0x00000002
            Packet data are ignored

            Check if Player->field_255 (0x3FC) is NULL, if True send packet F_CLIENT_DATA
            In all case send packet F_INTERFACE_COMMAND
        """
        p = struct.pack(">B", opcode_entry[0])
        p += PACKET_F_PLAYER_INIT_COMPLETE.build(construct.Container(unk_word_00 = 0x0000))
        self.send_data(p)

    def response_S_PLAYER_INITTED(self, opcode_entry, packet_client_header, packet_client, packet_data):
        """
            S_PLAYER_INITTED (0x88)
            Function 0x4C6346 will convert all Big Endian field to Little Endian.
            Then packet data is handled by 0x004DE151.

            For region ID, refer to file 0x5B701C61C34ABF61 "zones/zones.dat" in world.myp
        """

        p = struct.pack(">B", opcode_entry[0])
        p += PACKET_S_PLAYER_INITTED.build(construct.Container(object_id = 0x4242,
            character_id = 0x4444,
            coord_z = 8456,         # Mount Bloodhorn, Green Skin War Camp (X=810465, Y=863153, Z=8456)
            coord_x = 810465,
            coord_y = 863153,
            coord_o = 0x0CB6,
            player_realm = 2,
            unk_word_00 = 0,
            unk_word_01 = 0,
            region_id = 1,          # ;region001=Dwarf - Greenskin Tier 1 (zones 11 and 6)
            instance_id = 0,
            unk_word_02 = 0,
            unk_word_03 = 0,
            unk_word_04 = 0,
            unk_word_05 = 0))
        self.send_data(p)

    def response_F_BAG_INFO(self, opcode_entry, packet_client_header, packet_client, packet_data):
        """
            F_BAG_INFO (0x95)

            Packet handling is done:
                - 0x4C00D6
            /!\ Little endian /!\
            First byte is a command that can have the value:
                - 0x16:
                - 0x17:
                - 0x18:
                - 0x19:
                - 0x1A:
                - 0x1D:
                - 0x1E:
                - 0x1F:
                - 0x0B:
                - 0x0D:
                - 0x0E:
                - 0x0C:
                - 0x05:
                - 0x09:
                - 0x04:
        """
        p = struct.pack(">B", opcode_entry[0])
        p += struct.pack(">B", 0x0F)            # Command
        p += PACKET_F_BAG_INFO_COMMAND_0F.build(construct.Container(num_backpack_slots = 0x40,
            backpack_expansion_slots = 0x100,
            backpack_expansion_slots_cost = 0x640,
            num_bank_slots = 0x200,
            bank_expansion_slots = 0x50,
            bank_expansion_slots_cost = 0x10
            ))
        self.send_data(p)

    def response_item(self):
        """

            0x2A87C15DF8425A8C data/gamedata/itemdata.csv

        """
        p = struct.pack(">H", 14)           # Slot ID
        p += struct.pack(">B", 0x00)            # unk_byte_00
        p += struct.pack(">I", 0x0133)          # Info Entry        ; i
        p += struct.pack(">H", 0x0446)          # Model ID          ; icon
        p += "\x00" * 7
        p += struct.pack(">H", 0x0000)          # Slot ID
        p += struct.pack(">B", 0x0B)            # Type
        p += struct.pack(">B", 0x00)            # MIN RANK ?
        p += struct.pack(">B", 0x00)            # MIN RANK ?
        p += struct.pack(">B", 0x00)            # MIN RENOWN ?
        p += struct.pack(">B", 0x00)            # MIN RENOWN ?
        p += struct.pack(">B", 0x00)            # MIN RENOWN ?
        p += struct.pack(">B", 0x01)            # RARITY
        p += struct.pack(">B", 0x00)            # UNK
        p += struct.pack(">B", 0x04)            # RACE
        p += struct.pack("<I", 0x00)            # CAREER ?
        p += struct.pack("<I", 0x00)            # UNK
        p += struct.pack("<I", 0x00)            # SELL PRICE
        p += struct.pack(">H", 0x01)            # Count
        p += struct.pack("<I", 0x00)            # UNK
        p += struct.pack("<H", 0x00)            # UNK
        p += struct.pack(">I", 0x400)            # SKILLS
        p += struct.pack(">H", 0x49)            # DPS
        p += struct.pack(">H", 0x190)            # SPEED
        p += WAR_Utils.MakeBBuffer("M3 Ol' St1ck")  # NAME
        p += struct.pack(">B", 0x00)            # NB STATS
        # TODO MAKE STAT
        p += struct.pack(">B", 0x00)            # UNK
        p += struct.pack(">B", 0x00)            # UNK
        p += struct.pack(">B", 0x00)            # UNK
        p += struct.pack(">B", 0x00)            # UNK
        p += struct.pack(">B", 0x00)            # NB TALISMAN SLOTS
        p += WAR_Utils.MakeBBuffer("Description ITEM")  # NAME
        p += struct.pack(">B", 0x00)            # UNK
        p += struct.pack(">B", 0x00)            # UNK
        p += struct.pack(">B", 0x00)            # UNK
        p += struct.pack(">B", 0x00)            # UNK
        p += struct.pack(">H", 0x0302)          # UNK
        p += "\x00" * 8
        p += struct.pack(">B", 0x00)            # UNK
        p += struct.pack(">B", 0x00)            # UNK
        p += "\x00" * 11
        return p

    def reponse_0x4F(self, opcode_entry, packet_client_header, packet_client, packet_data):
        p = struct.pack(">B", opcode_entry[0])
        p += struct.pack(">H", 0x4242)          # Objet ID
        p += struct.pack(">H", 302)             # MOUNT ID ? ; 194,Mount Squig Orange 03,280,200,160,194,0,0,0,,,,,,,,,,,  ; [+] "data/gamedata/monsters.csv" = 4362852945EB393E (dwRetAddr = 00626EDC)
        p += struct.pack(">H", 0x0000)          # UNK
        p += struct.pack(">H", 0x0000)          # UNK
        p += struct.pack(">H", 0x0000)          # UNK
        p += struct.pack(">H", 0x0000)          # UNK
        p += struct.pack(">H", 0x0000)          # UNK
        p += struct.pack(">H", 0x0000)          # UNK
        p += struct.pack(">H", 0x0000)          # UNK
        self.send_data(p)

    def reponse_F_GET_ITEM(self, opcode_entry, packet_client_header, packet_client, packet_data):
        """
            F_GET_ITEM (0xAA)

            Packet handling is done:
                - 0x4D64A2

        """
        p = struct.pack(">B", opcode_entry[0])
        p += struct.pack(">B", 0x01)            # NB
        p += "\x00" * 3                         # PADDING
        p += self.response_item()
        self.send_data(p)

    def response_player_init(self, opcode_entry, packet_client_header, packet_client, packet_data):
        """
            Send all informations related to player initialization
        """

        self.response(F_PLAYER_WEALTH, packet_client_header, packet_client, packet_data)
        self.response(F_MAX_VELOCITY, packet_client_header, packet_client, packet_data)

        self.response(S_PLAYER_INITTED, packet_client_header, packet_client, packet_data)

        #p = 'e21c0000000a9600000018c400000028f000000039ee0000004fb000000065fe00000082320000009ec0000000be96000000e2040300000000000001050e000001302403000000000000015acc00000189840300000000000001bc88000001ee74030000000000000229ca00000263900300000000000002a0bc0400000000000002d26c030000000000000309620300000000000003512e03000000000000039f800300000000000003ec3803000000000000043e04030000000000000488640300000000000004fa1a03000000000000059a240300000000000006442403000000000400000000000006fc2a0300000000000007cec00300000000000008a19c03000000000000097fe0030000000000000ab342030000000000000b6ea4030000000000000c2e02030000000000000d00fc030000000000000dcc8a030000000000000ea19603000000000400000000050000000a06000000000500000050060000000005000000e6060000000005000001b8060000000005000002da06000000000500000438060000000005000005dc060000000005000007d006000000000500000a0006000000000500000c76060000000004000000000500000f320600000000050000122a06000000000500001572060000000005000018f606000000000500001cb6060000000005000020bc060000000005000025080600000000050000299006000000000500002e540600000000050000335e0600000000040000000005000038a406000000000500003e30060000000005000043ee060000000005000049f206000000000500005032060000000005000056ae06000000000500005d660600000000050000646406000000000500006b9406000000000500007300060000000004000000000500007aa80600000000050000828c06000000000500008aa2060000000005000092fe06000000000500009b8c0600000000050000a44c0600000000050000ad520600000000050000b68a0600000000050000bff40600000000050000c99a06000000000300000000050000d3720600000000050000dd860600000000050000e7cc0600000000050000f2440600000000050000fcf80600000000040000000005000107d4060000000005000112ec06000000000500011e36060000000005000129bc0600000000050001356a06000000000300000000050001414a06000000000500014ece06000000000500015e1e06000000000500016f4e06000000000500018290060000000005000198160600000000050001b0120600000000050001caac0600000000050001e820060000000005000208a0060000000003000000000500022c68060000000005000253a006000000000500027e840600000000050002ad5a0600000000050002e0540600000000040000000005000317c2060000000005000353cc060000000005000394b80600000000050003dad6060000000005000426620600000000030000000005000477a20600000000050004cedc06000000000500052c560600000000050005906a0600000000050005fb54060000000004000000000500066d6e0600000000050006e6fe060000000005000768540600000000050007f1ca060000000005000883ba0600000000040000000005000a473d060000000005000ad441060000000005000b6143060000000005000bee460600000000040000000005000c7b48060000000005000d084a060000000005000d954c060000000005000e224f0600000000040000000005000eaf51060000000005000f3c53060000000005000fc9550600000000050010565806000000000400000000050010e35a0600000000050011705c0600000000050011fd5f06000000000500128a610600000000040000000005001317630600000000050013a465060000000005001431680600000000050014be6a06000000000400000000000000000000'.decode('hex')
        #self.send_data(p)

        self.response(F_PLAYER_EXPERIENCE, packet_client_header, packet_client, packet_data)
        self.response(F_PLAYER_RENOWN, packet_client_header, packet_client, packet_data)

        #p = 'be030000000703400800000000'.decode('hex')
        #self.send_data(p)

        self.response(F_PLAYER_HEALTH, packet_client_header, packet_client, packet_data)
        self.response(F_BAG_INFO, packet_client_header, packet_client, packet_data)

        #p = 'aa03000000000a0000000133044600000000000000000a0b0000000000010004000000000000000000000000000100010000000000000400004901900c4d65204f6c2720537469636b000000000000000000000003020000000000000000000000000000000000000000000014000002dcd412c9000000000000000014000000000000010100000000400000000000000000000100010000000000000000000100000f4d6520536f6665737420536869727400000000000000000000000302000000000000000000000000000000000000000000002a0000002e8f0213000000000000000000000000000001050000000000000000000000000000000100010000000000000000000000000f426f6f6b206f662042696e64696e670000000000007355736520746f2072657475726e20746f20796f75722072616c6c7920706f696e742e20596f752063616e2073657420796f75722072616c6c7920706f696e742062792074616c6b696e6720746f207468652052616c6c79204d617374657220696e20616e79206368617074657220617265612e000000000302000000000000000000000000000000000000000000'.decode('hex')
        #self.send_data(p)
        self.response(F_GET_ITEM, packet_client_header, packet_client, packet_data)

        #p = 'be01060300010701010b0101d301076a01076b0100f500'.decode('hex')
        #self.send_data(p)

        #p = 'ea00'.decode('hex')
        #self.send_data(p)
        self.response(0xEA, packet_client_header, packet_client, packet_data)

        p = '4f1aae000000000000000000000000000000000000'.decode('hex')
        self.send_data(p)

        self.response(F_PLAYER_INIT_COMPLETE, packet_client_header, packet_client, packet_data)
    ### ALL HANDLE

    def handle_unknown(self, opcode_entry, packet_client_header, packet_data):
        WAR_Utils.LogInfo("[-] Calling Opcode : 0x%02X (%d) not handled, exit !" % (opcode_entry[0], opcode_entry[0]), 1)
        thread.interrupt_main()
        raise WAR_Utils.WarError("EXIT !")

    def handle_0x01(self, opcode_entry, packet_client_header, packet_data):
        # TODO
        pass

    def handle_F_PLAYER_EXIT(self, opcode_entry, packet_client_header, packet_data):
        #packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        packet_client = opcode_entry[3].parse(packet_data)
        WAR_Utils.LogInfo(packet_client, 2)

    def handle_0x07(self, opcode_entry, packet_client_header, packet_data):
        #packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        packet_client = ""
        packet_data = packet_data[1:]
        WAR_Utils.LogInfo(packet_client, 2)
        print "CMD = " + packet_data
        if packet_data[1:5] == "quit" or packet_data[1:5] == "exit":
            self.response(0x0C, packet_client_header, packet_client, packet_data)
        if packet_data[1:10] == "say mount":
            p = '1E00AE0100'.decode('hex')
            self.send_data(p)
            self.response(0x4F, packet_client_header, packet_client, packet_data)
        if packet_data[1:9] == "say zone":
            p = '1F0000000000000001010000000000000000000000000000'
            self.send_data(p)
        #pass

    def handle_F_PING(self, opcode_entry, packet_client_header, packet_data):
        """
            This packet is sent from method in WAR.exe:
                - 0x004B2F33, size = 0x00000014
            Server has to answer with S_PONG (0x81).
        """
        packet_client = opcode_entry[3].parse(packet_data)
        packet_data = packet_data[SIZE_PACKET_F_PING:]
        WAR_Utils.LogInfo(packet_client, 2)
        self.response(S_PONG, packet_client_header, packet_client, packet_data)

    def handle_0x0D(self, opcode_entry, packet_client_header, packet_data):
        # TODO
        pass

    def handle_0x0E(self, opcode_entry, packet_client_header, packet_data):
        # TODO
        pass

    def handle_F_CONNECT(self, opcode_entry, packet_client_header, packet_data):
        #packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        packet_client = opcode_entry[3].parse(packet_data)
        packet_data = packet_data[SIZE_PACKET_F_CONNECT:]
        WAR_Utils.LogInfo(packet_client, 2)
        xml_data = packet_data[:packet_client['size_xml']]
        #WAR_Utils.LogInfo(xml_data, 2)
        packet_data = packet_data[packet_client['size_xml']:]
        self.response(S_CONNECTED, packet_client_header, packet_client, packet_data)

    def handle_0x10(self, opcode_entry, packet_client_header, packet_data):
        packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        WAR_Utils.LogInfo(packet_client, 2)
        self.finish()

    def handle_0x13(self, opcode_entry, packet_client_header, packet_data):
        packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        WAR_Utils.LogInfo(packet_client, 2)
        self.response(0x13, packet_client_header, packet_client, packet_data)

    def handle_F_OPEN_GAME(self, opcode_entry, packet_client_header, packet_data):
        """
            Opcode 0x17 can be sent in WAR.exe from:
                - 0x004BFF5D, size = 0x00000002
            Server must answer with S_GAME_OPENED (0x85)
        """
        #packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        packet_client = opcode_entry[3].parse(packet_data)
        packet_data = packet_data[SIZE_PACKET_F_OPEN_GAME:]
        WAR_Utils.LogInfo(packet_client, 2)
        self.response(S_GAME_OPENED, packet_client_header, packet_client, packet_data)

    def handle_0x18(self, opcode_entry, packet_client_header, packet_data):
        # TODO
        pass

    def handle_0x25(self, opcode_entry, packet_client_header, packet_data):
        # TODO
        pass

    def handle_F_DUMP_ARENAS_LARGE(self, opcode_entry, packet_client_header, packet_data):
        """
            Opcode 0x35 can be sent in WAR.exe from:
                - 0x004BFEF2, size = 0x00000002
            Server must answer with F_WORLD_ENTER (0x19)
        """
        packet_client = opcode_entry[3].parse(packet_data)
        packet_data = packet_data[SIZE_PACKET_F_DUMP_ARENAS_LARGE:]
        WAR_Utils.LogInfo(packet_client, 2)
        self.response(F_WORLD_ENTER, packet_client_header, packet_client, packet_data)

    def handle_0x40(self, opcode_entry, packet_client_header, packet_data):
        # TODO
        packet_client = ""
        self.response(0xD6, packet_client_header, packet_client, packet_data)
        self.response(0x83, packet_client_header, packet_client, packet_data)

    def handle_F_REQUEST_CHAR(self, opcode_entry, packet_client_header, packet_data):
        #packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        packet_client = opcode_entry[3].parse(packet_data)
        packet_data = packet_data[SIZE_PACKET_F_REQUEST_CHAR:]
        WAR_Utils.LogInfo(packet_client, 2)
        if packet_client['command'] == 0x2D58:
            self.response(0x56, packet_client_header, packet_client, packet_data)
        elif packet_client['command'] == 0x2D53:
            self.response(0x55, packet_client_header, packet_client, packet_data)
        else:
            raise WAR_Utils.WarError("[-] handle_0x54 : UNKNOW command !")

    def handle_F_ENCRYPTKEY(self, opcode_entry, packet_client_header, packet_data):
        """
            First packet received from the client after connection.
            If the field key_present is NULL, server has to answer with F_RECEIVE_ENCRYPTKEY (0x8A).
            If the field key_present is not NULL, RC4 key (256 bytes) is present a the end of packet.

            Opcode 0x5C can be sent from two methods in WAR.exe:
                - 0x004B1819, size = 0x00000006 : key_present is NULL
                - 0x004B2C1B, size = 0x00000106 : RC4 key present
        """
        packet_client = opcode_entry[3].parse(packet_data)
        packet_data = packet_data[SIZE_PACKET_F_ENCRYPTKEY:]
        WAR_Utils.LogInfo(packet_client, 2)
        if packet_client['key_present'] == 0:
            self.response(F_RECEIVE_ENCRYPTKEY, packet_client_header, packet_client, packet_data)
        else:
            key = packet_data[0 : 256]
            WAR_Utils.LogInfo("[+] Key (len(key) = %08X) :" % (len(key)), 3)
            WAR_Utils.LogInfo(WAR_Utils.hexdump(key), 3)
            self.encrypted = True
            self.RC4Key = key

    def handle_0x62(self, opcode_entry, packet_client_header, packet_data):
        #packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        #WAR_Utils.LogInfo(packet_client, 2)
        #print WAR_Utils.hexdump(packet_data)

        F_PLAYER_STATE2 = construct.Struct("F_PLAYER_STATE2",
            construct.UBInt16("unk_word_00"),                           # + 0x00
            construct.UBInt8("flag_movement"),                          # + 0x02
            construct.UBInt8("unk_byte_00"),                            # + 0x02
            construct.UBInt8("unk_byte_01"),                            # + 0x03
            construct.UBInt8("unk_byte_02"),                            # + 0x03
            )

        WAR_Utils.LogInfo(WAR_Utils.hexdump(packet_data[:0x100]))
        packet_un = F_PLAYER_STATE2.parse(packet_data)
        WAR_Utils.LogInfo(packet_un)
        packet_client = ""
        self.response(0x62, packet_client_header, packet_client, packet_data)

    def handle_0x68(self, opcode_entry, packet_client_header, packet_data):
        packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        WAR_Utils.LogInfo(packet_client, 2)
        self.response(0x6A, packet_client_header, packet_client, packet_data)

    def handle_F_INIT_PLAYER(self, opcode_entry, packet_client_header, packet_data):
        """
            Opcode 0x7C can be sent from:
                - 0x004C6D11, size = 0x00000016
        """
        #packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        packet_client = opcode_entry[3].parse(packet_data)
        packet_data = packet_data[SIZE_PACKET_F_INIT_PLAYER:]
        WAR_Utils.LogInfo(packet_client, 2)
        # TODO MAKE ANSWER

        self.response_player_init(opcode_entry, packet_client_header, packet_client, packet_data)

    def handle_0x83(self, opcode_entry, packet_client_header, packet_data):
        # TODO
        pass

    def handle_0xA1(self, opcode_entry, packet_client_header, packet_data):
        packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        WAR_Utils.LogInfo(packet_client, 2)

    def handle_0x91(self, opcode_entry, packet_client_header, packet_data):
        packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        WAR_Utils.LogInfo(packet_client, 2)
        # if sucess
        self.response(0x58, packet_client_header, packet_client, packet_data)
        # else
        #self.response(0x59, packet_client_header, packet_client, packet_data)

    def handle_0x9A(self, opcode_entry, packet_client_header, packet_data):
        # TODO
        pass

    def handle_0xA8(self, opcode_entry, packet_client_header, packet_data):
        # TODO
        pass

    def handle_0xB6(self, opcode_entry, packet_client_header, packet_data):
        # TODO
        pass
        #packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        #WAR_Utils.LogInfo(packet_client, 2)

    def handle_F_PLAYER_ENTER_FULL(self, opcode_entry, packet_client_header, packet_data):
        """
            TODO
        """
        #packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        packet_client = opcode_entry[3].parse(packet_data)
        packet_data = packet_data[SIZE_PACKET_F_PLAYER_ENTER_FULL:]
        WAR_Utils.LogInfo(packet_client, 2)
        self.response(0x80, packet_client_header, packet_client, packet_data)

    def handle_F_INTERFACE_COMMAND(self, opcode_entry, packet_client_header, packet_data):
        """
            This opcode can be sent from methods:
                - 0x004B6DC0, size = 0x00000006,
                - 0x004B6E03, size = ??????????
            TODO CHECK NO RESPONSE?
        """
        #packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        packet_client = opcode_entry[3].parse(packet_data)
        packet_data = packet_data[SIZE_PACKET_F_INTERFACE_COMMAND:]
        WAR_Utils.LogInfo(packet_client, 2)

    def handle_0xD5(self, opcode_entry, packet_client_header, packet_data):
        packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        WAR_Utils.LogInfo(packet_client, 2)
        print "%04X" % packet_client['unk_word_00']
        print "%04X" % packet_client['unk_word_01']
        print "%04X" % packet_client['unk_word_02']
        print "%04X" % packet_client['unk_word_03']
        print "%04X" % packet_client['unk_word_04']
        print "%04X" % packet_client['unk_word_05']
        print "%04X" % packet_client['ABILITY_ID']
        print "%04X" % packet_client['SEQUENCE']
        print "%04X" % packet_client['unk_byte_01']
        print "%04X" % packet_client['unk_word_07']

    #("unk_word_00", WAR_Utils.WORD),
    #("unk_word_01", WAR_Utils.WORD),
    #("unk_word_02", WAR_Utils.WORD),
    #("unk_word_03", WAR_Utils.WORD),
    #("unk_word_04", WAR_Utils.WORD),
    #("unk_word_05", WAR_Utils.WORD),
    #("ABILITY_ID", WAR_Utils.WORD),
    #("SEQUENCE", WAR_Utils.BYTE),
    #("unk_byte_01", WAR_Utils.BYTE),
    #("unk_word_07", WAR_Utils.WORD),

        # IF EVEYRTHING OK
        #time.sleep(3)
        #self.response(0x05, packet_client_header, packet_client, packet_data)
        self.response(0xDA, packet_client_header, packet_client, packet_data)
        #self.send_data("\xB3\x8F\x78\x8F\x63\x07\x6A")

    def handle_0xDB(self, opcode_entry, packet_client_header, packet_data):
        # TODO !
        pass

    def handle_0xDC(self, opcode_entry, packet_client_header, packet_data):
        packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        WAR_Utils.LogInfo(packet_client, 2)

    def handle_0xE5(self, opcode_entry, packet_client_header, packet_data):
        # TODO !
        pass

    def handle_0xE8(self, opcode_entry, packet_client_header, packet_data):
        # TODO !
        pass

    def handle_0xFE(self, opcode_entry, packet_client_header, packet_data):
        # TODO!
        #packet_client, packet_data = WAR_Utils.depack(opcode_entry[3], packet_data)
        #WAR_Utils.LogInfo(packet_client, 2)
        pass

    def handle(self):
        self.name = "WorldTCPHandler"
        self.encrypted = False
        self.OpcodesTableRecv = [
        (0x00, "UNKNOWN", self.handle_unknown, None), (0x01, "UNKNOWN", self.handle_0x01, None),
        (0x02, "UNKNOWN", self.handle_unknown, None), (0x03, "UNKNOWN", self.handle_unknown, None),
        (0x04, "F_PLAYER_EXIT", self.handle_F_PLAYER_EXIT, PACKET_F_PLAYER_EXIT), (0x05, "UNKNOWN", self.handle_unknown, None),
        (0x06, "UNKNOWN", self.handle_unknown, None), (0x07, "F_TEXT", self.handle_0x07, PACKET_F_TEXT),
        (0x08, "UNKNOWN", self.handle_unknown, None), (0x09, "UNKNOWN", self.handle_unknown, None),
        (0x0A, "UNKNOWN", self.handle_unknown, None), (0x0B, "F_PING", self.handle_F_PING, PACKET_F_PING),
        (0x0C, "UNKNOWN", self.handle_unknown, None), (0x0D, "UNKNOWN", self.handle_0x0D, None),
        (0x0E, "UNKNOWN", self.handle_0x0E, None), (0x0F, "F_CONNECT", self.handle_F_CONNECT, PACKET_F_CONNECT),
        (0x10, "F_DISCONNECT", self.handle_0x10, PACKET_F_DISCONNECT), (0x11, "UNKNOWN", self.handle_unknown, None),
        (0x12, "UNKNOWN", self.handle_unknown, None), (0x13, "F_REQUEST_CHAR_TEMPLATES", self.handle_0x13, PACKET_F_REQUEST_CHAR_TEMPLATES),
        (0x14, "UNKNOWN", self.handle_unknown, None), (0x15, "UNKNOWN", self.handle_unknown, None),
        (0x16, "UNKNOWN", self.handle_unknown, None), (0x17, "F_OPEN_GAME", self.handle_F_OPEN_GAME, PACKET_F_OPEN_GAME),
        (0x18, "F_PLAYER_INFO", self.handle_0x18, PACKET_F_PLAYER_INFO), (0x19, "UNKNOWN", self.handle_unknown, None),
        (0x1A, "UNKNOWN", self.handle_unknown, None), (0x1B, "UNKNOWN", self.handle_unknown, None),
        (0x1C, "UNKNOWN", self.handle_unknown, None), (0x1D, "UNKNOWN", self.handle_unknown, None),
        (0x1E, "UNKNOWN", self.handle_unknown, None), (0x1F, "UNKNOWN", self.handle_unknown, None),
        (0x20, "UNKNOWN", self.handle_unknown, None), (0x21, "UNKNOWN", self.handle_unknown, None),
        (0x22, "UNKNOWN", self.handle_unknown, None), (0x23, "UNKNOWN", self.handle_unknown, None),
        (0x24, "UNKNOWN", self.handle_unknown, None), (0x25, "F_GUILD_COMMAND", self.handle_0x25, None),
        (0x26, "UNKNOWN", self.handle_unknown, None), (0x27, "UNKNOWN", self.handle_unknown, None),
        (0x28, "UNKNOWN", self.handle_unknown, None), (0x29, "UNKNOWN", self.handle_unknown, None),
        (0x2A, "UNKNOWN", self.handle_unknown, None), (0x2B, "UNKNOWN", self.handle_unknown, None),
        (0x2C, "UNKNOWN", self.handle_unknown, None), (0x2D, "UNKNOWN", self.handle_unknown, None),
        (0x2E, "UNKNOWN", self.handle_unknown, None), (0x2F, "UNKNOWN", self.handle_unknown, None),
        (0x30, "UNKNOWN", self.handle_unknown, None), (0x31, "UNKNOWN", self.handle_unknown, None),
        (0x32, "UNKNOWN", self.handle_unknown, None), (0x33, "UNKNOWN", self.handle_unknown, None),
        (0x34, "UNKNOWN", self.handle_unknown, None), (0x35, "F_DUMP_ARENAS_LARGE", self.handle_F_DUMP_ARENAS_LARGE, PACKET_F_DUMP_ARENAS_LARGE),
        (0x36, "UNKNOWN", self.handle_unknown, None), (0x37, "UNKNOWN", self.handle_unknown, None),
        (0x38, "UNKNOWN", self.handle_unknown, None), (0x39, "UNKNOWN", self.handle_unknown, None),
        (0x3A, "UNKNOWN", self.handle_unknown, None), (0x3B, "UNKNOWN", self.handle_unknown, None),
        (0x3C, "UNKNOWN", self.handle_unknown, None), (0x3D, "UNKNOWN", self.handle_unknown, None),
        (0x3E, "UNKNOWN", self.handle_unknown, None), (0x3F, "UNKNOWN", self.handle_unknown, None),
        (0x40, "F_REQUEST_WORLD_LARGE", self.handle_0x40, PACKET_F_REQUEST_WORLD_LARGE), (0x41, "UNKNOWN", self.handle_unknown, None),
        (0x42, "UNKNOWN", self.handle_unknown, None), (0x43, "UNKNOWN", self.handle_unknown, None),
        (0x44, "UNKNOWN", self.handle_unknown, None), (0x45, "UNKNOWN", self.handle_unknown, None),
        (0x46, "UNKNOWN", self.handle_unknown, None), (0x47, "UNKNOWN", self.handle_unknown, None),
        (0x48, "UNKNOWN", self.handle_unknown, None), (0x49, "UNKNOWN", self.handle_unknown, None),
        (0x4A, "UNKNOWN", self.handle_unknown, None), (0x4B, "UNKNOWN", self.handle_unknown, None),
        (0x4C, "UNKNOWN", self.handle_unknown, None), (0x4D, "UNKNOWN", self.handle_unknown, None),
        (0x4E, "UNKNOWN", self.handle_unknown, None), (0x4F, "UNKNOWN", self.handle_unknown, None),
        (0x50, "UNKNOWN", self.handle_unknown, None), (0x51, "UNKNOWN", self.handle_unknown, None),
        (0x52, "UNKNOWN", self.handle_unknown, None), (0x53, "UNKNOWN", self.handle_unknown, None),
        (0x54, "F_REQUEST_CHAR", self.handle_F_REQUEST_CHAR, PACKET_F_REQUEST_CHAR), (0x55, "UNKNOWN", self.handle_unknown, None),
        (0x56, "UNKNOWN", self.handle_unknown, None), (0x57, "UNKNOWN", self.handle_unknown, None),
        (0x58, "UNKNOWN", self.handle_unknown, None), (0x59, "UNKNOWN", self.handle_unknown, None),
        (0x5A, "UNKNOWN", self.handle_unknown, None), (0x5B, "UNKNOWN", self.handle_unknown, None),
        (0x5C, "F_ENCRYPTKEY", self.handle_F_ENCRYPTKEY, PACKET_F_ENCRYPTKEY), (0x5D, "UNKNOWN", self.handle_unknown, None),
        (0x5E, "UNKNOWN", self.handle_unknown, None), (0x5F, "UNKNOWN", self.handle_unknown, None),
        (0x60, "UNKNOWN", self.handle_unknown, None), (0x61, "UNKNOWN", self.handle_unknown, None),
        (0x62, "F_PLAYER_STATE2", self.handle_0x62, PACKET_F_PLAYER_STATE2), (0x63, "UNKNOWN", self.handle_unknown, None),
        (0x64, "UNKNOWN", self.handle_unknown, None), (0x65, "UNKNOWN", self.handle_unknown, None),
        (0x66, "UNKNOWN", self.handle_unknown, None), (0x67, "UNKNOWN", self.handle_unknown, None),
        (0x68, "F_CHECK_NAME", self.handle_0x68, F_CHECK_NAME), (0x69, "UNKNOWN", self.handle_unknown, None),
        (0x6A, "UNKNOWN", self.handle_unknown, None), (0x6B, "UNKNOWN", self.handle_unknown, None),
        (0x6C, "UNKNOWN", self.handle_unknown, None), (0x6D, "UNKNOWN", self.handle_unknown, None),
        (0x6E, "UNKNOWN", self.handle_unknown, None), (0x6F, "UNKNOWN", self.handle_unknown, None),
        (0x70, "UNKNOWN", self.handle_unknown, None), (0x71, "UNKNOWN", self.handle_unknown, None),
        (0x72, "UNKNOWN", self.handle_unknown, None), (0x73, "UNKNOWN", self.handle_unknown, None),
        (0x74, "UNKNOWN", self.handle_unknown, None), (0x75, "UNKNOWN", self.handle_unknown, None),
        (0x76, "UNKNOWN", self.handle_unknown, None), (0x77, "UNKNOWN", self.handle_unknown, None),
        (0x78, "UNKNOWN", self.handle_unknown, None), (0x79, "UNKNOWN", self.handle_unknown, None),
        (0x7A, "UNKNOWN", self.handle_unknown, None), (0x7B, "UNKNOWN", self.handle_unknown, None),
        (0x7C, "F_INIT_PLAYER", self.handle_F_INIT_PLAYER, PACKET_F_INIT_PLAYER), (0x7D, "UNKNOWN", self.handle_unknown, None),
        (0x7E, "UNKNOWN", self.handle_unknown, None), (0x7F, "UNKNOWN", self.handle_unknown, None),
        (0x80, "UNKNOWN", self.handle_unknown, None), (0x81, "UNKNOWN", self.handle_unknown, None),
        (0x82, "UNKNOWN", self.handle_unknown, None), (0x83, "S_WORLD_SENT", self.handle_0x83, PACKET_S_WORLD_SENT),
        (0x84, "UNKNOWN", self.handle_unknown, None), (0x85, "UNKNOWN", self.handle_unknown, None),
        (0x86, "UNKNOWN", self.handle_unknown, None), (0x87, "UNKNOWN", self.handle_unknown, None),
        (0x88, "UNKNOWN", self.handle_unknown, None), (0x89, "UNKNOWN", self.handle_unknown, None),
        (0x8A, "UNKNOWN", self.handle_unknown, None), (0x8B, "UNKNOWN", self.handle_unknown, None),
        (0x8C, "UNKNOWN", self.handle_unknown, None), (0x8D, "UNKNOWN", self.handle_unknown, None),
        (0x8E, "UNKNOWN", self.handle_unknown, None), (0x8F, "UNKNOWN", self.handle_unknown, None),
        (0x90, "UNKNOWN", self.handle_unknown, None), (0x91, "F_CREATE_CHARACTER", self.handle_0x91, PACKET_F_CREATE_CHARACTER),
        (0x92, "UNKNOWN", self.handle_unknown, None), (0x93, "UNKNOWN", self.handle_unknown, None),
        (0x94, "UNKNOWN", self.handle_unknown, None), (0x95, "UNKNOWN", self.handle_unknown, None),
        (0x96, "UNKNOWN", self.handle_unknown, None), (0x97, "UNKNOWN", self.handle_unknown, None),
        (0x98, "UNKNOWN", self.handle_unknown, None), (0x99, "UNKNOWN", self.handle_unknown, None),
        (0x9A, "F_HELP_DATA", self.handle_0x9A, None), (0x9B, "UNKNOWN", self.handle_unknown, None),
        (0x9C, "UNKNOWN", self.handle_unknown, None), (0x9D, "UNKNOWN", self.handle_unknown, None),
        (0x9E, "UNKNOWN", self.handle_unknown, None), (0x9F, "UNKNOWN", self.handle_unknown, None),
        (0xA0, "UNKNOWN", self.handle_unknown, None), (0xA1, "F_INTERRUPT", self.handle_0xA1, PACKET_F_INTERRUPT),
        (0xA2, "UNKNOWN", self.handle_unknown, None), (0xA3, "UNKNOWN", self.handle_unknown, None),
        (0xA4, "UNKNOWN", self.handle_unknown, None), (0xA5, "UNKNOWN", self.handle_unknown, None),
        (0xA6, "UNKNOWN", self.handle_unknown, None), (0xA7, "UNKNOWN", self.handle_unknown, None),
        (0xA8, "F_INTERACT_QUEUE", self.handle_0xA8, PACKET_F_INTERACT_QUEUE), (0xA9, "UNKNOWN", self.handle_unknown, None),
        (0xAA, "UNKNOWN", self.handle_unknown, None), (0xAB, "UNKNOWN", self.handle_unknown, None),
        (0xAC, "UNKNOWN", self.handle_unknown, None), (0xAD, "UNKNOWN", self.handle_unknown, None),
        (0xAE, "UNKNOWN", self.handle_unknown, None), (0xAF, "UNKNOWN", self.handle_unknown, None),
        (0xB0, "UNKNOWN", self.handle_unknown, None), (0xB1, "UNKNOWN", self.handle_unknown, None),
        (0xB2, "UNKNOWN", self.handle_unknown, None), (0xB3, "UNKNOWN", self.handle_unknown, None),
        (0xB4, "UNKNOWN", self.handle_unknown, None), (0xB5, "UNKNOWN", self.handle_unknown, None),
        (0xB6, "F_SOCIAL_NETWORK", self.handle_0xB6, None), (0xB7, "UNKNOWN", self.handle_unknown, None),
        (0xB8, "F_PLAYER_ENTER_FULL", self.handle_F_PLAYER_ENTER_FULL, PACKET_F_PLAYER_ENTER_FULL), (0xB9, "UNKNOWN", self.handle_unknown, None),
        (0xBA, "UNKNOWN", self.handle_unknown, None), (0xBB, "UNKNOWN", self.handle_unknown, None),
        (0xBC, "UNKNOWN", self.handle_unknown, None), (0xBD, "UNKNOWN", self.handle_unknown, None),
        (0xBE, "UNKNOWN", self.handle_unknown, None), (0xBF, "UNKNOWN", self.handle_unknown, None),
        (0xC0, "UNKNOWN", self.handle_unknown, None), (0xC1, "UNKNOWN", self.handle_unknown, None),
        (0xC2, "UNKNOWN", self.handle_unknown, None), (0xC3, "UNKNOWN", self.handle_unknown, None),
        (0xC4, "UNKNOWN", self.handle_unknown, None), (0xC5, "UNKNOWN", self.handle_unknown, None),
        (0xC6, "UNKNOWN", self.handle_unknown, None), (0xC7, "UNKNOWN", self.handle_unknown, None),
        (0xC8, "F_INTERFACE_COMMAND", self.handle_F_INTERFACE_COMMAND, PACKET_F_INTERFACE_COMMAND), (0xC9, "UNKNOWN", self.handle_unknown, None),
        (0xCA, "UNKNOWN", self.handle_unknown, None), (0xCB, "UNKNOWN", self.handle_unknown, None),
        (0xCC, "UNKNOWN", self.handle_unknown, None), (0xCD, "UNKNOWN", self.handle_unknown, None),
        (0xCE, "UNKNOWN", self.handle_unknown, None), (0xCF, "UNKNOWN", self.handle_unknown, None),
        (0xD0, "UNKNOWN", self.handle_unknown, None), (0xD1, "UNKNOWN", self.handle_unknown, None),
        (0xD2, "UNKNOWN", self.handle_unknown, None), (0xD3, "UNKNOWN", self.handle_unknown, None),
        (0xD4, "UNKNOWN", self.handle_unknown, None), (0xD5, "F_DO_ABILITY", self.handle_0xD5, PACKET_F_DO_ABILITY),
        (0xD6, "UNKNOWN", self.handle_unknown, None), (0xD7, "UNKNOWN", self.handle_unknown, None),
        (0xD8, "UNKNOWN", self.handle_unknown, None), (0xD9, "UNKNOWN", self.handle_unknown, None),
        (0xDA, "UNKNOWN", self.handle_unknown, None), (0xDB, "F_INFLUENCE_DETAILS", self.handle_0xDB, PACKET_F_INFLUENCE_DETAILS),
        (0xDC, "F_SWITCH_ATTACK_MODE", self.handle_0xDC, PACKET_F_SWITCH_ATTACK_MODE), (0xDD, "UNKNOWN", self.handle_unknown, None),
        (0xDE, "UNKNOWN", self.handle_unknown, None), (0xDF, "UNKNOWN", self.handle_unknown, None),
        (0xE0, "UNKNOWN", self.handle_unknown, None), (0xE1, "UNKNOWN", self.handle_unknown, None),
        (0xE2, "UNKNOWN", self.handle_unknown, None), (0xE3, "UNKNOWN", self.handle_unknown, None),
        (0xE4, "UNKNOWN", self.handle_unknown, None), (0xE5, "F_UI_MOD", self.handle_0xE5, PACKET_F_UI_MOD),
        (0xE6, "UNKNOWN", self.handle_unknown, None), (0xE7, "UNKNOWN", self.handle_unknown, None),
        (0xE8, "F_CLIENT_DATA", self.handle_0xE8, PACKET_F_CLIENT_DATA), (0xE9, "UNKNOWN", self.handle_unknown, None),
        (0xEA, "UNKNOWN", self.handle_unknown, None), (0xEB, "UNKNOWN", self.handle_unknown, None),
        (0xEC, "UNKNOWN", self.handle_unknown, None), (0xED, "UNKNOWN", self.handle_unknown, None),
        (0xEE, "UNKNOWN", self.handle_unknown, None), (0xEF, "UNKNOWN", self.handle_unknown, None),
        (0xF0, "UNKNOWN", self.handle_unknown, None), (0xF1, "UNKNOWN", self.handle_unknown, None),
        (0xF2, "UNKNOWN", self.handle_unknown, None), (0xF3, "UNKNOWN", self.handle_unknown, None),
        (0xF4, "UNKNOWN", self.handle_unknown, None), (0xF5, "UNKNOWN", self.handle_unknown, None),
        (0xF6, "UNKNOWN", self.handle_unknown, None), (0xF7, "UNKNOWN", self.handle_unknown, None),
        (0xF8, "UNKNOWN", self.handle_unknown, None), (0xF9, "UNKNOWN", self.handle_unknown, None),
        (0xFA, "UNKNOWN", self.handle_unknown, None), (0xFB, "UNKNOWN", self.handle_unknown, None),
        (0xFC, "UNKNOWN", self.handle_unknown, None), (0xFD, "UNKNOWN", self.handle_unknown, None),
        (0xFE, "F_PLAY_VOICE_OVER", self.handle_0xFE, PACKET_F_PLAY_VOICE_OVER), (0xFF, "UNKNOWN", self.handle_unknown, None),
        ]
        self.WorldSent = [
            (0x05, "F_PLAYER_HEALTH", self.response_F_PLAYER_HEALTH),
            (0x0C, "F_PLAYER_QUIT", self.reponse_0x0C),
            (0x13, "F_REQUEST_CHAR_TEMPLATES", self.response_0x13),
            (0x19, "F_WORLD_ENTER", self.response_F_WORLD_ENTER),
            (0x1E, "F_MAX_VELOCITY", self.response_F_MAX_VELOCITY),
            (0x39, "F_PLAYER_EXPERIENCE", self.response_F_PLAYER_EXPERIENCE),
            (0x4E, "F_PLAYER_RENOWN", self.response_F_PLAYER_RENOWN),
            (0x4F, "F_MOUNT_UPDATE", self.reponse_0x4F),
            (0x52, "F_PLAYER_WEALTH", self.response_F_PLAYER_WEALTH),
            (0x55, "F_REQUEST_CHAR_RESPONSE", self.response_F_REQUEST_CHAR_RESPONSE),
            (0x56, "F_REQUEST_CHAR_ERROR", self.response_0x56),
            (0x58, "F_SEND_CHARACTER_RESPONSE", self.response_0x58),
            (0x59, "F_SEND_CHARACTER_ERROR", self.response_0x59),
            (0x62, "F_PLAYER_STATE2", self.response_0x62),
            (0x6A, "F_CHECK_NAME_RESPONSE", self.response_0x6A),
            (0x80, "S_PID_ASSIGN", self.response_S_PID_ASSIGN),
            (0x81, "S_PONG", self.response_S_PONG),
            (0x82, "S_CONNECTED", self.response_S_CONNECTED),
            (0x83, "S_WORLD_SENT", self.response_0x83),
            (0x85, "S_GAME_OPENED", self.response_S_GAME_OPENED),
            (0x88, "S_PLAYER_INITTED", self.response_S_PLAYER_INITTED),
            (0x8A, "F_RECEIVE_ENCRYPTKEY", self.response_F_RECEIVE_ENCRYPTKEY),
            (0x95, "F_BAG_INFO", self.response_F_BAG_INFO),
            (0xAA, "F_GET_ITEM", self.reponse_F_GET_ITEM),
            (0xD6, "F_SET_TIME", self.response_0xD6),
            (0xDA, "F_USE_ABILITY", self.response_0xDA),
            (0xEA, "F_QUEST_LIST", self.response_0xEA),
            (0xEF, "F_PLAYER_INIT_COMPLETE", self.response_F_PLAYER_INIT_COMPLETE),
            (0xF4, "F_PLAYER_RANK_UPDATE", self.response_F_PLAYER_RANK_UPDATE)
        ]
        WAR_Utils.LogInfo("WorldTCPHandler : New connection from %s : %d" % (self.client_address[0], self.client_address[1]), 1)
        self.handle_recv_data()

    def finish(self):
        WAR_Utils.LogInfo("WorldTCPHandler : Closing connection from %s : %d" % (self.client_address[0], self.client_address[1]), 1)
        return SocketServer.BaseRequestHandler.finish(self)

if __name__ == "__main__":

    WorldServer = WAR_TCPHandler.ThreadedTCPServer((WAR_TCPHandler.WorldHost, WAR_TCPHandler.WorldPort), WorldTCPHandler)
    WorldServer.allow_reuse_address = True
    WorldServerThr = threading.Thread(target=WorldServer.serve_forever)
    WorldServerThr.daemon = True
    WorldServerThr.start()
    WAR_Utils.LogInfo("[+] WorldServer started on \"%s\" : %d" % (WAR_TCPHandler.WorldHost, WAR_TCPHandler.WorldPort), 1)

    raw_input('Press enter to stop servers.\n')
    WorldServerThr._Thread__stop()