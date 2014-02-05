import SocketServer
import struct
import threading

import WAR_Utils

LoginHost, LoginPort = "", 18046
WorldHost, WorldPort = "", 18047
WorldName = "moo"

class TCPHandler(SocketServer.BaseRequestHandler):

    def recv_data(self, size = 1000):
        buf = self.request.recv(size)
        print "[+] Receiving data (%s) from %s : %d" % (self.name, self.client_address[0], self.client_address[1])
        buf_len = len(buf)
        print "[+] len(buf) = %d (0x%08X)" % (buf_len, buf_len)
        if buf_len == 0:
            return ""
        print WAR_Utils.hexdump(buf)
        return buf

    def send_data(self, buf):
        print "[+] Sending data (%s) to %s : %d" % (self.name, self.client_address[0], self.client_address[1])
        print "[+] len(buf) = %d (0x%08X)" % (len(buf), len(buf))
        print WAR_Utils.hexdump(buf)
        self.request.send(buf)
        return