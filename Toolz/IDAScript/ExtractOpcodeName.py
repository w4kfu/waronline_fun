from idautils import *
from idc import *

# Script tested on
# HEADER:00400000 ; Input MD5   : DC4F692AAA7A9AEF5EE2D2A3F00C690B
# HEADER:00400000 ; Input CRC32 : C30909BD
# HEADER:00400000 ; PDB File Name : e:\build\warhammer.test\src\project\Win32VC8\PublicTest\WAR.pdb

# sub_49CF7D
EA = 0x49CF7D

opcode_num = 0
opcode_name = ""
opcodes = []

for e in list(FuncItems(EA)):
    if idc.GetMnem(e) == "push":
        if idc.GetOpType(e, 0) == o_imm:
            val = idc.GetOperandValue(e, 0)
            if val < 0x100:
                opcode_num = val
            else:
                opcode_name = idc.GetString(val)
    elif idc.GetMnem(e) == "call":
        if idc.GetOpType(e, 0) == o_near:
            if idc.GetOperandValue(e, 0) == 0x48A93E:
                if opcode_num != 0 and opcode_name != "":
                    opcodes.append((opcode_num, opcode_name))
                    opcode_num = 0
                    opcode_name = ""
                else:
                    print "WTF"
                    exit(0)

opcodes = sorted(opcodes)

for opcode_num, opcode_name in opcodes: 
    print "[+] %3d (0x%02X) ; %s" % (opcode_num, opcode_num, opcode_name)
    
    #print "%X" % e, GetDisasm(e)
