import SocketServer
import struct
import time
import zlib

import WAR_TCPHandler
import WAR_Utils

import protobuf.VerifyProtocolReq_pb2
import protobuf.VerifyProtocolReply_pb2
import protobuf.ResultCodes_pb2
import protobuf.AuthSessionTokenReq_pb2
import protobuf.AuthSessionTokenReply_pb2
import protobuf.GetAcctPropListReq_pb2
import protobuf.GetAcctPropListReply_pb2
import protobuf.MetricEventNotify_pb2
import protobuf.GetClusterListReply_pb2
import protobuf.ClusterStatus_pb2
import protobuf.GetCharSummaryListReply_pb2

class LoginTCPHandler(WAR_TCPHandler.TCPHandler):

    def handle(self):
        self.encrypted = False
        self.name = "LoginTCPHandler"
        print "LoginTCPHandler : New connection from %s : %d" % (self.client_address[0], self.client_address[1])

        while True:
            buf = self.recv_data()
            if buf == "":
                break
            size_packet, buf = WAR_Utils.GetByte(buf)
            opcode_packet, buf = WAR_Utils.GetByte(buf)
            print "[+] Size packet : %08X" % (size_packet)
            print "[+] Opcode packet : %08X" % (opcode_packet)
            if size_packet != 0:
                buf = self.recv_data(size_packet)
            else:
                buf = ""
            self.handle_opcode(opcode_packet, buf)

    def handle_opcode(self, opcode, buf):
        if opcode == 0x01:
            self.handle_VerifyProtocolReq(buf)
        elif opcode == 0x05:
            self.handle_AuthSessionTokenReq(buf)
        elif opcode == 0x07:
            self.handle_GetCharSummaryListReq(buf)
        elif opcode == 0x09:
            self.handle_GetClusterList(buf)
        elif opcode == 0x0B:
            self.handle_MetricEventNotify(buf)
        elif opcode == 0x0D:
            self.handle_GetAccountProperties(buf)
        else:
            print "[-] UNNKOW OPCODE %d (%02X)" % (opcode, opcode)
            exit(0)

    def handle_VerifyProtocolReq(self, buf):
        print "[+] handle_VerifyProtocolReq"
        # we don't need to unserialize
        #vreq = protobuf.VerifyProtocolReq_pb2.VerifyProtocolReq()
        #vreq.ParseFromString(buf)
        vrep = protobuf.VerifyProtocolReply_pb2.VerifyProtocolReply()
        vrep.result_code = protobuf.ResultCodes_pb2.RES_SUCCESS
        vrep.iv1 = "\x12" * 16
        vrep.iv2 = "\x12" * 16
        buf_rep = vrep.SerializeToString()
        p = struct.pack(">B", len(buf_rep))
        # VerifyProtocolReply
        p += struct.pack(">B", 0x02)
        p += buf_rep
        self.send_data(p)

    def handle_AuthSessionTokenReq(self, buf):
        print "[+] handle_AuthSessionTokenReq"
        vreq = protobuf.AuthSessionTokenReq_pb2.AuthSessionTokenReq()
        vreq.ParseFromString(buf)
        print "[+] Session_token = " + vreq.session_token
        vrep = protobuf.AuthSessionTokenReply_pb2.AuthSessionTokenReply()
        vrep.result_code = protobuf.ResultCodes_pb2.RES_SUCCESS
        buf_rep = vrep.SerializeToString()
        p = struct.pack(">B", len(buf_rep))
        # AuthSessionTokenReply
        p += struct.pack(">B", 0x06)
        p += buf_rep
        self.send_data(p)

    def handle_GetAccountProperties(self, buf):
        """ RVA Client : 0x956E24 """
        print "[+] handle_GetAccountProperties"
        vreq = protobuf.GetAcctPropListReq_pb2.GetAcctPropListReq()
        vreq.ParseFromString(buf)

        print "[+] prop_list = " + str(vreq.prop_list)

        vrep = protobuf.GetAcctPropListReply_pb2.GetAcctPropListReply()
        vrep.result_code = protobuf.ResultCodes_pb2.RES_SUCCESS
        buf_rep = vrep.SerializeToString()
        p = struct.pack(">B", len(buf_rep))
        # GetAcctPropListReply
        p += struct.pack(">B", 0x0C)
        p += buf_rep
        self.send_data(p)

    def handle_MetricEventNotify(self, buf):
        print "[+] handle_MetricEventNotify"
        vreq = protobuf.MetricEventNotify_pb2.MetricEventNotify()
        vreq.ParseFromString(buf)

    def handle_GetClusterList(self, buf):

        REALM_ID = 1
        REALM_NAME = "moo"

        print "[+] handle_GetClusterList"

        vrep = protobuf.GetClusterListReply_pb2.GetClusterListReply()
        vrep.result_code = protobuf.ResultCodes_pb2.RES_SUCCESS

        cluster_info = vrep.cluster_list.add()

        cluster_info.cluster_id = REALM_ID
        cluster_info.cluster_name = REALM_NAME
        cluster_info.lobby_host = "127.0.0.1"
        cluster_info.lobby_port = WAR_TCPHandler.WorldPort

        #cluster_info.cluster_pop = ???
        #cluster_info.max_cluster_pop = ???
        #cluster_info.cluster_pop_status.add() ???

        cluster_info.language_id = 0

        cluster_info.cluster_status = protobuf.ClusterStatus_pb2.STATUS_ONLINE

        server_info = cluster_info.server_list.add()

        server_info.server_id = REALM_ID
        server_info.server_name = REALM_NAME

        #cluster_prop = clust_info.property_list.add()

        buf_rep = vrep.SerializeToString()
        p = struct.pack(">B", len(buf_rep))
        # GetClusterListReply
        p += struct.pack(">B", 0x0A)
        p += buf_rep
        self.send_data(p)

    def handle_GetCharSummaryListReq(self, buf):
        print "[+] handle_GetCharSummaryListReq"

        vrep = protobuf.GetCharSummaryListReply_pb2.GetCharSummaryListReply()
        vrep.result_code = protobuf.ResultCodes_pb2.RES_SUCCESS

        buf_rep = vrep.SerializeToString()
        p = struct.pack(">B", len(buf_rep))
        # GetCharSummaryListReply
        p += struct.pack(">B", 0x08)
        p += buf_rep
        self.send_data(p)

    def finish(self):
        print "LoginTCPHandler : Closing connection from %s : %d" % (self.client_address[0], self.client_address[1])
        return SocketServer.BaseRequestHandler.finish(self)