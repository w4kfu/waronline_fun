from idaapi import *
from idc import *
from idautils import *

# SendWorldPacket_
FUNC_EA = 0x004AFCF6

for current_ea in list(CodeRefsTo(FUNC_EA, 0)):
    # This technic doesn't work if the arguments are moved on the stack
    nb_push = 0
    call_ea = current_ea
    while (nb_push != 2):
        prev_ea = idc.PrevHead(current_ea, idc.MinEA())
        if (GetMnem(prev_ea) == "push"):
            nb_push = nb_push + 1
        current_ea = prev_ea

    op1_type = GetOpType(current_ea, 0)
    if op1_type == o_imm:
        val_op1 = GetOperandValue(current_ea, 0)
        print "[+] SendWorldPacket at %08X with Opcode %08X" % (call_ea, val_op1)
    else:
        print "[+] SendWorldPacket at %08X without Immediate" % (call_ea)