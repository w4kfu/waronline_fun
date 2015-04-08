from idaapi import *
from idc import *
from idautils import *

# Found in crc16.cpp from flair
def CRC16(data):
    POLY = 0x8408
    crc = 0xFFFF
    for c in data:
        c = ord(c)
        for i in xrange(0, 8):
            if ((crc ^ c) & 1) != 0:
                crc = (crc >> 1) ^ POLY
            else:
                crc >>= 1
            c >>= 1
    crc = (~crc)
    data = crc
    crc = (crc << 8) | ((data >> 8) & 0xFF)
    return (crc & 0xFFFF)

def ComputeCRCFunc(func_start_ea, func_len, byte_ref):
    pos = 32
    crc = ""
    while pos < func_len and pos < (255 + 32) and (func_start_ea + pos) not in byte_ref:
        crc += chr(Byte(func_start_ea + pos))
        pos += 1
    crc = CRC16(crc)
    crc_len = pos - 32
    return (crc, crc_len)

def FindRefLoc(ea, ref):
    if (isCode(getFlags(ea))):
        op1 = GetOpType(ea, 0)
        if op1 == o_near:
            ref = ref - get_item_end(ea)
    for i in xrange(ea, (get_item_end(ea) - 4) + 1):
        if get_long(i) == ref:
            return i
    return BADADDR

def MakePatFunc(func):
    func_start_ea = func.startEA
    func_end_ea = func.endEA
    func_len = func_end_ea - func_start_ea
    #print "[+] Start : %08X" % func_start_ea
    #print "[+] End : %08X" % func_end_ea
    byte_ref = []
    ea = func_start_ea
    while ea - func_start_ea < func_len:
        l_ref = [i for i in DataRefsFrom(ea)]
        if len(l_ref) > 0:
            # Data location referenced
            ref_ea = l_ref[0]
            ref_loc_ea = FindRefLoc(ea, ref_ea)
            #print "[-] TODO : %08X" % ref_loc_ea
            byte_ref.extend((ref_loc_ea + 0, ref_loc_ea + 1, ref_loc_ea + 2, ref_loc_ea + 3))
            #return
        else:
            l_ref = [i for i in CodeRefsFrom(ea, 0)]
            if len(l_ref) > 0:
                # Code location referenced
                ref_ea = l_ref[0]
                if (ref_ea < func_start_ea) or (ref_ea >= func_start_ea + func_len):
                    ref_ea = l_ref[0]
                    ref_loc_ea = FindRefLoc(ea, ref_ea)
                    #print "[-] TODO : %08X" % ref_loc_ea
                    byte_ref.extend((ref_loc_ea + 0, ref_loc_ea + 1, ref_loc_ea + 2, ref_loc_ea + 3))
                    #return
        ea = NextHead(ea)
    first_str_len = 32 if func_len > 32 else func_len
    first_str = ""
    for i in xrange(0, first_str_len):
        if (func_start_ea + i) in byte_ref:
            first_str += ".."
        else:
            first_str += chr(Byte(func_start_ea + i)).encode('hex')
    #first_str = GetManyBytes(func_start_ea, first_str_len).encode('hex')
    for i in xrange(0, 32 - first_str_len):
        first_str += ".."
    crc, crc_len = ComputeCRCFunc(func_start_ea, func_len, byte_ref)
    pat_res = "%s %02X %04X %04X " % (first_str, crc_len, crc, func_len)
    pat_res += ":0000 %s" % get_func_name(func_start_ea)
    print pat_res
    #print "[+] Finish"

ea = get_screen_ea()
func = get_func(ea)
#if func == None:
    #print "[-] Not in a function"
#else:
#print func
MakePatFunc(func)
