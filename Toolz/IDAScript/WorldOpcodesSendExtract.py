from idaapi import *
from idc import *
from idautils import *

# SendWorldPacket_
FUNC_EA = 0x004AFCF6

pos_sent = {}
unknow = []

for current_ea in list(CodeRefsTo(FUNC_EA, 0)):
    # This technic doesn't work if the arguments are moved on the stack
    nb_push = 0
    call_ea = current_ea
    l = []
    while (nb_push != 3):
        prev_ea = idc.PrevHead(current_ea, idc.MinEA())
        if (GetMnem(prev_ea) == "push"):
            nb_push = nb_push + 1
            if nb_push == 2:
                l.append(prev_ea)
            if nb_push == 3:
                l.append(prev_ea)
        current_ea = prev_ea

    print map(hex, l)
        
    #sys.exit(42)
        
    op1_type = GetOpType(l[0], 0)
    if op1_type == o_imm:
        val_op1 = GetOperandValue(l[0], 0)
        print "[+] SendWorldPacket at %08X with Opcode %08X" % (call_ea, val_op1)
        
        op2_type = GetOpType(l[1], 0)
        if op2_type == o_imm:
            size_packet = GetOperandValue(l[1], 0)
        else:
            size_packet = 0xFFFFFFFF
        
        if val_op1 in pos_sent:
            pos_sent[val_op1].append((call_ea, size_packet))
        else:
            pos_sent[val_op1] = [(call_ea, size_packet)]
    else:
        print "[+] SendWorldPacket at %08X without Immediate" % (call_ea)
        unknow.append(call_ea)
        
l = pos_sent.items()
l.sort()        
        
for opcode_val, calls_ea in l:
    print "# 0x%02X called from %s" % (opcode_val, ','.join("0x%08X (size=0x%08X)" % (x, y) for (x, y) in calls_ea))
    
print "##### UNK"    
for unk in unknow:
    print "# 0x?? called from 0x%08X" % unk