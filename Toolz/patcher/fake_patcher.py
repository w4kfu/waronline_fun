import BaseHTTPServer
import urlparse
import urllib 
import SocketServer
import threading
import zlib

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 80

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines).rstrip('\n')

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        print "[+] GET"
        print self.path
        if self.path == "/products/patcher/manifest/patcher.prod.sig":
            msg = '''<MythicMFT>
                <signature id="3" v="AICwAnz1+uJjEmQrfcbGklzSiNLncFVoxUy0ha6EE/eV/Y4Lvfyt7Z6inrhy1rQH0IN2RlHWknGU1fBKi7KTrnHPMe74mNmwz5O8708uhF02GLrZxmGP2ZPvF2xeBkJUKF5/nnztYOJTiyQ/E6ACAEOfGgbGyRS+ZDyLRMbjY2FPtQ==" />
            </MythicMFT>'''
        elif self.path == "/products/patcher/manifest/patcher.prod":
            msg = '''<MythicMFT>
    <product serial="1220248331" launchfile="war.exe">
        <manifestrepos>
            <repo url="http://127.0.0.1/patcher-valid-qa/patch/patcher/manifest/" />
        </manifestrepos>
        <filerepos>
            <repo url="http://127.0.0.1/patcher-valid-qa/patch/patcher/files/" />
        </filerepos>
        <stages>
            <stage name="main" priority="0">

            </stage>
        </stages>
    </product>
</MythicMFT>
'''
        elif self.path == "/patcher-valid-qa/patch/patcher/manifest/base/pkg.mft":
            msg = '''<MythicMFT>
    <manifest>
        <files>
            <f n="war.jpg" ul="1b07c" t="4654a36c">
                <sig id="3" v="AIEBUpN/vQAHWNTuThKs0/NLYLu/tjVs4NcHGFJPzStHWcXBpfv4NTGoRKU3zvkjEIjfuuOIuxbF1Qpk2VpxNAst4Vz+F00sThczev/aEdjtqqTZUkXlI51iVn5KMmPQFoSIjtdrQG10qGfax78O7pCONo44XFinUCmNKHt5VWS+wzM=" />
            </f>
        </files>
    </manifest>
</MythicMFT>
'''
            msg = zlib.compress(msg)
            print hexdump(msg)
        elif self.path == "/patcher-valid-qa/patch/patcher/manifest/productlist":
            msg = '''<MythicMFT>
    <productList>

    </productList>
</MythicMFT>
'''        

        self.send_response(200)
        self.send_header("Content-type", "application/octet-stream")
        self.send_header('Content-Length', len(msg))
        self.end_headers()
        self.wfile.write(msg)

        #if self.path == "/patch/patcher/manifest/patcher-goa.prod.sig":
        #    self.wfile.write(msg)
        #    return
        #elif self.path == '/manifest':
        #    self.wfile.write(open("manifest", "rb").read())
        #    return
        return    

    def do_POST(self):
        print "[+] POST"
        print self.path
        pass

if __name__ == '__main__':
    print "[+] Don't forget to patch warpatch.exe!"
    httpd = BaseHTTPServer.HTTPServer((HOST_NAME, PORT_NUMBER), Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
    print "Server Stopped - %s:%s" % (HOST_NAME, PORT_NUMBER)
