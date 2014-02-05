import SocketServer
import threading

import WAR_LoginServer
import WAR_WorldServer

import WAR_TCPHandler

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":

    LoginServer = ThreadedTCPServer((WAR_TCPHandler.LoginHost, WAR_TCPHandler.LoginPort), WAR_LoginServer.LoginTCPHandler)
    LoginServer.allow_reuse_address = True
    LoginServerThr = threading.Thread(target=LoginServer.serve_forever)
    LoginServerThr.daemon = True
    LoginServerThr.start()
    print "[+] LoginServer started on \"%s\" : %d" % (WAR_TCPHandler.LoginHost, WAR_TCPHandler.LoginPort)

    WorldServer = ThreadedTCPServer((WAR_TCPHandler.WorldHost, WAR_TCPHandler.WorldPort), WAR_WorldServer.WorldTCPHandler)
    WorldServer.allow_reuse_address = True
    WorldServerThr = threading.Thread(target=WorldServer.serve_forever)
    WorldServerThr.daemon = True
    WorldServerThr.start()
    print "[+] WorldServer started on \"%s\" : %d" % (WAR_TCPHandler.WorldHost, WAR_TCPHandler.WorldPort)

    raw_input('Press enter to stop servers.\n')
    LoginServerThr._Thread__stop()
    WorldServerThr._Thread__stop()
