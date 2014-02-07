import SocketServer
import struct
import time
import zlib
import threading

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

    VERIFYPROTOCOLREPLY = 0x02
    AUTHSESSIONTOKENREPLY = 0x06
    GETCHARSUMMARYLISTREPLY = 0x08
    GETCLUSTERLISTREPLY = 0x0A
    GETACCTPROPLISTREPLY = 0x0C

    def handle(self):
        self.OpcodesTableRecv = [
            (0x00, "UNKNOWN", self.handle_unknown),
            (0x01, "VerifyProtocolReq", self.handle_VerifyProtocolReq),
            (0x02, "UNKNOWN", self.handle_unknown),
            (0x03, "UNKNOWN", self.handle_unknown),
            (0x04, "UNKNOWN", self.handle_unknown),
            (0x05, "AuthSessionTokenReq", self.handle_AuthSessionTokenReq),
            (0x06, "UNKNOWN", self.handle_unknown),
            (0x07, "GetCharSummaryListReq", self.handle_GetCharSummaryListReq),
            (0x08, "UNKNOWN", self.handle_unknown),
            (0x09, "GetClusterList", self.handle_GetClusterList),
            (0x0A, "UNKNOWN", self.handle_unknown),
            (0x0B, "MetricEventNotify", self.handle_MetricEventNotify),
            (0x0C, "UNKNOWN", self.handle_unknown),
            (0x0D, "GetAccountProperties", self.handle_GetAccountProperties),
            (0x0E, "UNKNOWN", self.handle_unknown),
            (0x0F, "UNKNOWN", self.handle_unknown),
        ]
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
        if opcode <= len(self.OpcodesTableRecv):
            entry_opcode = self.OpcodesTableRecv[opcode]
            print "[+] Calling opcode 0x%02X : %s" % (entry_opcode[0], entry_opcode[1])
            entry_opcode[2](buf)
        else:
            print "[-] OPCODE LARGER THAN OpcodesTableRecv size : (%02X) %d " % (opcode, opcode)
            exit(0)

    def handle_unknown(self, buf):
        print "[-] EXIT !"
        exit(0)

    def putheaderandsend(self, opcode, buf):
        p = struct.pack(">B", len(buf))
        p += struct.pack(">B", opcode)
        p += buf
        self.send_data(p)

    def handle_VerifyProtocolReq(self, buf):
        # we don't need to unserialize
        #vreq = protobuf.VerifyProtocolReq_pb2.VerifyProtocolReq()
        #vreq.ParseFromString(buf)
        vrep = protobuf.VerifyProtocolReply_pb2.VerifyProtocolReply()
        vrep.result_code = protobuf.ResultCodes_pb2.RES_SUCCESS
        vrep.iv1 = "\x12" * 16
        vrep.iv2 = "\x12" * 16
        buf_rep = vrep.SerializeToString()
        # VerifyProtocolReply
        self.putheaderandsend(self.VERIFYPROTOCOLREPLY, buf_rep)

    def handle_AuthSessionTokenReq(self, buf):
        vreq = protobuf.AuthSessionTokenReq_pb2.AuthSessionTokenReq()
        vreq.ParseFromString(buf)
        print "[+] Session_token = " + vreq.session_token
        vrep = protobuf.AuthSessionTokenReply_pb2.AuthSessionTokenReply()
        vrep.result_code = protobuf.ResultCodes_pb2.RES_SUCCESS
        buf_rep = vrep.SerializeToString()
        # AuthSessionTokenReply
        self.putheaderandsend(self.AUTHSESSIONTOKENREPLY, buf_rep)

    def handle_GetAccountProperties(self, buf):
        vreq = protobuf.GetAcctPropListReq_pb2.GetAcctPropListReq()
        vreq.ParseFromString(buf)
        print "[+] prop_list = " + str(vreq.prop_list)
        vrep = protobuf.GetAcctPropListReply_pb2.GetAcctPropListReply()
        vrep.result_code = protobuf.ResultCodes_pb2.RES_SUCCESS
        buf_rep = vrep.SerializeToString()

        # GetAcctPropListReply
        self.putheaderandsend(self.GETACCTPROPLISTREPLY, buf_rep)

    def handle_MetricEventNotify(self, buf):
        vreq = protobuf.MetricEventNotify_pb2.MetricEventNotify()
        vreq.ParseFromString(buf)

    def handle_GetClusterList(self, buf):

        REALM_ID = 1
        REALM_NAME = "moo"

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

        # GetClusterListReply
        self.putheaderandsend(self.GETCLUSTERLISTREPLY, buf_rep)

    def handle_GetCharSummaryListReq(self, buf):
        vrep = protobuf.GetCharSummaryListReply_pb2.GetCharSummaryListReply()
        vrep.result_code = protobuf.ResultCodes_pb2.RES_SUCCESS
        buf_rep = vrep.SerializeToString()

        # GetCharSummaryListReply
        self.putheaderandsend(self.GETCHARSUMMARYLISTREPLY, buf_rep)

    def finish(self):
        print "LoginTCPHandler : Closing connection from %s : %d" % (self.client_address[0], self.client_address[1])
        return SocketServer.BaseRequestHandler.finish(self)

if __name__ == "__main__":

    LoginServer = WAR_TCPHandler.ThreadedTCPServer((WAR_TCPHandler.LoginHost, WAR_TCPHandler.LoginPort), LoginTCPHandler)
    LoginServer.allow_reuse_address = True
    LoginServerThr = threading.Thread(target=LoginServer.serve_forever)
    LoginServerThr.daemon = True
    LoginServerThr.start()
    print "[+] LoginServer started on \"%s\" : %d" % (WAR_TCPHandler.LoginHost, WAR_TCPHandler.LoginPort)

    raw_input('Press enter to stop servers.\n')
    LoginServerThr._Thread__stop()