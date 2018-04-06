import idautils
import idc

def get_bb(ea=None):
    # from https://gist.github.com/w4kfu/4252f4c19be573eaaecceb76e1dc0c1c
    """
        Return the basic block if a desired effective address or the current one
    """
    if ea == None:
        ea = idc.here()
    f = idaapi.get_func(ea)
    if not f:
        return None
    fc = idaapi.FlowChart(f)
    for block in fc:
        if block.startEA <= ea and block.endEA > ea:
            return block
    return None

def get_string_ref(ea=None):
    # from https://gist.github.com/w4kfu/4252f4c19be573eaaecceb76e1dc0c1c
    """
        Get the string references in the given function from current effective
        address or desired one
    """
    if ea == None:
        ea = idc.here()
    func_ea = idc.GetFunctionAttr(ea, FUNCATTR_START)
    for item_ea in idautils.FuncItems(func_ea):
        for ref in idautils.DataRefsFrom(item_ea):
            type = idc.GetStringType(ref)
            if type not in range(0, 7) and type != 0x2000001:
                continue
            yield (item_ea, str(idc.GetString(ref, -1, type)))

# Script tested on
# HEADER:00400000 ; Input MD5   : DC4F692AAA7A9AEF5EE2D2A3F00C690B
# HEADER:00400000 ; Input CRC32 : C30909BD
# HEADER:00400000 ; PDB File Name : e:\build\warhammer.test\src\project\Win32VC8\PublicTest\WAR.pdb
# &&
# .text:00401000 ; Input SHA256 : 852C530DF2EF78E3662F8282640DEDABE10D808C94F7188885C8A2CB4E7A9F84
# .text:00401000 ; Input MD5    : 3C78A494DF37F707AB013360BA4CFBF6
# .text:00401000 ; Input CRC32  : 30F64FC5

opcodes = []

if GetInputMD5() == "DC4F692AAA7A9AEF5EE2D2A3F00C690B":
    # sub_49CF7D
    EA = 0x49CF7D
    
    opcode_num = 0
    opcode_name = ""
    
    for e in list(idautils.FuncItems(EA)):
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
elif GetInputMD5() == "3C78A494DF37F707AB013360BA4CFBF6":
    opcodes = []
    VA_FUNC = 0x004C30CE
    JMP_TABLE = 0x004C5482
    OP_TABLE = 0x004C56FA
    start_va_func = idc.GetFunctionAttr(VA_FUNC, FUNCATTR_START)
    switch_dst = [Dword(JMP_TABLE + x * 4) for x in [Byte(OP_TABLE + y) for y in xrange(0, 253)]]
    for va, name in get_string_ref(VA_FUNC):
        cur_va = va
        while cur_va > start_va_func:
            cur_bb = get_bb(cur_va)
            if cur_bb.startEA in switch_dst:
                # + 1 because opcode value (3th parameter) is decremented before the call to 0x004C30CE
                opcodes.append((switch_dst.index(cur_bb.startEA) + 1, name))
                break
            cur_va = list(idautils.XrefsTo(cur_bb.startEA))[0].frm
else:
    print("[-] Input file not supported : {0}".format(GetInputMD5()))

opcodes = sorted(opcodes)
for opcode_num, opcode_name in opcodes: 
    print "[+] %3d (0x%02X) ; %s" % (opcode_num, opcode_num, opcode_name)
